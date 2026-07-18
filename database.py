# database.py

import sqlite3
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")
os.makedirs(PASTA_DADOS, exist_ok=True)
BANCO = os.path.join(PASTA_DADOS, "usuarios.db")


def conectar():
    return sqlite3.connect(BANCO)


def aplicar_migracoes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(frota)")
    colunas_frota = [row[1] for row in cursor.fetchall()]
    if "status" not in colunas_frota:
        cursor.execute("ALTER TABLE frota ADD COLUMN status TEXT DEFAULT 'disponivel'")

    cursor.execute("UPDATE frota SET status = 'disponivel' WHERE status IS NULL OR status = ''")

    cursor.execute("PRAGMA table_info(usuarios)")
    colunas_usuarios = [row[1] for row in cursor.fetchall()]
    if "nome" not in colunas_usuarios:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN nome TEXT DEFAULT ''")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_veiculo INTEGER NOT NULL,
            id_cliente INTEGER NOT NULL,
            valor_venda REAL NOT NULL,
            valor_entrada REAL NOT NULL,
            modalidade TEXT NOT NULL,
            parcelas INTEGER,
            taxa_juros REAL,
            valor_parcela REAL,
            data_venda TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (id_veiculo) REFERENCES frota(id),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            nivel TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def criar_admin():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
    if not cursor.fetchone():
        senha = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO usuarios (usuario, nome, senha, nivel) VALUES (?, ?, ?, ?)",
            ("admin", "Administrador", senha.decode(), "admin")
        )
        conn.commit()
    conn.close()


def validar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha, nivel FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if not resultado:
        return None
    senha_ok = bcrypt.checkpw(senha.encode(), resultado[0].encode())
    if senha_ok:
        return {"usuario": usuario, "nivel": resultado[1]}
    return None


def cadastrar_usuario(usuario, nome, senha, nivel):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    if cursor.fetchone():
        conn.close()
        return False
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "INSERT INTO usuarios (usuario, nome, senha, nivel) VALUES (?, ?, ?, ?)",
        (usuario, nome, senha_hash, nivel)
    )
    conn.commit()
    conn.close()
    return True


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, nome, nivel FROM usuarios ORDER BY usuario")
    dados = cursor.fetchall()
    conn.close()
    return dados


def excluir_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conn.commit()
    conn.close()


def atualizar_usuario(id_usuario, usuario, nome, nivel):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET usuario = ?, nome = ?, nivel = ? WHERE id = ?",
        (usuario, nome, nivel, id_usuario)
    )
    conn.commit()
    conn.close()


def criar_tabela_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            cep TEXT,
            observacoes TEXT
        )
    """)
    conn.commit()
    conn.close()


def salvar_cliente(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, cpf, telefone, email, endereco, numero, bairro, cidade, uf, cep, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["Nome"], dados["CPF"], dados["Telefone"], dados["Email"],
        dados["Endereço"], dados["Número"], dados["Bairro"], dados["Cidade"],
        dados["UF"], dados["CEP"], dados["Observacoes"]
    ))
    conn.commit()
    conn.close()


def atualizar_cliente(id_cliente, dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes SET nome=?, cpf=?, telefone=?, email=?, endereco=?,
        numero=?, bairro=?, cidade=?, uf=?, cep=?, observacoes=? WHERE id=?
    """, (
        dados["Nome"], dados["CPF"], dados["Telefone"], dados["Email"],
        dados["Endereço"], dados["Número"], dados["Bairro"], dados["Cidade"],
        dados["UF"], dados["CEP"], dados["Observacoes"], id_cliente
    ))
    conn.commit()
    conn.close()


def listar_clientes():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nome")
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def excluir_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()


def criar_tabela_funcionarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            telefone TEXT,
            cargo TEXT,
            salario TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


def salvar_funcionario(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO funcionarios (nome, cpf, telefone, cargo, salario, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        dados["Nome"], dados["CPF"], dados["Telefone"],
        dados["Cargo"], dados["Salário"], dados["Email"]
    ))
    conn.commit()
    conn.close()


def listar_funcionarios():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funcionarios ORDER BY nome")
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def excluir_funcionario(id_funcionario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_funcionario,))
    conn.commit()
    conn.close()


def criar_tabela_financeiro():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def resumo_financeiro():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0)
        FROM financeiro
    """)
    row = cursor.fetchone()
    conn.close()
    receitas = row[0]
    despesas = row[1]
    return {"receitas": receitas, "despesas": despesas, "lucro": receitas - despesas}


def listar_financeiro():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financeiro ORDER BY data DESC, id DESC")
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def criar_tabela_frota():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            ano TEXT,
            placa TEXT,
            cor TEXT,
            km TEXT,
            valor TEXT,
            status TEXT DEFAULT 'disponivel'
        )
    """)
    conn.commit()
    conn.close()


