#========================================================================
# menu.py - Interface SysCar
#========================================================================

import tkinter as tk
from sessao import usuario_logado, encerrar_sessao
from permissoes import tem_permissao

COR_SIDEBAR  = "#020617"
COR_MENU     = "#0F172A"
COR_SUBMENU  = "#0A1628"
COR_HOVER    = "#1E293B"
COR_TEXTO    = "#E2E8F0"
COR_SUBTEXTO = "#94A3B8"
COR_DESTAQUE = "#FBBF24"
COR_BG       = "#F1F5F9"


def maximizar_janela(janela):
    try:
        janela.state("zoomed")
    except Exception:
        w = janela.winfo_screenwidth()
        h = janela.winfo_screenheight()
        janela.geometry(f"{w}x{h}+0+0")


def limpar_area(area):
    for w in area.winfo_children():
        w.destroy()


def mostrar_tela_cliente(area):
    limpar_area(area)
    import CadCli
    CadCli.mostrar_formulario(area)

def mostrar_pesquisa_cliente(area):
    limpar_area(area)
    import pesqCli
    pesqCli.mostrar_pesquisa(area)

def mostrar_pesquisa_veiculos(area):
    limpar_area(area)
    import frota
    frota.mostrar_frota(area)

def mostrar_cadastro_veiculos(area):
    limpar_area(area)
    import carro
    carro.mostrar_formulario(area)

def mostrar_agendamento(area):
    limpar_area(area)
    import agendamento
    agendamento.mostrar_agendamento(area)

def mostrar_dashboard(area):
    limpar_area(area)
    import dashboard
    dashboard.mostrar_dashboard(area)

def mostrar_adm(area):
    limpar_area(area)
    import adm
    adm.mostrar_adm(area)

def mostrar_usuarios_sistema(area):
    limpar_area(area)
    import usuarios
    usuarios.mostrar_usuarios(area)

def mostrar_relatorios(area):
    limpar_area(area)
    import relatorios
    relatorios.mostrar_relatorio(area)

def mostrar_vendas(area):
    limpar_area(area)
    import vendas
    vendas.mostrar_vendas(area)

def fazer_logout(raiz):
    encerrar_sessao()
    raiz.destroy()
    import acesso
    acesso.criar_janela()


# =========================================================
# COMPONENTES
# =========================================================

def criar_item_menu(pai, icone, texto, subitens=None, acoes=None):

    container = tk.Frame(pai, bg=COR_SIDEBAR)
    container.pack(fill="x", pady=1)

    btn = tk.Frame(container, bg=COR_MENU)
    btn.pack(fill="x", padx=8)

    lbl_icone = tk.Label(btn, text=icone, font=("Segoe UI", 12),
                         bg=COR_MENU, fg=COR_DESTAQUE, padx=10, pady=10)
    lbl_icone.pack(side="left")

    lbl_texto = tk.Label(btn, text=texto, font=("Segoe UI", 10, "bold"),
                         bg=COR_MENU, fg=COR_TEXTO, anchor="w", pady=10)
    lbl_texto.pack(side="left", fill="x", expand=True)

    lbl_seta = tk.Label(btn, text="›", font=("Segoe UI", 13),
                        bg=COR_MENU, fg=COR_SUBTEXTO, padx=10, pady=10)
    if subitens:
        lbl_seta.pack(side="right")

    todos_btn = [btn, lbl_icone, lbl_texto, lbl_seta]

    def hover_on(e):
        for w in todos_btn: w.config(bg=COR_HOVER)
    def hover_off(e):
        for w in todos_btn: w.config(bg=COR_MENU)
    for w in todos_btn:
        w.bind("<Enter>", hover_on)
        w.bind("<Leave>", hover_off)

    if not subitens:
        return container

    sub_panel = tk.Frame(container, bg=COR_SUBMENU)
    aberto = [False]

    for sub_icone, nome in subitens:
        acao = (acoes or {}).get(nome, lambda: None)
        sub_row = tk.Frame(sub_panel, bg=COR_SUBMENU)
        sub_row.pack(fill="x", padx=8, pady=1)

        tk.Label(sub_row, text="", bg=COR_SUBMENU, width=3, pady=8).pack(side="left")
        tk.Frame(sub_row, bg="#2D3F55", width=2).pack(side="left", fill="y", padx=(0, 8))

        lbl_si = tk.Label(sub_row, text=sub_icone, font=("Segoe UI", 10),
                          bg=COR_SUBMENU, fg="#94A3B8", pady=8)
        lbl_si.pack(side="left", padx=(0, 6))

        lbl_sn = tk.Label(sub_row, text=nome, font=("Segoe UI", 9),
                          bg=COR_SUBMENU, fg="#CBD5E1", anchor="w", pady=8)
        lbl_sn.pack(side="left", fill="x", expand=True)

        todos_sub = [sub_row, lbl_si, lbl_sn]

        def sub_on(e, ws=todos_sub):
            for w in ws: w.config(bg=COR_HOVER)
        def sub_off(e, ws=todos_sub):
            for w in ws: w.config(bg=COR_SUBMENU)
        def sub_click(e, a=acao): a()

        for w in todos_sub:
            w.bind("<Enter>", sub_on)
            w.bind("<Leave>", sub_off)
            w.bind("<Button-1>", sub_click)

    def toggle(e=None):
        if aberto[0]:
            sub_panel.pack_forget()
            lbl_seta.config(text="›")
            aberto[0] = False
        else:
            sub_panel.pack(fill="x")
            lbl_seta.config(text="⌄")
            aberto[0] = True

    for w in todos_btn:
        w.bind("<Button-1>", toggle)

    return container


