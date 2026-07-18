#========================================================================
# CadCli.py - Cadastro de Clientes
#========================================================================

import tkinter as tk
from tkinter import messagebox
import os

from database import (
    salvar_cliente,
    atualizar_cliente
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")
os.makedirs(PASTA_DADOS, exist_ok=True)

# Paleta
COR_BG       = "#F8FAFC"
COR_CARD     = "#FFFFFF"
COR_TOPO     = "#0F172A"
COR_DESTAQUE = "#FBBF24"
COR_PRIMARIA = "#2563EB"
COR_TEXTO    = "#1E293B"
COR_SUBTEXTO = "#64748B"
COR_BORDA    = "#E2E8F0"
COR_INPUT    = "#F1F5F9"
COR_HOVER    = "#1D4ED8"
COR_CANCEL   = "#64748B"

MAPA_CAMPOS = {
    "Nome":     "nome",
    "CPF":      "cpf",
    "Telefone": "telefone",
    "Email":    "email",
    "Endereço": "endereco",
    "Número":   "numero",
    "Bairro":   "bairro",
    "Cidade":   "cidade",
    "UF":       "uf",
    "CEP":      "cep",
}

CAMPOS_TEXTO     = {"Nome", "Endereço", "Bairro", "Cidade"}
CAMPOS_MAIUSCULO = {"UF"}


# ====================================================
# MASCARAS
# ====================================================

def aplicar_capitalize(entry):
    def evento(e):
        valor = entry.get()
        novo = valor.title()
        if novo != valor:
            pos = entry.index(tk.INSERT)
            entry.delete(0, tk.END)
            entry.insert(0, novo)
            try:
                entry.icursor(pos)
            except Exception:
                pass
    entry.bind("<KeyRelease>", evento)


def aplicar_maiusculo(entry):
    def evento(e):
        valor = entry.get()
        novo = valor.upper()
        if novo != valor:
            pos = entry.index(tk.INSERT)
            entry.delete(0, tk.END)
            entry.insert(0, novo)
            try:
                entry.icursor(pos)
            except Exception:
                pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_cpf(entry):
    def evento(e):
        if e.keysym in ("BackSpace","Delete","Left","Right","Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())[:11]
        f = valor
        if len(valor) > 3:
            f = valor[:3] + "." + valor[3:]
        if len(valor) > 6:
            f = valor[:3] + "." + valor[3:6] + "." + valor[6:]
        if len(valor) > 9:
            f = valor[:3] + "." + valor[3:6] + "." + valor[6:9] + "-" + valor[9:]
        pos = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, f)
        try:
            entry.icursor(min(pos + 1, len(f)))
        except Exception:
            pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_telefone(entry):
    def evento(e):
        if e.keysym in ("BackSpace","Delete","Left","Right","Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())[:11]
        f = valor
        if len(valor) >= 2:
            f = "(" + valor[:2] + ") " + valor[2:]
        if len(valor) > 7:
            f = "(" + valor[:2] + ") " + valor[2:7] + "-" + valor[7:]
        pos = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, f)
        try:
            entry.icursor(min(pos + 1, len(f)))
        except Exception:
            pass
    entry.bind("<KeyRelease>", evento)


def aplicar_mascara_cep(entry):
    def evento(e):
        if e.keysym in ("BackSpace","Delete","Left","Right","Tab"):
            return
        valor = ''.join(c for c in entry.get() if c.isdigit())[:8]
        f = valor
        if len(valor) > 5:
            f = valor[:5] + "-" + valor[5:]
        pos = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, f)
        try:
            entry.icursor(min(pos, len(f)))
        except Exception:
            pass
    entry.bind("<KeyRelease>", evento)


# ====================================================
# HELPER UI
# ====================================================

def criar_entry(parent, largura=28):
    e = tk.Entry(
        parent,
        width=largura,
        font=("Segoe UI", 10),
        relief="flat",
        bd=0,
        bg=COR_INPUT,
        fg=COR_TEXTO,
        insertbackground=COR_PRIMARIA
    )
    return e


