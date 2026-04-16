# ------------------------------------------------------------ IMPORTATION
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from Bio.Blast import NCBIWWW
from Bio.Seq import Seq

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

blast_type = None
blast_db = None

# ------------------------------------------------------------ LES FONCTIONS

# Fonction pour afficher le bouton "BLAST" après avoir sélectionné le type de blast et la database


def show_blast_button():
    blast_button.grid(column=0, row=5, columnspan=2, ipadx=30, ipady=10, pady=20)
    status_label.configure(text="")


# Fonction qui permet de selectionner BLASTN


def blastn_button():
    global program_blastn_core_nt, program_blastn_nt

    type_blastn_button.destroy()
    type_blastp_button.destroy()

    program_blastn_core_nt = ctk.CTkButton(
        frame, text="core_nt", command=program_core_nt
    )
    program_blastn_core_nt.grid(column=0, row=3, ipadx=20, ipady=10, **options)

    program_blastn_nt = ctk.CTkButton(frame, text="nt", command=program_nt)
    program_blastn_nt.grid(column=1, row=3, ipadx=20, ipady=10, **options)

    global blast_type
    blast_type = "blastn"


# Fonction qui permet de selectionner BLASTP


def blastp_button():
    global program_blastp_nr, program_blastp_refseq

    type_blastn_button.destroy()
    type_blastp_button.destroy()

    program_blastp_nr = ctk.CTkButton(frame, text="nr", command=program_nr)
    program_blastp_nr.grid(column=0, row=3, ipadx=20, ipady=10, **options)

    program_blastp_refseq = ctk.CTkButton(
        frame, text="refseq_protein", command=program_refseq
    )
    program_blastp_refseq.grid(column=1, row=3, ipadx=20, ipady=10, **options)

    global blast_type
    blast_type = "blastp"


# Les 4 fonctions qui choisissent les différents databases sélectionnable


def program_core_nt():
    global blast_db
    blast_db = "core_nt"
    program_blastn_core_nt.destroy()
    program_blastn_nt.destroy()
    show_blast_button()


def program_nt():
    global blast_db
    blast_db = "nt"
    program_blastn_core_nt.destroy()
    program_blastn_nt.destroy()
    show_blast_button()


def program_nr():
    global blast_db
    blast_db = "nr"
    program_blastp_nr.destroy()
    program_blastp_refseq.destroy()
    show_blast_button()


def program_refseq():
    global blast_db
    blast_db = "refseq_protein"
    program_blastp_nr.destroy()
    program_blastp_refseq.destroy()
    show_blast_button()


# Fonctions qui sert à lire le fichier fournit


def lire_fasta(fichier):
    fasta = open(fichier, "r")
    fasta.readline()
    sequence = ""
    for ligne in fasta:
        sequence += ligne.strip()
    fasta.close()
    return Seq(sequence)


# Fonction principal qui run l'analyse BLAST


def run_blast():
    try:
        blast_button.grid_remove()
        status_label.configure(
            text="⏳ BLAST en cours, veuillez patienter..."
        )  # permet de garder l'utilisateur à jour sur ce qu'il se passe
        root.update()

        fichier_fasta_path = (
            fichier_fasta.get().replace("\\", "/").strip('"')
        )  # permet de copier-coller directement depuis Windows sans se soucier des //
        fichier_sortie_path = fichier_sortie.get().replace("\\", "/").strip('"')

        if (
            fichier_sortie_path.strip() == ""
        ):  # fonction qui permet de créer automatiquement un fichier .txt de sortie
            dossier = "/".join(fichier_fasta_path.split("/")[:-1])
            nom_fasta = fichier_fasta_path.split("/")[-1].replace(".fasta", "")
            fichier_sortie_path = dossier + "/" + nom_fasta + "_blast.txt"

        sequence = lire_fasta(fichier_fasta_path)

        # Vérification du format de séquence
        nucleotides = set("ATCGNatcgn")
        acides_amines = set("ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy")

        est_nucl = all(c in nucleotides for c in sequence)
        est_prot = any(c in acides_amines - nucleotides for c in sequence)

        if (
            blast_type == "blastn" and not est_nucl
        ):  #  If qui permet de retourner des erreurs en cas de pb de séquence
            blast_button.grid()
            status_label.configure(
                text="❌ Erreur : séquence protéique détectée, blastn attend du nucléotide !"
            )
            return

        if blast_type == "blastp" and not est_prot:
            blast_button.grid()
            status_label.configure(
                text="❌ Erreur : séquence nucléotidique détectée, blastp attend une protéine !"
            )
            return

        result_blast = NCBIWWW.qblast(
            blast_type, blast_db, sequence, format_type="Text"
        )  # Fonction .qblast qui fait la query sur NCBI

        with open(fichier_sortie_path, "w", encoding="utf-8") as f:
            f.write(result_blast.read())

        result_blast.close()  # permet de mettre le bon résultat du blast
        status_label.configure(
            text=f"✅ BLAST terminé avec succès !\n📁 Résultat sauvegardé dans : {fichier_sortie_path}"
        )
        close_button.grid(column=1, row=7, ipadx=20, ipady=10, pady=10)
        nouveau_blast_button.grid(column=0, row=7, ipadx=20, ipady=10, pady=10)

    except Exception as e:  # Erreur si jamais NCBI plante pour raison X ou Y
        blast_button.grid()
        status_label.configure(text=f"❌ Erreur : {e}")


