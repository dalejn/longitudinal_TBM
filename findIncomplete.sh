#!bin/bash

comm -3 \
    <(find ./*normflow11/_subject_id_sub-*/jacobian/ -maxdepth 0 -mindepth 0 -type d | sed 's#jacobian/##g') \
    <(find ./*normflow11/_subject_id_sub-*/ -maxdepth 0 -mindepth 0 -type d | sort) \