def criar_separador(pai):
    tk.Frame(pai, bg="#1A2535", height=1).pack(fill="x", padx=12, pady=3)

def criar_label_secao(pai, texto):
    tk.Label(pai, text=texto, font=("Segoe UI", 7, "bold"),
             bg=COR_SIDEBAR, fg="#374151", anchor="w",
             padx=20, pady=5).pack(fill="x")


# =========================================================
# SIDEBAR COM SCROLL
# =========================================================

def criar_sidebar(raiz):

    sidebar = tk.Frame(raiz, bg=COR_SIDEBAR, width=260)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar.grid_propagate(False)

    logo_frame = tk.Frame(sidebar, bg=COR_SIDEBAR)
    logo_frame.pack(fill="x", side="top")
    tk.Frame(logo_frame, bg="#1E293B", height=1).pack(fill="x")
    logo_inner = tk.Frame(logo_frame, bg=COR_SIDEBAR)
    logo_inner.pack(fill="x", padx=22, pady=18)
    tk.Label(logo_inner, text="SysCar", font=("Segoe UI", 24, "bold"),
             bg=COR_SIDEBAR, fg=COR_DESTAQUE).pack(anchor="w")
    tk.Label(logo_inner, text="ERP AUTOMOTIVO", font=("Segoe UI", 8, "bold"),
             bg=COR_SIDEBAR, fg="#334155").pack(anchor="w")
    tk.Frame(logo_frame, bg="#1E293B", height=1).pack(fill="x")

    canvas = tk.Canvas(sidebar, bg=COR_SIDEBAR, highlightthickness=0)
    scrollbar = tk.Scrollbar(sidebar, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    menu_frame = tk.Frame(canvas, bg=COR_SIDEBAR)
    canvas_win = canvas.create_window((0, 0), window=menu_frame, anchor="nw")

    def atualizar_scroll(e=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_larg(e):
        canvas.itemconfig(canvas_win, width=e.width)

    def scroll_mouse(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def bind_scroll(widget):
        widget.bind("<MouseWheel>", scroll_mouse)
        for child in widget.winfo_children():
            bind_scroll(child)

    menu_frame.bind("<Configure>", lambda e: (
        atualizar_scroll(), bind_scroll(menu_frame)))
    canvas.bind("<Configure>", ajustar_larg)
    canvas.bind("<MouseWheel>", scroll_mouse)

    return menu_frame


# =========================================================
# MONTAR MENU
# =========================================================

def montar_menu(menu, area):

    if tem_permissao("clientes"):
        criar_label_secao(menu, "  CLIENTES")
        criar_item_menu(menu, "👤", "Cliente",
            subitens=[("＋", "Cadastro"), ("🔍", "Pesquisa")],
            acoes={
                "Cadastro": lambda: mostrar_tela_cliente(area),
                "Pesquisa": lambda: mostrar_pesquisa_cliente(area),
            })
        criar_separador(menu)

    if tem_permissao("frota"):
        criar_label_secao(menu, "  FROTA")
        criar_item_menu(menu, "🚗", "Veículos",
            subitens=[("＋", "Cadastrar"), ("🔍", "Pesquisar")],
            acoes={
                "Cadastrar": lambda: mostrar_cadastro_veiculos(area),
                "Pesquisar": lambda: mostrar_pesquisa_veiculos(area),
            })
        criar_separador(menu)

    if tem_permissao("vendas"):
        criar_label_secao(menu, "  COMERCIAL")
        criar_item_menu(menu, "💰", "Vendas",
            subitens=[("＋", "Nova Venda")],
            acoes={"Nova Venda": lambda: mostrar_vendas(area)})
        criar_separador(menu)

    criar_label_secao(menu, "  AGENDA")
    criar_item_menu(menu, "📅", "Agendamentos",
        subitens=[("📆", "Calendário")],
        acoes={"Calendário": lambda: mostrar_agendamento(area)})
    criar_separador(menu)

    if tem_permissao("dashboard"):
        criar_label_secao(menu, "  GESTÃO")
        criar_item_menu(menu, "📊", "Dashboard",
            subitens=[("📈", "Visão Geral")],
            acoes={"Visão Geral": lambda: mostrar_dashboard(area)})
        criar_separador(menu)

    if tem_permissao("adm"):
        criar_label_secao(menu, "  ADMINISTRAÇÃO")
        criar_item_menu(menu, "⚙", "Administração",
            subitens=[
                ("💵", "Financeiro"),
                ("👥", "Usuários"),
                ("📄", "Relatórios"),
            ],
            acoes={
                "Financeiro": lambda: mostrar_adm(area),
                "Usuários":   lambda: mostrar_usuarios_sistema(area),
                "Relatórios": lambda: mostrar_relatorios(area),
            })


# =========================================================
# TELA INICIAL
# =========================================================

def mostrar_tela_inicial(area):
    limpar_area(area)
    frame = tk.Frame(area, bg="#F1F5F9")
    frame.pack(fill="both", expand=True)
    centro = tk.Frame(frame, bg="#F1F5F9")
    centro.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(centro, text="🚗", font=("Segoe UI", 56), bg="#F1F5F9").pack()
    tk.Label(centro, text="SysCar ERP", font=("Segoe UI", 32, "bold"),
             bg="#F1F5F9", fg="#0F172A").pack(pady=(10, 4))
    tk.Label(centro, text="Selecione uma opção no menu lateral para começar.",
             font=("Segoe UI", 12), bg="#F1F5F9", fg="#64748B").pack()
    usuario = usuario_logado.get("usuario", "")
    nivel   = usuario_logado.get("nivel", "")
    tk.Label(centro, text=f"Bem-vindo, {usuario}  •  {nivel.upper()}",
             font=("Segoe UI", 10), bg="#F1F5F9", fg="#94A3B8").pack(pady=(20, 0))


# =========================================================
# MAIN
# =========================================================

def iniciar_menu():

    raiz = tk.Tk()
    raiz.title("SysCar ERP")
    raiz.configure(bg=COR_BG)
    raiz.minsize(1200, 700)
    maximizar_janela(raiz)

    raiz.grid_columnconfigure(1, weight=1)
    raiz.grid_rowconfigure(1, weight=1)

    menu_frame = criar_sidebar(raiz)

    topbar = tk.Frame(raiz, bg="white", height=64)
    topbar.grid(row=0, column=1, sticky="nsew")
    topbar.grid_propagate(False)
    tk.Frame(topbar, bg="#E2E8F0", height=1).pack(side="bottom", fill="x")

    topbar_right = tk.Frame(topbar, bg="white")
    topbar_right.pack(side="right", fill="y", padx=25)

    usuario = usuario_logado.get("usuario", "")
    nivel   = usuario_logado.get("nivel", "")

    user_box = tk.Frame(topbar_right, bg="white")
    user_box.pack(side="left", fill="y", padx=(0, 15))
    tk.Label(user_box, text=f"👤  {usuario}", font=("Segoe UI", 10, "bold"),
             bg="white", fg="#334155").pack(anchor="w", pady=(16, 1))
    tk.Label(user_box, text=nivel.upper(), font=("Segoe UI", 7, "bold"),
             bg="white", fg="#94A3B8").pack(anchor="w")

    tk.Frame(topbar_right, bg="#E2E8F0", width=1).pack(
        side="left", fill="y", pady=15, padx=(0, 15))

    btn_sair = tk.Button(topbar_right, text="Sair",
        font=("Segoe UI", 9, "bold"),
        bg="#FEE2E2", fg="#DC2626", relief="flat", cursor="hand2",
        padx=16, pady=7, bd=0,
        activebackground="#FECACA", activeforeground="#DC2626",
        command=lambda: fazer_logout(raiz))
    btn_sair.pack(side="left", anchor="center", pady=18)
    btn_sair.bind("<Enter>", lambda e: btn_sair.config(bg="#FECACA"))
    btn_sair.bind("<Leave>", lambda e: btn_sair.config(bg="#FEE2E2"))

    conteudo = tk.Frame(raiz, bg=COR_BG)
    conteudo.grid(row=1, column=1, sticky="nsew")

    montar_menu(menu_frame, conteudo)
    mostrar_tela_inicial(conteudo)

    raiz.mainloop()


if __name__ == "__main__":
    iniciar_menu()