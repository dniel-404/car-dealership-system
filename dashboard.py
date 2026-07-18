#========================================================================
# dashboard.py - Dashboard Executivo
#========================================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from database import (
    listar_clientes,
    listar_veiculos,
    listar_agendamentos,
    listar_usuarios,
    resumo_financeiro,
    listar_vendas
)

COR_BG      = "#F1F5F9"
COR_CARD    = "#FFFFFF"
COR_TOPO    = "#0F172A"
COR_TEXTO   = "#1E293B"
COR_SUB     = "#64748B"
COR_BORDA   = "#E2E8F0"


def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def _scroll_bind(canvas, widget):
    """Propaga scroll do mouse para o canvas."""
    def on_scroll(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    widget.bind("<MouseWheel>", on_scroll)
    for child in widget.winfo_children():
        _scroll_bind(canvas, child)


def mostrar_dashboard(parent):

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
    topo_inner.pack(fill="x", padx=35, pady=20)

    agora = datetime.now()

    tk.Label(topo_inner, text="📊  Dashboard Executivo",
             font=("Segoe UI", 22, "bold"),
             bg=COR_TOPO, fg="#FBBF24").pack(side="left")

    tk.Label(topo_inner,
             text=agora.strftime("%d/%m/%Y  •  %H:%M"),
             font=("Segoe UI", 10),
             bg=COR_TOPO, fg="#475569").pack(side="right", pady=(6, 0))

    # ====================================================
    # ÁREA SCROLLÁVEL
    # ====================================================

    container = tk.Frame(frame, bg=COR_BG)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
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
    # DADOS
    # ====================================================

    clientes    = listar_clientes()
    veiculos    = listar_veiculos()
    agendamentos = listar_agendamentos()
    usuarios    = listar_usuarios()
    financeiro  = resumo_financeiro()
    vendas      = listar_vendas()

    disponiveis = [v for v in veiculos if v.get("status") in ("disponivel", None, "")]
    vendidos    = [v for v in veiculos if v.get("status") == "vendido"]

    # ====================================================
    # CARDS DE MÉTRICAS
    # ====================================================

    def criar_card_metrica(pai, icone, titulo, valor, cor, subtitulo=""):
        card = tk.Frame(pai, bg=COR_CARD, bd=1, relief="solid")
        card.pack(side="left", padx=(0, 16), fill="both", expand=True)

        # Barra colorida no topo
        tk.Frame(card, bg=cor, height=4).pack(fill="x")

        inner = tk.Frame(card, bg=COR_CARD)
        inner.pack(fill="both", expand=True, padx=20, pady=16)

        # Ícone + título
        top_row = tk.Frame(inner, bg=COR_CARD)
        top_row.pack(fill="x")

        tk.Label(top_row, text=icone, font=("Segoe UI", 20),
                 bg=COR_CARD).pack(side="left")

        tk.Label(top_row, text=titulo, font=("Segoe UI", 10, "bold"),
                 bg=COR_CARD, fg=COR_SUB).pack(side="left", padx=(10, 0), pady=(4, 0))

        # Valor
        tk.Label(inner, text=str(valor), font=("Segoe UI", 28, "bold"),
                 bg=COR_CARD, fg=cor).pack(anchor="w", pady=(8, 2))

        if subtitulo:
            tk.Label(inner, text=subtitulo, font=("Segoe UI", 9),
                     bg=COR_CARD, fg="#94A3B8").pack(anchor="w")

        return card

    # Linha 1 — Resumo operacional
    sec1 = tk.Frame(corpo, bg=COR_BG)
    sec1.pack(fill="x", padx=35, pady=(28, 0))

    tk.Label(sec1, text="Resumo Operacional",
             font=("Segoe UI", 13, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(anchor="w", pady=(0, 12))

    cards1 = tk.Frame(sec1, bg=COR_BG)
    cards1.pack(fill="x")

    criar_card_metrica(cards1, "👤", "Clientes",      len(clientes),     "#2563EB", "cadastrados")
    criar_card_metrica(cards1, "🚗", "Frota Total",   len(veiculos),     "#0EA5E9", f"{len(disponiveis)} disponíveis")
    criar_card_metrica(cards1, "✅", "Vendidos",       len(vendidos),     "#059669", "veículos vendidos")
    criar_card_metrica(cards1, "📅", "Agendamentos",  len(agendamentos), "#7C3AED", "registrados")
    criar_card_metrica(cards1, "👥", "Usuários",      len(usuarios),     "#EA580C", "do sistema")

    # Linha 2 — Financeiro
    sec2 = tk.Frame(corpo, bg=COR_BG)
    sec2.pack(fill="x", padx=35, pady=(24, 0))

    tk.Label(sec2, text="Painel Financeiro",
             font=("Segoe UI", 13, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(anchor="w", pady=(0, 12))

    cards2 = tk.Frame(sec2, bg=COR_BG)
    cards2.pack(fill="x")

    cor_lucro = "#059669" if financeiro["lucro"] >= 0 else "#DC2626"
    icone_lucro = "📈" if financeiro["lucro"] >= 0 else "📉"

    criar_card_metrica(cards2, "💵", "Receitas",
                       formatar_moeda(financeiro["receitas"]), "#059669", "total em vendas")
    criar_card_metrica(cards2, "💸", "Despesas",
                       formatar_moeda(financeiro["despesas"]), "#DC2626", "total em compras")
    criar_card_metrica(cards2, icone_lucro, "Lucro Líquido",
                       formatar_moeda(financeiro["lucro"]), cor_lucro, "receitas − despesas")

    # ====================================================
    # ÚLTIMAS VENDAS
    # ====================================================

    sec3 = tk.Frame(corpo, bg=COR_BG)
    sec3.pack(fill="x", padx=35, pady=(28, 0))

    cab3 = tk.Frame(sec3, bg=COR_BG)
    cab3.pack(fill="x", pady=(0, 12))

    tk.Label(cab3, text="Últimas Vendas",
             font=("Segoe UI", 13, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(side="left")

    tk.Label(cab3, text=f"{len(vendas)} venda(s) no total",
             font=("Segoe UI", 9),
             bg=COR_BG, fg=COR_SUB).pack(side="right", pady=(4, 0))

    tabela_card = tk.Frame(sec3, bg=COR_CARD, bd=1, relief="solid")
    tabela_card.pack(fill="x")
    tk.Frame(tabela_card, bg="#059669", height=3).pack(fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dash.Treeview",
                    background=COR_CARD, foreground=COR_TEXTO,
                    rowheight=34, fieldbackground=COR_CARD,
                    font=("Segoe UI", 10), borderwidth=0)
    style.configure("Dash.Treeview.Heading",
                    background="#1E293B", foreground="#94A3B8",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Dash.Treeview",
              background=[("selected", "#DBEAFE")],
              foreground=[("selected", "#2563EB")])

    cols = ("data", "veiculo", "cliente", "valor", "modalidade")
    tree = ttk.Treeview(tabela_card, columns=cols, show="headings",
                        style="Dash.Treeview", height=6)

    cfg = {
        "data":       ("Data",       100),
        "veiculo":    ("Veículo",    220),
        "cliente":    ("Cliente",    180),
        "valor":      ("Valor",      130),
        "modalidade": ("Modalidade", 120),
    }

    for col, (titulo, larg) in cfg.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=larg, anchor="center")

    tree.tag_configure("par",   background=COR_CARD)
    tree.tag_configure("impar", background="#F8FAFC")

    ultimas = vendas[:10]
    for i, v in enumerate(ultimas):
        tag = "par" if i % 2 == 0 else "impar"
        tree.insert("", tk.END, tags=(tag,), values=(
            v.get("data_venda", ""),
            f"{v.get('marca','')} {v.get('modelo','')} {v.get('ano','')}",
            v.get("cliente_nome", ""),
            formatar_moeda(v.get("valor_venda", 0)),
            v.get("modalidade", "")
        ))

    if not ultimas:
        tree.insert("", tk.END, values=("—", "Nenhuma venda registrada", "—", "—", "—"))

    tree.pack(fill="x", padx=10, pady=10)

    # ====================================================
    # PRÓXIMOS AGENDAMENTOS
    # ====================================================

    sec4 = tk.Frame(corpo, bg=COR_BG)
    sec4.pack(fill="x", padx=35, pady=(24, 30))

    tk.Label(sec4, text="Próximos Agendamentos",
             font=("Segoe UI", 13, "bold"),
             bg=COR_BG, fg=COR_TEXTO).pack(anchor="w", pady=(0, 12))

    ag_card = tk.Frame(sec4, bg=COR_CARD, bd=1, relief="solid")
    ag_card.pack(fill="x")
    tk.Frame(ag_card, bg="#7C3AED", height=3).pack(fill="x")

    hoje = datetime.now().date()
    proximos = []
    for a in agendamentos:
        try:
            data_ag = datetime.strptime(a["data"], "%d/%m/%Y").date()
            if data_ag >= hoje:
                proximos.append(a)
        except Exception:
            pass

    proximos = proximos[:8]

    if not proximos:
        tk.Label(ag_card, text="Nenhum agendamento futuro registrado.",
                 font=("Segoe UI", 10), bg=COR_CARD, fg=COR_SUB,
                 pady=20).pack()
    else:
        for i, a in enumerate(proximos):
            cor_linha = COR_CARD if i % 2 == 0 else "#F8FAFC"
            linha = tk.Frame(ag_card, bg=cor_linha)
            linha.pack(fill="x", padx=15, pady=4)

            tk.Label(linha, text=f"📆  {a.get('data','')}  {a.get('hora','')}",
                     font=("Segoe UI", 10, "bold"),
                     bg=cor_linha, fg="#7C3AED").pack(side="left", padx=(0, 20))

            tk.Label(linha, text=a.get("cliente", ""),
                     font=("Segoe UI", 10),
                     bg=cor_linha, fg=COR_TEXTO).pack(side="left", padx=(0, 20))

            tipo_cor = "#059669" if a.get("tipo") == "Visita" else "#2563EB"
            tk.Label(linha, text=a.get("tipo", ""),
                     font=("Segoe UI", 9, "bold"),
                     bg=tipo_cor, fg="white",
                     padx=8, pady=2).pack(side="left")

    # Bind scroll nos filhos
    corpo.after(100, lambda: _scroll_bind(canvas, corpo))