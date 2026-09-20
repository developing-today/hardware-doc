# Landmark papers, by field and by server

Which preprint server did the work you actually depend on land on? This document collects the
**verified** entries across the whole pass, reorganised by *field* rather than by repository, and
answers the practical question: **when I go looking for foundational systems, hardware or software
work, where is it?**

- **Compiled:** 2026-09-01 / 2026-09-02.
- **Verification standard:** every identifier below was individually fetched from its server's API
  or abstract page and its title machine-checked against the response. Entries that could not be
  confirmed were **dropped**, not hedged. See [`README.md § Evidence and method`](README.md#evidence-and-method).
- **Totals verified in this pass:** **79** on [arXiv](arxiv.md), **41** on
  [Cryptology ePrint](cryptology-eprint-archive.md), **14** on [HAL](hal.md), plus entries on
  [Optimization Online](optimization-online.md), [ECSarXiv](ecsarxiv.md), [Zenodo](zenodo.md) and
  [bioRxiv](biorxiv-and-medrxiv.md).
- This file is a **curated cross-section**. The complete per-server tables live in each record's §7.

## How to read the "preprint first?" column

Taken from the arXiv record's method note, and applied consistently:

- **proven** — the record carries venue metadata dated *later* than v1. Provable from metadata alone.
- **de facto** — no venue metadata exists at all. The preprint is the only citable record the
  authors ever supplied, and it is what the field cites.
- **companion** — the record declares itself the full or extended version of a paper at a named
  venue. Not a precedence claim.

---

## 1. The single most important finding

**The canonical distributed-systems and database papers are not on any preprint server.**

This is not a gap in our search; it is a property of the field. Systems research published through
OSDI, SOSP, NSDI, VLDB and SIGMOD in the 2000s and early 2010s went to the ACM and USENIX digital
libraries and nowhere else. Verified absent from arXiv by title search (arXiv §7.10):

| Paper | Venue | arXiv title search |
|---|---|---|
| MapReduce: Simplified Data Processing on Large Clusters | OSDI 2004 | **0 hits** |
| The Google File System | SOSP 2003 | **0 hits** |
| Bigtable: A Distributed Storage System for Structured Data | OSDI 2006 | 2 hits, **neither is the paper** |
| Dynamo: Amazon's Highly Available Key-value Store | SOSP 2007 | **0 hits** |
| In Search of an Understandable Consensus Algorithm (**Raft**) | USENIX ATC 2014 | **0 hits** |
| Paxos Made Simple | SIGACT News 2001 | 1 hit — *"Moderately Complex Paxos Made Simple"*, a different 2017 paper |
| ZooKeeper: Wait-free coordination for internet-scale systems | USENIX ATC 2010 | 2 hits, **neither is the paper** |
| Spanner: Google's Globally-Distributed Database | OSDI 2012 | 291 hits — **all about *graph* spanners**, an unrelated combinatorics object |
| Resilient Distributed Datasets (**Spark**) | NSDI 2012 | **0 hits** |
| RAMCloud | SOSP / TOCS | **0 hits** |
| Bitcoin: A Peer-to-Peer Electronic Cash System | self-published | **0 hits** |
| Flipping Bits in Memory Without Accessing Them (**RowHammer**) | ISCA 2014 | 1 hit — the **2023 retrospective**, not the original |
| seL4: Formal verification of an OS kernel | SOSP 2009 | 5 hits, **none is the original** |
| CompCert (formally verified C compiler) | POPL 2006 / CACM 2009 | 4 hits, **none is the original** — but see §5, it is on **HAL** |
| BBR: Congestion-Based Congestion Control | ACM Queue 2016 | 34 hits, **none is the original** |
| The Chubby lock service | OSDI 2006 | **[NOT-VERIFIED]** — not separately probed; nothing surfaced adjacently |

The `Spanner` case is the trap worth remembering: a title search returns **291 confident hits**, and
every one of them is about a different object. A keyword count is not a literature search.

The equivalent boundary exists on Cryptology ePrint. Verified **absent** there: the original
HotStuff, the original Algorand, ROCA, the original RowHammer paper, Spectre/Meltdown, the PRESENT
cipher paper, the Keccak/SHA-3 specification, "Short Signatures from the Weil Pairing", Dwork et
al.'s differential-privacy paper, TPM-FAIL, Logjam and DROWN. **ePrint is dominant for cryptology,
not for systems security generally.**

---

## 2. Distributed systems and consensus

Split across three servers, and the split is systematic: **protocol designs with security proofs go
to ePrint; systems papers go to arXiv; the French contributions go to HAL.**

### On arXiv

| Paper | arXiv ID | v1 | Why it matters | First? |
|---|---|---|---|---|
| Majority is not Enough: Bitcoin Mining is Vulnerable | [1311.0243](https://arxiv.org/abs/1311.0243) | 2013-11-01 | Selfish mining: <50% attacks on Bitcoin | de facto |
| Lightweight Asynchronous Snapshots for Distributed Dataflows | [1506.08603](https://arxiv.org/abs/1506.08603) | 2015-06-29 | **Apache Flink's checkpointing algorithm** | de facto |
| Algorand | [1607.01341](https://arxiv.org/abs/1607.01341) | 2016-07-05 | Byzantine agreement via VRFs; now at v9 | de facto |
| Casper the Friendly Finality Gadget | [1710.09437](https://arxiv.org/abs/1710.09437) | 2017-10-25 | PoS finality; basis of Ethereum's transition | de facto |
| HotStuff: BFT Consensus in the Lens of Blockchain | [1803.05069](https://arxiv.org/abs/1803.05069) | 2018-03-13 | Linear-communication pipelined BFT; basis of DiemBFT | de facto |
| The latest gossip on BFT consensus (**Tendermint**) | [1807.04938](https://arxiv.org/abs/1807.04938) | 2018-07-13 | The Tendermint consensus specification | de facto |
| Study of Firecracker MicroVM | [2005.12821](https://arxiv.org/abs/2005.12821) | 2020-05-26 | microVM isolation — one of only **1,455 papers in all of `cs.OS`** | de facto |
| TensorFlow: Large-Scale ML on Heterogeneous Distributed Systems | [1603.04467](https://arxiv.org/abs/1603.04467) | 2016-03-14 | The TensorFlow whitepaper — **never a venue paper** | de facto |
| Ray: A Distributed Framework for Emerging AI Applications | [1712.05889](https://arxiv.org/abs/1712.05889) | 2017-12-16 | Task+actor model for distributed ML | de facto |

### On Cryptology ePrint

| Paper | ID | Recv | v | Publication info | First? |
|---|---|---|---|---|---|
| The Bitcoin Backbone Protocol: Analysis and Applications | [2014/765](https://eprint.iacr.org/2014/765) | 2014-09-30 | **17** | EUROCRYPT 2015 | **yes** |
| Ouroboros: A Provably Secure Proof-of-Stake Blockchain Protocol | [2016/889](https://eprint.iacr.org/2016/889) | 2016-09-14 | 8 | CRYPTO 2017 | **yes, ~10 months** |
| ALGORAND AGREEMENT: Super Fast and Partition Resilient BA | [2018/377](https://eprint.iacr.org/2018/377) | 2018-04-30 | 2 | Preprint | **never formally published** |
| Compact Multi-Signatures for Smaller Blockchains (**BLS aggregation**) | [2018/483](https://eprint.iacr.org/2018/483) | 2018-05-23 | 2 | Preprint | **never formally published** |
| Sync HotStuff: Simple and Practical Synchronous SMR | [2019/270](https://eprint.iacr.org/2019/270) | 2019-03-12 | 6 | Preprint | **yes** |

> Two of the five above were **never formally published anywhere**. If you cite BLS aggregate
> signatures or Algorand Agreement, the ePrint report *is* the paper.

### CRDTs — the case where the preprint server matters most

The conflict-free replicated data type literature is the clearest example in this whole survey of
why knowing the right server matters. **The originals are on HAL, not arXiv.**

| Paper | HAL identifier | Year | Why it matters |
|---|---|---|---|
| Shapiro, Preguiça, Baquero, Zawirski — *A comprehensive study of Convergent and Commutative Replicated Data Types* | [`inria-00555588`](https://inria.hal.science/inria-00555588v1) | 2011 | **The** CRDT reference text. INRIA **RR-7506**, 50 pp. Foundation of Automerge, Yjs, Riak, Redis CRDTs and every modern eventually-consistent store |
| Shapiro et al. — *Conflict-free Replicated Data Types* | [`inria-00609399`](https://inria.hal.science/inria-00609399v2) | 2011 | INRIA **RR-7687**, 18 pp. The condensed statement of the result |
| Shapiro et al. — *Conflict-free Replicated Data Types* (SSS 2011) | [`hal-00932836`](https://inria.hal.science/hal-00932836v1) | 2011 | The peer-reviewed SSS 2011 conference version — the canonical citation |

arXiv carries only a **2018 encyclopedia entry** ([1805.06358](https://arxiv.org/abs/1805.06358))
and a **2018 overview** ([1806.10254](https://arxiv.org/abs/1806.10254)). A title search on arXiv
for "Conflict-free Replicated Data Types" returns 11 hits and **none is the 2011 original**.
**Cite `inria-00555588` for priority.**

---

## 3. Databases

The thinnest category in the entire survey — four verified arXiv entries, and nothing meaningful
anywhere else. Database research is a conference-proceedings field that never adopted preprinting.

| Paper | arXiv ID | v1 | Why it matters | First? |
|---|---|---|---|---|
| The Missing Piece in Complex Analytics: Low Latency, Scalable Model Management | [1409.3809](https://arxiv.org/abs/1409.3809) | 2014-09-12 | Early framing of model management as a DB problem (CIDR line) | de facto |
| **The Case for Learned Index Structures** | [1712.01208](https://arxiv.org/abs/1712.01208) | 2017-12-04 | Launched the entire learned-index / learned-systems programme | de facto |
| LSM-based Storage Techniques: A Survey | [1812.07527](https://arxiv.org/abs/1812.07527) | 2018-12-18 | The reference survey for LSM engines | **proven** (VLDBJ 2019) |
| Neo: A Learned Query Optimizer | [1904.03711](https://arxiv.org/abs/1904.03711) | 2019-04-07 | Learned query optimisation | **proven** (PVLDB 2019) |

Relevant adjacent work sits under privacy rather than data management — **Path ORAM**
([2013/280](https://eprint.iacr.org/2013/280), ePrint, 2013-05-16, posted before CCS 2013) is the
oblivious-storage result that encrypted-database designs build on.

---

## 4. Computer architecture, hardware and accelerators

| Paper | arXiv ID | v1 | Why it matters | First? |
|---|---|---|---|---|
| EIE: Efficient Inference Engine on Compressed Deep Neural Network | [1602.01528](https://arxiv.org/abs/1602.01528) | 2016-02-04 | Sparse-weight inference accelerator; ISCA-line work | de facto |
| Efficient Processing of Deep Neural Networks: A Tutorial and Survey | [1703.09039](https://arxiv.org/abs/1703.09039) | 2017-03-27 | Sze et al. — the standard tutorial on DNN accelerator design | de facto |
| **In-Datacenter Performance Analysis of a Tensor Processing Unit** | [1704.04760](https://arxiv.org/abs/1704.04760) | 2017-04-16 | Google's TPUv1 — the defining industrial domain-specific-architecture measurement paper | de facto |
| Eyeriss v2: A Flexible Accelerator for Emerging DNNs on Mobile Devices | [1807.07928](https://arxiv.org/abs/1807.07928) | 2018-07-10 | Flexible NoC dataflow accelerator for sparse/compact DNNs | de facto |
| **The gem5 Simulator: Version 20.0+** | [2007.03152](https://arxiv.org/abs/2007.03152) | 2020-07-07 | The citable reference for the standard architecture simulator | de facto |
| Deep Compression (pruning + quantisation + Huffman coding) | [1510.00149](https://arxiv.org/abs/1510.00149) | 2015-10-01 | Model compression pipeline that drove a generation of accelerator design | de facto |
| FlashAttention: IO-Awareness | [2205.14135](https://arxiv.org/abs/2205.14135) | 2022-05-27 | An attention kernel that is really a memory-hierarchy result | de facto |

**A caution about volume.** `cs.AR` (Hardware Architecture) holds **8,932** papers and `cs.ET`
(Emerging Technologies) **7,815**, against `cs.LG`'s **283,807**. Computer architecture is a
*small* presence on arXiv. Its principal venues — ISCA, MICRO, HPCA, ASPLOS, DAC — remain
proceedings-first.

**No canonical RISC-V paper is on arXiv.** 250 hits for `ti:"RISC-V" AND cat:cs.AR`, but the
foundational documents are Berkeley EECS technical reports and RISC-V International specifications,
neither of which is a preprint deposit.

---

## 5. Embedded, side-channel and hardware security

**This is the section where Cryptology ePrint is irreplaceable**, and it is the strongest reason for
an embedded engineer to know the server exists. The CHES → TCHES and FSE → ToSC diamond-open-access
pipelines mean ePrint functions as *primary* literature for hardware security, not as a shadow copy.

| Paper | ID | Recv | Publication info | First? |
|---|---|---|---|---|
| Provably Secure Higher-Order Masking of AES | [2010/441](https://eprint.iacr.org/2010/441) | 2010-08-17 | full version, **CHES 2010** | companion |
| High-speed high-security signatures (**Ed25519**) | [2011/368](https://eprint.iacr.org/2011/368) | 2011-07-10 | full version, **CHES** | companion |
| Threshold Implementations of all 3x3 and 4x4 S-boxes | [2012/300](https://eprint.iacr.org/2012/300) | 2012-06-03 | extended version, **CHES 2012** | **yes, pre-CHES** |
| **Flush+Reload**: a High Resolution, Low Noise, L3 Cache Side-Channel Attack | [2013/448](https://eprint.iacr.org/2013/448) | 2013-07-22 | USENIX Security 2014 | **yes, ~1 year** |
| CacheBleed: A Timing Attack on OpenSSL Constant Time RSA | [2016/224](https://eprint.iacr.org/2016/224) | 2016-03-01 | Preprint | **yes** |
| ECDSA Key Extraction from Mobile Devices via Nonintrusive Physical Side Channels | [2016/230](https://eprint.iacr.org/2016/230) | 2016-03-02 | ACM CCS 2016 | **yes** |
| Number "Not Used" Once — practical fault attack on **pqm4** NIST candidates | [2018/211](https://eprint.iacr.org/2018/211) | 2018-02-26 | Preprint | **never formally published** |
| Differential Power Analysis of XMSS and SPHINCS | [2018/673](https://eprint.iacr.org/2018/673) | 2018-07-13 | COSADE 2018 | companion |
| **pqm4**: Testing and Benchmarking NIST PQC on **ARM Cortex-M4** | [2019/844](https://eprint.iacr.org/2019/844) | 2019-07-19 | Preprint | **never formally published** |
| LadderLeak: Breaking ECDSA With Less Than One Bit Of Nonce Leakage | [2020/615](https://eprint.iacr.org/2020/615) | 2020-05-25 | ACM CCS 2020 | **yes** |
| **Minerva**: The curse of ECDSA nonces (smartcards / secure elements) | [2020/728](https://eprint.iacr.org/2020/728) | 2020-06-17 | **TCHES 2020** | **yes** |
| **Ascon** PRF, MAC, and Short-Input MAC (NIST lightweight-crypto winner family) | [2021/1574](https://eprint.iacr.org/2021/1574) | 2021-12-03 | CT-RSA 2024 | **yes, ~2.5 years** |
| Combined Fault Injection + Side-Channel for **Android Secure-Boot Bypassing** | [2022/602](https://eprint.iacr.org/2022/602) | 2022-05-17 | CARDIS 2022 | **yes** |
| When Frodo Flips: End-to-End Key Recovery on FrodoKEM via **Rowhammer** | [2022/952](https://eprint.iacr.org/2022/952) | 2022-07-23 | ACM CCS 2022 | **yes** |
| To Be, or Not to Be Stateful: **Post-Quantum Secure Boot** using Hash-Based Signatures | [2022/1198](https://eprint.iacr.org/2022/1198) | 2022-09-11 | ASHES 2022 | **yes** |
| Recommendations for the Design and Validation of a Physical **TRNG** in a Cryptographic System | [2024/301](https://eprint.iacr.org/2024/301) | 2024-02-22 | Preprint (**CC0**) | **never formally published** |
| Optimized Implementations of Keccak, Kyber, and Dilithium on the **MSP430** | [2026/235](https://eprint.iacr.org/2026/235) | 2026-02-12 | **TCHES 2026** | **yes** |

Four of the seventeen were **never formally published** — including `pqm4`, which is the de facto
benchmark suite for post-quantum crypto on Cortex-M, and the TRNG design-and-validation
recommendations. For microcontroller cryptography, ePrint is not a preview of the literature; it
*is* the literature.

### The microarchitectural attacks are on arXiv, not ePrint

| Paper | arXiv ID | v1 | Why it matters |
|---|---|---|---|
| **Spectre Attacks: Exploiting Speculative Execution** | [1801.01203](https://arxiv.org/abs/1801.01203) | 2018-01-03 | Broke the CPU security model industry-wide |
| **Meltdown** | [1801.01207](https://arxiv.org/abs/1801.01207) | 2018-01-03 | Out-of-order execution reads kernel memory; forced KPTI worldwide |
| RowHammer: A Retrospective | [1904.09724](https://arxiv.org/abs/1904.09724) | 2019-04-22 | Mutlu & Kim's synthesis of DRAM disturbance research |
| Retrospective: Flipping Bits in Memory Without Accessing Them | [2306.16093](https://arxiv.org/abs/2306.16093) | 2023-06-28 | Retrospective on the 2014 original, **which is not on arXiv** |

### The one break that defines the server

**SIKE.** NIST advanced SIKE to the fourth round of its post-quantum standardisation process on
**2022-07-05**. Castryck and Decru posted *An efficient key recovery attack on SIDH* as
[**2022/975**](https://eprint.iacr.org/2022/975) at **2022-07-30 07:20:07 UTC** — twenty-five days
later, and roughly **nine months before** the EUROCRYPT 2023 paper existed. A NIST candidate was
killed by an unreviewed ePrint report. This is simultaneously the best argument for reading ePrint
and the clearest illustration that its contents are not reviewed.

---

## 6. Programming languages, compilers, formal methods and networking

The strongest HAL cluster after CRDTs, plus a thin arXiv presence.

### On HAL

| Paper | HAL identifier | Year | Why it matters |
|---|---|---|---|
| Leroy — *Formal verification of a realistic compiler* | `inria-00415861` | 2009 | **CompCert.** CACM 52(7). Proof that an optimising C compiler can be machine-verified |
| Leroy — *A formally verified compiler back-end* | `inria-00360768` | 2009 | The full CompCert back-end, J. Automated Reasoning 43(4):363–446 |
| Cornes, Courant, Filliâtre, Huet, Manoury et al. — *The Coq Proof Assistant, Reference Manual, Version 5.10* | `inria-00069994` | **1995** | Primary-source Coq documentation, INRIA **RT-0177** |
| Barras, Boutin, Cornes, Courant, Filliâtre et al. — *Coq Reference Manual: Version 6.1* | `inria-00069968` | 1997 | The Coq 6.x lineage |
| Filliâtre, Paskevich, Melquiond, Marché, Bobot — *Why3 version 1.0* | `hal-03136256` | 2018 | Deductive program verification platform |
| Duprat, Moya Lamiel, Kirchner, Correnson, Delmas — *Spreading Static Analysis with Frama-C in Industrial Contexts* | `hal-01260276` | 2016 | **Frama-C in real embedded/avionics practice** |
| Patte, Prevosto — *Typestates specification and verification in Frama-C* | `cea-05312386` | 2025 | Current CEA formal-methods work |
| Pedregosa, Varoquaux, Gramfort, Michel, Thirion et al. — *Scikit-learn: Machine Learning in Python* | `hal-00650905` | 2011 | One of the most-cited software papers in existence |
| Mansard, Khatib, Kheddar — *A unified approach to integrate unilateral constraints in the stack of tasks* | `lirmm-00798676` | 2009 | IEEE T-RO. Whole-body control; ancestor of modern task-priority stacks |

Note the dates: **Coq's 1995 reference manual is on HAL and nowhere else in this survey.** If you
need primary sources for the French formal-methods and verified-compiler tradition, HAL is the only
server that has them.

### On arXiv

| Paper | arXiv ID | v1 | Why it matters | First? |
|---|---|---|---|---|
| **MLIR: A Compiler Infrastructure for the End of Moore's Law** | [2002.11054](https://arxiv.org/abs/2002.11054) | 2020-02-25 | Multi-level IR; now the substrate for ML compilers and much EDA tooling | de facto |
| **Programming Protocol-Independent Packet Processors (P4)** | [1312.1719](https://arxiv.org/abs/1312.1719) | 2013-12-05 | Defined programmable data planes | de facto |
| Channel polarization: capacity-achieving codes for symmetric binary-input memoryless channels | [0807.3917](https://arxiv.org/abs/0807.3917) | 2008-07-24 | **Arıkan's polar codes — adopted for 5G NR control channels**; at v5 | de facto |
| What Will 5G Be? | [1405.2957](https://arxiv.org/abs/1405.2957) | 2014-05-12 | The agenda-setting 5G survey | ≈ same-year |

---

## 7. Protocol security — TLS and Signal

| Paper | ID | Recv | Publication info | First? |
|---|---|---|---|---|
| A Cryptographic Analysis of the **TLS 1.3** Handshake Protocol Candidates | [2015/914](https://eprint.iacr.org/2015/914) | 2015-09-22 | ACM CCS 2015 | **yes — analysed drafts pre-RFC** |
| A Formal Security Analysis of the **Signal** Messaging Protocol | [2016/1013](https://eprint.iacr.org/2016/1013) | 2016-10-27 | IEEE EuroS&P 2017 | **yes** |
| A Cryptographic Analysis of the TLS 1.3 Handshake Protocol (journal version) | [2020/1044](https://eprint.iacr.org/2020/1044) | 2020-08-28 | **JoC 2021** | **yes** |

The TLS 1.3 entry is the interesting one: the analysis was posted **while the RFC was still in
draft**, and fed back into the standard. That is the mechanism by which an unreviewed preprint
server does load-bearing work in protocol design.

---

## 8. Zero-knowledge, FHE and post-quantum — all ePrint

These fields preprint on ePrint essentially universally. Two entries below have **never been
formally published** and are nonetheless deployed in production systems worldwide.

| Paper | ID | Recv | v | Publication info | First? |
|---|---|---|---|---|---|
| Pinocchio: Nearly Practical Verifiable Computation | [2013/279](https://eprint.iacr.org/2013/279) | 2013-05-16 | 1 | full version of IEEE S&P 2013 | companion |
| Zerocash: Decentralized Anonymous Payments from Bitcoin | [2014/349](https://eprint.iacr.org/2014/349) | 2014-05-19 | 1 | IEEE S&P 2014 | companion |
| On the Size of Pairing-based Non-interactive Arguments (**Groth16**) | [2016/260](https://eprint.iacr.org/2016/260) | 2016-03-08 | 2 | EUROCRYPT 2016 | **yes** |
| Bulletproofs: Short Proofs for Confidential Transactions and More | [2017/1066](https://eprint.iacr.org/2017/1066) | 2017-11-10 | **14** | IEEE S&P 2018 | **yes** |
| Scalable, transparent, post-quantum secure computational integrity (**STARK**) | [2018/046](https://eprint.iacr.org/2018/046) | 2018-01-10 | 4 | Preprint | **never formally published** |
| **PLONK** | [2019/953](https://eprint.iacr.org/2019/953) | 2019-08-21 | **44** | Preprint | **never formally published** |
| Fully Homomorphic Encryption without Bootstrapping (**BGV**) | [2011/277](https://eprint.iacr.org/2011/277) | 2011-05-28 | 3 | "Unknown where it was published" | **yes** |
| Somewhat Practical Fully Homomorphic Encryption (**BFV**) | [2012/144](https://eprint.iacr.org/2012/144) | 2012-03-22 | 1 | "Unknown where it was published" | **yes** |
| Homomorphic Encryption for Arithmetic of Approximate Numbers (**CKKS**) | [2016/421](https://eprint.iacr.org/2016/421) | 2016-05-01 | 5 | ASIACRYPT 2017 | **yes, ~18 months** |
| Towards quantum-resistant cryptosystems from supersingular isogenies (**SIDH**) | [2011/506](https://eprint.iacr.org/2011/506) | 2011-09-18 | 2 | PQCrypto 2011 | companion |
| SPHINCS: practical stateless hash-based signatures | [2014/795](https://eprint.iacr.org/2014/795) | 2014-10-10 | 2 | EUROCRYPT 2015 | **yes** |
| Post-quantum key exchange — a new hope (**NewHope**) | [2015/1092](https://eprint.iacr.org/2015/1092) | 2015-11-10 | 9 | USENIX Security 2016 | **yes** |
| CRYSTALS-Dilithium (**→ NIST ML-DSA**) | [2017/633](https://eprint.iacr.org/2017/633) | 2017-06-27 | 2 | **TCHES 2018** | **yes** |
| CRYSTALS-Kyber (**→ NIST ML-KEM**) | [2017/634](https://eprint.iacr.org/2017/634) | 2017-06-27 | 2 | EuroS&P 2018 | **yes** |
| **An efficient key recovery attack on SIDH** (killed SIKE) | [2022/975](https://eprint.iacr.org/2022/975) | 2022-07-30 | 4 | EUROCRYPT 2023 | **yes, ~9 months** |

**PLONK is at version 44 and was never published.** Both NIST post-quantum standards — ML-KEM and
ML-DSA — were on ePrint years before standardisation.

---

## 9. Machine learning and ML systems — arXiv, effectively exclusively

Thirty foundational and seventeen systems entries were verified; the complete tables are in
[arXiv §7.1 and §7.2](arxiv.md). The pattern is uniform and worth stating once rather than
reproducing: **almost every one is marked "de facto"** — no venue metadata at all. For this
field the arXiv document *is* the version of record, permanently.

A representative slice:

| Paper | arXiv ID | v1 | Note |
|---|---|---|---|
| **Attention Is All You Need** | [1706.03762](https://arxiv.org/abs/1706.03762) | 2017-06-12 | The Transformer. Now at **v7**, last updated 2023-08-02 |
| Adam: A Method for Stochastic Optimization | [1412.6980](https://arxiv.org/abs/1412.6980) | 2014-12-22 | The default optimiser of deep learning; now at **v9** |
| Deep Residual Learning for Image Recognition (**ResNet**) | [1512.03385](https://arxiv.org/abs/1512.03385) | 2015-12-10 | The author comment reads **"Tech report"** |
| Language Models are Few-Shot Learners (**GPT-3**) | [2005.14165](https://arxiv.org/abs/2005.14165) | 2020-05-28 | In-context learning at 175B parameters |
| Training Compute-Optimal LLMs (**Chinchilla**) | [2203.15556](https://arxiv.org/abs/2203.15556) | 2022-03-29 | Reset industry training budgets |
| ZeRO: Memory Optimizations Toward Trillion Parameter Models | [1910.02054](https://arxiv.org/abs/1910.02054) | 2019-10-04 | Sharded optimiser state; DeepSpeed's core |
| Efficient Memory Management for LLM Serving with **PagedAttention** (vLLM) | [2309.06180](https://arxiv.org/abs/2309.06180) | 2023-09-12 | Virtual-memory paging applied to the KV cache |
| PyTorch: An Imperative Style, High-Performance DL Library | [1912.01703](https://arxiv.org/abs/1912.01703) | 2019-12-03 | The PyTorch reference paper |
| **DeepSeek-R1** | [2501.12948](https://arxiv.org/abs/2501.12948) | 2025-01-22 | `journal_ref` = *Nature* 645:633–638 (2025) — **proven** arXiv-first |

Only **6 of the 79** verified arXiv landmarks carry a `journal_ref` at all.

---

## 10. Optimisation, solvers and scientific software

Not glamorous, but these are the entries a working engineer is most likely to actually depend on.

### Optimization Online

| Eprint | Why it matters |
|---|---|
| **IPOPT** (`2004/03/836`) | The interior-point NLP solver embedded in a generation of engineering tooling |
| **Computing in Operations Research using Julia** (`2013/05/3883`) | JuMP's ancestor |
| **QUBO tutorial** (`2019/01/7014`) | The reference introduction for quantum-annealing and Ising-machine formulations |
| SCIP Optimization Suite 9.0 / 10.0 | The release documentation for the standard academic MILP solver |

The durability result matters as much as the content: `DB_HTML/2004/03/836.html` **still resolves
22 years later**. The caveat is that old `DB_FILE/*.pdf` links now land on the HTML abstract page.

### ECSarXiv — batteries, MEMS and semiconductor process

Only 323 preprints exist, but the subject graft includes *Atomic Layer Deposition/Etching*,
*High-k / Low-k Dielectrics*, *Interconnects*, *Group III-V Semiconductors* and *VLSI and Circuits,
Embedded and Hardware Systems*. Verified content includes the **PyBaMM** announcement, nonlinear
EIS of Li-ion cells, a stretched-exponential capacity-fade master curve, lithium-plating detection,
a high-temperature silicon **MEMS pressure-sensor bridge circuit**, MOS gas sensors, KOH-IPA wafer
etching and low-temperature Cu-Cu wafer bonding. **44 records are deposited under LGPL-3.0** —
i.e. they are software.

### Zenodo — where the software itself lives

Zenodo hosts few preprints (3.4% of records) but **284,518 software concept records across 712,318
versions** — a 2.5× version-to-concept ratio against 1.14× corpus-wide, which is direct quantitative
evidence that the GitHub-release-to-DOI pipeline is being used at scale. This is where conference
artifact-evaluation packages, firmware releases and KiCad projects get citable identifiers. See
[Zenodo § concept vs version DOI](zenodo.md) — **cite the version DOI**, not the concept DOI.

### bioRxiv — the scientific-software channel nobody expects

`Bioinformatics` is **30,363** preprints, 8.7% of bioRxiv and its #3 category in 2025. Combined
with a **69–78% eventual-publication rate** for mature cohorts, it is measurably the most reliable
large server in this survey — and a great deal of widely used scientific software was announced
there first.

---

## 11. Summary — where to look, by field

| If you are looking for… | Go to | Do **not** rely on |
|---|---|---|
| Classic distributed systems / databases (pre-2015) | **ACM DL, USENIX** — not a preprint server | arXiv (verified absent) |
| Modern consensus protocols with proofs | **Cryptology ePrint** | arXiv alone |
| Modern distributed systems / dataflow | **arXiv `cs.DC`** | — |
| CRDTs, CompCert, Coq, Frama-C | **HAL** | arXiv (only later derivatives) |
| ML, ML systems, inference infrastructure | **arXiv** | anywhere else |
| Side-channel, fault injection, MCU crypto | **Cryptology ePrint** | arXiv |
| Speculative-execution and DRAM attacks | **arXiv `cs.CR`** | ePrint (verified absent) |
| Computer architecture | **ISCA/MICRO/HPCA proceedings**; arXiv `cs.AR` is thin (8,932) | — |
| Solvers, MILP, scheduling | **Optimization Online** + arXiv `math.OC` | — |
| Batteries, MEMS, semiconductor process | **ECSarXiv**, **ChemRxiv** | arXiv |
| The open copy of an IEEE paper | **TechRxiv** via the Crossref `is-preprint-of` link | — |
| Research code, firmware, datasets, artifacts | **Zenodo** | any preprint server |
| Scientific software announcements | **bioRxiv `Bioinformatics`** | — |
