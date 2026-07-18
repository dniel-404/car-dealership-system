#========================================================================
# pesqFunc.py - Pesquisa Profissional de Funcionários
#========================================================================

import tkinter as tk
from tkinter import messagebox

from database import (
    listar_funcionarios,
    excluir_funcionario
)

COR_BG = "#F1F5F9"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#0F172A"


def mostrar_pesquisa(parent):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(
        parent,
        bg=COR_BG
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # ====================================================
    # TOPO
    # ====================================================

    topo = tk.Frame(
        frame,
        bg="#0F172A",
        height=80
    )

    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Pesquisa de Funcionários",
        font=("Segoe UI", 24, "bold"),
        bg="#0F172A",
        fg="#FBBF24"
    ).pack(
        anchor="w",
        padx=30,
        pady=20
    )

    # ====================================================
    # CARD PRINCIPAL
    # ====================================================

    card = tk.Frame(
        frame,
        bg=COR_CARD,
        bd=1,
        relief="solid"
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    # ====================================================
    # BUSCA
    # ====================================================

    busca_frame = tk.Frame(
        card,
        bg=COR_CARD
    )

    busca_frame.pack(
        fill="x",
        padx=25,
        pady=25
    )

    tk.Label(
        busca_frame,
        text="Buscar funcionário",
        font=("Segoe UI", 10, "bold"),
        bg=COR_CARD,
        fg=COR_TEXTO
    ).pack(anchor="w", pady=(0, 8))

    linha_busca = tk.Frame(
        busca_frame,
        bg=COR_CARD
    )

    linha_busca.pack(anchor="w")

    entrada = tk.Entry(
        linha_busca,
        width=45,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )

    entrada.pack(
        side="left",
        ipady=7,
        padx=(0, 10)
    )

    # ====================================================
    # LISTA
    # ====================================================

    lista = tk.Listbox(
        card,
        width=100,
        height=18,
        font=("Consolas", 11),
        bg="#F8FAFC",
        fg=COR_TEXTO,
        bd=0,
        highlightthickness=0,
        selectbackground="#2563EB"
    )

    lista.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    resultados = []

    def pesquisar():

        lista.delete(0, tk.END)

        resultados.clear()

        termo = entrada.get().lower()

        dados = listar_funcionarios()

        for f in dados:

            texto = (
                f"{f['nome']}   |   "
                f"{f['cargo']}   |   "
                f"{f['telefone']}"
            )

            if termo in texto.lower():

                lista.insert(
                    tk.END,
                    texto
                )

                resultados.append(f)

    tk.Button(
        linha_busca,
        text="Pesquisar",
        bg="#2563EB",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=pesquisar
    ).pack(side="left")

    # ====================================================
    # EXCLUIR
    # ====================================================

    def excluir():

        selecionado = lista.curselection()

        if not selecionado:

            messagebox.showwarning(
                "Aviso",
                "Selecione um funcionário."
            )

            return

        index = selecionado[0]

        funcionario = resultados[index]

        confirmar = messagebox.askyesno(
            "Confirmação",
            f"Excluir funcionário {funcionario['nome']}?"
        )

        if not confirmar:
            return

        excluir_funcionario(funcionario["id"])

        pesquisar()

        messagebox.showinfo(
            "Sucesso",
            "Funcionário excluído com sucesso."
        )

    # ====================================================
    # BOTÕES
    # ====================================================

    botoes = tk.Frame(
        card,
        bg=COR_CARD
    )

    botoes.pack(pady=10)

    tk.Button(
        botoes,
        text="Excluir Funcionário",
        bg="#DC2626",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=10,
        command=excluir
    ).pack(side="left", padx=8)

    pesquisar()