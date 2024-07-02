import os
import glob
import pymol
from pymol import cmd

def boot_up_pymol():
    pymol.finish_launching(['pymol', '-cq'])

def merge_and_label_pdb(neutral_pdb, ligand_pdb, final_pdb):
    cmd.load(neutral_pdb, "neutral")
    cmd.load(ligand_pdb, "ligand")
    cmd.create("full_structure", "neutral + ligand")
    cmd.sort("full_structure")
    cmd.save(final_pdb, "full_structure")
    cmd.delete("all")

def go_through_directories():
    all_dirs = glob.glob(os.path.join(os.getcwd(), 'pdb_*'))
    patterns = ["pdb_pattern_*"]

    for each_dir in all_dirs:
        for pattern in patterns:
            for folder in glob.glob(os.path.join(each_dir, pattern)):
                neutral_path = os.path.join(folder, "neutral.pdb")
                ligand_path = os.path.join(folder, "ligand.pdb")
                output_path = os.path.join(folder, f"cut_{os.path.basename(folder)}.pdb")
                
                if os.path.exists(neutral_path) and os.path.exists(ligand_path):
                    merge_and_label_pdb(neutral_path, ligand_path, output_path)
                    print(f"done: {output_path}")
                else:
                    print(f"error")

if __name__ == "__main__":
    boot_up_pymol()
    go_through_directories()

