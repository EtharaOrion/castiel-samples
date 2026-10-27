<p align="center"><img src="images/hero.svg" alt="castiel" width="720"></p>

# castiel: samples

<p align="center"><b>The samples lane: 10 of 30 Harbor task bundles.</b></p>

<p align="center"><a href="#summary"><img src="https://img.shields.io/badge/bundles-10_of_30-845EF7" alt="bundles: 10 of 30"></a> <a href="#evidence-status"><img src="https://img.shields.io/badge/sealed-0-845EF7" alt="sealed: 0"></a> <a href="#difficulty-tiers"><img src="https://img.shields.io/badge/difficulty-measured-845EF7" alt="difficulty: measured"></a></p>

<p align="center"><sub><a href="#abstract">Abstract</a> | <a href="#summary">Summary</a> | <a href="#difficulty-tiers">Difficulty tiers</a> | <a href="#evidence-status">Evidence status</a> | <a href="#coverage">Coverage</a> | <a href="#dataset-structure">Dataset structure</a> | <a href="#verification-and-quality-assurance">Verification and quality assurance</a> | <a href="#reproduction">Reproduction</a> | <a href="#cite">Cite</a> | <a href="#license">License</a> | <a href="#contact">Contact</a></sub></p>

## Abstract

The curated lane of this corpus: at most 30 Harbor task bundles, every anchor seated first and every other bundle in seal order. Bundles past that ceiling live in `delivery/`.

Each bundle is one Harbor task in a directory named by its content-derived uuid5, so the name doubles as an integrity check. This page is rendered from the resident bundles on every reconcile; a value a bundle does not carry reads `absent`, and the page never fills one in.

## Summary

| Property | Value |
| --- | --- |
| Bundles | 10 of 30 |
| Sealed | 0 of 10 |
| Registrations | unregistered (10) |
| Audit verdicts | none (10) |
| Harbor schema | 1.3 (10) |

## Difficulty tiers

Difficulty is measured by the signed pilot alone and never declared in a bundle, so this page states no tier a bundle claims.

## Evidence status

The verdict is the audit outcome recorded at the sealed digest, and `none` means no verdict has landed for that digest yet. Only an authoring run removes a bundle from this lane, so removal waits for the next one.

| uuid | Verdict | Sealed digest | Stream |
| --- | --- | --- | --- |
| 04c752f2-7380-5bec-91ff-11f7a84a4d89 | none | absent | none |
| 3988315c-22da-5cde-8f92-ab31a6aaf161 | none | absent | none |
| 3eb7a993-32f6-5dbb-92ec-4c47b5b89902 | none | absent | none |
| 458e3df0-37f8-5861-b007-00325c4baa9b | none | absent | none |
| 90329493-d360-568e-96af-0736ea57f739 | none | absent | none |
| 98006496-3e9d-512a-ba2d-ebd0c20b285d | none | absent | none |
| 9a0ce3eb-b85d-57e8-b78d-25a048051e3a | none | absent | none |
| ab3b2b6b-a382-5da6-bc38-b90f52b7ff40 | none | absent | none |
| caddac3b-17a1-5aa0-a1c7-469a012dd0d1 | none | absent | none |
| ce69dba4-bc24-5b53-a3b3-24ad826a9f99 | none | absent | none |

## Coverage

No resident bundle declares a keyword.

## Dataset structure

