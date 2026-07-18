#========================================================================
# vendas.py - Sistema de Vendas com Simulador de Financiamento
#========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    listar_veiculos,
    listar_clientes,
    registrar_venda,
    listar_vendas
)

COR_BG = "#F1F5F9"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#0F172A"
COR_VERDE = "#059669"
COR_AZUL = "#2563EB"
COR_VERMELHO = "#DC2626"
COR_AMARELO = "#FBBF24"


# ====================================================
# UTILITÁRIOS
# ====================================================

def valor_para_float(valor_str):
    """
    Converte qualquer formato de valor para float.
    Trata: '200 000', '200.000', '200.000,00', '200000', '200,00'
    """
    try:
        s = str(valor_str).strip()
        # Remove espaços (separador de milhar em alguns locais)
        s = s.replace(" ", "")
        # Se tem vírgula E ponto: ponto é milhar, vírgula é decimal
        if "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".")
        # Se só tem vírgula: pode ser decimal (1.500,00) ou milhar (1,500)
        elif "," in s:
            # Se tem mais de 2 dígitos após a vírgula, é milhar
            partes = s.split(",")
            if len(partes[-1]) != 2:
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
        # Se só tem ponto: pode ser milhar (200.000) ou decimal (200.50)
        elif "." in s:
            partes = s.split(".")
            if len(partes[-1]) != 2:
                s = s.replace(".", "")
        return float(s)
    except Exception:
        return 0.0


def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def calcular_price(valor_financiado, taxa_mensal, parcelas):
    """Tabela Price (juros compostos)"""
    if taxa_mensal == 0:
        return valor_financiado / parcelas
    i = taxa_mensal / 100
    fator = (i * (1 + i) ** parcelas) / ((1 + i) ** parcelas - 1)
    return valor_financiado * fator


# ====================================================
# TELA PRINCIPAL DE VENDAS
# ====================================================

def mostrar_vendas(parent):

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
        text="Sistema de Vendas",
        font=("Segoe UI", 24, "bold"),
        bg="#0F172A",
        fg=COR_AMARELO
    ).pack(anchor="w", padx=30, pady=20)

    # ====================================================
    # ABAS
    # ====================================================

    abas = ttk.Notebook(frame)
    abas.pack(fill="both", expand=True, padx=30, pady=20)

    aba_nova = tk.Frame(abas, bg=COR_BG)
    aba_historico = tk.Frame(abas, bg=COR_BG)

    abas.add(aba_nova, text="  Nova Venda  ")
    abas.add(aba_historico, text="  Histórico de Vendas  ")

    _montar_nova_venda(aba_nova, abas, aba_historico)
    _montar_historico(aba_historico)


# ====================================================
# ABA: NOVA VENDA
# ====================================================

