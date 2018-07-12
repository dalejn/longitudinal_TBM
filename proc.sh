for x in `cat subs.txt`;do
    echo "source proj_conf.sh;python ants_test_slurm_${x}r.py"
done