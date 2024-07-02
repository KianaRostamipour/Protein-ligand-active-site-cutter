#!/bin/bash

base_dir=$(pwd)
expect_script_path="GROMACSProteinSetup.expect"
patterns=("pdb_pattern_*")

for pattern in "${patterns[@]}"; do
    for dir in ${base_dir}/pdb_*/${pattern}; do
        if [ -d "$dir" ]; then
            echo "Handling: $dir"
            
            sed "s|set pdb_file \"protein.pdb\"|set pdb_file \"${dir}/protein.pdb\"|g" "$expect_script_path" > "${dir}/temp_expect_script.expect"
            chmod +x "${dir}/temp_expect_script.expect"
            
            pushd "$dir" > /dev/null
            "./temp_expect_script.expect"
            popd > /dev/null
            
            rm "${dir}/temp_expect_script.expect"
        fi
    done
done

