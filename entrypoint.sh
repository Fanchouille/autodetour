#!/usr/bin/env bash
eval "$(conda shell.bash hook)"
conda activate ${PWD}/.conda
python main.py