while read line; do
    for i in {1..2}; do
	echo "$line"
done
done < T1_list.txt