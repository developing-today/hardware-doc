# The ContentProtection library — how CrossPoint reads DRM'd books

> The portable library behind CrossPoint's Adobe ADEPT support, read from source
> and **validated against the captured headers and implementation** on
> 2026-09-11.
>
> Source reads are `executed-success`. **Nothing was built, flashed or run**, and
> no book was decrypted. Runtime claims are `inferred` from source.

## What it is

`libs/book/ContentProtection` in `Free-Ink/freeink-sdk` @ `fde240fa` — a
freestanding C++17 PlatformIO library (v0.1.0) with **storage and crypto both
injected**, so it builds for host tests as well as the device. The firmware glue
is `lib/Epub/ContentProtection.cpp` on branch `feat-sd-plugins`.

Compiled `-fno-exceptions`, which shapes an unusual amount of the code — see
[memory discipline](#memory-discipline), the most transferable part of it.

## It is ADEPT-only. "LCP support" is a keyword, not code.

This needs stating plainly because a `library.json` keyword implies otherwise:

```
library.json:5:  "keywords": "epub, ebook, decrypt, rights, protected, lcp",
```

**That is the only occurrence of `lcp` in the entire library.** There is no LCP
implementation, no stub, no enum, and **no scheme abstraction of any kind**.

The algorithm gate is a substring test (`ProtectedBook.cpp:377`):

```cpp
aes128 = tagAttr(tag, len, "Algorithm", &value) && value.find("aes128-cbc") != std::string::npos;
```

Anything not containing `aes128-cbc` is never recorded as encrypted. RSA is
hardcoded to 1024-bit (`kRsaBlock = 128`) and `unwrapBookKey` hard-fails any
other size. **Readium LCP requires AES-256-CBC, so this library cannot process
LCP** — not "does not yet", *cannot*, without new code.

## The public API is three virtuals

```cpp
// ContentProtection.h
using ContentChunkSink = bool (*)(void* context, const uint8_t* data, size_t size);

class ContentDecryptor {
  virtual bool   isEncrypted(const char* itemPath) = 0;
  virtual size_t decryptedSize(const char* itemPath) = 0;
  virtual bool   decryptToSink(const char* itemPath, ContentChunkSink, void* context) = 0;
};

ContentDecryptor* openProtectedBook(const char* epubPath, std::string& err);
```

`openProtectedBook` has a documented **three-way return contract** that is easy
to get wrong:

| Return | Meaning |
|---|---|
| non-null | protected **and** readable — route item reads through it |
| null, `err` **empty** | **plain content**, not protected — read normally |
| null, `err` non-empty | protected but **unreadable** — no credential, or expired |

## How a book is opened

1. Scan the zip. **No `META-INF/encryption.xml` → plain EPUB, return null/empty.**
2. Stream-parse the manifest, collecting FNV-1a-64 hashes of each
   `CipherReference URI` whose algorithm contains `aes128-cbc`. The manifest is
   **never materialised** — it measured ~60 KB on large books and was aborting
   devices on allocation.
3. Empty hash set → font obfuscation only, **not** treated as protected.
4. Load rights: **sidecar `<book>.epub.rights` preferred**, in-zip
   `META-INF/rights.xml` as fallback.
5. Check account binding, unwrap the content key.

`isEncrypted()` is a **binary search over 64-bit hashes**, not string comparison —
a deliberate choice for a device with a slow CPU and a large manifest.

## Why the sidecar exists

From the firmware glue's own comment (`ContentProtection.cpp:129-131`):

> *"Prefer an out-of-band rights document delivered as a sidecar next to the EPUB
> (`<book>.epub.rights`), so the EPUB on disk stays **byte-identical to what the
> server sent**. Falls back to a rights.xml injected into the zip."*

The only file handle opened is `O_RDONLY`. **The library has no write API at
all** — it is architecturally incapable of producing a decrypted file. A
downstream caller could of course point a sink at one; that is the caller's
doing, not the library's.

## The read path — and the stage that is easy to miss

Per zip entry, on demand. The on-disk entry is:

```
[16-byte IV][ AES-128-CBC( deflate( plaintext ) ) ]
```

So there is a **deflate stage** — the sink receives *decompressed* plaintext, not
raw decrypted bytes:

- IV = first 16 bytes of the entry
- ciphertext decrypted in 2 KB chunks, CBC chaining carried manually across chunks
- PKCS#7 unpad on the final chunk only
- each decrypted chunk fed to `mz_inflate` (raw deflate, `-15`), emitted to the
  sink in 4 KB pieces

Entries failing `compressedSize < 32 || (compressedSize - 16) % 16 != 0` are
rejected outright.

`decryptedSize()` returns the zip central directory's `uncompressedSize` and is
**not validated against actual output** — worth knowing if you rely on it.

## Key unwrap

An optional first pass handles newer ACS variants: AES-128-CBC with
key = `sha256(keyType)` asymmetrically rotated by `strtol(keyType) mod 16`,
IV = `deviceId XOR fulfillmentId XOR voucherId`. Then a raw RSA private operation
with the credential's PKCS#8 key, followed by a **manual PKCS#1 v1.5 type-2
padding check**; the content key is the trailing 16 bytes.

### A fixed out-of-bounds write worth reading

`ProtectedBook.cpp:148-151`:

```cpp
// keyType is attacker-controlled (from rights.xml); C++ % keeps the sign, so
// a negative value would make `remainder` negative and drive the memcpys out
// of bounds. Normalize into [0,16) — matches the reference's unsigned rotate.
const int remainder = static_cast<int>(((nonce % 16) + 16) % 16);
```

**The fix is correct** — checked: with `remainder ∈ [0,16)`, the two reads reach
at most offset 30 in a 32-byte digest. This is the only bug in this record
confirmed *fixed* against source, and the comment is a model of the genre: names
the attacker-controlled input, the language rule, and the consequence.

## Credential storage — the sharp edge

```cpp
constexpr const char* kCredentialPath = "/.crosspoint/content.key";   // ContentProtection.cpp:30
std::string privateLicenseKey;  // base64 PKCS#8 DER (clear; sensitive)  // Credential.h:31
```

A line-oriented `key: value` text file, magic `FREEINK-CONTENT-KEY 1`, on the
**FAT32 SD card**. Consumed with a plain base64 decode — **no passphrase, no KDF,
no device binding**:

```cpp
const std::string pkcs8 = base64Decode(identity.privateLicenseKey);   // ProtectedBook.cpp:181
```

**Base64 is an encoding, not encryption. The key is stored in the clear.**

**Physical possession of the card ⇒ the private key ⇒ every book ever fulfilled
to that device is decryptable offline, permanently.** The authors document this
in the header rather than hiding it; it is a deliberate portability trade
(survives a firmware reinstall).

### One precision correction

It is the **device's** ADEPT key — RSA-1024, registered to the account alongside
`deviceUuid`, `fingerprint` and `serial` — **not an account master key**. The
practical blast radius above is unchanged, but "your Adobe account's key"
overstates it.

PKCS#12 with a `base64(device key)` passphrase **does** appear in the codebase —
but only in `pkcs12Extract`, under the header's *"client (off-device credential
setup)"* section. It unwraps the Adobe-supplied bundle during provisioning. **It
is never called on the read path and does not protect what sits on the card.**