| Bundle | Task | Keywords | Registration | Sealed at | Tier |
| --- | --- | --- | --- | --- | --- |
| [`04c752f2-7380-5bec-91ff-11f7a84a4d89`](04c752f2-7380-5bec-91ff-11f7a84a4d89/) | `ethara-ai/pcre2-match-overflow` | absent | unregistered | unsealed | - |
| [`3988315c-22da-5cde-8f92-ab31a6aaf161`](3988315c-22da-5cde-8f92-ab31a6aaf161/) | `ethara-ai/libjpeg-turbo-smooth-overflow` | absent | unregistered | unsealed | - |
| [`3eb7a993-32f6-5dbb-92ec-4c47b5b89902`](3eb7a993-32f6-5dbb-92ec-4c47b5b89902/) | `ethara-ai/c-ares-2-aaaa-reply-overflow` | absent | unregistered | unsealed | - |
| [`458e3df0-37f8-5861-b007-00325c4baa9b`](458e3df0-37f8-5861-b007-00325c4baa9b/) | `ethara-ai/harfbuzz-cff-blend-overflow` | absent | unregistered | unsealed | - |
| [`90329493-d360-568e-96af-0736ea57f739`](90329493-d360-568e-96af-0736ea57f739/) | `ethara-ai/openjpeg-mct-decode-overflow` | absent | unregistered | unsealed | - |
| [`98006496-3e9d-512a-ba2d-ebd0c20b285d`](98006496-3e9d-512a-ba2d-ebd0c20b285d/) | `ethara-ai/harfbuzz-kerx-sanitize-overflow` | absent | unregistered | unsealed | - |
| [`9a0ce3eb-b85d-57e8-b78d-25a048051e3a`](9a0ce3eb-b85d-57e8-b78d-25a048051e3a/) | `ethara-ai/jsoncpp-readcomment-overflow` | absent | unregistered | unsealed | - |
| [`ab3b2b6b-a382-5da6-bc38-b90f52b7ff40`](ab3b2b6b-a382-5da6-bc38-b90f52b7ff40/) | `ethara-ai/lz4-compress-write32-overflow` | absent | unregistered | unsealed | - |
| [`caddac3b-17a1-5aa0-a1c7-469a012dd0d1`](caddac3b-17a1-5aa0-a1c7-469a012dd0d1/) | `ethara-ai/openjpeg-mct-real-overflow` | absent | unregistered | unsealed | - |
| [`ce69dba4-bc24-5b53-a3b3-24ad826a9f99`](ce69dba4-bc24-5b53-a3b3-24ad826a9f99/) | `ethara-ai/harfbuzz-post-array-overflow` | absent | unregistered | unsealed | - |

```mermaid
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#131a33","primaryTextColor":"#e8ecff","primaryBorderColor":"#845EF7","lineColor":"#22d3ee","fontFamily":"monospace"}}}%%
flowchart LR
    bundle["&lt;uuid&gt;/"]
    bundle --> n0["task.toml<br/>runner manifest"]
    bundle --> n1["instruction.md<br/>objective the agent reads"]
    bundle --> n2["environment/<br/>agent sandbox image"]
    bundle --> n3["tests/<br/>verifier, hidden from the agent"]
    bundle --> n4["solution/<br/>private oracle"]
```

```mermaid
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#131a33","primaryTextColor":"#e8ecff","primaryBorderColor":"#845EF7","lineColor":"#22d3ee","fontFamily":"monospace"}}}%%
flowchart LR
    staging["staging/"]
    staging --> samples["samples/<br/>10 of 30"]
    samples --> delivery["delivery/<br/>0 of 10000"]
    delivery --> stock["stock/<br/>0 of 10000"]
```

## Verification and quality assurance

Each bundle's signed provenance carrier holds its screening roots, screening instant, and absolute expiry. Placement moves that carrier into the private derivation set, which this page never reads, so reconcile lists no root it cannot verify here.

## Reproduction

Each bundle directory is a complete Harbor task: `task.toml` is the runner manifest, `instruction.md` the objective, `environment/` the sandbox image, and `tests/` the verifier. Point a Harbor runner at one bundle directory to reproduce it; `solution/` stays private.

## Cite

```bibtex
@misc{castielsamples,
  title = {castiel: samples}
}
```

## License

See the license of the repository that publishes this lane.

## Contact

[Ethara AI on GitHub](https://github.com/Ethara-Ai), [SECURITY.md](SECURITY.md) for a private report, and [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution route.

---

## Copyright

Copyright (c) 2026 Green Rider Technology LLP (Ethara AI). All rights reserved.
