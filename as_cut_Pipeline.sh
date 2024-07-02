#!/bin/bash 
python ResidueExplorer.py
bash QuartileProcessor.sh
python PDBMerger.py
bash PDBtoXYZConverter.sh

