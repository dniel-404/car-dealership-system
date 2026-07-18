#========================================================================
# agendamento.py - Agenda Profissional
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from database import (
    salvar_agendamento,
    listar_agendamentos,
    excluir_agendamento,
    listar_clientes
)

COR_BG      = "#F1F5F9"
COR_CARD    = "#FFFFFF"
COR_TOPO    = "#0F172A"
COR_DESTAQUE = "#FBBF24"
COR_PRIMARIA = "#2563EB"
COR_VERMELHO = "#DC2626"
COR_TEXTO   = "#1E293B"
COR_SUB     = "#64748B"
COR_BORDA   = "#E2E8F0"
COR_INPUT   = "#F1F5F9"


def _scroll_bind(canvas, widget):
    def on_scroll(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    widget.bind("<MouseWheel>", on_scroll)
    for child in widget.winfo_children():
        _scroll_bind(canvas, child)


def mostrar_agendamento(parent):

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

    tk.Label(topo_inner, text="📅  Agendamentos",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg=COR_DESTAQUE).pack(side="left")

    tk.Label(topo_inner, text="Gerencie visitas e test drives",
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
    # CARD FORMULÁRIO
    # ====================================================

    form_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    form_card.pack(fill="x", padx=35, pady=(25, 0))

    tk.Frame(form_card, bg=COR_PRIMARIA, height=3).pack(fill="x")

    tk.Label(form_card, text="Novo Agendamento",
             font=("Segoe UI", 12, "bold"),
             bg=COR_CARD, fg=COR_TEXTO,
             padx=25, pady=14).pack(anchor="w")

    tk.Frame(form_card, bg=COR_BORDA, height=1).pack(fill="x")

    form = tk.Frame(form_card, bg=COR_CARD)
    form.pack(padx=25, pady=20)

    def campo_label(texto, row, col):
        tk.Label(form, text=texto, font=("Segoe UI", 9, "bold"),
                 bg=COR_CARD, fg=COR_SUB).grid(
            row=row, column=col, sticky="w", padx=(0, 20), pady=(0, 4))

    # ── Cliente (Combobox com clientes do banco) ──────────
    campo_label("CLIENTE", 0, 0)

    clientes_db = listar_clientes()
    nomes_clientes = [c.get("nome", "") for c in clientes_db if c.get("nome")]

    cliente_var = tk.StringVar()
    combo_cliente = ttk.Combobox(
        form,
        textvariable=cliente_var,
        values=nomes_clientes,
        state="readonly",
        width=28,
        font=("Segoe UI", 10)
    )
    combo_cliente.grid(row=1, column=0, ipady=5, padx=(0, 20), pady=(0, 14))

    if not nomes_clientes:
        combo_cliente.set("Nenhum cliente cadastrado")
    else:
        combo_cliente.set("")

    # ── Data ──────────────────────────────────────────────
    campo_label("DATA", 0, 1)

    calendario = DateEntry(
        form,
        width=18,
        date_pattern="dd/mm/yyyy",
        mindate=datetime.now().date(),
        font=("Segoe UI", 10),
        background="#0F172A",
        foreground="white",
        bordercolor=COR_BORDA,
        headersbackground="#1E293B",
        headersforeground="white",
        selectbackground=COR_PRIMARIA
    )
    calendario.grid(row=1, column=1, ipady=5, padx=(0, 20), pady=(0, 14))

    # ── Hora ──────────────────────────────────────────────
    campo_label("HORA", 0, 2)

    hora_combo = ttk.Combobox(
        form,
        values=["08:00","09:00","10:00","11:00",
                "13:00","14:00","15:00","16:00","17:00"],
        state="readonly",
        width=12,
        font=("Segoe UI", 10)
    )
    hora_combo.grid(row=1, column=2, ipady=5, padx=(0, 20), pady=(0, 14))

    # ── Tipo ──────────────────────────────────────────────
    campo_label("TIPO", 0, 3)

    tipo_combo = ttk.Combobox(
        form,
        values=["Visita", "Test Drive"],
        state="readonly",
        width=14,
        font=("Segoe UI", 10)
    )
    tipo_combo.grid(row=1, column=3, ipady=5, pady=(0, 14))

    # ====================================================
    # LISTA DE AGENDAMENTOS
    # ====================================================

    lista_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    lista_card.pack(fill="x", padx=35, pady=(20, 0))

    tk.Frame(lista_card, bg="#7C3AED", height=3).pack(fill="x")

    cab = tk.Frame(lista_card, bg=COR_CARD)
    cab.pack(fill="x", padx=20, pady=(12, 8))

    tk.Label(cab, text="Agendamentos Cadastrados",
             font=("Segoe UI", 12, "bold"),
             bg=COR_CARD, fg=COR_TEXTO).pack(side="left")

    lbl_count = tk.Label(cab, text="",
                         font=("Segoe UI", 9),
                         bg=COR_CARD, fg=COR_SUB)
    lbl_count.pack(side="right", pady=(4, 0))

    tk.Frame(lista_card, bg=COR_BORDA, height=1).pack(fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Ag.Treeview",
                    background=COR_CARD, foreground=COR_TEXTO,
                    rowheight=34, fieldbackground=COR_CARD,
                    font=("Segoe UI", 10), borderwidth=0)
    style.configure("Ag.Treeview.Heading",
                    background="#1E293B", foreground="#94A3B8",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Ag.Treeview",
              background=[("selected", "#EDE9FE")],
              foreground=[("selected", "#7C3AED")])

    cols = ("data", "hora", "cliente", "tipo")
    tree = ttk.Treeview(lista_card, columns=cols, show="headings",
                        style="Ag.Treeview", height=8)

    cfg_cols = {
        "data":    ("Data",    130),
        "hora":    ("Hora",     90),
        "cliente": ("Cliente", 280),
        "tipo":    ("Tipo",    130),
    }
    for col, (titulo, larg) in cfg_cols.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=larg, anchor="center")

    tree.tag_configure("par",   background=COR_CARD)
    tree.tag_configure("impar", background="#F8FAFC")
    tree.tag_configure("visita",    foreground="#059669")
    tree.tag_configure("testdrive", foreground="#2563EB")

    sc_y = ttk.Scrollbar(lista_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc_y.set)
    sc_y.pack(side="right", fill="y", padx=(0, 5), pady=10)
    tree.pack(fill="x", padx=10, pady=10)

    resultados = []

    def atualizar():
        tree.delete(*tree.get_children())
        resultados.clear()

        for i, a in enumerate(listar_agendamentos()):
            tag_par = "par" if i % 2 == 0 else "impar"
            tag_tipo = "visita" if a.get("tipo") == "Visita" else "testdrive"
            tree.insert("", tk.END, tags=(tag_par, tag_tipo), values=(
                a.get("data", ""),
                a.get("hora", ""),
                a.get("cliente", ""),
                a.get("tipo", "")
            ))
            resultados.append(a)

        lbl_count.config(text=f"{len(resultados)} agendamento(s)")

    # ====================================================
    # BOTÕES
    # ====================================================

    tk.Frame(lista_card, bg=COR_BORDA, height=1).pack(fill="x")

    btn_area = tk.Frame(lista_card, bg=COR_CARD)
    btn_area.pack(fill="x", padx=20, pady=14)

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

    def agendar():
        cliente = cliente_var.get().strip()
        data    = calendario.get()
        hr      = hora_combo.get()
        tp      = tipo_combo.get()

        if not cliente or not data or not hr or not tp:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        if cliente == "Nenhum cliente cadastrado":
            messagebox.showwarning("Atenção", "Cadastre um cliente primeiro.")
            return

        data_obj = datetime.strptime(data, "%d/%m/%Y").date()
        if data_obj < datetime.now().date():
            messagebox.showerror("Erro", "Não é possível agendar em datas passadas.")
            return

        for a in listar_agendamentos():
            if a["data"] == data and a["hora"] == hr:
                messagebox.showerror("Erro",
                    f"Já existe um agendamento para {data} às {hr}.")
                return

        salvar_agendamento({
            "Cliente": cliente,
            "Tipo":    tp,
            "Data":    data,
            "Hora":    hr
        })

        atualizar()
        cliente_var.set("")
        hora_combo.set("")
        tipo_combo.set("")
        messagebox.showinfo("Sucesso", "Agendamento realizado com sucesso!")

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um agendamento.")
            return
        idx = tree.index(sel[0])
        a = resultados[idx]
        if messagebox.askyesno("Confirmar",
                f"Excluir agendamento de {a['cliente']} em {a['data']}?"):
            excluir_agendamento(a["id"])
            atualizar()

    make_btn(btn_area, "✔  Salvar Agendamento",
             COR_PRIMARIA, "#1D4ED8", agendar).pack(side="left", padx=(0, 10))

    make_btn(btn_area, "🗑  Excluir",
             COR_VERMELHO, "#B91C1C", excluir).pack(side="left")

    atualizar()

    # Bind scroll
    corpo.after(100, lambda: _scroll_bind(canvas, corpo))