def parcourir_fasta():  # fonction qui permet au bouton de parcourir les fichiers de l'ordinateur pour simplifier la selection
    chemin = filedialog.askopenfilename(
        title="Choisir un fichier FASTA",
        filetypes=[("Fichiers FASTA", "*.fasta"), ("Tous les fichiers", "*.*")],
    )
    if chemin:
        fichier_fasta.set(chemin)


def parcourir_sortie():  # fonction qui permet au bouton de parcourir les fichiers de l'ordinateur pour simplifier la selection
    chemin = filedialog.asksaveasfilename(
        title="Choisir le fichier de sortie",
        defaultextension=".txt",
        filetypes=[("Fichiers texte", "*.txt")],
    )
    if chemin:
        fichier_sortie.set(chemin)


def reset():  # bouton qui permet de reset la fenêtre pour faire de nouvelles recherches sans avoir à redémarrer
    global type_blastn_button, type_blastp_button, blast_type, blast_db

    # Cacher les boutons de fin
    blast_button.grid_remove()
    close_button.grid_remove()
    nouveau_blast_button.grid_remove()
    status_label.configure(text="")

    # Détruire les boutons de database s'ils existent encore
    for widget in frame.grid_slaves():
        if widget.grid_info().get("row") == 3:
            widget.destroy()

    # Remettre les variables à zéro
    blast_type = None
    blast_db = None

    # Recréer les boutons blastn et blastp
    type_blastn_button = ctk.CTkButton(frame, text="BlastN", command=blastn_button)
    type_blastn_button.grid(column=0, row=3, ipadx=20, ipady=10, padx=50, pady=10)

    type_blastp_button = ctk.CTkButton(frame, text="BlastP", command=blastp_button)
    type_blastp_button.grid(column=1, row=3, ipadx=20, ipady=10, padx=50, pady=10)


# ------------------------------------------------------------ CREATION DE LA FENÊTRE

root = ctk.CTk()
root.title("BLAST")
root.resizable(True, True)

# ------------------------------------------------------------ CREATION DU SUPPORT DES WIDGET

frame = ctk.CTkFrame(root)
options = {"padx": 10, "pady": 10}

# ------------------------------------------------------------ CREATION DES WIDGETS

ctk.CTkLabel(frame, text="Chemin du fichier fasta :", font=("Arial", 13)).grid(
    column=0, row=0, sticky="W", **options
)
ctk.CTkLabel(
    frame,
    text="[optionnel] Chemin du fichier de sortie (format .txt) :",
    font=("Arial", 13),
).grid(column=0, row=1, sticky="W", **options)

fichier_fasta = tk.StringVar()
fichier_fasta_entry = ctk.CTkEntry(frame, textvariable=fichier_fasta, width=300)
fichier_fasta_entry.grid(column=1, row=0, **options)

fichier_sortie = tk.StringVar()
fichier_sortie_entry = ctk.CTkEntry(frame, textvariable=fichier_sortie, width=300)
fichier_sortie_entry.grid(column=1, row=1, **options)

ctk.CTkButton(frame, text="Parcourir", command=parcourir_fasta, width=100).grid(
    column=2, row=0, **options
)
ctk.CTkButton(frame, text="Parcourir", command=parcourir_sortie, width=100).grid(
    column=2, row=1, **options
)

ctk.CTkLabel(frame, text="Type de Blast / Database :", font=("Arial", 13)).grid(
    columnspan=2, row=2, pady=10
)

type_blastn_button = ctk.CTkButton(frame, text="BlastN", command=blastn_button)
type_blastn_button.grid(column=0, row=3, ipadx=20, ipady=10, **options)

type_blastp_button = ctk.CTkButton(frame, text="BlastP", command=blastp_button)
type_blastp_button.grid(column=1, row=3, ipadx=20, ipady=10, **options)

blast_button = ctk.CTkButton(
    frame, text="BLAST", command=run_blast, font=("Arial", 15, "bold")
)
status_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), wraplength=600)
status_label.grid(column=0, row=6, columnspan=2, pady=10)

close_button = ctk.CTkButton(
    frame, text="Fermer", command=root.destroy, fg_color="red", hover_color="darkred"
)
nouveau_blast_button = ctk.CTkButton(
    frame,
    text="Nouveau BLAST",
    command=reset,
    fg_color="green",
    hover_color="darkgreen",
)

# ------------------------------------------------------------ Fonction permanente de l'affichage de la fenêtre

frame.grid(padx=10, pady=10)
root.geometry("780x300")
root.update()
root.mainloop()
