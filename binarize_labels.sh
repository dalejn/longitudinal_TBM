#!/bin/bash

paste dil_list2.txt | while IFS="$(printf '\t')" read -r f1
do
  printf 'fslmaths %s -bin %s\n' "$f1" "$f1" >> binarize
done