## Expiry is enforced in the firmware, not the library

Easy to get wrong, and the handoff research did: **the portable library parses
expiry and never checks a clock.** `finishOpen()` does exactly three checks —
manifest present, account match, key unwrap.

Enforcement lives in the glue (`ContentProtection.cpp:171-187`):

```cpp
// Loan enforcement. The clock is a persisted monotonic floor (TrustedTime):
// it can lag real time while the device sat powered off, but can never be
// rolled back — staying offline delays the due date at most by the
// powered-off gap, it does not suspend it. A book carrying a due date with
// no trustworthy clock at all fails closed rather than open.
if (book->expiresAt() != 0) {
  const int64_t now = trustedtime::trustedNow();
  if (now == 0)             { err = "loan date unverified"; return nullptr; }
  if (book->isExpired(now)) { err = "access expired";       return nullptr; }
}
```

That is a **monotonic floor that fails closed** — materially more thought than
"parsed and enforced". The error strings are a **UI contract** matched by the
reader, so changing them breaks the user-facing message.

Parsing detail: `expiresAt` comes from `<until>` inside a `<display>` element,
else `fulfillmentEpoch + durationSecs`. **`expiresAt == 0` means *no expiry
found*, not expired.**

Two imprecisions in the parser, noted for anyone relying on it:

- `until`/`duration` are scoped to a `<display>` element only — the code does
  **not** verify a `permissions` parent, despite the header saying
  "permissions/display".
- The `duration` fallback takes `fulfillmentEpoch` from the **last `<date>`
  element anywhere in the document**, not a sibling of `<fulfillment>` as the
  adjacent comment implies.

**Not verified:** `expiresAt()` and `isExpired()` are inline in `ProtectedBook.h`,
which was not captured. The comparison itself is unread.

## Memory discipline

The most reusable engineering content here, driven by `-fno-exceptions` (a failed
allocation `abort()`s rather than throwing):

- `heapProbe()` nothrow probes **before every throwing allocation**
- pre-reserved `carry` / `value` / hash buffers
- SSO-sized fallback error literals for when the heap can't take a concatenation
- cache reclaim before decrypt
- **a documented allocation-ordering requirement**: the ~40 KB contiguous inflate
  state must be taken *before* the 8 KB scratch, with a measured field failure
  recorded in the comment (`maxAlloc=47092` with `41168` required)

That last one is the kind of finding that only comes from a real device.

## Crypto interface — ten methods, split by trust domain

The header divides them explicitly:

| Read path (on device) | Client (off-device setup) |
|---|---|
| `rsaPrivateRaw` — unwraps the book key | `rsaGenerate` |
| `aes128CbcDecrypt` | `rsaPublicEncrypt` |
| `sha1` | `rsaPrivateSignRaw` |
| `sha256` | `aes128CbcEncrypt` |
| | `pkcs12Extract` |
| | `randomBytes` |

`WolfsslCrypto` is the only captured implementation; host tests are stated to use
OpenSSL. On ESP32, `rsaGenerate` routes to **mbedTLS** instead, because
*"wolfSSL 5.7.2's Tom's Fast Math key-generation path is unstable on the
ESP32-C3"* — an interesting note given keygen is nominally off-device.

## What was not verified

- **`ProtectedBook.h` was not captured** — so `expiresAt()`/`isExpired()` bodies
  and the class definition are unread.
- Also absent: `Credential.cpp` (the actual parser), `Zip.cpp`, `Xml.h`,
  `Util.h`, and **`test/host/`** — which is what would show whether any
  non-ADEPT scheme is exercised anywhere.
- **Nothing was executed.** No book was opened, no credential parsed, no
  expiry triggered.

## See also

- [Plugin architecture](../../applications/crosspoint-reader/plugins/plugin-architecture.md) — the other half of the chain
- [`dtsbytebooks.com` review](../../applications/crosspoint-reader/plugins/dtsbytebooks-review.md) — who operates ADEPT now
- [Calibre and the Libby path](../../tooling/calibre/README.md)
