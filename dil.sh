paste dil_list.txt dil_list2.txt | while IFS="$(printf '\t')" read -r f1 f2
do
  printf 'source proj_conf.sh; fslmaths %s -dilF -dilF -dilF %s\n' "$f1" "$f2" >> dil
done