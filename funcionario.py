#========================================================================
# funcionario.py - Cadastro Profissional de Funcionários
#========================================================================

import tkinter as tk
from tkinter import messagebox
from database import salvar_funcionario

COR_BG = "#F1F5F9"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#0F172A"

CAMPOS_TEXTO = {"Nome", "Cargo"}


# ====================================================
# HELPERS DE MÁSCARA
# ====================================================

def aplicar_capitalize(entry):
    def evento(e):
        valor = entry.get()
        novo = valor.title()
        if novo != valor:
            pos = entry.index(tk.INSERT)
            entry.delete(0, tk.END)
            entry.insert(0, novo)
            try:
                entry.icursor(pos)
            except Exception:
                pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_monetaria(entry):
    """Formata salário como 1.000,00 enquanto digita."""
    def evento(e):
        if e.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())
        if not valor:
            return
        centavos = int(valor)
        reais = centavos // 100
        cents = centavos % 100
        reais_str = f"{reais:,}".replace(",", ".")
        formatado = f"{reais_str},{cents:02d}"
        entry.delete(0, tk.END)
        entry.insert(0, formatado)
        entry.icursor(tk.END)
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_cpf(entry):
    """Formata CPF: 000.000.000-00"""
    def evento(e):
        if e.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())[:11]
        formatado = valor
        if len(valor) > 3:
            formatado = valor[:3] + "." + valor[3:]
        if len(valor) > 6:
            formatado = valor[:3] + "." + valor[3:6] + "." + valor[6:]
        if len(valor) > 9:
            formatado = valor[:3] + "." + valor[3:6] + "." + valor[6:9] + "-" + valor[9:]
        pos = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, formatado)
        try:
            entry.icursor(min(pos + 1, len(formatado)))
        except Exception:
            pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_telefone(entry):
    """Formata telefone: (00) 00000-0000"""
    def evento(e):
        if e.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())[:11]
        formatado = valor
        if len(valor) >= 2:
            formatado = "(" + valor[:2] + ") " + valor[2:]
        if len(valor) > 7:
            formatado = "(" + valor[:2] + ") " + valor[2:7] + "-" + valor[7:]
        pos = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, formatado)
        try:
            entry.icursor(min(pos + 1, len(formatado)))
        except Exception:
            pass
    entry.bind("<KeyRelease>", evento)


# ====================================================
# FORMULÁRIO
# ====================================================

def mostrar_formulario(parent):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # =========================
    # TOPO
    # =========================

    topo = tk.Frame(frame, bg="#0F172A", height=80)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Cadastro de Funcionários",
        font=("Segoe UI", 24, "bold"),
        bg="#0F172A",
        fg="#FBBF24"
    ).pack(anchor="w", padx=30, pady=20)

    # =========================
    # CARD
    # =========================

    card = tk.Frame(frame, bg=COR_CARD, bd=1, relief="solid")
    card.pack(padx=30, pady=30, fill="both", expand=True)

    conteudo = tk.Frame(card, bg=COR_CARD)
    conteudo.pack(padx=30, pady=30)

    entradas = {}

    campos = ["Nome", "CPF", "Telefone", "Cargo", "Salário", "Email"]

    for i, campo in enumerate(campos):

        tk.Label(
            conteudo,
            text=campo,
            font=("Segoe UI", 10, "bold"),
            bg=COR_CARD,
            fg=COR_TEXTO
        ).grid(row=i, column=0, sticky="w", pady=(10, 5), padx=10)

        e = tk.Entry(
            conteudo,
            width=40,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        e.grid(row=i, column=1, pady=5, padx=10, ipady=7)

        # Máscaras
        if campo in CAMPOS_TEXTO:
            aplicar_capitalize(e)
        elif campo == "CPF":
            aplicar_mascara_cpf(e)
        elif campo == "Telefone":
            aplicar_mascara_telefone(e)
        elif campo == "Salário":
            aplicar_mascara_monetaria(e)

        entradas[campo] = e

    # =========================
    # CADASTRAR
    # =========================

    def cadastrar():

        dados = {k: v.get() for k, v in entradas.items()}

        if "" in dados.values():
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        salvar_funcionario(dados)

        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")

        for e in entradas.values():
            e.delete(0, tk.END)

    # =========================
    # BOTÃO
    # =========================

    botoes = tk.Frame(conteudo, bg=COR_CARD)
    botoes.grid(row=10, column=0, columnspan=2, pady=25)

    tk.Button(
        botoes,
        text="Cadastrar Funcionário",
        bg="#2563EB",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        width=24,
        pady=10,
        command=cadastrar
    ).pack()