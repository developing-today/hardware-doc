# Using `M5Unit-NFC` in practice — traps, timings and measured numbers

> Practical working knowledge of M5Stack's `M5Unit-NFC` library and the ST25R3916,
> collected from Japanese-language sources and **cross-verified against library
> source** on 2026-09-11.
>
> Source verifications are `executed-success`. **The measurements are other
> people's**, taken on their hardware, and are attributed. Nothing here was
> reproduced by this project — no device exists.

Most of the substance comes from `ippoan/alc-app-s3`, a Japanese commercial
driver roll-call kiosk whose issue tracker is the best public bug-hunting record
of this library. Their method is notably disciplined: they instrument, measure,
and **retract their own hypotheses** when data contradicts them.

## Get logging on before anything else

Under ESP-IDF this is the highest-leverage single setting:

> 「ビルドのどこにも `M5_LOG_LEVEL` / `CORE_DEBUG_LEVEL` が定義されておらず、
> `library_log.hpp` の `logOutputLevel` が `None` に落ちて `M5_LIB_LOGE` 含む全ログが
> コンパイル時に消えていた」
>
> *"Neither `M5_LOG_LEVEL` nor `CORE_DEBUG_LEVEL` was defined anywhere in the
> build, so `logOutputLevel` fell to `None` and **every log including
> `M5_LIB_LOGE` was compiled out**."*

Silently invisible without it: `CHECK_MODE`'s *"Illegal mode"*, `wait_for_FIFO`'s
*"Timeout"*, and `detect`'s *"Detected:"*. Fix:

```cmake
target_compile_definitions(<M5Utility target> PUBLIC M5_LOG_LEVEL=4)
```

## `config()` does not configure the chip

The single most costly API trap, and it is *by design*:

> 「`UnitST25R3916::config()` は cfg 構造体を書き換えるだけで実チップには反映されない
> （`configureNFCMode()` を呼んで初めて反映される、`begin()` 内で一度呼ばれるのみ）」
>
> *"`config()` merely rewrites the cfg struct and is not reflected on the actual
> chip — it is only applied once `configureNFCMode()` is called, which happens
> only once inside `begin()`."*

This matches the framework's documented contract: in M5UnitUnified, only
`readFoo` / `writeFoo` are specified to touch hardware; `config()` is a settings
accessor applied at `begin()`.

**Consequence:** switching NFC-F ↔ NFC-B by calling `config()` alone leaves the
chip in the old mode. Call `configureNFCMode()` explicitly on every mode change.
This is also the root cause of upstream issue #1.

Two related facts, both from instrumented runs:

- `configureNFCMode()` **alone does not drop the RF field** (`Already tx_en`) —
  drive the OP register directly to break it.
- After a reconfiguration, WUPB in the first **~20 ms fails 100 %**. They run a
  60 ms settle and note ≥100 ms would be safer.

## Default timeouts are short, and asymmetric

**Verified against library headers** — the single-PICC overloads are much tighter
than the vector ones:

| Layer | `detect(PICC&)` | `detect(vector&)` | Header |
|---|---|---|---|
| NFC-A | **100 ms** | 1000 ms | `nfc_layer_a.hpp:155,165` |
| NFC-B | **50 ms** | 1000 ms | `nfc_layer_b.hpp:165,177` |
| NFC-F | **100 ms** | **500 ms** | `nfc_layer_f.hpp:98,107` |

Also verified: `TIMEOUT_REQ_WUP_B{5}`, **`TIMEOUT_ATTRIB{50}`**, `TIMEOUT_HLTB{5}`,
`TIMEOUT_DESELECT{5}` (`src/nfc/b/nfcb.hpp:266-269`).

> ⚠ One number in the original report is wrong: it gives NFC-F's vector default
> as 1000 ms. The header says **500 ms**. Their conclusion — that accidentally
> using the vector overload is why NFC-F worked — still holds.

## `detect()` halts the card on NFC-B

Not a passive observer. **Verified at `nfc_layer_b.cpp:112`:**

```cpp
hlt(rx);  // If you don't perform hlt, it will be detected again
```

