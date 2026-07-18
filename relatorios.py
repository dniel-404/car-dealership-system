#========================================================================
# relatorios.py - Relatório Unificado: Clientes, Frota e Vendas
# pip install reportlab
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from database import (
    listar_clientes,
    listar_veiculos,
    listar_vendas,
    resumo_financeiro
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_RELATORIOS = os.path.join(BASE_DIR, "relatorios")
os.makedirs(PASTA_RELATORIOS, exist_ok=True)

COR_BG = "#F1F5F9"
COR_CARD = "#FFFFFF"

AZUL = colors.HexColor("#2563EB")
AZUL_CLARO = colors.HexColor("#DBEAFE")
VERDE = colors.HexColor("#059669")
VERDE_CLARO = colors.HexColor("#D1FAE5")
VERMELHO = colors.HexColor("#DC2626")
CINZA = colors.HexColor("#F8FAFC")
CINZA_BORDA = colors.HexColor("#CBD5E1")
TEXTO = colors.HexColor("#0F172A")


# ====================================================
# UTILITÁRIO
# ====================================================

def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


# ====================================================
# GERAÇÃO DO PDF
# ====================================================

def gerar_pdf(secoes):
    """
    secoes: lista de strings com as seções a incluir
    Ex: ["clientes", "frota", "vendas"]
    """

    clientes = listar_clientes()
    veiculos = listar_veiculos()
    vendas = listar_vendas()
    financeiro = resumo_financeiro()

    agora = datetime.now()
    nome_arquivo = f"relatorio_{agora.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    caminho = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    doc = SimpleDocTemplate(
        caminho,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    estilos = getSampleStyleSheet()

    estilo_titulo_doc = ParagraphStyle(
        "TituloDoc",
        parent=estilos["Title"],
        fontSize=20,
        textColor=TEXTO,
        spaceAfter=4,
        alignment=TA_CENTER
    )

    estilo_subtitulo_doc = ParagraphStyle(
        "SubtituloDoc",
        parent=estilos["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=16,
        alignment=TA_CENTER
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=estilos["Heading1"],
        fontSize=13,
        textColor=colors.white,
        backColor=AZUL,
        spaceBefore=18,
        spaceAfter=8,
        leftIndent=-4,
        rightIndent=-4,
        leading=20
    )

    estilo_resumo = ParagraphStyle(
        "Resumo",
        parent=estilos["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8
    )

    elementos = []

    # ====================================================
    # CABEÇALHO
    # ====================================================

    elementos.append(Paragraph("SysCar ERP", estilo_titulo_doc))
    elementos.append(Paragraph(
        f"Relatório Gerencial — Gerado em {agora.strftime('%d/%m/%Y às %H:%M')}",
        estilo_subtitulo_doc
    ))
    elementos.append(HRFlowable(width="100%", thickness=2, color=AZUL))
    elementos.append(Spacer(1, 16))

    # ====================================================
    # RESUMO FINANCEIRO (sempre aparece)
    # ====================================================

    elementos.append(Paragraph("  Resumo Financeiro", estilo_secao))
    elementos.append(Spacer(1, 6))

    cor_lucro = VERDE if financeiro["lucro"] >= 0 else VERMELHO

    dados_fin = [
        ["Receitas (Vendas)", "Despesas (Compras)", "Lucro Líquido"],
        [
            formatar_moeda(financeiro["receitas"]),
            formatar_moeda(financeiro["despesas"]),
            formatar_moeda(financeiro["lucro"])
        ]
    ]

    tabela_fin = Table(dados_fin, colWidths=[5.5 * cm, 5.5 * cm, 5.5 * cm])
    tabela_fin.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  AZUL),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  10),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",     (0, 1), (-1, 1),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 1), (-1, 1),  12),
        ("TEXTCOLOR",    (0, 1), (0, 1),   VERDE),
        ("TEXTCOLOR",    (1, 1), (1, 1),   VERMELHO),
        ("TEXTCOLOR",    (2, 1), (2, 1),   cor_lucro),
        ("BACKGROUND",   (0, 1), (-1, 1),  CINZA),
        ("GRID",         (0, 0), (-1, -1), 0.5, CINZA_BORDA),
        ("ROWBACKGROUNDS", (0, 1), (-1, 1), [CINZA]),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
    ]))

    elementos.append(tabela_fin)
    elementos.append(Spacer(1, 16))

    # ====================================================
    # SEÇÃO CLIENTES
    # ====================================================

    if "clientes" in secoes:

        elementos.append(Paragraph(f"  Clientes Cadastrados ({len(clientes)})", estilo_secao))
        elementos.append(Spacer(1, 6))

        if not clientes:
            elementos.append(Paragraph("Nenhum cliente cadastrado.", estilo_resumo))
        else:
            cabecalho_cli = [["Nome", "CPF", "Telefone", "Cidade / UF", "Email"]]
            linhas_cli = []

            for c in clientes:
                cidade_uf = f"{c.get('cidade', '')} / {c.get('uf', '')}"
                linhas_cli.append([
                    c.get("nome", ""),
                    c.get("cpf", ""),
                    c.get("telefone", ""),
                    cidade_uf,
                    c.get("email", "")
                ])

            dados_cli = cabecalho_cli + linhas_cli

            tabela_cli = Table(
                dados_cli,
                colWidths=[4.5*cm, 3*cm, 3*cm, 3.5*cm, 4*cm]
            )
            tabela_cli.setStyle(TableStyle([
                ("BACKGROUND",     (0, 0), (-1, 0),  AZUL),
                ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
                ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",       (0, 0), (-1, -1), 8),
                ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
                ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
                ("GRID",           (0, 0), (-1, -1), 0.4, CINZA_BORDA),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA]),
                ("TOPPADDING",     (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
            ]))

            elementos.append(tabela_cli)

        elementos.append(Spacer(1, 16))

    # ====================================================
    # SEÇÃO FROTA
    # ====================================================

    if "frota" in secoes:

        disponiveis = [v for v in veiculos if v.get("status") in ("disponivel", None, "")]
        vendidos = [v for v in veiculos if v.get("status") == "vendido"]

        elementos.append(Paragraph(
            f"  Frota de Veículos ({len(veiculos)} total — "
            f"{len(disponiveis)} disponíveis / {len(vendidos)} vendidos)",
            estilo_secao
        ))
        elementos.append(Spacer(1, 6))

        if not veiculos:
            elementos.append(Paragraph("Nenhum veículo cadastrado.", estilo_resumo))
        else:
            cabecalho_frota = [["Marca", "Modelo", "Ano", "Placa", "Cor", "KM", "Valor", "Status"]]
            linhas_frota = []

            for v in veiculos:
                status = v.get("status") or "disponivel"
                linhas_frota.append([
                    v.get("marca", ""),
                    v.get("modelo", ""),
                    v.get("ano", ""),
                    v.get("placa", ""),
                    v.get("cor", ""),
                    v.get("km", ""),
                    v.get("valor", ""),
                    status.capitalize()
                ])

            dados_frota = cabecalho_frota + linhas_frota

            tabela_frota = Table(
                dados_frota,
                colWidths=[2.3*cm, 3*cm, 1.5*cm, 2.2*cm, 2*cm, 2*cm, 2.5*cm, 2.5*cm]
            )

            estilo_frota = [
                ("BACKGROUND",     (0, 0), (-1, 0),  VERDE),
                ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
                ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",       (0, 0), (-1, -1), 8),
                ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
                ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
                ("GRID",           (0, 0), (-1, -1), 0.4, CINZA_BORDA),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA]),
                ("TOPPADDING",     (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
            ]

            # Colorir linha de vendidos em vermelho claro
            for i, v in enumerate(veiculos, start=1):
                if v.get("status") == "vendido":
                    estilo_frota.append(
                        ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#FEE2E2"))
                    )

            tabela_frota.setStyle(TableStyle(estilo_frota))
            elementos.append(tabela_frota)

        elementos.append(Spacer(1, 16))

    # ====================================================
    # SEÇÃO VENDAS
    # ====================================================

    if "vendas" in secoes:

        total_receita = sum(v["valor_venda"] for v in vendas)

        elementos.append(Paragraph(
            f"  Histórico de Vendas ({len(vendas)} vendas — "
            f"Receita total: {formatar_moeda(total_receita)})",
            estilo_secao
        ))
        elementos.append(Spacer(1, 6))

        if not vendas:
            elementos.append(Paragraph("Nenhuma venda registrada.", estilo_resumo))
        else:
            cabecalho_vendas = [["Data", "Veículo", "Cliente", "Valor Venda", "Modalidade", "Parcelas"]]
            linhas_vendas = []

            for v in vendas:
                parcela_txt = (
                    f"{v['parcelas']}x {formatar_moeda(v['valor_parcela'])}"
                    if v.get("modalidade") == "Financiamento" and v.get("parcelas")
                    else "-"
                )
                linhas_vendas.append([
                    v.get("data_venda", ""),
                    f"{v.get('marca','')} {v.get('modelo','')} {v.get('ano','')}",
                    v.get("cliente_nome", ""),
                    formatar_moeda(v.get("valor_venda", 0)),
                    v.get("modalidade", ""),
                    parcela_txt
                ])

            dados_vendas = cabecalho_vendas + linhas_vendas

            tabela_vendas = Table(
                dados_vendas,
                colWidths=[2.2*cm, 4*cm, 3.5*cm, 2.8*cm, 2.5*cm, 3*cm]
            )
            tabela_vendas.setStyle(TableStyle([
                ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#7C3AED")),
                ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
                ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",       (0, 0), (-1, -1), 8),
                ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
                ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
                ("GRID",           (0, 0), (-1, -1), 0.4, CINZA_BORDA),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA]),
                ("TOPPADDING",     (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
            ]))

            elementos.append(tabela_vendas)

        elementos.append(Spacer(1, 16))

    # ====================================================
    # RODAPÉ DO DOC
    # ====================================================

    elementos.append(HRFlowable(width="100%", thickness=1, color=CINZA_BORDA))
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(
        f"© SysCar ERP — Relatório gerado automaticamente em {agora.strftime('%d/%m/%Y às %H:%M')}",
        ParagraphStyle(
            "Rodape",
            parent=estilos["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#94A3B8"),
            alignment=TA_CENTER
        )
    ))

    doc.build(elementos)

    return caminho


