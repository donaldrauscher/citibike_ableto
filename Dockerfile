FROM continuumio/miniconda3:4.3.27

ADD environment.yml .

ENV PORT 9018
ENV CONDA_ENV citike
ENV PATH /opt/conda/envs/$CONDA_ENV/bin:$PATH

WORKDIR /app

COPY environment.yml .
RUN conda  env  update  --file=environment.yml --name=${CONDA_ENV}

ADD . .

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE $PORT

ENTRYPOINT ["/bin/bash", "-c", "entrypoint.sh"]