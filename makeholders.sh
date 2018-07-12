paste make_holder.txt make_holder2.txt | while IFS="$(printf '\t')" read -r f1 f2
do
  printf 'cp %s %s\n' "$f1" "$f2" >> makeholder
done