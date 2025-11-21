import pandas as pd
from usuarios import get_dataframe_talentos, get_dataframe_empresas
from projetos import gerar_dataframe_projetos, gerar_dataframe_participacoes


def gerar_relatorios():
    """
    Gera e retorna vários DataFrames:
    - df_talentos
    - df_empresas
    - df_projetos
    - df_participacoes
    - df_consolidado (talento x projeto x status)
    """
    df_talentos = get_dataframe_talentos()
    df_empresas = get_dataframe_empresas()
    df_projetos = gerar_dataframe_projetos()
    df_participacoes = gerar_dataframe_participacoes()

    if df_talentos.empty or df_participacoes.empty:
        df_consolidado = pd.DataFrame()
    else:
        df_consolidado = df_participacoes.merge(
            df_talentos[["email", "nome", "area_interesse", "reputacao"]],
            left_on="email_talento",
            right_on="email",
            how="left",
        )
        df_consolidado = df_consolidado.merge(
            df_projetos[["id", "titulo", "area"]],
            left_on="projeto_id",
            right_on="id",
            how="left",
        )
        df_consolidado = df_consolidado.drop(columns=["email", "id"])

    return df_talentos, df_empresas, df_projetos, df_participacoes, df_consolidado


def gerar_top_talentos(df_talentos, n=5):
    """
    Ordena talentos por reputação e retorna o TOP N.
    """
    if df_talentos.empty:
        return df_talentos
    return df_talentos.sort_values(by="reputacao", ascending=False).head(n)