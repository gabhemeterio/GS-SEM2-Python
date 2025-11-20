import streamlit as st
import pandas as pd


def init_state():
    """
    Inicializa as estruturas de dados na session_state do Streamlit.
    - usuarios: lista de dicionários com dados dos usuários
    - participacoes: lista de participações em projetos
    - usuario_logado: e-mail do usuário logado (simulação de sessão)
    """
    if "usuarios" not in st.session_state:
        st.session_state["usuarios"] = []
    if "participacoes" not in st.session_state:
        st.session_state["participacoes"] = []
    if "usuario_logado" not in st.session_state:
        st.session_state["usuario_logado"] = None


def cadastrar_usuario(nome, email, faixa_etaria, objetivo, senha):
    """
    Cadastra um novo usuário e calcula o nível de cadastro.
    Demonstra:
    - Função dentro de função (calcular_nivel_cadastro)
    - Estrutura de condição (if/elif/else)
    """

    def calcular_nivel_cadastro():
        """
        Função interna usada apenas aqui.
        Quanto mais campos preenchidos, maior o nível.
        """
        campos_preenchidos = sum(
            [
                1 if nome else 0,
                1 if email else 0,
                1 if faixa_etaria else 0,
                1 if objetivo else 0,
            ]
        )

        if campos_preenchidos == 4:
            return 3
        elif campos_preenchidos >= 2:
            return 2
        else:
            return 1

    nivel = calcular_nivel_cadastro()

    usuario = {
        "nome": nome,
        "email": email,
        "faixa_etaria": faixa_etaria,
        "objetivo": objetivo,
        "senha": senha,
        "nivel_cadastro": nivel,
        "reputacao": 0,
        "projetos_concluidos": 0,
    }

    st.session_state["usuarios"].append(usuario)
    st.session_state["usuario_logado"] = email
    return usuario


def autenticar_usuario(email, senha):
    """
    Simula autenticação percorrendo a lista de usuários.
    Demonstra:
    - Estrutura de repetição (for)
    - Estrutura de condição (comparação de e-mail e senha)
    """
    for user in st.session_state["usuarios"]:
        if user["email"] == email and user["senha"] == senha:
            st.session_state["usuario_logado"] = email
            return user
    return None


def get_usuario_logado():
    """
    Retorna o dicionário do usuário logado atualmente (se existir).
    """
    email = st.session_state.get("usuario_logado")
    if not email:
        return None

    for user in st.session_state["usuarios"]:
        if user["email"] == email:
            return user
    return None


def atualizar_reputacao(email, pontos):
    """
    Atualiza reputação e contador de projetos concluídos.
    """
    for user in st.session_state["usuarios"]:
        if user["email"] == email:
            user["reputacao"] += pontos
            user["projetos_concluidos"] += 1
            break


def gerar_dataframe_usuarios():
    """
    Gera um DataFrame com os usuários cadastrados.
    Demonstra:
    - Criação de DataFrame a partir de lista de dicionários
    """
    if not st.session_state["usuarios"]:
        return pd.DataFrame()
    return pd.DataFrame(st.session_state["usuarios"])