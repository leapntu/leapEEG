#!/bin/bash

#folder=$1
#echo $file
#while IFS= read -r line

#old=$1

mkdir "converted"

#cd "$old"/

for file in *.wav

do
#echo "$file"
    sox "$file" -r 48000 converted/"$file"
done