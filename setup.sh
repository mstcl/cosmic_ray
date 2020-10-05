
# setup environment for cosmic ray experiment
export CR_BASE=$PWD

export PATH=/opt/anaconda/bin:$CR_BASE/DAQ:$CR_BASE/analysis:$PATH

export PYTHONPATH=$PYTHONPATH:$CR_BASE/DAQ:$CR_BASE/analysis

