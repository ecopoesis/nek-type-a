#!/bin/bash
source activate nek-type-a && python -u /opt/cadquery/cq_cmd.py "${@:2}"
