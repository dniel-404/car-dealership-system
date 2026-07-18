#========================================================================
# frota.py - Gestão de Frota
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox

from database import listar_veiculos, atualizar_veiculo, excluir_veiculo

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


def mostrar_frota(parent):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # ====================================================
    # TOPO
    # ====================================================

    topo = tk.Frame(frame, bg=COR_TOPO)
    topo.pack(fill="x")

    topo_inner = tk.Frame(topo, bg=COR_TOPO)
    topo_inner.pack(fill="x", padx=35, pady=22)

    tk.Label(topo_inner, text="🚗  Gestão de Frota",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg=COR_DESTAQUE).pack(side="left")

    tk.Label(topo_inner, text="Pesquise, edite ou exclua veículos",
             font=("Segoe UI", 10),
             bg=COR_TOPO, fg="#94A3B8").pack(side="left", padx=(15, 0), pady=(6, 0))

    # ====================================================
    # ÁREA SCROLLÁVEL
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

    tk.Label(busca_inner, text="PESQUISAR VEÍCULO",
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
                       relief="flat", bd=0, bg=COR_INPUT, fg=COR_TEXTO,
                       insertbackground=COR_PRIMARIA)
    entrada.pack(side="left", fill="x", expand=True)

    entrada.bind("<FocusIn>",  lambda e: busca_borda.config(bg=COR_PRIMARIA))
    entrada.bind("<FocusOut>", lambda e: busca_borda.config(bg=COR_BORDA))

    lbl_total = tk.Label(busca_inner, text="", font=("Segoe UI", 9),
                         bg=COR_CARD, fg=COR_SUB)
    lbl_total.pack(anchor="w", pady=(8, 0))

    # ====================================================
    # TABELA
    # ====================================================

    tabela_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    tabela_card.pack(fill="x", padx=35, pady=(16, 30))
    tk.Frame(tabela_card, bg=COR_VERDE, height=3).pack(fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Frt.Treeview",
                    background=COR_CARD, foreground=COR_TEXTO,
                    rowheight=36, fieldbackground=COR_CARD,
                    font=("Segoe UI", 10), borderwidth=0)
    style.configure("Frt.Treeview.Heading",
                    background="#1E293B", foreground="#94A3B8",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Frt.Treeview",
              background=[("selected", "#D1FAE5")],
              foreground=[("selected", "#059669")])

    cols = ("marca","modelo","ano","placa","cor","km","valor","status")
    tree = ttk.Treeview(tabela_card, columns=cols, show="headings",
                        style="Frt.Treeview", height=14, selectmode="browse")

    cfg = {
        "marca":  ("Marca",   110),
        "modelo": ("Modelo",  140),
        "ano":    ("Ano",      70),
        "placa":  ("Placa",   100),
        "cor":    ("Cor",      90),
        "km":     ("KM",       90),
        "valor":  ("Valor",   120),
        "status": ("Status",  100),
    }
    for col, (titulo, larg) in cfg.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=larg, anchor="center")

    tree.tag_configure("par",        background=COR_CARD)
    tree.tag_configure("impar",      background="#F8FAFC")
    tree.tag_configure("disponivel", foreground="#059669")
    tree.tag_configure("vendido",    foreground="#DC2626")

    sc = ttk.Scrollbar(tabela_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc.set)
    sc.pack(side="right", fill="y", padx=(0, 5), pady=10)
    tree.pack(fill="x", padx=10, pady=10)

    resultados = []

    def atualizar_lista(filtro=""):
        tree.delete(*tree.get_children())
        resultados.clear()
        dados = listar_veiculos()
        filtro_l = filtro.lower()
        encontrados = [
            v for v in dados
            if filtro_l in f"{v.get('marca','')} {v.get('modelo','')} {v.get('placa','')} {v.get('cor','')}".lower()
        ] if filtro_l else dados

        for i, v in enumerate(encontrados):
            tag_par = "par" if i % 2 == 0 else "impar"
            status = v.get("status") or "disponivel"
            tag_st = "disponivel" if status == "disponivel" else "vendido"
            tree.insert("", tk.END, tags=(tag_par, tag_st), values=(
                v.get("marca",""), v.get("modelo",""), v.get("ano",""),
                v.get("placa",""), v.get("cor",""), v.get("km",""),
                f"R$ {v.get('valor','')}",
                status.capitalize()
            ))
            resultados.append(v)

        lbl_total.config(text=f"{len(encontrados)} veículo(s) encontrado(s)")

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

    make_btn(linha_busca, "Pesquisar", COR_PRIMARIA, "#1D4ED8",
             lambda: atualizar_lista(entrada.get())).pack(side="left")

    entrada.bind("<KeyRelease>", lambda e: atualizar_lista(entrada.get()))

    # ====================================================
    # BOTÕES DE AÇÃO
    # ====================================================

    tk.Frame(tabela_card, bg=COR_BORDA, height=1).pack(fill="x")

    acoes = tk.Frame(tabela_card, bg="#F8FAFC")
    acoes.pack(fill="x", padx=20, pady=16)

    def get_sel():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return None
        return resultados[tree.index(sel[0])]

    def editar():
        v = get_sel()
        if not v:
            return
        abrir_edicao(frame, v, lambda: atualizar_lista(entrada.get()))

    def excluir():
        v = get_sel()
        if not v:
            return
        if messagebox.askyesno("Confirmar",
                f"Excluir o veículo {v['marca']} {v['modelo']}?\nEssa ação não pode ser desfeita."):
            excluir_veiculo(v["id"])
            atualizar_lista(entrada.get())
            messagebox.showinfo("Sucesso", "Veículo excluído.")

    make_btn(acoes, "✎  Editar",  COR_VERDE,    "#047857", editar).pack(side="left", padx=(0, 10))
    make_btn(acoes, "🗑  Excluir", COR_VERMELHO, "#B91C1C", excluir).pack(side="left")

    tk.Label(acoes, text="Selecione um veículo antes de editar ou excluir.",
             font=("Segoe UI", 9), bg="#F8FAFC", fg="#94A3B8").pack(
        side="right", padx=(0, 5))

    atualizar_lista()

    def bind_scroll(widget):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        for child in widget.winfo_children():
            bind_scroll(child)

    corpo.after(100, lambda: bind_scroll(corpo))


