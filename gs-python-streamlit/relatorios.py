import pandas as pd
from usuarios import gerar_dataframe_usuarios
from projetos import obter_projetos, gerar_dataframe_participacoes


def gerar_relatorio_geral():
    """
    Gera diferentes DataFrames de relatório:
    - df_usuarios: todos os usuários
    - df_participacoes: log de participações
    - df_projetos: projetos disponíveis
    - df_geral: junção de usuários, projetos e participações
    Demonstra:
    - Manipulação de DataFrames
    - Junções (merge) para cruzar informações
    """
    df_usuarios = gerar_dataframe_usuarios()
    df_participacoes = gerar_dataframe_participacoes()
    df_projetos = pd.DataFrame(obter_projetos())

    if df_usuarios.empty or df_participacoes.empty:
        return df_usuarios, df_participacoes, df_projetos, pd.DataFrame()

    df = df_participacoes.merge(
        df_usuarios[["email", "nome", "faixa_etaria", "reputacao"]],
        on="email",
        how="left",
    )

    df = df.merge(
        df_projetos[["id", "titulo", "area"]],
        left_on="projeto_id",
        right_on="id",
        how="left",
    )

    df = df.drop(columns=["id"])
    return df_usuarios, df_participacoes, df_projetos, df