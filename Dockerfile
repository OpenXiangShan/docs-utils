FROM ubuntu:noble

COPY . /app
RUN /app/dependency.sh && \
    apt clean && \
    git config --global --add safe.directory /work

WORKDIR /work
ENV PATH="/root/.local/bin:/root/bin:${PATH}"
CMD [ "/bin/bash" ]
