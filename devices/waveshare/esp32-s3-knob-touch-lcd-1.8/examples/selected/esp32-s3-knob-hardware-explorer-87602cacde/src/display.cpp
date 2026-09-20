/*
 * display.cpp — Arduino_GFX (QSPI/ST77916) + LVGL v9 Bridge
 *
 * Pin-Mapping (laut Tasmota/Waveshare Wiki):
 *   QSPI Bus:  CS=14, PCLK=13, D0=15, D1=16, D2=17, D3=18
 *   Panel:     RST=21, BL=47 (Backlight)
 *
 * Render-Modus: Strip-Buffer 360x40 in INTERNAL DMA-faehigem RAM.
 * Wir nutzen NICHT PSRAM fuer den Buffer — DMA mag das nicht zuverlaessig.
 * 360 * 40 * 2 byte = 28800 byte ≈ 28 KB → passt locker ins interne RAM.
 */

#include "display.h"
#include <Arduino_GFX_Library.h>
#include <lvgl.h>

// ── Display-Pins ──────────────────────────────────────────────────────────
#define PIN_LCD_CS    14
#define PIN_LCD_PCLK  13
#define PIN_LCD_D0    15
#define PIN_LCD_D1    16
#define PIN_LCD_D2    17
#define PIN_LCD_D3    18
#define PIN_LCD_RST   21
#define PIN_LCD_BL    47

#define LCD_W  360
#define LCD_H  360

// ── Arduino_GFX Bus + Panel ───────────────────────────────────────────────
// Arduino_ESP32QSPI: 4-Bit Daten ueber das ESP32-S3 LCD-Peripheral
static Arduino_DataBus *bus = new Arduino_ESP32QSPI(
    PIN_LCD_CS, PIN_LCD_PCLK,
    PIN_LCD_D0, PIN_LCD_D1, PIN_LCD_D2, PIN_LCD_D3
);

// Arduino_ST77916: 360x360 Round-Display, QSPI
// WICHTIG: Default ist st77916_180_init_operations, das fuer 1.85" Panels gedacht ist.
// Unser Waveshare KNOB 1.8" (anderes Panel!) braucht st77916_150_init_operations.
// Ohne diesen Override sieht man nur einen Mittelstreifen statt Vollbild.
static Arduino_GFX *gfx = new Arduino_ST77916(
    bus, PIN_LCD_RST, /*rotation*/ 2, /*ips*/ true,
    LCD_W, LCD_H,
    /*col_offset1*/ 0, /*row_offset1*/ 0,
    /*col_offset2*/ 0, /*row_offset2*/ 0,
    st77916_150_init_operations,
    sizeof(st77916_150_init_operations)
);

// ── LVGL Buffer ───────────────────────────────────────────────────────────
// Strip-Buffer: 1/9 vom Screen — guter Kompromiss aus RAM-Bedarf und Flush-Frequenz
#define LV_BUF_LINES 40
static uint8_t  *lv_draw_buf = nullptr;
static lv_display_t *lv_disp = nullptr;

// Flag: erst auf true wenn LVGL ticken DARF
// (verhindert Race zwischen display_test_pattern() und lv_timer_handler())
static volatile bool lvgl_tick_enabled = false;

// ── LVGL Callbacks ────────────────────────────────────────────────────────

/**
 * Flush-Callback: LVGL hat einen Bereich gerendert, wir schieben ihn aufs Display.
 * In LVGL v9 kommt der Pixel-Buffer als uint8_t* — bei RGB565 also byte-Stream.
 */
static void my_disp_flush(lv_display_t *disp, const lv_area_t *area, uint8_t *px_map)
{
    uint32_t w = area->x2 - area->x1 + 1;
    uint32_t h = area->y2 - area->y1 + 1;

    // LVGL v9 schreibt RGB565 in Native-Endian (Little-Endian auf ESP32-S3).
    // draw16bitRGBBitmap nimmt Native-Endian und schickt's so wie es ist;
    // draw16bitBeRGBBitmap wuerde nochmal Bytes swappen → falsch.
    gfx->draw16bitRGBBitmap(area->x1, area->y1,
                            (uint16_t *)px_map, w, h);

    lv_display_flush_ready(disp);
}

