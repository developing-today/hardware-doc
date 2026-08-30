/**
 * @file lv_conf.h
 * Configuration file for LVGL v9.2 — Hardware Explorer
 *
 * Display: Waveshare ESP32-S3-Knob-Touch-LCD-1.8
 *   - 360 x 360 pixels, ST77916 QSPI, RGB565
 *   - Touch: CST816 (I2C)
 *   - PSRAM: 8MB Octal (nutzen wir fuer LVGL-Buffer)
 *
 * Aktiviert via -DLV_CONF_INCLUDE_SIMPLE in platformio.ini
 */

#ifndef LV_CONF_H
#define LV_CONF_H

/*====================
   COLOR SETTINGS
 *====================*/

/* Farbtiefe: 16 (RGB565) — passt zum ST77916 */
#define LV_COLOR_DEPTH 16

/*=========================
   STDLIB WRAPPER SETTINGS
 *=========================*/

/* clib: ohne OS einfach malloc/free verwenden, wir nutzen aber heap_caps fuer PSRAM extern */
#define LV_USE_STDLIB_MALLOC    LV_STDLIB_BUILTIN
#define LV_USE_STDLIB_STRING    LV_STDLIB_BUILTIN
#define LV_USE_STDLIB_SPRINTF   LV_STDLIB_BUILTIN

/* LVGL eigener Heap: 48KB reichen fuer Hello-World; spaeter bei Bedarf hochsetzen */
#define LV_MEM_SIZE             (48 * 1024U)
#define LV_MEM_POOL_EXPAND_SIZE 0
#define LV_MEM_ADR              0

/*====================
   HAL SETTINGS
 *====================*/

/* Tick: wir setzen lv_tick_set_cb(millis) im Code → kein Custom-Source */
#define LV_TICK_CUSTOM             0
#define LV_DEF_REFR_PERIOD         16   /* ~60 FPS Ziel */
#define LV_DPI_DEF                 130  /* unwichtig fuer 1.8" */

/*=======================
 * FEATURE CONFIGURATION
 *=======================*/

/* DRAW UNITS — Software-Render reicht fuer Hello-World */
#define LV_DRAW_SW_SUPPORT_RGB565        1
#define LV_DRAW_SW_SUPPORT_RGB565_SWAPPED 0
#define LV_DRAW_SW_SUPPORT_RGB888        0
#define LV_DRAW_SW_SUPPORT_ARGB8888      0
#define LV_DRAW_SW_SUPPORT_L8            0
#define LV_DRAW_SW_SUPPORT_AL88          0
#define LV_DRAW_SW_SUPPORT_A8            0
#define LV_DRAW_SW_SUPPORT_I1            0

#define LV_DRAW_SW_DRAW_UNIT_CNT         1
#define LV_DRAW_SW_COMPLEX               1
#define LV_DRAW_SW_SHADOW_CACHE_SIZE     0
#define LV_DRAW_SW_CIRCLE_CACHE_SIZE     4

/*=================
 * OPERATING SYSTEM
 *=================*/

/* FreeRTOS gibt's auf dem ESP32 — aber LVGL ohne OS-Lock ist einfacher fuer den ersten Test */
#define LV_USE_OS                  LV_OS_NONE

/*=====================
 *  COMPILER SETTINGS
 *====================*/
#define LV_BIG_ENDIAN_SYSTEM       0
#define LV_ATTRIBUTE_MEM_ALIGN_SIZE 1
#define LV_ATTRIBUTE_MEM_ALIGN
#define LV_ATTRIBUTE_FAST_MEM
#define LV_USE_LARGE_COORD         0

/*================
 * LOG
 *===============*/
#define LV_USE_LOG                 1
#if LV_USE_LOG
    #define LV_LOG_LEVEL           LV_LOG_LEVEL_WARN
    #define LV_LOG_PRINTF          0  /* wir registrieren eigenen print_cb */
#endif

/*=================
 * ASSERT
 *================*/
#define LV_USE_ASSERT_NULL         1
#define LV_USE_ASSERT_MALLOC       1
#define LV_USE_ASSERT_STYLE        0
#define LV_USE_ASSERT_MEM_INTEGRITY 0
#define LV_USE_ASSERT_OBJ          0

/*=================
 * FONTS
 *================*/
