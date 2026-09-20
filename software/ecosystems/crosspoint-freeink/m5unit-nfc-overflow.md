# `M5Unit-NFC` — stack buffer overflow in the NFC-A emulation listener

> **Status: `inferred` from source. Not demonstrated, not exploited, not
> disclosed.** No hardware was involved. This is a source-level analysis of a
> publicly available library, written up because the finding is concrete and the
> defective path is reachable from RF.
>
> Analysed **2026-09-11** against `m5stack/M5Unit-NFC` @
> `93745b547364f310cd64b5155a870103a7800a5d` (2026-06-10), archived locally at
> `archive/software/ecosystems/crosspoint-freeink/nfc-source-snapshots/m5stack_M5Unit-NFC/`.

## Summary

`UnitST25R3916::readFIFO()` **does** bounds-check — but against a size its
*caller* supplies. In the NFC-A emulation `Active` handler the caller passes the
**FIFO length** where the function expects the **buffer capacity**, so the check
compares a value against itself and passes. The read then proceeds into a 64-byte
stack array.

The same file gets it right ~70 lines earlier, in the `Idle` handler, using the
correct idiom. So this is a single-call-site oversight, not a design assumption.

**The bug is not "there is no bounds check". It is "the bounds check is given the
wrong bound."** That distinction matters for anyone triaging or fixing it.

## The mechanism

`readFIFO` clamps correctly, given honest inputs —
`src/unit/unit_ST25R3916.cpp:484`:

```cpp
uint32_t UnitST25R3916::readFIFO(uint16_t& actual, uint8_t* buf, const uint16_t buf_size)
{
    actual = 0;
    uint16_t bytes{}; uint8_t bits{};
    if (readFIFOSize(bytes, bits)) {
        auto readSz = std::min<uint16_t>(bytes, buf_size);   // clamp to CAPACITY
        if (!readSz) return false;
        TRANSACTION_GUARD();
        if (!readRegister(OP_READ_FIFO, buf, readSz, 0, false)) return false;
        actual = readSz;
        ...
```

The third parameter is named `buf_size` and is meant to be the capacity of `buf`.

### The safe call site — `Idle` handler, `emulation_layer_a_ST25R3916.cpp:375`

```cpp
uint8_t rx[64]{};
uint16_t rx_len{}, actual{};
_u.readFIFOSize(bytes, bits);
rx_len = std::min<uint16_t>(bytes, sizeof(rx));   // ← clamped to sizeof(rx)
_u.readFIFO(actual, rx, rx_len);
```

Correct: `rx_len` can never exceed 64, so `min(bytes, rx_len)` ≤ 64.

### The defective call site — `Active` handler, same file, line 444

```cpp
uint8_t rx[64]{};
uint16_t rx_len{}, actual{};
if (irq32 & I_rxe32) {
    _u.readFIFOSize(bytes, bits);
    rx_len = bytes;                          // ← NOT clamped. FIFO length, not capacity.

    if (irq32 & (I_par32 | I_crc32 | I_err132 | I_err232) || rx_len <= 2) {
        _u.readFIFO(actual, rx, rx_len);     // ← overflow path 1 (error branch)
        ...
    }
    if (irq32 & I_rxe32) {
        rx_len -= 2;
        _u.readFIFO(actual, rx, rx_len);     // ← overflow path 2 (normal branch)
        _data_flag = true;
        auto state = _layer.receive_callback(rx, rx_len);
        ...
```

With `rx_len = bytes`, the clamp inside `readFIFO` becomes
`min(bytes, bytes) == bytes`. **The guard is inert.** `readRegister` then writes
`bytes` into a 64-byte stack array.

**Two distinct overflow paths** at this one site: the error branch and the normal
receive branch.

## How much can be written

`readFIFOSize` reconstructs the length from the chip's FIFO status registers —
`src/unit/unit_ST25R3916.cpp`:

```cpp
bytes = (s >> 8) | ((s & 0x00C0) << 2);
```

That is a 10-bit reconstruction (8 bits plus two high bits relocated to 8–9), and
the ST25R3916's FIFO is **512 bytes**. So `bytes` is bounded by the hardware at
512, against a **64-byte** destination — up to roughly **448 bytes of stack
overwrite past the end of `rx`**, with contents taken from the RF frame.

Corvelis's patch docstring gives a concrete real-world figure: their tested
transport uses a **253-byte command (240-byte DATA payload)** — already ~189
bytes past the buffer in normal, non-adversarial operation.

## Reachability

The `Active` handler runs when the device is in **NFC-A card emulation** and a
reader is in the field. `rx_len` derives from a frame the reader sends.

