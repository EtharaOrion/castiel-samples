# castiel-samples

A **public, un-gated sample slice** of the castiel corpus. It exists so that a
reader without vendor credentials can inspect the shape of a castiel task —
schema, provenance, contamination labels, expert-review record — without ever
touching an exploit-capable artifact.

| Field | Value |
| :--- | :--- |
| Vendor | `ethara-ai` |
| Schema | Harbor task package, version 1.3 |
| Access tier | Public only |
| Full corpus | 21 tasks, gated — see the `dataset` submodule |
| Verifier | Deterministic differential, no LLM in the reward loop |

---

## What this repository is

castiel is a frontier-defeating benchmark: an agent receives a vulnerable
source tree behind a sidecar and must craft a proof-of-concept input that
crashes the vulnerable build while leaving the fixed build clean. Grading is a
closed-form differential — no language model and no human in the reward loop.

The complete corpus of 21 real OSS-Fuzz vulnerability tasks lives in the
**gated** `dataset` submodule. This `samples` repository carries only the
**public tier** of that corpus, so it can be browsed by anyone.

## What is — and is not — here

Following the tiered-access model in the dataset README, a sample package
carries the public tier only:

**Included (public):**
- Task metadata and Harbor `task.toml` schema (version 1.3)
- Distribution tables (project, sanitizer, bug class, category)
- Contamination labels and disclosure
- Expert-review records and provenance (OSV / OSS-Fuzz identifiers)
- Human-readable task descriptions and this README

**Excluded (gated / embargoed — never in this repository):**
- Proof-of-concept input bytes (`ground_truth_poc`)
- Vulnerable and fixed container images (pulled by sha256 digest from a private
  registry with vendor-issued credentials)
- Per-task bearer tokens and oracle `/solve` payloads

To reproduce a task end-to-end — pull pinned images, submit the gold PoC, run
the differential verifier — you need gated access to the `dataset` submodule
and its private registry. See `dataset/README.md`, sections 6 and 8.

## Current status

**No sample package has landed here yet.** This slice is a placeholder, empty
by design, in the same spirit as the parent README's empty Results, Analysis,
and Coverage sections: content appears only once it is produced through
regenerable code from the gated corpus, never authored by assertion. When a
sample lands, it will follow the per-task contract documented in
`dataset/README.md`, section 3, restricted to the public tier above.

## Provenance and responsible use

Every task in the castiel corpus is drawn from the public OSS-Fuzz corpus and
carries `contamination_risk: high`: canonical identifiers and their PoCs are
publicly disclosed and almost certainly present in frontier-model pretraining
data. Evaluators who care about clean held-out performance should
canary-mutate inputs and reword prompts before measuring capability.

This corpus evaluates offensive security capability. Any attacker-capability
claim built on it must be paired with a corresponding defensive evaluation
against the same tasks. Arbitrary third-party live targets are out of scope.

## References

| Resource | URL |
| :--- | :--- |
| Harbor framework | https://www.harborframework.com/docs |
| OSV.dev | https://osv.dev |
| OSS-Fuzz | https://google.github.io/oss-fuzz |
| CyberGym (UC Berkeley) | https://arxiv.org/abs/2506.02548 |

## License

Released under the MIT License. See the `LICENSE` file. Task bundles and
datasets produced through castiel retain their own upstream licenses.
