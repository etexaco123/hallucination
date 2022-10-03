#!/bin/bash
#SBATCH --time=3-00:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=120GB
#SBATCH --partition=gpu

module load IPython/7.9.0-fosscuda-2019b-Python-3.7.4
module remove SciPy-bundle
source /data/$USER/envs/jnmt_env/bin/activate

pip install click==7.1.2

jupyter nbconvert --to notebook --execute translate.ipynb --ExecutePreprocessor.timeout=300000

