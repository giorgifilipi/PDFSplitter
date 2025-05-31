import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

class NotaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Notas")
        self.geometry()

        # PDF Upload
        self.pdf_path = tk.StringVar()
        tk.Label(self, text="Arquivo PDF:").pack(anchor="w", padx=10, pady=(10,0))
        tk.Entry(self, textvariable=self.pdf_path, width=40, state="readonly").pack(padx=10, anchor="w")
        tk.Button(self, text="Selecionar PDF", command=self.upload_pdf).pack(padx=10, pady=5, anchor="w")

        # Nome da turma
        tk.Label(self, text="Nome da Turma:").pack(anchor="w", padx=10, pady=(10,0))
        self.turma_entry = tk.Entry(self, width=40)
        self.turma_entry.pack(padx=10, anchor="w")

        # Turno
        tk.Label(self, text="Turno:").pack(anchor="w", padx=10, pady=(10,0))
        self.turno_var = tk.StringVar(value="Matutino")
        tk.Radiobutton(self, text="Matutino", variable=self.turno_var, value="Matutino").pack(anchor="w", padx=20)
        tk.Radiobutton(self, text="Vespertino", variable=self.turno_var, value="Vespertino").pack(anchor="w", padx=20)

         # Nome da turma
        tk.Label(self, text="Nome da Matéria:").pack(anchor="w", padx=10, pady=(10,0))
        self.materia_entry = tk.Entry(self, width=40)
        self.materia_entry.pack(padx=10, anchor="w")

        # Lista de nomes
        tk.Label(self, text="Lista de Nomes (um por linha):").pack(anchor="w", padx=10, pady=(10,0))
        self.nomes_text = tk.Text(self, width=40, height=8)
        self.nomes_text.pack(padx=10, anchor="w")

        # Botão de envio
        tk.Button(self, text="Gerar PDF's", command=self.enviar).pack(pady=20)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")],
            title="Selecione o arquivo PDF"
        )
        if file_path:
            self.pdf_path.set(file_path)

    def enviar(self):
        pdf = self.pdf_path.get()
        turma = self.turma_entry.get()
        turno = self.turno_var.get()
        materia = self.materia_entry.get()
        nomes = self.nomes_text.get("1.0", tk.END).strip().splitlines()

        if not pdf or not turma or not nomes:
            messagebox.showerror("Erro", "Preencha todos os campos e selecione um PDF.")
            return
        
        # Split PDF e nomear pelos nomes
        try:
            turno_nome = turno.strip().replace(" ", "_")
            turma_nome = turma.strip().replace(" ", "_")
            output_dir = os.path.join(os.path.dirname(pdf), f"{turma_nome}_{turno_nome}")
            os.makedirs(output_dir, exist_ok=True)
            reader = PdfReader(pdf)
            total_paginas = len(reader.pages)
            if len(nomes) != total_paginas:
                messagebox.showerror("Erro", f"A quantidade de nomes ({len(nomes)}) não corresponde ao número de páginas do PDF ({total_paginas}).")
                return
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                nome = nomes[i].strip().replace(" ", "_")
                output_path = os.path.join(output_dir, f"{nome}_{turma_nome}_{turno_nome}.pdf")
                with open(output_path, "wb") as f_out:
                    writer.write(f_out)
            messagebox.showinfo("Sucesso", f"PDF dividido e nomeado conforme a lista na pasta '{turma_nome}_{turno_nome}_{materia}'.")
        except Exception as e:
            messagebox.showerror("Erro ao dividir PDF", str(e))

if __name__ == "__main__":
    app = NotaApp()
    app.mainloop()