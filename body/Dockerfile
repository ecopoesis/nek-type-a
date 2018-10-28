FROM dcowden/cadquery:latest

USER root
COPY environment.yml conda_cq.sh cq_cmd.py $CQ_HOME/
RUN cd $CQ_HOME && conda env create environment.yml
RUN chmod ugo+x /opt/conda/bin/activate $CQ_HOME/conda_cq.sh

USER cq
ENTRYPOINT [ "/opt/cadquery/conda_cq.sh" ]
