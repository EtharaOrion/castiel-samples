# Agent environment. Sources the read-only target tree from the vulnerable image
# (pinned by @sha256; floating tags forbidden) and strips every ground-truth
# path so the compiled binary, the oracle PoC, and the arvo runner never reach
# the agent. The compiled target runs only behind the task-server sidecar.
FROM --platform=linux/amd64 426628337772.dkr.ecr.ap-south-1.amazonaws.com/castiel@sha256:9eeaa616847760d0756f08544269101f663b4f6e64d6061988848c1847b5ccc8 AS src-stage

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
