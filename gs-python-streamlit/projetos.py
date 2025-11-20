import streamlit as st
import pandas as pd
from usuarios import atualizar_reputacao


def obter_projetos():
    """
    Retorna a lista de projetos de experiência disponíveis.
    Na prática, poderia vir de um banco de dados.
    """
    projetos = [
        {
            "id": 1,
            "titulo": "Landing page para campanha de educação financeira",
            "empresa": "Fintech Clara",
            "area": "Front-end",
            "nivel": "Iniciante / Júnior",
            "duracao": "10–15h",
            "formato": "Individual",
            "pontos_reputacao": 10,
        },
        {
            "id": 2,
            "titulo": "Dashboard de leads em Power BI",
            "empresa": "EdTech Aurora",
            "area": "Dados",
            "nivel": "Júnior",
            "duracao": "15–20h",
            "formato": "Individual",
            "pontos_reputacao": 12,
        },
    ]
    return projetos


def registrar_participacao(email, projeto_id, status="concluido"):
    """
    Registra a participação de um usuário em um projeto.
    Se o status for 'concluido', aumenta a reputação.
    Demonstra:
    - Entrada (parâmetros)
    - Condições para regras de negócio
    """
    if "participacoes" not in st.session_state:
        st.session_state["participacoes"] = []

    projetos = obter_projetos()
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)

    if not projeto:
        return

    participacao = {
        "email": email,
        "projeto_id": projeto_id,
        "status": status,
    }
    st.session_state["participacoes"].append(participacao)

    if status == "concluido":
        atualizar_reputacao(email, projeto["pontos_reputacao"])


def gerar_dataframe_participacoes():
    """
    Gera um DataFrame com as participações registradas.
    """
    if not st.session_state.get("participacoes"):
        return pd.DataFrame()
    return pd.DataFrame(st.session_state["participacoes"])