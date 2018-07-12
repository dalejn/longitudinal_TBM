umask 0007
export base=/data/Hippo_ETPB/
export SUBJECTS_DIR=$base/sourcedata
module load freesurfer/6.0.0
source $FREESURFER_HOME/SetUpFreeSurfer.sh
module load fsl afni
export ANTSPATH=/data/zhoud4/build/antsbinApr2016/bin/
export PATH=$base/scripts:/data/DSST/scripts:${PATH}
source /data/DSST/scripts/aliases.sh
source conda/etc/profile.d/conda.sh; conda activate NiPype