def _montar_nova_venda(parent, abas, aba_historico):

    canvas = tk.Canvas(parent, bg=COR_BG, highlightthickness=0)
    scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)

    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    conteudo = tk.Frame(canvas, bg=COR_BG)
    janela_canvas = canvas.create_window((0, 0), window=conteudo, anchor="nw")

    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_largura(event):
        canvas.itemconfig(janela_canvas, width=event.width)

    conteudo.bind("<Configure>", ajustar_scroll)
    canvas.bind("<Configure>", ajustar_largura)

    # ====================================================
    # SEÇÃO 1: VEÍCULO
    # ====================================================

    sec_veiculo = _secao(conteudo, "1. Selecionar Veículo")

    veiculos_disponiveis = listar_veiculos(status="disponivel")

    veiculo_selecionado = {"dados": None, "valor_tabela": 0.0}

    if not veiculos_disponiveis:
        tk.Label(
            sec_veiculo,
            text="Nenhum veículo disponível no estoque.",
            font=("Segoe UI", 11),
            bg=COR_CARD,
            fg=COR_VERMELHO
        ).pack(padx=20, pady=10)
    else:
        tk.Label(
            sec_veiculo,
            text="Veículos disponíveis (clique para selecionar)",
            font=("Segoe UI", 10, "bold"),
            bg=COR_CARD,
            fg="#64748B"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        lista_veiculos = tk.Listbox(
            sec_veiculo,
            font=("Consolas", 11),
            height=6,
            bg="#F8FAFC",
            fg=COR_TEXTO,
            bd=0,
            highlightthickness=1,
            highlightcolor="#2563EB",
            selectbackground=COR_AZUL,
            selectforeground="white"
        )
        lista_veiculos.pack(fill="x", padx=20, pady=(0, 15))

        for v in veiculos_disponiveis:
            val = valor_para_float(v["valor"])
            lista_veiculos.insert(
                tk.END,
                f"{v['marca']} {v['modelo']} {v['ano']}  |  "
                f"Placa: {v['placa']}  |  "
                f"Cor: {v['cor']}  |  "
                f"{v['km']} KM  |  "
                f"Valor Tabela: {formatar_moeda(val)}"
            )

        lbl_veiculo_sel = tk.Label(
            sec_veiculo,
            text="Nenhum veículo selecionado",
            font=("Segoe UI", 10, "bold"),
            bg="#FEF3C7",
            fg="#92400E",
            pady=8,
            padx=15
        )
        lbl_veiculo_sel.pack(fill="x", padx=20, pady=(0, 15))

        def ao_selecionar_veiculo(event):
            sel = lista_veiculos.curselection()
            if not sel:
                return
            v = veiculos_disponiveis[sel[0]]
            veiculo_selecionado["dados"] = v
            val = valor_para_float(v["valor"])
            veiculo_selecionado["valor_tabela"] = val
            lbl_veiculo_sel.config(
                text=f"✔  {v['marca']} {v['modelo']} {v['ano']} — "
                     f"{formatar_moeda(val)}",
                bg="#D1FAE5",
                fg="#065F46"
            )
            entrada_valor_venda.delete(0, tk.END)
            entrada_valor_venda.insert(
                0,
                f"{val:.2f}".replace(".", ",")
            )

        lista_veiculos.bind("<<ListboxSelect>>", ao_selecionar_veiculo)

    # ====================================================
    # SEÇÃO 2: CLIENTE
    # ====================================================

    sec_cliente = _secao(conteudo, "2. Selecionar Cliente")

    clientes = listar_clientes()

    cliente_selecionado = {"dados": None}

    tk.Label(
        sec_cliente,
        text="Buscar cliente pelo nome ou CPF",
        font=("Segoe UI", 10, "bold"),
        bg=COR_CARD,
        fg="#64748B"
    ).pack(anchor="w", padx=20, pady=(10, 5))

    linha_busca = tk.Frame(sec_cliente, bg=COR_CARD)
    linha_busca.pack(fill="x", padx=20, pady=(0, 8))

    entrada_busca_cli = tk.Entry(
        linha_busca,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1,
        width=40
    )
    entrada_busca_cli.pack(side="left", ipady=6, padx=(0, 8))

    lista_clientes_box = tk.Listbox(
        sec_cliente,
        font=("Consolas", 10),
        height=5,
        bg="#F8FAFC",
        fg=COR_TEXTO,
        bd=0,
        highlightthickness=1,
        highlightcolor="#2563EB",
        selectbackground=COR_AZUL,
        selectforeground="white"
    )
    lista_clientes_box.pack(fill="x", padx=20, pady=(0, 8))

    resultados_clientes = []

    def buscar_cliente(*args):
        lista_clientes_box.delete(0, tk.END)
        resultados_clientes.clear()
        termo = entrada_busca_cli.get().lower().strip()
        for c in clientes:
            if termo in c.get("nome", "").lower() or termo in c.get("cpf", "").lower():
                lista_clientes_box.insert(
                    tk.END,
                    f"{c['nome']}  |  CPF: {c['cpf']}  |  Tel: {c['telefone']}"
                )
                resultados_clientes.append(c)

    entrada_busca_cli.bind("<KeyRelease>", buscar_cliente)

    tk.Button(
        linha_busca,
        text="Buscar",
        bg=COR_AZUL,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=16,
        pady=6,
        command=buscar_cliente
    ).pack(side="left")

    lbl_cliente_sel = tk.Label(
        sec_cliente,
        text="Nenhum cliente selecionado",
        font=("Segoe UI", 10, "bold"),
        bg="#FEF3C7",
        fg="#92400E",
        pady=8,
        padx=15
    )
    lbl_cliente_sel.pack(fill="x", padx=20, pady=(0, 15))

    def ao_selecionar_cliente(event):
        sel = lista_clientes_box.curselection()
        if not sel:
            return
        c = resultados_clientes[sel[0]]
        cliente_selecionado["dados"] = c
        lbl_cliente_sel.config(
            text=f"✔  {c['nome']}  —  CPF: {c['cpf']}",
            bg="#D1FAE5",
            fg="#065F46"
        )

    lista_clientes_box.bind("<<ListboxSelect>>", ao_selecionar_cliente)

    buscar_cliente()

    # ====================================================
    # SEÇÃO 3: CONDIÇÕES DE VENDA
    # ====================================================

    sec_condicoes = _secao(conteudo, "3. Condições de Venda")

    form = tk.Frame(sec_condicoes, bg=COR_CARD)
    form.pack(padx=20, pady=10, anchor="w")

    def label(texto, row):
        tk.Label(
            form,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg=COR_CARD,
            fg=COR_TEXTO
        ).grid(row=row, column=0, sticky="w", pady=8, padx=(0, 20))

    label("Valor de Venda (R$)", 0)
    entrada_valor_venda = tk.Entry(
        form, width=22, font=("Segoe UI", 11),
        relief="solid", bd=1
    )
    entrada_valor_venda.grid(row=0, column=1, ipady=7, pady=8, padx=(0, 30))

    label("Valor de Entrada (R$)", 1)
    entrada_entrada = tk.Entry(
        form, width=22, font=("Segoe UI", 11),
        relief="solid", bd=1
    )
    entrada_entrada.insert(0, "0,00")
    entrada_entrada.grid(row=1, column=1, ipady=7, pady=8, padx=(0, 30))

    label("Modalidade", 2)
    modalidade = ttk.Combobox(
        form,
        values=["À Vista", "Financiamento", "Consórcio"],
        state="readonly",
        width=20,
        font=("Segoe UI", 10)
    )
    modalidade.grid(row=2, column=1, pady=8, ipady=4, padx=(0, 30))
    modalidade.set("À Vista")

    # ====================================================
    # SIMULADOR DE FINANCIAMENTO
    # ====================================================

    frame_fin = tk.Frame(sec_condicoes, bg="#F0F9FF", bd=1, relief="solid")

    tk.Label(
        frame_fin,
        text="Simulador de Financiamento",
        font=("Segoe UI", 13, "bold"),
        bg="#F0F9FF",
        fg="#0369A1"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    form_fin = tk.Frame(frame_fin, bg="#F0F9FF")
    form_fin.pack(padx=20, pady=(0, 10), anchor="w")

    def lf(texto, row):
        tk.Label(
            form_fin,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg="#F0F9FF",
            fg=COR_TEXTO
        ).grid(row=row, column=0, sticky="w", pady=6, padx=(0, 20))

    lf("Nº de Parcelas", 0)
    parcelas_combo = ttk.Combobox(
        form_fin,
        values=["12", "24", "36", "48", "60", "72", "84"],
        state="readonly",
        width=10,
        font=("Segoe UI", 10)
    )
    parcelas_combo.grid(row=0, column=1, pady=6, ipady=4)
    parcelas_combo.set("36")

    lf("Taxa de Juros ao Mês (%)", 1)
    entrada_taxa = tk.Entry(
        form_fin, width=12, font=("Segoe UI", 10),
        relief="solid", bd=1
    )
    entrada_taxa.insert(0, "1,49")
    entrada_taxa.grid(row=1, column=1, ipady=6, pady=6)

    resultado_fin = tk.Frame(frame_fin, bg="#E0F2FE", bd=1, relief="solid")

    lbl_parcela = tk.Label(
        resultado_fin,
        text="",
        font=("Segoe UI", 14, "bold"),
        bg="#E0F2FE",
        fg="#0369A1"
    )
    lbl_parcela.pack(pady=8, padx=20)

    lbl_total_fin = tk.Label(
        resultado_fin,
        text="",
        font=("Segoe UI", 10),
        bg="#E0F2FE",
        fg="#475569"
    )
    lbl_total_fin.pack(pady=(0, 8), padx=20)

    valor_parcela_calculado = {"valor": 0.0}

    def simular():
        try:
            valor_venda = valor_para_float(entrada_valor_venda.get())
            valor_entrada = valor_para_float(entrada_entrada.get())
            taxa = valor_para_float(entrada_taxa.get())
            n = int(parcelas_combo.get())

            financiado = valor_venda - valor_entrada

            if financiado <= 0:
                messagebox.showwarning(
                    "Aviso",
                    "O valor de entrada é maior ou igual ao valor de venda."
                )
                return

            parcela = calcular_price(financiado, taxa, n)
            total = parcela * n
            juros_total = total - financiado

            valor_parcela_calculado["valor"] = parcela

            lbl_parcela.config(
                text=f"{n}x de {formatar_moeda(parcela)}"
            )
            lbl_total_fin.config(
                text=(
                    f"Valor financiado: {formatar_moeda(financiado)}   |   "
                    f"Total: {formatar_moeda(total)}   |   "
                    f"Juros: {formatar_moeda(juros_total)}"
                )
            )

            resultado_fin.pack(fill="x", padx=20, pady=(0, 15))

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Verifique os valores digitados.\n{e}"
            )

    tk.Button(
        form_fin,
        text="Simular Financiamento",
        bg="#0369A1",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=simular
    ).grid(row=2, column=0, columnspan=2, pady=15, sticky="w")

    def ao_mudar_modalidade(event):
        if modalidade.get() == "Financiamento":
            frame_fin.pack(fill="x", padx=20, pady=(0, 15))
        else:
            frame_fin.pack_forget()
            resultado_fin.pack_forget()
            valor_parcela_calculado["valor"] = 0.0

    modalidade.bind("<<ComboboxSelected>>", ao_mudar_modalidade)

    # ====================================================
    # SEÇÃO 4: OBSERVAÇÕES
    # ====================================================

    sec_obs = _secao(conteudo, "4. Observações")

    entrada_obs = tk.Text(
        sec_obs,
        height=4,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )
    entrada_obs.pack(fill="x", padx=20, pady=15)

    # ====================================================
    # BOTÃO FINALIZAR VENDA
    # ====================================================

    btn_frame = tk.Frame(conteudo, bg=COR_BG)
    btn_frame.pack(pady=25)

    def finalizar_venda():

        if not veiculo_selecionado.get("dados"):
            messagebox.showwarning("Aviso", "Selecione um veículo.")
            return

        if not cliente_selecionado.get("dados"):
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return

        valor_venda = valor_para_float(entrada_valor_venda.get())

        if valor_venda <= 0:
            messagebox.showerror("Erro", "Valor de venda inválido.")
            return

        valor_entrada = valor_para_float(entrada_entrada.get())

        mod = modalidade.get()

        if not mod:
            messagebox.showwarning("Aviso", "Selecione a modalidade.")
            return

        parcelas = None
        taxa_juros = None
        valor_parcela = None

        if mod == "Financiamento":
            try:
                parcelas = int(parcelas_combo.get())
                taxa_juros = valor_para_float(entrada_taxa.get())
                valor_parcela = valor_parcela_calculado["valor"]
                if valor_parcela == 0.0:
                    messagebox.showwarning(
                        "Aviso",
                        "Clique em 'Simular Financiamento' antes de finalizar."
                    )
                    return
            except Exception:
                messagebox.showerror("Erro", "Dados do financiamento inválidos.")
                return

        confirmar = messagebox.askyesno(
            "Confirmar Venda",
            f"Confirmar venda?\n\n"
            f"Veículo: {veiculo_selecionado['dados']['marca']} "
            f"{veiculo_selecionado['dados']['modelo']}\n"
            f"Cliente: {cliente_selecionado['dados']['nome']}\n"
            f"Valor: {formatar_moeda(valor_venda)}\n"
            f"Modalidade: {mod}"
        )

        if not confirmar:
            return

        registrar_venda({
            "id_veiculo": veiculo_selecionado["dados"]["id"],
            "id_cliente": cliente_selecionado["dados"]["id"],
            "valor_venda": valor_venda,
            "valor_entrada": valor_entrada,
            "modalidade": mod,
            "parcelas": parcelas,
            "taxa_juros": taxa_juros,
            "valor_parcela": valor_parcela,
            "observacoes": entrada_obs.get("1.0", tk.END).strip()
        })

        messagebox.showinfo(
            "Venda Realizada!",
            f"Venda registrada com sucesso!\n\n"
            f"{veiculo_selecionado['dados']['marca']} "
            f"{veiculo_selecionado['dados']['modelo']} vendido para "
            f"{cliente_selecionado['dados']['nome']}."
        )

        _montar_historico(aba_historico)
        abas.select(aba_historico)

    tk.Button(
        btn_frame,
        text="✔  Finalizar Venda",
        bg=COR_VERDE,
        fg="white",
        font=("Segoe UI", 13, "bold"),
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=14,
        command=finalizar_venda
    ).pack()


# ====================================================
# ABA: HISTÓRICO
# ====================================================

def _montar_historico(parent):

    for w in parent.winfo_children():
        w.destroy()

    card = tk.Frame(parent, bg=COR_CARD, bd=1, relief="solid")
    card.pack(fill="both", expand=True, padx=10, pady=15)

    tk.Label(
        card,
        text="Histórico de Vendas",
        font=("Segoe UI", 16, "bold"),
        bg=COR_CARD,
        fg=COR_TEXTO
    ).pack(anchor="w", padx=20, pady=15)

    colunas = ("data", "veiculo", "cliente", "valor", "modalidade", "parcelas")

    tree = ttk.Treeview(
        card,
        columns=colunas,
        show="headings",
        height=18
    )

    cabecalhos = {
        "data":       ("Data",        100),
        "veiculo":    ("Veículo",     220),
        "cliente":    ("Cliente",     180),
        "valor":      ("Valor Venda", 130),
        "modalidade": ("Modalidade",  120),
        "parcelas":   ("Parcelas",    150)
    }

    for col, (titulo, largura) in cabecalhos.items():
        tree.heading(col, text=titulo)
        tree.column(col, width=largura, anchor="center")

    scroll_y = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    scroll_y.pack(side="right", fill="y", padx=(0, 10))
    tree.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    vendas = listar_vendas()

    total_vendas = 0.0

    for v in vendas:

        total_vendas += v["valor_venda"]

        parcela_txt = (
            f"{v['parcelas']}x {formatar_moeda(v['valor_parcela'])}"
            if v["modalidade"] == "Financiamento" and v["parcelas"]
            else "-"
        )

        tree.insert("", tk.END, values=(
            v["data_venda"],
            f"{v['marca']} {v['modelo']} {v['ano']}",
            v["cliente_nome"],
            formatar_moeda(v["valor_venda"]),
            v["modalidade"],
            parcela_txt
        ))

    rodape = tk.Frame(card, bg="#F0FDF4", bd=1, relief="solid")
    rodape.pack(fill="x", padx=20, pady=(0, 15))

    tk.Label(
        rodape,
        text=f"Total de vendas: {len(vendas)}   |   "
             f"Receita total: {formatar_moeda(total_vendas)}",
        font=("Segoe UI", 11, "bold"),
        bg="#F0FDF4",
        fg="#065F46",
        pady=10
    ).pack()


# ====================================================
# HELPER: CRIAR SEÇÃO
# ====================================================

def _secao(parent, titulo):

    frame = tk.Frame(parent, bg=COR_CARD, bd=1, relief="solid")
    frame.pack(fill="x", padx=10, pady=(0, 15))

    tk.Label(
        frame,
        text=titulo,
        font=("Segoe UI", 13, "bold"),
        bg="#0F172A",
        fg=COR_AMARELO,
        pady=10,
        padx=20,
        anchor="w"
    ).pack(fill="x")

    return frame