for x in `cat subs.txt`;do
    echo ${x}
#    echo "export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;AverageImages 3 ${x}-lhtemplate0.nii.gz 1 dil-${x}*.lh.hippoSfLabels-T1.long.v10.nii.gz lh.frame.nii.gz" >> templates
#    echo "export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;AverageImages 3 ${x}-rhtemplate0.nii.gz 1 dil-${x}*.rh.hippoSfLabels-T1.long.v10.nii.gz rh.frame.nii.gz" >> templates
    echo "export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;AverageImages 3 ${x}-lhtemplate2.nii.gz 1 ${x}*.2.lh.hippoSfLabels-T1.long.v10.nii.gz lh.frame.nii.gz" >> templates
    echo "export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;AverageImages 3 ${x}-rhtemplate2.nii.gz 1 ${x}*.2.rh.hippoSfLabels-T1.long.v10.nii.gz rh.frame.nii.gz" >> templates
done