/* Wir aktivieren nur was wir brauchen — spart Flash */
#define LV_FONT_MONTSERRAT_8       0
#define LV_FONT_MONTSERRAT_10      0
#define LV_FONT_MONTSERRAT_12      0
#define LV_FONT_MONTSERRAT_14      1   /* default */
#define LV_FONT_MONTSERRAT_16      1
#define LV_FONT_MONTSERRAT_18      0
#define LV_FONT_MONTSERRAT_20      0
#define LV_FONT_MONTSERRAT_22      0
#define LV_FONT_MONTSERRAT_24      1   /* fuer fette Hello-World-Schrift */
#define LV_FONT_MONTSERRAT_26      0
#define LV_FONT_MONTSERRAT_28      0
#define LV_FONT_MONTSERRAT_30      0
#define LV_FONT_MONTSERRAT_32      0
#define LV_FONT_MONTSERRAT_34      0
#define LV_FONT_MONTSERRAT_36      0
#define LV_FONT_MONTSERRAT_38      0
#define LV_FONT_MONTSERRAT_40      0
#define LV_FONT_MONTSERRAT_42      0
#define LV_FONT_MONTSERRAT_44      0
#define LV_FONT_MONTSERRAT_46      0
#define LV_FONT_MONTSERRAT_48      0

#define LV_FONT_DEFAULT            &lv_font_montserrat_14
#define LV_FONT_FMT_TXT_LARGE      0
#define LV_USE_FONT_COMPRESSED     0
#define LV_USE_FONT_PLACEHOLDER    1

/*=================
 *  TEXT SETTINGS
 *=================*/
#define LV_TXT_ENC                 LV_TXT_ENC_UTF8
#define LV_TXT_BREAK_CHARS         " ,.;:-_"
#define LV_TXT_LINE_BREAK_LONG_LEN 0

/*===================
 *  WIDGETS (alle an fuer's Erste — abschalten wenn Flash knapp)
 *==================*/
#define LV_USE_OBJ_NAME            0
#define LV_USE_ANIMIMG             1
#define LV_USE_ARC                 1
#define LV_USE_BAR                 1
#define LV_USE_BUTTON              1
#define LV_USE_BUTTONMATRIX        1
#define LV_USE_CALENDAR            0
#define LV_USE_CANVAS              1
#define LV_USE_CHART               1
#define LV_USE_CHECKBOX            1
#define LV_USE_DROPDOWN            1
#define LV_USE_IMAGE               1
#define LV_USE_IMAGEBUTTON         1
#define LV_USE_KEYBOARD            0
#define LV_USE_LABEL               1
#define LV_LABEL_TEXT_SELECTION    1
#define LV_LABEL_LONG_TXT_HINT     1
#define LV_USE_LED                 1
#define LV_USE_LINE                1
#define LV_USE_LIST                1
#define LV_USE_LOTTIE              0
#define LV_USE_MENU                0
#define LV_USE_MSGBOX              0
#define LV_USE_ROLLER              1
#define LV_USE_SCALE               1
#define LV_USE_SLIDER              1
#define LV_USE_SPAN                0
#define LV_USE_SPINBOX             1
#define LV_USE_SPINNER             1
#define LV_USE_SWITCH              1
#define LV_USE_TEXTAREA            1
#define LV_USE_TABLE               0
#define LV_USE_TABVIEW             0
#define LV_USE_TILEVIEW            0
#define LV_USE_WIN                 0

/*===================
 *  THEMES & DEMOS
 *==================*/
#define LV_USE_THEME_DEFAULT       1
#if LV_USE_THEME_DEFAULT
    #define LV_THEME_DEFAULT_DARK              0
    #define LV_THEME_DEFAULT_GROW              1
    #define LV_THEME_DEFAULT_TRANSITION_TIME   80
#endif
#define LV_USE_THEME_SIMPLE        1
#define LV_USE_THEME_MONO          0

/* Layouts */
#define LV_USE_FLEX                1
#define LV_USE_GRID                1

/* Demos: wir aktivieren nur Widgets-Demo, falls man mal spielen will */
#define LV_USE_DEMO_WIDGETS        0   /* spaeter ggf. auf 1 stellen */
#define LV_USE_DEMO_KEYPAD_AND_ENCODER 0
#define LV_USE_DEMO_BENCHMARK      0
#define LV_USE_DEMO_RENDER         0
#define LV_USE_DEMO_STRESS         0
#define LV_USE_DEMO_MUSIC          0

/*===================
 *  OTHERS
 *==================*/
#define LV_USE_SNAPSHOT            0
#define LV_USE_SYSMON              0
#define LV_USE_PROFILER            0
#define LV_USE_MONKEY              0
#define LV_USE_GRIDNAV             0
#define LV_USE_FRAGMENT            0
#define LV_USE_IMGFONT             0
#define LV_USE_OBSERVER            1
#define LV_USE_PINYIN_IME          0

#endif /*LV_CONF_H*/
