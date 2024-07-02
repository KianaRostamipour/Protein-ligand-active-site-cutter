#!/bin/bash

base_dir=$(pwd)
patterns=("pdb_pattern_*")

for pattern in "${patterns[@]}"; do
    find "$base_dir" -type d -path "*/pdb_*/$pattern" | while read input_directory; do
        for input_file in "$input_directory"/cut_*.pdb "$input_directory"/neutral.pdb "$input_directory"/ligand.pdb; do
            [[ -e $input_file ]] || continue
            base_name=$(basename "$input_file" .pdb)
            output_file="$input_directory/$base_name.xyz"
            obabel -ipdb "$input_file" -oxyz -O "$output_file"
            echo "Converted: $input_file -> $output_file"
        done
    done
done

find "$base_dir" -type f \( -name "cut_pdb_*.xyz" -o -name "neutral.xyz" -o -name "ligand.xyz" \) -print0 | while IFS= read -r -d '' file_path; do
    echo "Handling: $file_path"
    file_dir=$(dirname "$file_path")
    parent_dir=$(dirname "$file_dir")
    base_name=$(basename "$file_path" .xyz)

    if [[ "$file_path" == *"cut"* ]]; then
        target_dir_name="complex_$base_name"
    elif [[ "$file_path" == *"neutral.xyz"* || "$file_path" == *"ligand.xyz"* ]]; then
        dir_for_naming=$(basename "$file_dir")
        target_dir_name="${dir_for_naming}_as"
        [[ "$file_path" == *"ligand.xyz"* ]] && target_dir_name="${dir_for_naming}_lig"
    fi

    target_dir="$parent_dir/$target_dir_name"
    mkdir -p "$target_dir"
    mv "$file_path" "$target_dir/"
    echo "Moved: $file_path -> $target_dir"
done


