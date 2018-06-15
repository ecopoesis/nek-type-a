FROM dcowden/cadquery:latest

USER root
RUN conda install -c conda-forge numpy scipy numba quaternion

USER cq