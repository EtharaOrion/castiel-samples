# Task-server sidecar. Holds BOTH the vulnerable and the fixed build and serves
# them behind /submit (vul only, no auth), /verify (both, bearer-gated), and
# /solve (oracle PoC, bearer-gated). Both base images are pinned by @sha256
# digest; floating tags are forbidden (remediates the CRUCIBLE G-DEL-PIN finding).
FROM --platform=linux/amd64 426628337772.dkr.ecr.ap-south-1.amazonaws.com/castiel@sha256:3686e2031c245c6be00d6da211126261a6ad237fa0def9e727a17b9ba23a81dd AS fix-runner

FROM --platform=linux/amd64 426628337772.dkr.ecr.ap-south-1.amazonaws.com/castiel@sha256:9eeaa616847760d0756f08544269101f663b4f6e64d6061988848c1847b5ccc8

RUN apt-get update && apt-get install -y --no-install-recommends curl python3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /cybergym/vul/out /cybergym/vul/bin /cybergym/fix/out /cybergym/fix/bin /tests
COPY --from=fix-runner /out /cybergym/fix/out
COPY --from=fix-runner /bin/arvo /cybergym/fix/bin/arvo
RUN cp -a /out/. /cybergym/vul/out/ && cp /bin/arvo /cybergym/vul/bin/arvo
RUN cp /tmp/poc /tests/ground_truth_poc
RUN rm -rf /out /tmp/poc

COPY task_server.py /task_server.py
EXPOSE 9111
CMD ["python3", "-u", "/task_server.py"]
