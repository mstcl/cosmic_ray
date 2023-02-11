#! /bin/sh

for filename in $HOME/data/${1}/*.txt
  do
    [ -e "$filename" ] || continue
    convert.py -i "$filename" -o "$(echo "${filename}" | cut -d "." -f 1).dat"
done
