# ====================================================
# acesso.py - Login Profissional SysCar
# ====================================================

import tkinter as tk
from tkinter import messagebox
from database import validar_login
from sessao import iniciar_sessao

COR_BG       = "#0F172A"
COR_CARD     = "#1E293B"
COR_INPUT    = "#0F172A"
COR_BORDA    = "#334155"
COR_TEXTO    = "#F1F5F9"
COR_SUB      = "#94A3B8"
COR_DESTAQUE = "#FBBF24"
COR_PRIMARIA = "#2563EB"
COR_HOVER    = "#1D4ED8"


def maximizar_janela(janela):
    try:
        janela.state("zoomed")
    except Exception:
        w = janela.winfo_screenwidth()
        h = janela.winfo_screenheight()
        janela.geometry(f"{w}x{h}+0+0")


def abrir_menu(janela):
    janela.destroy()
    import menu
    menu.iniciar_menu()


def ao_acessar(campo_login, campo_senha, janela):
    login = campo_login.get().strip()
    senha = campo_senha.get().strip()

    if not login or not senha:
        messagebox.showwarning("Atenção", "Informe login e senha.")
        return

    usuario = validar_login(login, senha)

    if not usuario:
        messagebox.showerror("Acesso Negado", "Login ou senha incorretos.")
        campo_senha.delete(0, tk.END)
        campo_senha.focus()
        return

    iniciar_sessao(usuario["usuario"], usuario["nivel"])
    abrir_menu(janela)


def criar_janela():

    raiz = tk.Tk()
    raiz.title("SysCar — Acesso ao Sistema")
    raiz.configure(bg=COR_BG)
    raiz.minsize(1100, 650)
    raiz.after(50, lambda: maximizar_janela(raiz))

    # ====================================================
    # LAYOUT PRINCIPAL — dois painéis lado a lado
    # ====================================================

    raiz.grid_columnconfigure(0, weight=3)
    raiz.grid_columnconfigure(1, weight=2)
    raiz.grid_rowconfigure(0, weight=1)

    # ====================================================
    # PAINEL ESQUERDO — marca / visual
    # ====================================================

    painel_esq = tk.Frame(raiz, bg="#020617")
    painel_esq.grid(row=0, column=0, sticky="nsew")

    centro_esq = tk.Frame(painel_esq, bg="#020617")
    centro_esq.place(relx=0.5, rely=0.5, anchor="center")

    # Ícone grande
    tk.Label(centro_esq, text="🚗",
             font=("Segoe UI", 72),
             bg="#020617").pack(pady=(0, 16))

    tk.Label(centro_esq, text="SysCar",
             font=("Segoe UI", 48, "bold"),
             bg="#020617", fg=COR_DESTAQUE).pack()

    tk.Label(centro_esq, text="SISTEMA AUTOMOTIVO",
             font=("Segoe UI", 12, "bold"),
             bg="#020617", fg="#334155",
             ).pack(pady=(4, 32))

    # Divisor
    tk.Frame(centro_esq, bg="#1E293B", height=1, width=280).pack(pady=(0, 28))

    # Benefícios
    beneficios = [
        ("📋", "Gestão completa de clientes e frota"),
        ("💰", "Controle de vendas e financeiro"),
        ("📅", "Agendamentos e test drives"),
        ("📊", "Dashboard e relatórios gerenciais"),
    ]

    for icone, texto in beneficios:
        linha = tk.Frame(centro_esq, bg="#020617")
        linha.pack(anchor="w", pady=5)
        tk.Label(linha, text=icone, font=("Segoe UI", 14),
                 bg="#020617").pack(side="left", padx=(0, 12))
        tk.Label(linha, text=texto, font=("Segoe UI", 11),
                 bg="#020617", fg="#64748B").pack(side="left")

    # Rodapé esquerdo
    tk.Label(painel_esq, text="© 2026 SysCar. Todos os direitos reservados.",
             font=("Segoe UI", 8), bg="#020617", fg="#1E293B").pack(
        side="bottom", pady=16)

    # ====================================================
    # PAINEL DIREITO — formulário de login
    # ====================================================

    painel_dir = tk.Frame(raiz, bg=COR_BG)
    painel_dir.grid(row=0, column=1, sticky="nsew")

    # Linha decorativa vertical
    tk.Frame(painel_dir, bg=COR_DESTAQUE, width=3).pack(
        side="left", fill="y")

    form_area = tk.Frame(painel_dir, bg=COR_BG)
    form_area.pack(fill="both", expand=True)

    card = tk.Frame(form_area, bg=COR_BG)
    card.place(relx=0.5, rely=0.5, anchor="center")

    # Cabeçalho do form
    tk.Label(card, text="Bem-vindo de volta",
             font=("Segoe UI", 26, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(anchor="w")

    tk.Label(card, text="Entre com suas credenciais para acessar",
             font=("Segoe UI", 11),
             bg=COR_BG, fg=COR_SUB).pack(anchor="w", pady=(4, 32))

    # ── Campo Login ──────────────────────────────────────

    def criar_campo(parent, label, show=None):
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"),
                 bg=COR_BG, fg=COR_SUB).pack(anchor="w", pady=(0, 5))

        borda = tk.Frame(parent, bg=COR_BORDA)
        borda.pack(fill="x", pady=(0, 18))

        inner = tk.Frame(borda, bg=COR_INPUT, padx=14, pady=10)
        inner.pack(fill="x", padx=1, pady=1)

        e = tk.Entry(inner, font=("Segoe UI", 11), relief="flat", bd=0,
                     bg=COR_INPUT, fg=COR_TEXTO,
                     insertbackground=COR_DESTAQUE, show=show)
        e.pack(fill="x")

        def on_in(ev):  borda.config(bg=COR_DESTAQUE)
        def on_out(ev): borda.config(bg=COR_BORDA)

        e.bind("<FocusIn>",  on_in)
        e.bind("<FocusOut>", on_out)

        return e

    entrada_login = criar_campo(card, "USUÁRIO")
    entrada_senha = criar_campo(card, "SENHA", show="*")

    # ── Botão Entrar ─────────────────────────────────────

    btn_entrar = tk.Button(
        card, text="Entrar no Sistema",
        font=("Segoe UI", 11, "bold"),
        bg=COR_PRIMARIA, fg="white",
        relief="flat", cursor="hand2",
        padx=30, pady=13, bd=0,
        activebackground=COR_HOVER,
        activeforeground="white",
        command=lambda: ao_acessar(entrada_login, entrada_senha, raiz)
    )
    btn_entrar.pack(fill="x", pady=(6, 0))
    btn_entrar.bind("<Enter>", lambda e: btn_entrar.config(bg=COR_HOVER))
    btn_entrar.bind("<Leave>", lambda e: btn_entrar.config(bg=COR_PRIMARIA))

    # Enter no teclado
    raiz.bind("<Return>", lambda e: ao_acessar(
        entrada_login, entrada_senha, raiz))

    # ── Rodapé do form ───────────────────────────────────

    tk.Frame(card, bg=COR_BORDA, height=1, width=340).pack(pady=(28, 16))

    tk.Label(card, text="Problemas de acesso? Contate o administrador.",
             font=("Segoe UI", 9), bg=COR_BG, fg="#475569").pack()

    entrada_login.focus()
    raiz.mainloop()


if __name__ == "__main__":
    criar_janela()