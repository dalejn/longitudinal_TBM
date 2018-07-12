paste T1_list2.txt dil_label_list.txt mask_list.txt | while IFS="$(printf '\t')" read -r f1 f2 f3
do
  printf 'source proj_conf.sh; mri_mask %s %s %s\n' "$f1" "$f2" "$f3" >> mask
done