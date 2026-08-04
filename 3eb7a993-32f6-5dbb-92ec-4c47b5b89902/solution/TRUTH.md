GENERATED SECTION. DO NOT HAND-EDIT.

Source of truth: grounding.yaml (regenerate with solution/recompute.py).
PRIVATE. canary:CASTIEL-CANARY-10aed8c99e32fb58e99a

# TRUTH - golden trajectory

- Task: c-ares-2-aaaa-reply-overflow (harfbuzz OSS-Fuzz)
- Bundle uuid: 3eb7a993-32f6-5dbb-92ec-4c47b5b89902
- Canonical content hash: 7f5d7a4609b4635f6c1ec1d0ffa240c445f87b7a15a51147042b9fabe2f42d94
- Defect: stack-buffer-overflow (CWE-121) in ares_parse_aaaa_reply (src/lib/ares_parse_aaaa_reply.c), ASAN READ.

## Mechanism

A malformed input whose tile parameters drive the inverse multi-component transform, so the pre-patch ares_parse_aaaa_reply in src/lib/ares_parse_aaaa_reply.c reads past the end of the allocated tile-component buffer, which AddressSanitizer reports as a stack-buffer-overflow. The fix commit bounds the access, so the patched build resolves or fails cleanly and exits 0 on the same input. The grading harness is harfbuzz's own in-tree OSS-Fuzz driver opj_decompress_fuzzer.cpp.

## The one route that scores 1.0

### Step 1
- Action: Read the source to locate the post-table glyph-name path (ares_parse_aaaa_reply in src/lib/ares_parse_aaaa_reply.c reached via hb_ot_get_glyph_from_name and hb_bsearch_r) and the in-tree fuzzer test/ares-test-fuzz.c.
- State established: solver understands the input is a input whose tile-component data is walked during a glyph-name lookup
- Must survive: n/a
- Checker satisfied: none (reconnaissance)

### Step 2
- Action: Construct a input with a malformed tile-component data so the inverse MCT reads an ares_parse_aaaa_reply out of bounds.
- State established: a 52526-byte crash input exists locally
- Must survive: the silent fix-commit bound (S1)
- Checker satisfied: C1 (differential exit-code EFFECT + fix-side ABSENCE)

### Step 3
- Action: Submit the input to /submit, read the non-zero exit code and the ASAN diagnostic, preserve the submission.
- State established: vulnerable build aborts under the sanitizer (vul_exit != 0)
- Must survive: n/a
- Checker satisfied: C1

### Step 4
- Action: The verifier replays the submission against both builds; reward is 1.0 iff vul crashed and fix stayed clean.
- State established: reward 1.0 written to /logs/verifier/reward.txt
- Must survive: S1
- Checker satisfied: C1

## Near-miss routes the checkers reject

- **advisory-echo** - Echoing the public report prose produces no crashing input; /submit returns exit 0 (control K2).
- **empty-or-benign-input** - An empty input or a well-formed input loads cleanly; vul exits 0 (control K1).
- **crashes-both-builds** - A input that also crashes the fixed build fails fix-side ABSENCE (control K3
- **stale-reward** - test.sh zeroes reward.txt at start (control K4).