# ====================================================
# TELA
# ====================================================

def mostrar_relatorio(parent):

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
        text="Relatórios",
        font=("Segoe UI", 24, "bold"),
        bg="#0F172A",
        fg="#FBBF24"
    ).pack(anchor="w", padx=30, pady=20)

    # ====================================================
    # CARD
    # ====================================================

    card = tk.Frame(frame, bg=COR_CARD, bd=1, relief="solid")
    card.pack(padx=30, pady=30, fill="both", expand=True)

    conteudo = tk.Frame(card, bg=COR_CARD)
    conteudo.pack(pady=50)

    tk.Label(
        conteudo,
        text="Gerar Relatório PDF",
        font=("Segoe UI", 20, "bold"),
        bg=COR_CARD,
        fg="#0F172A"
    ).pack(pady=(0, 8))

    tk.Label(
        conteudo,
        text="Selecione as seções que deseja incluir no relatório:",
        font=("Segoe UI", 11),
        bg=COR_CARD,
        fg="#475569"
    ).pack(pady=(0, 25))

    # ====================================================
    # CHECKBOXES
    # ====================================================

    checks_frame = tk.Frame(conteudo, bg=COR_CARD)
    checks_frame.pack(pady=(0, 30))

    var_clientes = tk.BooleanVar(value=True)
    var_frota = tk.BooleanVar(value=True)
    var_vendas = tk.BooleanVar(value=True)

    opcoes = [
        (var_clientes, "Clientes",  "#2563EB"),
        (var_frota,    "Frota",     "#059669"),
        (var_vendas,   "Vendas",    "#7C3AED"),
    ]

    for var, texto, cor in opcoes:

        linha = tk.Frame(checks_frame, bg=COR_CARD)
        linha.pack(anchor="w", pady=6)

        barra = tk.Frame(linha, bg=cor, width=4, height=28)
        barra.pack(side="left", padx=(0, 12))
        barra.pack_propagate(False)

        tk.Checkbutton(
            linha,
            text=texto,
            variable=var,
            font=("Segoe UI", 12),
            bg=COR_CARD,
            fg="#0F172A",
            activebackground=COR_CARD,
            cursor="hand2"
        ).pack(side="left")

    tk.Label(
        conteudo,
        text="O resumo financeiro é sempre incluído.",
        font=("Segoe UI", 9),
        bg=COR_CARD,
        fg="#94A3B8"
    ).pack(pady=(0, 25))

    # ====================================================
    # BOTÃO GERAR
    # ====================================================

    def gerar():

        secoes = []

        if var_clientes.get():
            secoes.append("clientes")

        if var_frota.get():
            secoes.append("frota")

        if var_vendas.get():
            secoes.append("vendas")

        try:
            caminho = gerar_pdf(secoes)
            messagebox.showinfo(
                "PDF Gerado!",
                f"Relatório gerado com sucesso!\n\n{caminho}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erro ao gerar PDF",
                f"Ocorreu um erro:\n{e}\n\n"
                "Verifique se o reportlab está instalado:\n"
                "pip install reportlab"
            )

    tk.Button(
        conteudo,
        text="Gerar PDF",
        bg="#2563EB",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=14,
        command=gerar
    ).pack()