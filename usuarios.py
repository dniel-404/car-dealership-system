#========================================================================
# usuarios.py - Gerenciamento de Usuários
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    cadastrar_usuario,
    listar_usuarios,
    excluir_usuario,
    atualizar_usuario
)

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


def mostrar_usuarios(parent):

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

    tk.Label(topo_inner, text="👥  Gerenciamento de Usuários",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg=COR_DESTAQUE).pack(side="left")

    tk.Label(topo_inner, text="Cadastre e gerencie os acessos ao sistema",
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
    # CARD CADASTRO
    # ====================================================

    cad_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    cad_card.pack(fill="x", padx=35, pady=(25, 0))

    tk.Frame(cad_card, bg=COR_PRIMARIA, height=3).pack(fill="x")

    tk.Label(cad_card, text="Novo Usuário",
             font=("Segoe UI", 12, "bold"),
             bg=COR_CARD, fg=COR_TEXTO,
             padx=25, pady=14).pack(anchor="w")

    tk.Frame(cad_card, bg=COR_BORDA, height=1).pack(fill="x")

    form = tk.Frame(cad_card, bg=COR_CARD)
    form.pack(padx=25, pady=20, anchor="w")

    def campo_form(parent, label, row, show=None, width=24):
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"),
                 bg=COR_CARD, fg=COR_SUB).grid(
            row=row, column=0, sticky="w", pady=(0, 4), padx=(0, 20))

        borda = tk.Frame(parent, bg=COR_BORDA)
        borda.grid(row=row+1, column=0, sticky="w", pady=(0, 16), padx=(0, 20))

        inner = tk.Frame(borda, bg=COR_INPUT, padx=10, pady=7)
        inner.pack(padx=1, pady=1)

        e = tk.Entry(inner, width=width, font=("Segoe UI", 10),
                     relief="flat", bd=0, bg=COR_INPUT, fg=COR_TEXTO,
                     insertbackground=COR_PRIMARIA, show=show)
        e.pack()

        def fi(ev):
            borda.config(bg=COR_PRIMARIA)

        def fo(ev):
            borda.config(bg=COR_BORDA)

        e.bind("<FocusIn>", fi)
        e.bind("<FocusOut>", fo)

        return e

    def nivel_form(parent, row):
        tk.Label(parent, text="NÍVEL DE ACESSO", font=("Segoe UI", 9, "bold"),
                 bg=COR_CARD, fg=COR_SUB).grid(
            row=row, column=1, sticky="w", pady=(0, 4), padx=(0, 20))

        borda = tk.Frame(parent, bg=COR_BORDA)
        borda.grid(row=row+1, column=1, sticky="w", pady=(0, 16), padx=(0, 20))

        inner = tk.Frame(borda, bg=COR_INPUT, padx=2, pady=2)
        inner.pack(padx=1, pady=1)

        combo = ttk.Combobox(
            inner,
            values=["admin", "gerente", "funcionario"],
            state="readonly",
            width=20,
            font=("Segoe UI", 10)
        )
        combo.pack()

        return combo

    entrada_usuario = campo_form(form, "USUÁRIO", 0, width=24)
    entrada_nome    = campo_form(form, "NOME COMPLETO", 2, width=24)
    entrada_senha   = campo_form(form, "SENHA", 4, show="*", width=24)

    # Nível na segunda coluna
    nivel_combo = nivel_form(form, 0)

    # ── Botão Cadastrar ──────────────────────────────────

    tk.Frame(cad_card, bg=COR_BORDA, height=1).pack(fill="x")

    btn_bar = tk.Frame(cad_card, bg="#F8FAFC")
    btn_bar.pack(fill="x", padx=25, pady=16)

    usuarios_ids = []

    def atualizar_lista():
        tree.delete(*tree.get_children())
        usuarios_ids.clear()

        for i, u in enumerate(listar_usuarios()):
            tag = "par" if i % 2 == 0 else "impar"
            nivel_txt = u[3]
            cor_tag = f"nivel_{nivel_txt}"

            tree.insert(
                "",
                tk.END,
                tags=(tag, cor_tag),
                values=(u[0], u[1], nivel_txt.capitalize())
            )

            usuarios_ids.append(u[0])

        lbl_count.config(text=f"{len(usuarios_ids)} usuário(s) cadastrado(s)")

    def salvar_novo():
        usuario = entrada_usuario.get().strip()
        nome    = entrada_nome.get().strip()
        senha   = entrada_senha.get().strip()
        nivel   = nivel_combo.get()

        if not usuario or not nome or not senha or not nivel:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        ok = cadastrar_usuario(usuario, nome, senha, nivel)

        if not ok:
            messagebox.showerror("Erro", f"Usuário '{usuario}' já existe.")
            return

        messagebox.showinfo("Sucesso", f"Usuário '{usuario}' cadastrado com sucesso!")

        entrada_usuario.delete(0, tk.END)
        entrada_nome.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)
        nivel_combo.set("")

        atualizar_lista()

    def make_btn(parent, texto, cor, hover, cmd):
        b = tk.Button(parent,
                      text=texto,
                      font=("Segoe UI", 10, "bold"),
                      bg=cor,
                      fg="white",
                      relief="flat",
                      cursor="hand2",
                      padx=22,
                      pady=9,
                      bd=0,
                      activebackground=hover,
                      activeforeground="white",
                      command=cmd)

        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=cor))

        return b

    make_btn(
        btn_bar,
        "＋  Cadastrar Usuário",
        COR_PRIMARIA,
        "#1D4ED8",
        salvar_novo
    ).pack(side="left")

    # ====================================================
    # CARD LISTA
    # ====================================================

    lista_card = tk.Frame(corpo, bg=COR_CARD, bd=1, relief="solid")
    lista_card.pack(fill="x", padx=35, pady=(20, 30))

    tk.Frame(lista_card, bg=COR_VERDE, height=3).pack(fill="x")

    cab = tk.Frame(lista_card, bg=COR_CARD)
    cab.pack(fill="x", padx=20, pady=(12, 8))

    tk.Label(cab, text="Usuários do Sistema",
             font=("Segoe UI", 12, "bold"),
             bg=COR_CARD, fg=COR_TEXTO).pack(side="left")

    lbl_count = tk.Label(cab, text="", font=("Segoe UI", 9),
                         bg=COR_CARD, fg=COR_SUB)

    lbl_count.pack(side="right", pady=(4, 0))

    tk.Frame(lista_card, bg=COR_BORDA, height=1).pack(fill="x")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Usr.Treeview",
                    background=COR_CARD,
                    foreground=COR_TEXTO,
                    rowheight=36,
                    fieldbackground=COR_CARD,
                    font=("Segoe UI", 10),
                    borderwidth=0)

    style.configure("Usr.Treeview.Heading",
                    background="#1E293B",
                    foreground="#94A3B8",
                    font=("Segoe UI", 9, "bold"),
                    relief="flat")

    style.map("Usr.Treeview",
              background=[("selected", "#DBEAFE")],
              foreground=[("selected", COR_PRIMARIA)])

    cols = ("id", "usuario", "nivel")

    tree = ttk.Treeview(
        lista_card,
        columns=cols,
        show="headings",
        style="Usr.Treeview",
        height=10,
        selectmode="browse"
    )

    tree.heading("id", text="#")
    tree.heading("usuario", text="Usuário")
    tree.heading("nivel", text="Nível de Acesso")

    tree.column("id", width=50, anchor="center")
    tree.column("usuario", width=250, anchor="w")
    tree.column("nivel", width=180, anchor="center")

    tree.tag_configure("par", background=COR_CARD)
    tree.tag_configure("impar", background="#F8FAFC")
    tree.tag_configure("nivel_admin", foreground="#DC2626")
    tree.tag_configure("nivel_gerente", foreground="#D97706")
    tree.tag_configure("nivel_funcionario", foreground="#059669")

    sc = ttk.Scrollbar(lista_card, orient="vertical", command=tree.yview)

    tree.configure(yscrollcommand=sc.set)

    sc.pack(side="right", fill="y", padx=(0, 5), pady=10)
    tree.pack(fill="x", padx=10, pady=10)

    # ── Botões de ação ───────────────────────────────────

    tk.Frame(lista_card, bg=COR_BORDA, height=1).pack(fill="x")

    acoes = tk.Frame(lista_card, bg="#F8FAFC")
    acoes.pack(fill="x", padx=20, pady=16)

    def get_sel():
        sel = tree.selection()

        if not sel:
            messagebox.showwarning("Atenção", "Selecione um usuário.")
            return None, None

        idx = tree.index(sel[0])

        return usuarios_ids[idx], idx

    def editar():
        id_u, idx = get_sel()

        if id_u is None:
            return

        todos = listar_usuarios()
        u = todos[idx]

        janela = tk.Toplevel(frame)
        janela.title("Editar Usuário")
        janela.geometry("420x300")
        janela.configure(bg=COR_BG)
        janela.resizable(False, False)
        janela.grab_set()

        tk.Frame(janela, bg=COR_PRIMARIA, height=3).pack(fill="x")

        tk.Label(janela, text="Editar Usuário",
                 font=("Segoe UI", 14, "bold"),
                 bg=COR_BG, fg=COR_TEXTO).pack(pady=(18, 4))

        frm = tk.Frame(janela, bg=COR_BG)
        frm.pack(padx=30, pady=10)

        tk.Label(frm, text="USUÁRIO", font=("Segoe UI", 9, "bold"),
                 bg=COR_BG, fg=COR_SUB).grid(row=0, column=0, sticky="w", pady=(0, 4))

        e_usr = tk.Entry(frm, width=24, font=("Segoe UI", 10),
                         relief="solid", bd=1)
        e_usr.grid(row=1, column=0, ipady=7, padx=(0, 20), pady=(0, 12))
        e_usr.insert(0, u[1])

        tk.Label(frm, text="NOME", font=("Segoe UI", 9, "bold"),
                 bg=COR_BG, fg=COR_SUB).grid(row=2, column=0, sticky="w", pady=(0, 4))

        e_nome = tk.Entry(frm, width=24, font=("Segoe UI", 10),
                          relief="solid", bd=1)
        e_nome.grid(row=3, column=0, ipady=7, padx=(0, 20), pady=(0, 12))
        e_nome.insert(0, u[2])

        tk.Label(frm, text="NÍVEL", font=("Segoe UI", 9, "bold"),
                 bg=COR_BG, fg=COR_SUB).grid(row=0, column=1, sticky="w", pady=(0, 4))

        c_nivel = ttk.Combobox(
            frm,
            values=["admin", "gerente", "funcionario"],
            state="readonly",
            width=16,
            font=("Segoe UI", 10)
        )

        c_nivel.grid(row=1, column=1, ipady=7, pady=(0, 12))
        c_nivel.set(u[3])

        def salvar_edicao():
            atualizar_usuario(id_u, e_usr.get(), e_nome.get(), c_nivel.get())
            atualizar_lista()
            janela.destroy()
            messagebox.showinfo("Sucesso", "Usuário atualizado.")

        tk.Button(janela,
                  text="Salvar Alterações",
                  font=("Segoe UI", 10, "bold"),
                  bg=COR_PRIMARIA,
                  fg="white",
                  relief="flat",
                  cursor="hand2",
                  padx=24,
                  pady=10,
                  command=salvar_edicao).pack(pady=10)

    def excluir():
        id_u, _ = get_sel()

        if id_u is None:
            return

        if messagebox.askyesno(
            "Confirmar",
            "Deseja excluir este usuário?\nEssa ação não pode ser desfeita."
        ):
            excluir_usuario(id_u)
            atualizar_lista()
            messagebox.showinfo("Sucesso", "Usuário excluído.")

    make_btn(
        acoes,
        "✎  Editar",
        COR_VERDE,
        "#047857",
        editar
    ).pack(side="left", padx=(0, 10))

    make_btn(
        acoes,
        "🗑  Excluir",
        COR_VERMELHO,
        "#B91C1C",
        excluir
    ).pack(side="left")

    tk.Label(
        acoes,
        text="Selecione um usuário antes de editar ou excluir.",
        font=("Segoe UI", 9),
        bg="#F8FAFC",
        fg="#94A3B8"
    ).pack(side="right", padx=(0, 5))

    atualizar_lista()

    def bind_scroll(widget):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        for child in widget.winfo_children():
            bind_scroll(child)

    corpo.after(100, lambda: bind_scroll(corpo))