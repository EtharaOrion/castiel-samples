# Agent environment. Sources the read-only target tree from the vulnerable image
# (pinned by @sha256; floating tags forbidden) and strips every ground-truth
# path so the compiled binary, the oracle PoC, and the arvo runner never reach
# the agent. The compiled target runs only behind the task-server sidecar.
#
# PENDING-PHASE1-REGISTRY-PUSH: the src-stage digest below is an all-zero
# placeholder. The jsoncpp vulnerable image has been built hermetically from
# solution/image-build/vul at commit 83946a28 and the differential is proven
# locally (reward 1.0); it is not yet pushed to a registry. Phase 1 pushes it and
# replaces this placeholder with the real registry manifest digest. This
# Dockerfile does NOT build until that pin is real.
FROM --platform=linux/amd64 PLACEHOLDER-REGISTRY/castiel@sha256:0000000000000000000000000000000000000000000000000000000000000000 AS src-stage

FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl python3 python3-venv build-essential git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace/task_data
COPY --from=src-stage /src /workspace/task_data/source

COPY submit.sh /workspace/submit.sh
RUN chmod +x /workspace/submit.sh

COPY description.md /workspace/task_data/description.md

# Strip every ground-truth carrier: the compiled harness, the arvo runner, and
# the baked oracle PoC. The agent-visible boundary excludes all of them.
RUN rm -rf /out /bin/arvo /tmp/poc /seeds 2>/dev/null || true

WORKDIR /workspace
CMD ["sleep", "infinity"]
