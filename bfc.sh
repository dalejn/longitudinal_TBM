paste bfc_list.txt| while IFS="$(printf '\t')" read -r f1
do
  printf 'export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;N4BiasFieldCorrection -d 3 -b [200] -c [50x50x40x30,0.00000001] -i %s -o %s -r 0 -s 2 --verbose 1\n' "$f1" "$f1" >> bfc
done