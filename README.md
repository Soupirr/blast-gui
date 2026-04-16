# NCBI BLAST GUI 

A simple and clean desktop application to run NCBI BLAST queries without opening a web browser. Built with Python, Biopython and CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-dark--mode-grey) ![Biopython](https://img.shields.io/badge/Biopython-BLAST-green)

---

## Features
- **BlastN & BlastP** support
- **Database selection** : nt, core_nt, nr, refseq_protein
- **Automatic output file** generated from the input FASTA filename if none is provided
- **Windows path compatibility** — paste paths directly from File Explorer
- **Sequence format validation** before launching the query
- **Clean dark mode interface** built with CustomTkinter

---

## Requirements
- Python 3.x
- [Biopython](https://biopython.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## Installation

Clone the repository and install the dependencies :
```bash
git clone https://github.com/soupirr/blast-gui.git
cd blast-gui
pip install biopython customtkinter
```

---

## Usage

1. Run the script :
```bash
python blast_gui.py
```
2. Provide a FASTA file path or use the **Browse** button
3. Optionally set an output file path (auto-generated if left empty)
4. Select the BLAST type (**BlastN** or **BlastP**)
5. Select the database
6. Click **BLAST** and wait for the results !

---

## Notes
> ⚠️ This tool queries the NCBI servers directly via Biopython. An internet connection is required. Query time may vary depending on NCBI server load.