/**
 * Tick-Callback: liefert millis() — LVGL braucht das fuer Animationen/Timer.
 */
static uint32_t my_tick_cb(void)
{
    return millis();
}

/**
 * Log-Callback: leitet LVGL-Meldungen an Serial weiter.
 */
#if LV_USE_LOG
static void my_log_cb(lv_log_level_t level, const char *buf)
{
    Serial.print("[LVGL] ");
    Serial.println(buf);
}
#endif

// ── Public API ────────────────────────────────────────────────────────────

bool display_init()
{
    printf("\n[DSP] LVGL + Arduino_GFX Init...\n");

    // 1) Backlight Pin auf OUTPUT — erstmal AUS, damit kein Flackern
    pinMode(PIN_LCD_BL, OUTPUT);
    digitalWrite(PIN_LCD_BL, LOW);

    // 2) Arduino_GFX: Bus + Panel initialisieren
    if (!gfx->begin()) {
        printf("[DSP] FEHLER: gfx->begin() fehlgeschlagen\n");
        return false;
    }
    gfx->fillScreen(0x0000);  // BLACK in RGB565
    printf("[DSP] OK Display init (%dx%d)\n", gfx->width(), gfx->height());

    // 3) Backlight an
    digitalWrite(PIN_LCD_BL, HIGH);

    // 4) LVGL Core
    lv_init();
    lv_tick_set_cb(my_tick_cb);
#if LV_USE_LOG
    lv_log_register_print_cb(my_log_cb);
#endif

    // 5) Draw-Buffer in internem DMA-faehigem RAM allokieren
    const size_t buf_bytes = LCD_W * LV_BUF_LINES * sizeof(uint16_t);
    lv_draw_buf = (uint8_t *)heap_caps_malloc(buf_bytes,
                                              MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
    if (!lv_draw_buf) {
        printf("[DSP] FEHLER: Draw-Buffer (%u byte) konnte nicht allokiert werden\n",
               (unsigned)buf_bytes);
        return false;
    }
    printf("[DSP] Draw-Buffer: %u byte in INTERNAL RAM\n", (unsigned)buf_bytes);

    // 6) LVGL Display registrieren
    lv_disp = lv_display_create(LCD_W, LCD_H);
    lv_display_set_flush_cb(lv_disp, my_disp_flush);
    lv_display_set_buffers(lv_disp, lv_draw_buf, NULL, buf_bytes,
                           LV_DISPLAY_RENDER_MODE_PARTIAL);

    printf("[DSP] OK LVGL v%d.%d.%d initialisiert\n",
           lv_version_major(), lv_version_minor(), lv_version_patch());
    return true;
}

void display_tick()
{
    if (!lvgl_tick_enabled) return;
    lv_timer_handler();
}

void display_show_hello()
{
    // Hello-Welt mit Text, dieses Mal mit aktiv unterdrueckten Theme-Effekten
    lv_obj_t *scr = lv_screen_active();
    lv_obj_set_style_bg_color(scr, lv_color_hex(0x101820), LV_PART_MAIN);  // Berliner Nachthimmel
    lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, LV_PART_MAIN);
    // Theme-Schatten/Border explizit ausschalten (Default-Theme hat die an)
    lv_obj_set_style_border_width(scr, 0, LV_PART_MAIN);
    lv_obj_set_style_shadow_width(scr, 0, LV_PART_MAIN);
    lv_obj_set_style_outline_width(scr, 0, LV_PART_MAIN);

    // Helper: Label OHNE Theme-Effekte
    auto make_label = [](lv_obj_t *parent, const char *txt,
                         const lv_font_t *font, uint32_t color,
                         lv_align_t align, int x, int y) {
        lv_obj_t *l = lv_label_create(parent);
        lv_label_set_text(l, txt);
        lv_obj_set_style_text_font(l, font, LV_PART_MAIN);
        lv_obj_set_style_text_color(l, lv_color_hex(color), LV_PART_MAIN);
        // Alle dekorativen Effekte aus, die das Theme draufpacken koennte:
        lv_obj_set_style_bg_opa(l, LV_OPA_TRANSP, LV_PART_MAIN);
        lv_obj_set_style_border_width(l, 0, LV_PART_MAIN);
        lv_obj_set_style_shadow_width(l, 0, LV_PART_MAIN);
        lv_obj_set_style_outline_width(l, 0, LV_PART_MAIN);
        lv_obj_set_style_pad_all(l, 0, LV_PART_MAIN);
        lv_obj_align(l, align, x, y);
        return l;
    };

    make_label(scr, ":)", &lv_font_montserrat_24, 0xFFD700, LV_ALIGN_CENTER, 0, -40);
    lv_obj_t *hi = make_label(scr, "Hallo Ingo!\nLVGL lebt.",
                              &lv_font_montserrat_16, 0xFFFFFF, LV_ALIGN_CENTER, 0, 10);
    lv_obj_set_style_text_align(hi, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN);

    char ver[32];
    snprintf(ver, sizeof(ver), "v0.4 / LVGL %d.%d",
             lv_version_major(), lv_version_minor());
    make_label(scr, ver, &lv_font_montserrat_14, 0x888888, LV_ALIGN_CENTER, 0, 70);
}