def salvar_veiculo(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO frota (marca, modelo, ano, placa, cor, km, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'disponivel')
    """, (
        dados["Marca"], dados["Modelo"], dados["Ano"], dados["Placa"],
        dados["Cor"], dados["KM"], dados["Valor"]
    ))
    valor_str = dados["Valor"].replace(".", "").replace(",", ".")
    try:
        valor_float = float(valor_str)
    except ValueError:
        valor_float = 0.0
    descricao = f"Compra: {dados['Marca']} {dados['Modelo']} {dados['Ano']} - Placa {dados['Placa']}"
    cursor.execute(
        "INSERT INTO financeiro (tipo, descricao, valor, data) VALUES ('despesa', ?, ?, DATE('now'))",
        (descricao, valor_float)
    )
    conn.commit()
    conn.close()


def listar_veiculos(status=None):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if status:
        cursor.execute("""
            SELECT * FROM frota
            WHERE status = ? OR (? = 'disponivel' AND (status IS NULL OR status = ''))
            ORDER BY marca
        """, (status, status))
    else:
        cursor.execute("SELECT * FROM frota ORDER BY marca")
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def atualizar_veiculo(id_veiculo, dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE frota SET marca=?, modelo=?, ano=?, placa=?, cor=?, km=?, valor=?
        WHERE id=?
    """, (
        dados["Marca"], dados["Modelo"], dados["Ano"], dados["Placa"],
        dados["Cor"], dados["KM"], dados["Valor"], id_veiculo
    ))
    conn.commit()
    conn.close()


def excluir_veiculo(id_veiculo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM frota WHERE id = ?", (id_veiculo,))
    conn.commit()
    conn.close()


def criar_tabela_vendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_veiculo INTEGER NOT NULL,
            id_cliente INTEGER NOT NULL,
            valor_venda REAL NOT NULL,
            valor_entrada REAL NOT NULL,
            modalidade TEXT NOT NULL,
            parcelas INTEGER,
            taxa_juros REAL,
            valor_parcela REAL,
            data_venda TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (id_veiculo) REFERENCES frota(id),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        )
    """)
    conn.commit()
    conn.close()


def registrar_venda(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vendas (id_veiculo, id_cliente, valor_venda, valor_entrada,
        modalidade, parcelas, taxa_juros, valor_parcela, data_venda, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE('now'), ?)
    """, (
        dados["id_veiculo"], dados["id_cliente"], dados["valor_venda"],
        dados["valor_entrada"], dados["modalidade"], dados.get("parcelas"),
        dados.get("taxa_juros"), dados.get("valor_parcela"), dados.get("observacoes", "")
    ))
    cursor.execute("UPDATE frota SET status = 'vendido' WHERE id = ?", (dados["id_veiculo"],))
    cursor.execute("SELECT marca, modelo, ano, placa FROM frota WHERE id = ?", (dados["id_veiculo"],))
    veiculo = cursor.fetchone()
    descricao = (
        f"Venda: {veiculo[0]} {veiculo[1]} {veiculo[2]} - Placa {veiculo[3]}"
        if veiculo else "Venda de veiculo"
    )
    cursor.execute(
        "INSERT INTO financeiro (tipo, descricao, valor, data) VALUES ('receita', ?, ?, DATE('now'))",
        (descricao, dados["valor_venda"])
    )
    conn.commit()
    conn.close()


def listar_vendas():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, v.valor_venda, v.valor_entrada, v.modalidade, v.parcelas,
               v.taxa_juros, v.valor_parcela, v.data_venda, v.observacoes,
               f.marca, f.modelo, f.ano, f.placa,
               c.nome AS cliente_nome, c.cpf AS cliente_cpf
        FROM vendas v
        JOIN frota f ON f.id = v.id_veiculo
        JOIN clientes c ON c.id = v.id_cliente
        ORDER BY v.data_venda DESC, v.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def criar_tabela_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            tipo TEXT,
            data TEXT,
            hora TEXT
        )
    """)
    conn.commit()
    conn.close()


def salvar_agendamento(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agendamentos (cliente, tipo, data, hora) VALUES (?, ?, ?, ?)",
        (dados["Cliente"], dados["Tipo"], dados["Data"], dados["Hora"])
    )
    conn.commit()
    conn.close()


def listar_agendamentos():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamentos ORDER BY data, hora")
    dados = cursor.fetchall()
    conn.close()
    return [dict(d) for d in dados]


def excluir_agendamento(id_agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id_agendamento,))
    conn.commit()
    conn.close()


# Inicializar todas as tabelas ao importar
criar_tabela()
criar_admin()
criar_tabela_clientes()
criar_tabela_funcionarios()
criar_tabela_financeiro()
criar_tabela_frota()
criar_tabela_vendas()
criar_tabela_agendamentos()
aplicar_migracoes()
