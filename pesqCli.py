#========================================================================
# pesqCli.py - Pesquisa de Clientes
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import os

from database import listar_clientes, excluir_cliente

COR_BG       = "#F8FAFC"
COR_CARD     = "#FFFFFF"
COR_TOPO     = "#0F172A"
COR_DESTAQUE = "#FBBF24"
COR_PRIMARIA = "#2563EB"
COR_VERDE    = "#059669"
COR_VERMELHO = "#DC2626"
COR_TEXTO    = "#1E293B"
COR_SUB      = "#64748B"
COR_BORDA    = "#E2E8F0"
COR_INPUT    = "#F1F5F9"


def mostrar_pesquisa(parent):

    for w in parent.winfo_children():
        w.destroy()

    import CadCli

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # ====================================================
    # TOPO
    # ====================================================

    topo = tk.Frame(frame, bg=COR_TOPO)
    topo.pack(fill="x")

    topo_inner = tk.Frame(topo, bg=COR_TOPO)
    topo_inner.pack(fill="x", padx=35, pady=22)

    tk.Label(topo_inner, text="🔍  Pesquisa de Clientes",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg=COR_DESTAQUE).pack(side="left")

    tk.Label(topo_inner, text="Busque, edite ou exclua clientes",
             font=("Segoe UI", 10),
             bg=COR_TOPO, fg="#94A3B8").pack(side="left", padx=(15, 0), pady=(6, 0))

    # ====================================================
    # CONTEÚDO SCROLLÁVEL
    # ====================================================

    container = tk.Frame(frame, bg=COR_BG)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    corpo = tk.Frame(canvas, bg=COR_BG)
    win = canvas.create_window((0, 0), window=corpo, anchor="nw")

    def ajustar(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_larg(e):
        canvas.itemconfig(win, width=e.width)

    corpo.bind("<Configure>", ajustar)
    canvas.bind("<Configure>", ajustar_larg)
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
        int(-1 * (e.delta / 120)), "units"))

    # ====================================================
    # CARD BUSCA
    # ====================================================

    busca_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    busca_card.pack(fill="x", padx=35, pady=(25, 0))

    tk.Frame(busca_card, bg=COR_PRIMARIA, height=3).pack(fill="x")

    busca_inner = tk.Frame(busca_card, bg=COR_CARD)
    busca_inner.pack(fill="x", padx=25, pady=18)

    tk.Label(busca_inner, text="BUSCAR CLIENTE",
             font=("Segoe UI", 9, "bold"),
             bg=COR_CARD, fg=COR_SUB).pack(anchor="w", pady=(0, 6))

    linha_busca = tk.Frame(busca_inner, bg=COR_CARD)
    linha_busca.pack(fill="x")

    busca_borda = tk.Frame(linha_busca, bg=COR_BORDA)
    busca_borda.pack(side="left", fill="x", expand=True, padx=(0, 12))

    busca_inner2 = tk.Frame(busca_borda, bg=COR_INPUT, padx=12, pady=8)
    busca_inner2.pack(fill="x", padx=1, pady=1)

    tk.Label(busca_inner2, text="🔍", font=("Segoe UI", 11),
             bg=COR_INPUT, fg=COR_SUB).pack(side="left", padx=(0, 8))

    entrada = tk.Entry(busca_inner2, font=("Segoe UI", 11),
                       relief="flat", bd=0, bg=COR_INPUT,
                       fg=COR_TEXTO, insertbackground=COR_PRIMARIA)
    entrada.pack(side="left", fill="x", expand=True)

    entrada.bind("<FocusIn>",  lambda e: busca_borda.config(bg=COR_PRIMARIA))
    entrada.bind("<FocusOut>", lambda e: busca_borda.config(bg=COR_BORDA))

    def make_btn(parent, texto, cor, hover, cmd):
        b = tk.Button(parent, text=texto,
                      font=("Segoe UI", 10, "bold"),
                      bg=cor, fg="white", relief="flat",
                      cursor="hand2", padx=20, pady=9, bd=0,
                      activebackground=hover, activeforeground="white",
                      command=cmd)
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=cor))
        return b

    lbl_total = tk.Label(busca_inner, text="",
                         font=("Segoe UI", 9),
                         bg=COR_CARD, fg=COR_SUB)
    lbl_total.pack(anchor="w", pady=(8, 0))

    # ====================================================
    # CARD TABELA
    # ====================================================

    tabela_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    tabela_card.pack(fill="x", padx=35, pady=(16, 0))

    tk.Frame(tabela_card, bg=COR_VERDE, height=3).pack(fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Cli.Treeview",
                    background=COR_CARD, foreground=COR_TEXTO,
                    rowheight=36, fieldbackground=COR_CARD,
                    font=("Segoe UI", 10), borderwidth=0)
    style.configure("Cli.Treeview.Heading",
                    background="#1E293B", foreground="#94A3B8",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Cli.Treeview",
              background=[("selected", "#DBEAFE")],
              foreground=[("selected", COR_PRIMARIA)])

    cols = ("nome", "cpf", "telefone", "email", "cidade", "uf")
    tree = ttk.Treeview(tabela_card, columns=cols, show="headings",
                        style="Cli.Treeview", height=14, selectmode="browse")

    cfg = {
        "nome":     ("Nome",     240),
        "cpf":      ("CPF",      130),
        "telefone": ("Telefone", 130),
        "email":    ("Email",    210),
        "cidade":   ("Cidade",   150),
        "uf":       ("UF",        50),
    }
    for col, (titulo, larg) in cfg.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=larg, anchor="w", minwidth=50)

    tree.tag_configure("par",   background=COR_CARD)
    tree.tag_configure("impar", background="#F8FAFC")

    sc_y = ttk.Scrollbar(tabela_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc_y.set)
    sc_y.pack(side="right", fill="y", padx=(0, 5), pady=10)
    tree.pack(fill="x", padx=10, pady=10)

    resultados = []

    def buscar(*args):
        tree.delete(*tree.get_children())
        resultados.clear()
        termo = entrada.get().lower().strip()
        dados = listar_clientes()
        encontrados = [
            c for c in dados
            if termo in c.get("nome", "").lower()
            or termo in c.get("cpf", "").lower()
            or termo in c.get("email", "").lower()
            or termo in c.get("telefone", "").lower()
        ]
        for i, c in enumerate(encontrados):
            tag = "par" if i % 2 == 0 else "impar"
            tree.insert("", tk.END, tags=(tag,), values=(
                c.get("nome", ""),
                c.get("cpf", ""),
                c.get("telefone", ""),
                c.get("email", ""),
                c.get("cidade", ""),
                c.get("uf", "")
            ))
            resultados.append(c)

        total = len(encontrados)
        lbl_total.config(
            text=f"{total} cliente{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

    entrada.bind("<KeyRelease>", buscar)

    # ====================================================
    # BOTÕES DE AÇÃO — sempre visíveis abaixo da tabela
    # ====================================================

    tk.Frame(tabela_card, bg=COR_BORDA, height=1).pack(fill="x")

    acoes = tk.Frame(tabela_card, bg="#F8FAFC")
    acoes.pack(fill="x", padx=20, pady=16)

    def get_selecionado():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um cliente na lista.")
            return None
        return resultados[tree.index(sel[0])]

    def editar():
        cliente = get_selecionado()
        if not cliente:
            return
        CadCli.mostrar_formulario(parent, cliente, cliente["id"])

    def excluir():
        cliente = get_selecionado()
        if not cliente:
            return
        if messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja excluir o cliente:\n\n{cliente['nome']}?\n\nEssa ação não pode ser desfeita."
        ):
            excluir_cliente(cliente["id"])
            buscar()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")

    make_btn(acoes, "✎  Editar Cliente",
             COR_VERDE,    "#047857", editar).pack(side="left", padx=(0, 10))

    make_btn(acoes, "🗑  Excluir Cliente",
             COR_VERMELHO, "#B91C1C", excluir).pack(side="left")

    tk.Label(acoes,
             text="Selecione um cliente na tabela antes de editar ou excluir.",
             font=("Segoe UI", 9), bg="#F8FAFC", fg="#94A3B8").pack(
        side="right", padx=(0, 5))

    # Botão buscar (agora após definir a função)
    make_btn(linha_busca, "Pesquisar",
             COR_PRIMARIA, "#1D4ED8", buscar).pack(side="left")

    # Carregar todos ao abrir
    buscar()

    # Bind scroll
    def bind_scroll(widget):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        for child in widget.winfo_children():
            bind_scroll(child)

    corpo.after(100, lambda: bind_scroll(corpo))