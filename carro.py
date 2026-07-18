#========================================================================
# carro.py - Cadastro de Veículos
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from database import salvar_veiculo

COR_BG       = "#F8FAFC"
COR_CARD     = "#FFFFFF"
COR_TOPO     = "#0F172A"
COR_DESTAQUE = "#FBBF24"
COR_VERDE    = "#059669"
COR_TEXTO    = "#1E293B"
COR_SUB      = "#64748B"
COR_BORDA    = "#E2E8F0"
COR_INPUT    = "#F1F5F9"

CAMPOS_TEXTO     = {"Marca", "Modelo", "Cor"}
CAMPOS_MAIUSCULO = {"Placa"}


def aplicar_capitalize(entry):
    def evento(e):
        v = entry.get(); n = v.title()
        if n != v:
            p = entry.index(tk.INSERT)
            entry.delete(0, tk.END); entry.insert(0, n)
            try: entry.icursor(p)
            except Exception: pass
    entry.bind("<KeyRelease>", evento)


def aplicar_maiusculo(entry):
    def evento(e):
        v = entry.get(); n = v.upper()
        if n != v:
            p = entry.index(tk.INSERT)
            entry.delete(0, tk.END); entry.insert(0, n)
            try: entry.icursor(p)
            except Exception: pass
    entry.bind("<KeyRelease>", evento)


def aplicar_apenas_numeros(entry):
    def evento(e):
        v = entry.get(); n = ''.join(c for c in v if c.isdigit())
        if n != v:
            p = entry.index(tk.INSERT)
            entry.delete(0, tk.END); entry.insert(0, n)
            try: entry.icursor(p)
            except Exception: pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_monetaria(entry):
    def evento(e):
        if e.keysym in ("BackSpace","Delete","Left","Right","Tab"): return
        v = ''.join(c for c in entry.get() if c.isdigit())
        if not v: return
        c = int(v); r = c // 100; cs = c % 100
        rs = f"{r:,}".replace(",", ".")
        entry.delete(0, tk.END); entry.insert(0, f"{rs},{cs:02d}")
        entry.icursor(tk.END)
    entry.bind("<KeyRelease>", evento)


def mostrar_formulario(parent):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # TOPO
    topo = tk.Frame(frame, bg=COR_TOPO)
    topo.pack(fill="x")
    topo_inner = tk.Frame(topo, bg=COR_TOPO)
    topo_inner.pack(fill="x", padx=35, pady=22)
    tk.Label(topo_inner, text="🚗  Cadastro de Veículos",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg=COR_DESTAQUE).pack(side="left")
    tk.Label(topo_inner, text="Preencha os dados do veículo para adicionar ao estoque",
             font=("Segoe UI", 10),
             bg=COR_TOPO, fg="#94A3B8").pack(side="left", padx=(15, 0), pady=(6, 0))

    # SCROLL
    container = tk.Frame(frame, bg=COR_BG)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    sc = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sc.set)
    sc.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    corpo = tk.Frame(canvas, bg=COR_BG)
    win = canvas.create_window((0, 0), window=corpo, anchor="nw")
    corpo.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # CARD
    card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    card.pack(padx=35, pady=25, fill="x")
    tk.Frame(card, bg=COR_VERDE, height=3).pack(fill="x")

    tk.Label(card, text="Informações do Veículo",
             font=("Segoe UI", 12, "bold"),
             bg=COR_CARD, fg=COR_TEXTO,
             padx=25, pady=14).pack(anchor="w")
    tk.Frame(card, bg=COR_BORDA, height=1).pack(fill="x")

    form = tk.Frame(card, bg=COR_CARD)
    form.pack(padx=25, pady=20, fill="x")

    campos = [
        ("Marca",  "Fabricante do veículo"),
        ("Modelo", "Modelo/versão"),
        ("Ano",    "Ano de fabricação"),
        ("Placa",  "Placa do veículo"),
        ("Cor",    "Cor"),
        ("KM",     "Quilometragem atual"),
        ("Valor",  "Valor de compra (R$)"),
    ]

    entradas = {}

    # Layout 2 colunas
    pares = [campos[i:i+2] for i in range(0, len(campos), 2)]

    for pair in pares:
        linha = tk.Frame(form, bg=COR_CARD)
        linha.pack(fill="x", pady=6)

        for nome, hint in pair:
            bloco = tk.Frame(linha, bg=COR_CARD)
            bloco.pack(side="left", fill="x", expand=True, padx=(0, 20))

            tk.Label(bloco, text=nome.upper(), font=("Segoe UI", 9, "bold"),
                     bg=COR_CARD, fg=COR_SUB).pack(anchor="w", pady=(0, 4))

            borda = tk.Frame(bloco, bg=COR_BORDA)
            borda.pack(fill="x")

            inner = tk.Frame(borda, bg=COR_INPUT, padx=10, pady=8)
            inner.pack(fill="x", padx=1, pady=1)

            e = tk.Entry(inner, font=("Segoe UI", 10), relief="flat", bd=0,
                         bg=COR_INPUT, fg=COR_TEXTO, insertbackground=COR_VERDE)
            e.pack(fill="x")

            tk.Label(bloco, text=hint, font=("Segoe UI", 8),
                     bg=COR_CARD, fg="#CBD5E1").pack(anchor="w", pady=(2, 0))

            def fi(ev, b=borda): b.config(bg=COR_VERDE)
            def fo(ev, b=borda): b.config(bg=COR_BORDA)
            e.bind("<FocusIn>", fi)
            e.bind("<FocusOut>", fo)

            if nome in CAMPOS_TEXTO:     aplicar_capitalize(e)
            elif nome in CAMPOS_MAIUSCULO: aplicar_maiusculo(e)
            elif nome in ("Ano", "KM"):  aplicar_apenas_numeros(e)
            elif nome == "Valor":        aplicar_mascara_monetaria(e)

            entradas[nome] = e

    # BOTÕES
    tk.Frame(card, bg=COR_BORDA, height=1).pack(fill="x")
    btn_area = tk.Frame(card, bg="#F8FAFC")
    btn_area.pack(fill="x", padx=25, pady=16)

    def cadastrar():
        dados = {k: v.get() for k, v in entradas.items()}
        if "" in dados.values():
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        salvar_veiculo(dados)
        messagebox.showinfo("Sucesso", "Veículo cadastrado e registrado como despesa no financeiro!")
        for e in entradas.values():
            e.delete(0, tk.END)

    def limpar():
        for e in entradas.values():
            e.delete(0, tk.END)

    def make_btn(parent, texto, cor, hover, cmd):
        b = tk.Button(parent, text=texto,
                      font=("Segoe UI", 10, "bold"),
                      bg=cor, fg="white", relief="flat",
                      cursor="hand2", padx=22, pady=9, bd=0,
                      activebackground=hover, activeforeground="white",
                      command=cmd)
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=cor))
        return b

    make_btn(btn_area, "💾  Cadastrar Veículo",
             COR_VERDE, "#047857", cadastrar).pack(side="left", padx=(0, 10))
    make_btn(btn_area, "🗑  Limpar",
             "#94A3B8", "#64748B", limpar).pack(side="left")

    tk.Label(btn_area,
             text="O valor de compra será registrado automaticamente no financeiro.",
             font=("Segoe UI", 9), bg="#F8FAFC", fg="#94A3B8").pack(
        side="right", padx=(0, 5))