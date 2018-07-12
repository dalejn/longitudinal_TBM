paste pad_list.txt | while IFS="$(printf '\t')" read -r f1
do
  printf 'source proj_conf.sh;ImageMath 3 %s PadImage %s  -245\n' "$f1" "$f1" >> pad2
done