`detect()` sends HLTB immediately after detection, dropping the card into HALT.
`select()` then issues WUPB to wake it — and some cards **never answer WUPB from
HALT**. A Japanese driving licence is one of them:

> 「`detect()` は検出直後に内部で HLTB を送ってカードを HALT に落とし、続く `select()`
> 内の WUPB にこの免許証は一度も応答しない」

**Correct pattern for such cards: skip `detect()` and poll `select()` only.**
WUPB also wakes IDLE cards, so it doubles as presence detection and sends no
HLTB.

## ISO-DEP framing is not optional

After ATTRIB, APDUs **must** be wrapped as I-blocks (`PCB 0x02`/`0x03`). Raw
APDUs are *silently ignored* — the card simply never answers and you burn the
full frame-waiting time. Construct `NFCBFileSystem` (its constructor lifts
FWI/FSC off the activated PICC into the isoDEP config) and send via
`isoDEP()->transceiveAPDU()`.

Note Type-B and Type-A share the same `IsoDEP` object. **FeliCa does not use
ISO-DEP at all** — IDm reads only.

## RF regulator voltage is the detection-margin knob

The most reusable register-level finding:

> 「**RF レギュレータ電圧 (reg 0x2C) が検出マージンの主因だった**。`configure_nfc_b()`
> 固定値の `0xD0` → `0xF8`（最大）でカード位置のシビアさが大きく改善」
>
> *"The RF regulator voltage (register `0x2C`) was the main driver of detection
> margin. Changing the hardcoded `0xD0` to `0xF8` (maximum) massively improved how
> fussy card positioning was."*

TX driver resistance was already at minimum, so `0x2C` was the only headroom left
in the register map.

> ⚠ **Do not confuse registers named `0x2C`.** On the ST25R3916, `0x2C` is the RF
> regulator voltage. On the SSD1677/SSD1683 e-paper controllers documented
> elsewhere in this knowledge base, command `0x2C` writes `VCOM`. Unrelated.

## The "slow NFC" investigation — and its real cause

Worth reading as a method example. Measured on their production unit:

| Card | Excess latency |
|---|---|
| Driving licence (Type-B) | **≈ 4.1 s** |
| Suica (FeliCa) | **≈ 0.75 s** |

**Four hypotheses were tested and falsified** — concurrent SPI/WebSocket load
(129 ms difference, "noise"), PSRAM thread-stack placement (moved 8 KB, no
effect), always-on polling (made it worse), and Type-B HALT carryover (rejected by
code reading). Their note on why instrumentation mattered:

> 「「変更は効いているが原因ではない」を分離できたのは計器のおかげ」
> *"It was only thanks to the instrumentation that we could separate 'the change
> took effect' from 'the change was the cause'."*

**The actual cause was physical.** Mounting the NFC unit next to a PoE base
(W5500 + LAN magnetics + metal) halved antenna amplitude:

> 「アンテナ振幅が 34 → 18 に半減し、免許証 (Type-B) は WUPB に応答できず痕跡ゼロ」

At amplitude 18, **112 consecutive cycles returned −2**. Moving it away restored
34 and gave 3/3 immediately.

**Operational heuristic worth keeping: `amp ≈ 34` is healthy, `≤ 20` is a dead
field.** Read it with `CMD_MEASURE_AMPLITUDE` before blaming software.

### Measured per-stage cost

| Stage | Per pass |
|---|---|
| F (FeliCa) | **91 ms** |
| A (NFC-A + cert check) | **140 ms** |
| B (licence APDU session) | **200 ms** |
| **Full F→A→B cycle** | **431–448 ms** |

They explicitly corrected their own code comment claiming detection was *"a few
ms"*: the measured figures are **10–30× higher**.

A structural consequence: `ensure_mode()` does field-off (10 ms) →
`configureNFCMode()` → 60 ms settle on every mode change, so **the card is
power-cycled three times per cycle**. `nfc_initial_field_on()`
(`unit_ST25R3916.cpp:364-377`) contains a **5 ms wait** — that is what satisfies
the ISO 14443-3 guard time at the head of each poll.

