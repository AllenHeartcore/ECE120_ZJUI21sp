#!/bin/bash

# Check if number of arguments is correct
if [ $# -ne 2 ]; then 
    echo Usage: $0 file1 file2
    exit
fi

# $@ is the positional parameters starting from parameter 1
# "$@" is equivalent to "$1" "$2" ...
for file in "$@"
do
    # Check for valid file
    if [ ! -f ${file} ]
    then
        echo "Invalid file: \"${file}\""
        exit
    fi
done
for file in "$@"
do
    # Check if extension is 'sol'
    if [ ${file##*.} != "sol" ]
    then
        # Extract output
        h_lines=$(grep -c "Set R[0-7] to " ${file})
        ((h_lines += 39))
        head -n ${h_lines} ${file} | tail -n 16 > ${file}.out
    fi
done

# Name output files
if [ ${1##*.} != "sol" ]
then
    file1=$1.out
else
    file1=$1
fi
if [ ${2##*.} != "sol" ]
then
    file2=$2.out
else
    file2=$2
fi

# diff should produce the empty string if output files are equal
if [ -z "`diff ${file1} ${file2}`" ]
then
    echo "Test passed"
else
    echo "Test failed"
fi
echo "Output files: ${file1} ${file2}"

# Give the user the option to see output files
while true
do
    read -rsp $'Do you want to see output files (y/n)? ' -n1 key
    echo ""
    if [[ ${key,,} == y ]]
    then
        gedit ${file1} ${file2}&
        break
    elif [[ ${key,,} == n ]]
    then
        break
    else
        echo "Choice not recognized"
    fi
done