# ====================================================
# JANELA DE EDIÇÃO
# ====================================================

def abrir_edicao(parent, carro, callback):

    janela = tk.Toplevel(parent)
    janela.title("Editar Veículo")
    janela.geometry("480x520")
    janela.configure(bg=COR_BG)
    janela.resizable(False, False)
    janela.grab_set()

    tk.Frame(janela, bg=COR_VERDE, height=3).pack(fill="x")

    tk.Label(janela, text="✎  Editar Veículo",
             font=("Segoe UI", 16, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(pady=(18, 4), padx=30, anchor="w")

    tk.Frame(janela, bg=COR_BORDA, height=1).pack(fill="x", padx=0, pady=(0, 10))

    frm = tk.Frame(janela, bg=COR_BG)
    frm.pack(padx=30, fill="x")

    campos = [
        ("Marca",  "marca"),
        ("Modelo", "modelo"),
        ("Ano",    "ano"),
        ("Placa",  "placa"),
        ("Cor",    "cor"),
        ("KM",     "km"),
        ("Valor",  "valor"),
    ]

    entradas = {}

    for i, (nome, chave) in enumerate(campos):
        row = i * 2
        tk.Label(frm, text=nome.upper(), font=("Segoe UI", 9, "bold"),
                 bg=COR_BG, fg=COR_SUB).grid(
            row=row, column=0, sticky="w", pady=(6, 2))

        borda = tk.Frame(frm, bg=COR_BORDA)
        borda.grid(row=row+1, column=0, sticky="ew", pady=(0, 4))
        frm.columnconfigure(0, weight=1)

        inner = tk.Frame(borda, bg=COR_INPUT, padx=10, pady=6)
        inner.pack(fill="x", padx=1, pady=1)

        e = tk.Entry(inner, font=("Segoe UI", 10), relief="flat", bd=0,
                     bg=COR_INPUT, fg=COR_TEXTO, insertbackground=COR_VERDE)
        e.pack(fill="x")
        e.insert(0, carro.get(chave, ""))

        def fi(ev, b=borda): b.config(bg=COR_VERDE)
        def fo(ev, b=borda): b.config(bg=COR_BORDA)
        e.bind("<FocusIn>", fi)
        e.bind("<FocusOut>", fo)

        entradas[nome] = e

    tk.Frame(janela, bg=COR_BORDA, height=1).pack(fill="x", pady=(10, 0))

    btn_area = tk.Frame(janela, bg=COR_BG)
    btn_area.pack(fill="x", padx=30, pady=16)

    def salvar():
        dados = {
            "Marca":  entradas["Marca"].get(),
            "Modelo": entradas["Modelo"].get(),
            "Ano":    entradas["Ano"].get(),
            "Placa":  entradas["Placa"].get(),
            "Cor":    entradas["Cor"].get(),
            "KM":     entradas["KM"].get(),
            "Valor":  entradas["Valor"].get(),
        }
        atualizar_veiculo(carro["id"], dados)
        messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso.")
        callback()
        janela.destroy()

    tk.Button(btn_area, text="💾  Salvar Alterações",
              font=("Segoe UI", 10, "bold"),
              bg=COR_VERDE, fg="white", relief="flat",
              cursor="hand2", padx=22, pady=9,
              command=salvar).pack(side="left", padx=(0, 10))

    tk.Button(btn_area, text="Cancelar",
              font=("Segoe UI", 10),
              bg="#94A3B8", fg="white", relief="flat",
              cursor="hand2", padx=16, pady=9,
              command=janela.destroy).pack(side="left")