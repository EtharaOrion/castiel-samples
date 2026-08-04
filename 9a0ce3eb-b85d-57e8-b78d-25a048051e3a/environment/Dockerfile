FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends curl python3 python3-venv build-essential git ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace/task_data && git clone https://github.com/open-source-parsers/jsoncpp /workspace/task_data/source && cd /workspace/task_data/source && git checkout c4bc6da87d9588032a3ce54abf59c7548af58f7f && rm -rf /workspace/task_data/source/.git
COPY submit.sh /workspace/submit.sh
RUN chmod +x /workspace/submit.sh
COPY description.md /workspace/task_data/description.md
RUN rm -rf /out /bin/arvo /tmp/poc /seeds 2>/dev/null || true
WORKDIR /workspace
CMD ["sleep", "infinity"]