- **Precondition:** the device is emulating a tag, and the attacker is within NFC
  range (centimetres).
- **No authentication** exists at this layer — none is defined for NFC-A frame
  reception.
- **Not reachable in reader/poller mode**, which is why the vendor's own
  `M5PaperMono-UserDemo` is unaffected: it probes tags rather than emulating one.

So the exposure is specific to emulation firmware. Of the three PaperMono NFC
implementations surveyed, **two emulate** — but only `Corvelis/m5-touch-card` uses
this library, and it patches the bug before compiling.
`ciniml/paper_name_plate` wrote its own stack in Rust and never touches this code.

## Evidence that it is an oversight

Three independent signals, all in the same library:

1. **The correct idiom is used 70 lines earlier**, in the `Idle` handler of the
   same file.
2. **`nfc_layer_a.cpp:2227` declares `uint8_t rx[256]`** — a larger buffer is used
   elsewhere for comparable work.
3. **`readFIFO` was deliberately written to clamp.** The author built the guard;
   one call site simply feeds it the wrong argument.

Counted across the library, `uint8_t rx[64]` appears at
`emulation_layer_a_ST25R3916.cpp:375` (safe), `:444` (defective), and
`nfc_layer_a.cpp:2425`; `rx[256]` at `nfc_layer_a.cpp:2227`.

## The third-party fix

`Corvelis/m5-touch-card` ships `firmware/scripts/patch_m5unit_nfc.py` — a 374-line
PlatformIO `pre:` script that rewrites the library in place at build time. For
this bug it does two things:

```cpp
uint8_t rx[64]{};   →   uint8_t rx[256]{};      // both listener buffers
```

```cpp
if (rx_len > sizeof(rx)) {                       // fail closed before the read
    M5_LIB_LOGE("A RX oversized %u", rx_len);
    _u.writeDirectCommand(CMD_CLEAR_FIFO);
    _u.writeDirectCommand(CMD_UNMASK_RECEIVE_DATA);
    return EmulationLayerA::State::Active;
}
```

Both are needed: the resize accommodates the real 253-byte transport, and the
guard handles anything larger. Note the patch **keeps the `rx_len` → `readFIFO`
call shape** and adds an explicit test, rather than switching to
`min(bytes, sizeof(rx))` as the `Idle` handler does. Either fixes it; the
`Idle`-handler idiom is smaller and matches existing style.

## Suggested upstream fix

The minimal change matching the library's own existing pattern:

```cpp
// emulation_layer_a_ST25R3916.cpp, Active handler
_u.readFIFOSize(bytes, bits);
rx_len = std::min<uint16_t>(bytes, sizeof(rx));   // was: rx_len = bytes;
```

That alone closes both overflow paths. Enlarging `rx` to 256 is a **separate,
also-necessary** change for correctness — at 64 bytes the listener silently
truncates legitimate 253-byte frames even once memory-safe.

Consider also auditing every other `readFIFO` call site for the same
capacity-vs-length confusion; the API's shape invites it, and renaming the
parameter or asserting on it would prevent recurrence.

## Provenance — the clamp was dropped in porting, not merely forgotten

**This is the single most important finding on the page, and it was established
only on 2026-09-11.**

`M5Unit-NFC` is a port of **STMicroelectronics' RFAL** (RF Abstraction Layer) for
the ST25R3916. The file still carries commented-out RFAL call sites, left in as
porting markers:

```
src/nfc/layer/a/emulation_layer_a_ST25R3916.cpp:182   //    rfalCheckDisableObsMode();
src/nfc/layer/a/emulation_layer_a_ST25R3916.cpp:272   //       rfalCheckEnableObsModeRx();
src/nfc/layer/a/emulation_layer_a_ST25R3916.cpp:397   // rfalCheckDisableObsMode(); …
src/nfc/layer/f/emulation_layer_f_ST25R3916.cpp:208   //    rfalCheckDisableObsMode();
src/unit/unit_ST25R3916.cpp:535                        //    rfalSetAnalogConfig(…)
```

**ST's original bounds every listen-mode FIFO read.** In
`rfal_rfst25r3916.c`, all three call sites use the same clamp:

```c
st25r3916ReadFifo( gRFAL.Lm.rxBuf,
                   MIN( *gRFAL.Lm.rxLen, rfalConvBitsToBytes(gRFAL.Lm.rxBufLen) ) );
```

— at `RFAL_LM_STATE_IDLE` (:3640), `RFAL_LM_STATE_READY_F` (:3713), and
**`RFAL_LM_STATE_ACTIVE_A` (:3801)**. That last one is the state M5Stack's
`update_active()` is a line-for-line port of: same IRQ mask, same `<= CRC_LEN`
guard, same clear-FIFO/unmask pair, same `rxLen -= RFAL_CRC_LEN`. Every step
matches **except** that `MIN(…)` is gone.