void display_enable_lvgl()
{
    lvgl_tick_enabled = true;
}

void display_test_pattern()
{
    printf("[DSP] === Test-Pattern ohne LVGL ===\n");

    // Test 1: Vollflaechen ROT (RGB565: 0xF800)
    printf("[DSP] Test 1: ROT (2 sek)\n");
    gfx->fillScreen(0xF800);
    vTaskDelay(pdMS_TO_TICKS(2000));

    // Test 2: Vollflaechen GRUEN (RGB565: 0x07E0)
    printf("[DSP] Test 2: GRUEN (2 sek)\n");
    gfx->fillScreen(0x07E0);
    vTaskDelay(pdMS_TO_TICKS(2000));

    // Test 3: Vollflaechen BLAU (RGB565: 0x001F)
    printf("[DSP] Test 3: BLAU (2 sek)\n");
    gfx->fillScreen(0x001F);
    vTaskDelay(pdMS_TO_TICKS(2000));

    // Test 4: Streifen-Muster — falls Init falsch, sieht man Versatz
    printf("[DSP] Test 4: Streifen (3 sek)\n");
    gfx->fillScreen(0x0000);
    for (int y = 0; y < LCD_H; y += 40) {
        uint16_t color = (y / 40) % 2 ? 0xFFFF : 0x0000;  // weiss/schwarz
        gfx->fillRect(0, y, LCD_W, 20, color);
    }
    vTaskDelay(pdMS_TO_TICKS(3000));

    // Test 5: Diagonalen-Kreuz — pruefen ob Pixel-Adressierung stimmt
    printf("[DSP] Test 5: Kreuz (3 sek)\n");
    gfx->fillScreen(0x0000);
    for (int i = 0; i < LCD_W; i++) {
        gfx->drawPixel(i, i, 0xFFE0);          // gelbe Diagonale
        gfx->drawPixel(LCD_W - 1 - i, i, 0xF81F); // magenta Anti-Diagonale
    }
    // Mittelpunkt-Kreuz fuer Orientierung
    gfx->drawFastHLine(0, LCD_H / 2, LCD_W, 0x07FF);  // cyan horizontal
    gfx->drawFastVLine(LCD_W / 2, 0, LCD_H, 0x07FF);  // cyan vertikal
    vTaskDelay(pdMS_TO_TICKS(3000));

    // Test 6: Text in ECKEN — ueberprueft Rotation/Mirror
    printf("[DSP] Test 6: Ecken-Text (3 sek)\n");
    gfx->fillScreen(0x0000);
    gfx->setTextColor(0xFFFF);
    gfx->setTextSize(2);
    gfx->setCursor(5, 5);          gfx->print("OL");      // oben links
    gfx->setCursor(LCD_W-40, 5);   gfx->print("OR");      // oben rechts
    gfx->setCursor(5, LCD_H-20);   gfx->print("UL");      // unten links
    gfx->setCursor(LCD_W-40, LCD_H-20); gfx->print("UR"); // unten rechts
    gfx->setCursor(LCD_W/2-30, LCD_H/2-8);
    gfx->setTextSize(3);
    gfx->print("OK");
    vTaskDelay(pdMS_TO_TICKS(3000));

    printf("[DSP] === Test-Pattern fertig ===\n");
}
