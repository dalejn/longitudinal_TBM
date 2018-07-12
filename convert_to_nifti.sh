paste label_list.txt subs_nifti.txt | while IFS="$(printf '\t')" read -r f1 f2
do
  printf 'mri_convert %s %s\n' "$f1" "$f2" >> convert_labels.sh
done