So the asymmetry is not an oversight that happened to land in one of two
handlers. **M5Stack preserved the clamp in `update_idle` (← ST's `LM_STATE_IDLE`)
and dropped it in `update_active` (← ST's `LM_STATE_ACTIVE_A`).**

Two details make the consequence worse than a simple omission:

1. **ST's `st25r3916ReadFifo` does not clamp internally, and documents that**
   (`st25r3916_com.h`: *"This function doesn't check whether `length` is really
   the number of available bytes in FIFO"*). ST relies entirely on the call-site
   `MIN`. M5Stack's `readFIFO` **does** clamp internally — a safer design — which
   is exactly why passing the FIFO count as `buf_size` *silently* defeats it.
   The safer API made the bug invisible.
2. **In RFAL, `rxBuf`/`rxBufLen` are caller-supplied** to `rfalListenStart()`, so
   the bound is a real parameter the application owns. M5Stack replaced that with
   a **64-byte stack local inside the handler**. That substitution is what turns a
   truncation into a stack write.

### Attribution

The repository is MIT, `Copyright (c) 2025 M5Stack Technology CO LTD`, with **no
`NOTICE`, no `THIRD-PARTY` file, and zero mentions of ST or RFAL in the README**
(verified). ST's RFAL ships under ST's own licence, not MIT. The maintainer has
publicly described the M5UnitUnified libraries as
「新規に書き起こし」 — *"newly written from scratch"*
([Qiita, 2024-12-11](https://qiita.com/GOB/items/b96a96ff5bbc112303df)).

**Precision, since that quote is load-bearing.** The article is about the
**M5UnitUnified framework** and is dated 2024-12-11 — it **predates `M5Unit-NFC`**
(repository created 2025-10-27), lists M5Unit-RFID as not yet released, and
contains **no NFC content whatsoever**. The statement is therefore about the
*family's* authoring policy, not a specific claim about this library. It is quoted
as context for the attribution question, **not** as a denial regarding
`M5Unit-NFC`.

The discrepancy is recorded as an observation. **No legal conclusion is drawn
here**, and none should be read into it.

## It is the only unclamped handler of four

The library has four emulation receive handlers. Three clamp correctly:

| Layer | Handler | Buffer | Clamped? |
|---|---|---|---|
| NFC-A | `update_idle` (:375) | `rx[64]` | ✅ `std::min(bytes, sizeof(rx))` |
| NFC-A | **`update_active` (:444)** | `rx[64]` | ❌ **`rx_len = bytes;`** |
| NFC-F | `:357` | `rx[128]` | ✅ |
| NFC-F | `:393` | `rx[128]` | ✅ |

The NFC-F sibling clamps in **both** of its handlers. A single outlier among four
is much harder to read as intentional than one-of-two.

Also noted, unexplained: the `max_fifo_depth()` override that would return
`MAX_FIFO_DEPTH` is **commented out** at `:56–61`.

## The same mistake was already found — and fixed — elsewhere in this library

**PR #4** (`Sped0n`, an Espressif engineer, merged 2026-05-20) fixed the
*identical semantic confusion* in the reader path:

> *"`nfcaReceive()` treated the caller-provided RX length as the expected frame
> size. In practice that value is the RX buffer capacity."*

The fix added the comment *"`rx_len_org` is the caller's buffer capacity, not an
expected frame length."* **The audit was never generalised to the emulation
layer.** The project has therefore already recognised this exact class of error
once, in code written by the same author, and the emulation site survived.

## Why this survived: the tested seam stops one layer above the bug

The library is **much better tested than its ecosystem reputation suggests** —
`test/` contains **17 host-test files**, including `isodep_test.cpp`,
`nfca_test.cpp`, `nfcb_test.cpp`, `nfcf_test.cpp`, `nfcv_test.cpp`,
`mifare_test.cpp`, `mifare_classic_crypto1_test.cpp`, `ndef_test.cpp` (21 KB),
`aes_test.cpp` and `desfire_detail_test.cpp`.

They work by mocking a single seam: `NFCLayerInterface::transceive` is pure
virtual, and `test/isodep_test.cpp` substitutes a `ScriptedLayer` to drive ISO-DEP
I/R/S block framing, automatic WTX extension, chaining and APDU status checking
entirely on the host.

**That seam sits immediately above the defect.** `transceive` is the boundary; the
overflow is in the register/FIFO handling *below* it, in
`emulation_layer_a_ST25R3916.cpp`. A developer working on this project stated the
division precisely:

> 「**プロトコルロジックは実機不要でテスト可能**」… 「実機知見が必須なのは別レイヤー:
> ST25R3916 のレジスタ/FIFO操作」
>
> *"The protocol logic is testable without hardware… What genuinely requires
> hardware knowledge is a different layer: ST25R3916 register/FIFO manipulation."*
> — [`ippoan/alc-app-s3#107`](https://github.com/ippoan/alc-app-s3/issues/107)

So the mocked tests **cannot reach this code by construction**, and the layer that
contains it has no host tests at all. That is a satisfying and unflattering
explanation for how an unclamped FIFO read survived in a project that otherwise
tests carefully.

It also suggests the cheapest possible fix path: the bug is a pure function of
`bytes` and `sizeof(rx)`, so a test that drives `readFIFO` with an oversized FIFO
count would catch it **without hardware** — if the seam were pushed one layer
down.

## Nobody has reported it

Searched 2026-09-11 across: the issue tracker (all 8 issues/PRs read), all 4
forks, Qiita (15 queries, full article bodies), Zenn (0 results for every relevant
query), and GitHub issue search. **No discussion of this inconsistency anywhere.**

Two crash reports were examined and **excluded**:

- `BruceDevices/firmware#2787` — *"ST25R3916 … Intermittent Freezes"*. Different
  codebase (ST's RFAL directly, not `M5Unit-NFC`), its card-emulation path is not
  wired in, and the reporter self-diagnosed it as an I²C bus race.
- `ippoan/alc-app-s3#96` — an ESP-IDF `abort()` at boot from a legacy/new I²C
  driver symbol conflict. A build-configuration fault, not a memory fault.

Neither is evidence for this defect. **Absence of reports is expected** given the
reachability analysis below, and is not reassurance.

## Reachability — stated conservatively

The shipped NFC-A emulation example emulates **MIFARE Ultralight / NTAG 213**,
Type 2 tags whose *compliant* reader commands are ≤ 6 bytes plus CRC. **A
standards-conforming reader will not produce a >64-byte frame here.** Triggering
this requires either a non-compliant or deliberately hostile reader, or a spurious
FIFO state.

One point cuts the other way, and it matters: **the error branch at `:451` also
reads unbounded**, and it runs on parity/CRC/framing errors — which *do* occur
naturally with marginal antenna coupling. That path reads the FIFO purely to log
`rx[0]`.



- **Not tested.** Nothing was built, flashed, or exercised against a reader. No
  proof-of-concept exists and none was attempted.
- **Exploitability not assessed.** A stack overwrite on an ESP32-S3 with RF-
  controlled data is serious on its face, but whether it is controllable enough
  for anything beyond a crash was not analysed. **Do not cite this as
  "exploitable"** — cite it as "unbounded write, untested".
- **Not disclosed.** No issue filed, no contact with M5Stack. That is a decision
  for the repository owner, not something to action unilaterally from a research
  pass.
- ~~Current upstream not checked~~ — **checked 2026-09-11: the defect is live on
  both branches.** `main` is `93745b5` (2026-06-10) and still has it. **`develop`
  is under active development *today*** — HEAD `3b6ae05`, 2026-09-11 — and
  `rx_len = bytes;` remains, at line 453. Only 5 commits have ever touched this
  file, none of them changing the clamp, and **no fork has modified it** (all four
  are byte-identical, one modulo line endings).

  Worth noting for tone: `develop`'s HEAD commit is itself titled *"Check that a
  capability container fits before trusting its block count"* — the maintainer is
  **actively hardening bounds checks in adjacent code right now**. This is a live,
  maintained project, not an abandoned one.

## Reproduction of the analysis

```bash
git clone https://github.com/m5stack/M5Unit-NFC && cd M5Unit-NFC
git checkout 93745b547364f310cd64b5155a870103a7800a5d
sed -n '440,470p' src/nfc/layer/a/emulation_layer_a_ST25R3916.cpp   # defective site
sed -n '370,382p' src/nfc/layer/a/emulation_layer_a_ST25R3916.cpp   # safe site
sed -n '484,505p' src/unit/unit_ST25R3916.cpp                       # readFIFO
```

## See also

- [NFC implementation comparison](nfc-implementation-comparison.md) — the three approaches, and the other six defects the same patch fixes
- [`components/stmicroelectronics/st25r3916`](../../../components/stmicroelectronics/st25r3916/README.md)
- Archived source, both the defective library and the patch that fixes it:
  `archive/software/ecosystems/crosspoint-freeink/nfc-source-snapshots/`