def campo_com_borda(parent, label_texto, largura=28):
    bloco = tk.Frame(parent, bg=COR_CARD)

    tk.Label(
        bloco,
        text=label_texto,
        font=("Segoe UI", 9, "bold"),
        bg=COR_CARD,
        fg=COR_SUBTEXTO
    ).pack(anchor="w", pady=(0, 3))

    borda = tk.Frame(bloco, bg=COR_BORDA, bd=0)
    borda.pack(fill="x")

    inner = tk.Frame(borda, bg=COR_INPUT, padx=10, pady=6)
    inner.pack(fill="x", padx=1, pady=1)

    entry = tk.Entry(
        inner,
        width=largura,
        font=("Segoe UI", 10),
        relief="flat",
        bd=0,
        bg=COR_INPUT,
        fg=COR_TEXTO,
        insertbackground=COR_PRIMARIA
    )
    entry.pack(fill="x")

    def on_focus_in(e):
        borda.config(bg=COR_PRIMARIA)

    def on_focus_out(e):
        borda.config(bg=COR_BORDA)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return bloco, entry


def btn_primario(parent, texto, comando, cor=None):
    c = cor or COR_PRIMARIA
    b = tk.Button(
        parent,
        text=texto,
        font=("Segoe UI", 10, "bold"),
        bg=c,
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=24,
        pady=10,
        bd=0,
        activebackground=COR_HOVER,
        activeforeground="white",
        command=comando
    )
    b.bind("<Enter>", lambda e: b.config(bg=COR_HOVER))
    b.bind("<Leave>", lambda e: b.config(bg=c))
    return b


# ====================================================
# FORMULÁRIO PRINCIPAL
# ====================================================

