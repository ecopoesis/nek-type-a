FROM dcowden/cadquery:latest

USER root
RUN conda install -c conda-forge numpy scipy numba quaternion svgwrite
RUN pip install svgpathtools

USER cq