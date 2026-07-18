# ====================================================
# sessao.py
# ====================================================

usuario_logado = {
    "usuario": None,
    "nivel": None
}

def iniciar_sessao(usuario, nivel):

    usuario_logado["usuario"] = usuario
    usuario_logado["nivel"] = nivel

def encerrar_sessao():

    usuario_logado["usuario"] = None
    usuario_logado["nivel"] = None