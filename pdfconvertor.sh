#!/bin/bash
echo hello



root_dir=$'/home/nabil/Documents/CG/labassignments/'
echo $(echo $root_dir)
all_jpg_file=$(find $root_dir -type f -name '*.JPG' -or -name '*.JPG');
#echo $all_jpg_file
for f in $all_jpg_file
do
	echo $f
    if [ -f "$f" ]
  	then
        echo "Processing file $f"
    fi
done
