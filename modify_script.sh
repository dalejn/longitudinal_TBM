for x in `cat subs.txt`; do
    echo ${x}
    cp ants_test_slurm.ipynb ants_test_slurm_${x}.ipynb
    sed -i "s/datadir,'sub-102/datadir,'${x}/g" ants_test_slurm_${x}.ipynb
    sed -i "s/Workflow(name='/Workflow(name='${x}_/g" ants_test_slurm_${x}.ipynb
    sed -i "s/datadir,'normflow/datadir,'${x}_normflow/g" ants_test_slurm_${x}.ipynb

    ls dil-${x}*lh*.nii.gz|cut -c5-24|tr '\n' ',' > ${x}_sessions.txt 
    sed -e 's/.$//' -e "s/^\|$/'/g" -e "s/,/','/g" ${x}_sessions.txt > ${x}_sessions2.txt
    sess_id=`cat ${x}_sessions2.txt` 
    echo ${sess_id}
    sed -i "s/placeholder/${sess_id}/g" ants_test_slurm_${x}.ipynb

    echo "jupyter nbconvert --to python ants_test_slurm_${x}.ipynb" >> convert_to_python
done