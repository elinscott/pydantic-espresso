#!/bin/bash

# This script fetches the documentation for Quantum ESPRESSO from the source code, and converts it to xml format

# Provide helptext
if [ $# -ne 1 ]; then
   echo "Usage: $0 <path-to-quantum-espresso-root-directory>"
   exit 1
fi

# Check that $@ corresponds to the root directory of Quantum ESPRESSO
if [ ! -f $@/dev-tools/helpdoc ]; then
   echo "Error: $@ does not appear to correspond to the root directory of Quantum ESPRESSO"
   exit 1
fi

# Loop over all the .def files in the source code and copy them to the destination directory
for file in def_files/*/*; do
   # Sanitise the name of the file, converting INPUT_<name>.def to INPUT_<lowercase_name>.def
   sanitised_path=$(echo $file | sed -e 's/INPUT_\(.*\)\.def/INPUT_\L\1.def/')
   sanitised_name=${sanitised_path##*/}
   # Extract the tag (the subdirectory name i.e. def_files/<tag>/<name>.def)
   dest=xml_files/${file#def_files/}
   mkdir -p ${dest%/*}
   cp $file $dest
done

# Run the helpdoc script to convert the .def files to xml format
for f in xml_files/*/*.def; do
   echo -n "Converting $f to xml format... "
   $@/dev-tools/helpdoc $f &> /dev/null
   echo "done"
done

# Removing unwanted files
rm xml_files/*/*.def
rm xml_files/*/*.html
rm xml_files/*/*.txt
rm xml_files/*/*.xsl

