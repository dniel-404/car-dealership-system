# ====================================================
# permissoes.py
# ====================================================

from sessao import usuario_logado

def tem_permissao(permissao):

    nivel = usuario_logado.get("nivel")

    permissoes = {

        "admin": [
            "clientes",
            "funcionarios",
            "frota",
            "vendas",
            "agendamento",
            "dashboard",
            "usuarios",
            "adm"
        ],

        "gerente": [
            "clientes",
            "funcionarios",
            "frota",
            "vendas",
            "agendamento",
            "dashboard"
        ],

        "funcionario": [
            "clientes",
            "vendas",
            "agendamento"
        ]
    }

    return permissao in permissoes.get(
        nivel,
        []
    )