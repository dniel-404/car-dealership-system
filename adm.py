# ====================================================
# adm.py - Painel Administrativo com Financeiro
# ====================================================

import tkinter as tk
from tkinter import ttk
from database import resumo_financeiro, listar_financeiro

COR_BG = "#F1F5F9"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#0F172A"


def formatar_moeda(valor):
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def criar_card_financeiro(parent, titulo, valor, cor, subtitulo=""):

    card = tk.Frame(
        parent,
        bg=COR_CARD,
        bd=1,
        relief="solid",
        width=280,
        height=130
    )

    card.pack_propagate(False)

    barra = tk.Frame(card, bg=cor, width=8)
    barra.pack(side="left", fill="y")

    corpo = tk.Frame(card, bg=COR_CARD)
    corpo.pack(fill="both", expand=True, padx=18, pady=14)

    tk.Label(
        corpo,
        text=titulo,
        font=("Segoe UI", 11, "bold"),
        bg=COR_CARD,
        fg="#64748B"
    ).pack(anchor="w")

    tk.Label(
        corpo,
        text=formatar_moeda(valor),
        font=("Segoe UI", 22, "bold"),
        bg=COR_CARD,
        fg=cor
    ).pack(anchor="w", pady=(4, 0))

    if subtitulo:
        tk.Label(
            corpo,
            text=subtitulo,
            font=("Segoe UI", 9),
            bg=COR_CARD,
            fg="#94A3B8"
        ).pack(anchor="w")

    return card


def mostrar_adm(parent):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # ====================================================
    # TOPO
    # ====================================================

    topo = tk.Frame(frame, bg="#0F172A", height=80)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Painel Administrativo",
        font=("Segoe UI", 24, "bold"),
        bg="#0F172A",
        fg="#FBBF24"
    ).pack(anchor="w", padx=30, pady=20)

    # ====================================================
    # CONTEÚDO
    # ====================================================

    conteudo = tk.Frame(frame, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=30, pady=25)

    tk.Label(
        conteudo,
        text="Resumo Financeiro",
        font=("Segoe UI", 16, "bold"),
        bg=COR_BG,
        fg=COR_TEXTO
    ).pack(anchor="w", pady=(0, 15))

    # ====================================================
    # CARDS FINANCEIROS
    # ====================================================

    resumo = resumo_financeiro()

    linha_cards = tk.Frame(conteudo, bg=COR_BG)
    linha_cards.pack(anchor="w", pady=(0, 25))

    criar_card_financeiro(
        linha_cards,
        "Receitas (Vendas)",
        resumo["receitas"],
        "#059669",
        "Total recebido com vendas"
    ).pack(side="left", padx=(0, 15))

    criar_card_financeiro(
        linha_cards,
        "Despesas (Compras)",
        resumo["despesas"],
        "#DC2626",
        "Total investido em estoque"
    ).pack(side="left", padx=(0, 15))

    cor_lucro = "#059669" if resumo["lucro"] >= 0 else "#DC2626"

    criar_card_financeiro(
        linha_cards,
        "Lucro Líquido",
        resumo["lucro"],
        cor_lucro,
        "Receitas − Despesas"
    ).pack(side="left")

    # ====================================================
    # HISTÓRICO FINANCEIRO
    # ====================================================

    tk.Label(
        conteudo,
        text="Histórico de Movimentações",
        font=("Segoe UI", 14, "bold"),
        bg=COR_BG,
        fg=COR_TEXTO
    ).pack(anchor="w", pady=(0, 10))

    tabela_card = tk.Frame(
        conteudo,
        bg=COR_CARD,
        bd=1,
        relief="solid"
    )

    tabela_card.pack(fill="both", expand=True)

    colunas = ("data", "tipo", "descricao", "valor")

    tree = ttk.Treeview(
        tabela_card,
        columns=colunas,
        show="headings",
        height=15
    )

    cabecalhos = {
        "data":      ("Data",        100),
        "tipo":      ("Tipo",         90),
        "descricao": ("Descrição",   420),
        "valor":     ("Valor",       130)
    }

    for col, (titulo, largura) in cabecalhos.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=largura, anchor="center")

    tree.tag_configure("receita", foreground="#059669")
    tree.tag_configure("despesa", foreground="#DC2626")

    scroll = ttk.Scrollbar(
        tabela_card,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scroll.set)

    scroll.pack(side="right", fill="y", padx=(0, 5), pady=10)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    movimentacoes = listar_financeiro()

    for m in movimentacoes:

        tipo_txt = "✔ Receita" if m["tipo"] == "receita" else "✖ Despesa"

        tree.insert(
            "",
            tk.END,
            values=(
                m["data"],
                tipo_txt,
                m["descricao"],
                formatar_moeda(m["valor"])
            ),
            tags=(m["tipo"],)
        )