def mostrar_formulario(parent, dados_cliente=None, indice=None):

    for w in parent.winfo_children():
        w.destroy()

    modo_edicao = indice is not None

    frame = tk.Frame(parent, bg=COR_BG)
    frame.pack(fill="both", expand=True)

    # ====================================================
    # TOPO
    # ====================================================

    topo = tk.Frame(frame, bg=COR_TOPO)
    topo.pack(fill="x")

    topo_inner = tk.Frame(topo, bg=COR_TOPO)
    topo_inner.pack(fill="x", padx=35, pady=22)

    icone = "✎" if modo_edicao else "＋"
    titulo = "Editar Cliente" if modo_edicao else "Novo Cliente"

    tk.Label(
        topo_inner,
        text=f"{icone}  {titulo}",
        font=("Segoe UI", 22, "bold"),
        bg=COR_TOPO,
        fg=COR_DESTAQUE
    ).pack(side="left")

    subtitulo = "Atualize os dados do cliente" if modo_edicao else "Preencha os dados para cadastrar"
    tk.Label(
        topo_inner,
        text=subtitulo,
        font=("Segoe UI", 10),
        bg=COR_TOPO,
        fg="#94A3B8"
    ).pack(side="left", padx=(15, 0), pady=(6, 0))

    # ====================================================
    # ÁREA SCROLLÁVEL
    # ====================================================

    container = tk.Frame(frame, bg=COR_BG)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scroll_frame = tk.Frame(canvas, bg=COR_BG)
    win = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def ajustar(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_largura(e):
        canvas.itemconfig(win, width=e.width)

    scroll_frame.bind("<Configure>", ajustar)
    canvas.bind("<Configure>", ajustar_largura)

    # ====================================================
    # CARD FORMULÁRIO
    # ====================================================

    card = tk.Frame(scroll_frame, bg=COR_CARD, bd=1, relief="solid")
    card.pack(padx=35, pady=30, fill="x")

    # Cabeçalho do card
    cab = tk.Frame(card, bg="#F8FAFC", bd=0)
    cab.pack(fill="x")
    tk.Frame(cab, bg=COR_PRIMARIA, height=3).pack(fill="x")
    tk.Label(
        cab,
        text="Informações do Cliente",
        font=("Segoe UI", 12, "bold"),
        bg="#F8FAFC",
        fg=COR_TEXTO,
        pady=14,
        padx=25
    ).pack(anchor="w")

    tk.Frame(card, bg=COR_BORDA, height=1).pack(fill="x")

    form = tk.Frame(card, bg=COR_CARD)
    form.pack(padx=25, pady=25, fill="x")

    entradas = {}

    def linha(campos_lista, row_frame):
        linha_frame = tk.Frame(row_frame, bg=COR_CARD)
        linha_frame.pack(fill="x", pady=6)
        for label, larg in campos_lista:
            bloco, entry = campo_com_borda(linha_frame, label, larg)
            bloco.pack(side="left", padx=(0, 20), fill="x", expand=True)
            # Mascaras
            if label in CAMPOS_TEXTO:
                aplicar_capitalize(entry)
            elif label in CAMPOS_MAIUSCULO:
                aplicar_maiusculo(entry)
            elif label == "CPF":
                aplicar_mascara_cpf(entry)
            elif label == "Telefone":
                aplicar_mascara_telefone(entry)
            elif label == "CEP":
                aplicar_mascara_cep(entry)
            entradas[label] = entry

    linha([("Nome", 35), ("CPF", 20)], form)
    linha([("Telefone", 20), ("Email", 35)], form)
    linha([("Endereço", 35), ("Número", 10)], form)
    linha([("Bairro", 25), ("Cidade", 25)], form)
    linha([("UF", 5), ("CEP", 15)], form)

    # Observações
    tk.Frame(form, bg=COR_BORDA, height=1).pack(fill="x", pady=(10, 16))

    tk.Label(
        form,
        text="OBSERVAÇÕES",
        font=("Segoe UI", 9, "bold"),
        bg=COR_CARD,
        fg=COR_SUBTEXTO
    ).pack(anchor="w", pady=(0, 4))

    obs_borda = tk.Frame(form, bg=COR_BORDA)
    obs_borda.pack(fill="x")

    obs_inner = tk.Frame(obs_borda, bg=COR_INPUT, padx=10, pady=8)
    obs_inner.pack(fill="x", padx=1, pady=1)

    obs = tk.Text(
        obs_inner,
        height=4,
        font=("Segoe UI", 10),
        relief="flat",
        bd=0,
        bg=COR_INPUT,
        fg=COR_TEXTO,
        insertbackground=COR_PRIMARIA,
        wrap="word"
    )
    obs.pack(fill="x")

    obs.bind("<FocusIn>",  lambda e: obs_borda.config(bg=COR_PRIMARIA))
    obs.bind("<FocusOut>", lambda e: obs_borda.config(bg=COR_BORDA))

    # ====================================================
    # PREENCHER SE EDIÇÃO
    # ====================================================

    if dados_cliente:
        for campo, entry in entradas.items():
            chave = MAPA_CAMPOS.get(campo)
            valor = ""
            if chave:
                valor = dados_cliente.get(chave, "") or dados_cliente.get(campo, "")
            if valor is None:
                valor = ""
            entry.insert(0, str(valor))

        obs_val = dados_cliente.get("observacoes", "") or dados_cliente.get("Observacoes", "") or ""
        if obs_val:
            obs.insert("1.0", str(obs_val))

    # ====================================================
    # BOTÕES
    # ====================================================

    tk.Frame(card, bg=COR_BORDA, height=1).pack(fill="x")

    btn_area = tk.Frame(card, bg="#F8FAFC")
    btn_area.pack(fill="x", padx=25, pady=18)

    def limpar():
        for e in entradas.values():
            e.delete(0, tk.END)
        obs.delete("1.0", tk.END)

    def cancelar():
        for w in parent.winfo_children():
            w.destroy()

    def salvar():
        novos = {k: v.get() for k, v in entradas.items()}
        novos["Observacoes"] = obs.get("1.0", tk.END).strip()

        if not novos.get("Nome"):
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório.")
            return

        if modo_edicao:
            atualizar_cliente(indice, novos)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        else:
            salvar_cliente(novos)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            limpar()

    btn_primario(btn_area, "💾  Salvar", salvar).pack(side="left", padx=(0, 10))

    if not modo_edicao:
        btn_primario(btn_area, "🗑  Limpar", limpar, cor="#94A3B8").pack(side="left", padx=(0, 10))

    btn_primario(btn_area, "✕  Cancelar", cancelar, cor=COR_CANCEL).pack(side="left")
