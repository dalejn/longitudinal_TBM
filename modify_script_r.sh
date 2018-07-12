for x in `cat subs.txt`; do
    echo ${x}
    cp ants_test_slurm_r.ipynb ants_test_slurm_${x}r.ipynb
    sed -i "s/datadir,'sub-102/datadir,'${x}r/g" ants_test_slurm_${x}r.ipynb
    sed -i "s/Workflow(name='/Workflow(name='${x}r_/g" ants_test_slurm_${x}r.ipynb
    sed -i "s/datadir,'normflow/datadir,'${x}r_normflow/g" ants_test_slurm_${x}r.ipynb

    ls dil-${x}*rh*.nii.gz|cut -c5-24|tr '\n' ',' > ${x}r_sessions.txt 
    sed -e 's/.$//' -e "s/^\|$/'/g" -e "s/,/','/g" ${x}r_sessions.txt > ${x}r_sessions2.txt
    sess_id=`cat ${x}r_sessions2.txt` 
    echo ${sess_id}
    sed -i "s/placeholder/${sess_id}/g" ants_test_slurm_${x}r.ipynb

    echo "jupyter nbconvert --to python ants_test_slurm_${x}r.ipynb" >> convert_to_python_r
done