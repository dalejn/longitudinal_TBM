#!/bin/bash

paste label_files_right.txt new_label_files_right.txt | while IFS="$(printf '\t')" read -r f1 f2
do
  printf 'mri_convert ~/Hippo_hr/moa/derivatives/fs_subj_expert_opts/%s ~/Hippo_hr/moa/derivatives/fs_subj_expert_opts/%s\n' "$f1" "$f2" >> cplabels_right.sh
done