## FeliCa / transit cards

**Chip selection trap, stated bluntly by the same author:**

> 「⚠ 命名の罠: **Unit RFID (MFRC522) / Unit RFID2 (WS1850S) は FeliCa 非対応**
> （Type-A/B のみ）。交通系IC を読むには必ず **ST25R3916 搭載の「Unit NFC」**」
>
> *"Naming trap: Unit RFID (MFRC522) and Unit RFID2 (WS1850S) do **not** support
> FeliCa — Type-A/B only. For transit cards you must use the ST25R3916-based
> 'Unit NFC'."*

> ⚠ A widely-linked Qiita article states that Unit NFC (SKU **U216**) carries a
> **PN532**. **It does not** — U216 is the ST25R3916, as that article's own linked
> product page shows. Do not propagate it.

System codes:

```cpp
constexpr uint16_t jtic_system_code[] = {
    0x0003,  // Suica, PASMO, ICOCA, PiTaPa, TOICA …
    0x80DE,  // IruCa
};
```

Poll `0x0003` first, fall back to `0xFFFF` (wildcard). Reading an IDm needs only
`detect()` + `picc.idmAsString()` — `activate()`/`read16()` are for
balance/history and unnecessary, since the IDm needs no authentication.

**IDm semantics, which matter if you are tempted to use it as an identity:**
Mobile Suica runs real FeliCa on a secure element, so the IDm is **fixed per
device**. But one person may have several (card, phone, watch), it changes on
handset replacement, and — decisively —

> 「IDm は平文で読めリプレイ可 → **単独で本人確認にはしない**」
> *"The IDm is readable in the clear and replayable — never use it alone for
> identification."*

### Type-A UID caution

| Source | UID length | UID0 | Usable as identity? |
|---|---|---|---|
| Phone (HCE) | 4 | `0x08` | **No** — random UID per ISO/IEC 14443-3 §6.4.4 |
| Employee card | 7 | `0x05` | Yes |

## ESP-IDF build blockers

Neither is a library bug, but both abort at boot:

```
CONFIG_I2C_SKIP_LEGACY_CONFLICT_CHECK=y
CONFIG_RMT_SKIP_LEGACY_CONFLICT_CHECK=y
```

Legacy `driver/i2c.h` and new `driver/i2c_master.h` symbols link into one binary,
and `check_i2c_driver_conflict` — an `__attribute__((constructor))` — calls
`abort()` before `app_main`. The RMT equivalent bites if you also drive a WS2812.

The library **does** support ESP-IDF natively (an `app_main` path), not Arduino
only.

## The library is host-testable — an under-advertised feature

`test/` contains **17 host-test files** covering ISO-DEP, APDU, NFC-A/B/F/V,
MIFARE, Crypto1, AES and NDEF, by mocking the single `NFCLayerInterface::transceive`
seam with a `ScriptedLayer`.

> 「**プロトコルロジックは実機不要でテスト可能**。「ISO14443-4 は実機 trial&error でしか
> 検証できない」は誤りだった」
>
> *"The protocol logic is testable without hardware. The belief that
> 'ISO14443-4 can only be verified by trial and error on real hardware' was
> wrong."*

What genuinely needs hardware is the layer **below** that seam: register/FIFO
handling and bit-oriented anticollision framing — which is also where
[the unclamped FIFO read](m5unit-nfc-overflow.md) lives.

## Limits of this page

- **Nothing here was reproduced.** Every measurement is from `ippoan/alc-app-s3`'s
  hardware and workload — a PoE-powered kiosk reading Japanese driving licences.
  Timings will differ elsewhere.
- The register and timeout values **were** verified against library source; the
  behavioural narratives were not.
- Their stack is Rust-over-C++-shim, so some API friction is specific to that.

## See also

- [`M5Unit-NFC` unclamped FIFO read](m5unit-nfc-overflow.md) — the defect in the layer below the tested seam
- [NFC implementation comparison](nfc-implementation-comparison.md)
- [`components/stmicroelectronics/st25r3916`](../../../components/stmicroelectronics/st25r3916/README.md)
