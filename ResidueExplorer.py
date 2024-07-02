import os
import pymol
from pymol import cmd, stored
from collections import defaultdict
import glob

os.environ['PYMOL_GUI'] = '0'
pymol.pymol_argv = ['pymol', '-cq']
pymol.finish_launching()

def add_unique_residue(resn, resi, chain, path_to_file):
    unique_id = (resn, resi, chain)
    if unique_id not in stored.unique_residues:
        with open(path_to_file, "a") as file:
            file.write(f"{resn} {resi} Chain {chain}\n")
        stored.unique_residues.add(unique_id)

def grab_residues_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    return [line.strip().split() for line in content]

def expand_residue_sequences(residues):
    residues_by_chain = defaultdict(list)
    for residue in residues:
        resn, resi, chain = residue[0], residue[1], " ".join(residue[3:])
        residues_by_chain[chain].append((resn, int(resi)))

    expanded_residues = set()
    for chain, items in residues_by_chain.items():
        items.sort(key=lambda x: x[1])
        for resn, resi in items:
            for expanded_resi in range(resi, resi + 5):
                expanded_residues.add((resn, str(expanded_resi), chain))
    return list(expanded_residues)

def record_residues(residues, file_path):
    with open(file_path, 'w') as file:
        for residue in sorted(residues, key=lambda x: (x[2], int(x[1]))):
            file.write(f"{residue[0]} {residue[1]} Chain {residue[2]}\n")

def build_selection_string(file_path):
    residues_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            resn, resi, chain = parts[0], parts[1], parts[-1]
            if chain not in residues_dict:
                residues_dict[chain] = []
            residues_dict[chain].append(int(resi))

    selection_fragments = []
    for chain, resi_list in residues_dict.items():
        resi_list = sorted(set(resi_list))
        ranges = []
        start, end = resi_list[0], resi_list[0]
        for resi in resi_list[1:]:
            if resi == end + 1:
                end = resi
            else:
                ranges.append((start, end))
                start = end = resi
        ranges.append((start, end))
        range_strings = [f"{start}-{end}" if start != end else f"{start}" for start, end in ranges]
        selection_fragments.append(f"(chain {chain} and resi {' or resi '.join(range_strings)})")
    return " or ".join(selection_fragments)

def handle_pdb_file(pdb_path, output_dir_base):
    pdb_name = os.path.basename(pdb_path).replace('.pdb', '')
    output_directory = os.path.join(output_dir_base, pdb_name)
    os.makedirs(output_directory, exist_ok=True)

    paths = {
        'unique_residues': os.path.join(output_directory, "unique_residues_chains.txt"),
        'extended_residues': os.path.join(output_directory, "extended_unique_residues_chains.txt"),
        'ligand': os.path.join(output_directory, 'ligand.pdb'),
        'binding_site_ligand': os.path.join(output_directory, "binding_site_and_ligand.pdb"),
        'protein': os.path.join(output_directory, 'protein.pdb')
    }

    stored.unique_residues = set()
    open(paths['unique_residues'], "w").close()

    cmd.load(pdb_path, "complex")
    cmd.select("ligand", "resn UNL")
    cmd.save(paths['ligand'], 'ligand')
    cmd.select("near_ligand", "byres (all within 3 of ligand)")

    residues = set()
    cmd.iterate("near_ligand", "residues.add((resn, resi, chain))", space=locals())

    for resn, resi, chain in residues:
        add_unique_residue(resn, resi, chain, paths['unique_residues'])

    residues = grab_residues_from_file(paths['unique_residues'])
    expanded_residues = expand_residue_sequences(residues)
    record_residues(expanded_residues, paths['extended_residues'])
    
    selection = build_selection_string(paths['extended_residues'])
    cmd.select("selected_residues", selection)
    cmd.show("sticks", "selected_residues")
    cmd.create("binding_site_and_ligand", "selected_residues or ligand")
    cmd.save(paths['binding_site_ligand'], "binding_site_and_ligand")
    cmd.select('protein_only', "binding_site_and_ligand and not resn UNL")
    cmd.save(paths['protein'], 'protein_only')
    cmd.reinitialize()
#the pdb_* is your folder, _*.pdb is your pdb file.
def run():
    pymol.finish_launching()
    for pdb_folder in glob.glob('pdb_*'):
        for pdb_file_path in glob.glob(os.path.join(pdb_folder, '_*.pdb')):
            handle_pdb_file(pdb_file_path, pdb_folder)

if __name__ == '__main__':
    run()

