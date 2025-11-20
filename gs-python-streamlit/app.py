import streamlit as st

from usuarios import (
    init_state,
    cadastrar_usuario,
    autenticar_usuario,
    get_usuario_logado,
    gerar_dataframe_usuarios,
)
from projetos import obter_projetos, registrar_participacao, gerar_dataframe_participacoes
from relatorios import gerar_relatorio_geral


# Configuração geral da página
st.set_page_config(page_title="LinkTech Python", layout="wide")

# Inicializa session_state
init_state()


def pagina_home():
    """
    Página inicial: explica a proposta da solução.
    Foca na experiência de leitura, como a landing feita em React.
    """
    st.title("LinkTech – Simulador em Python")
    st.subheader("Construa sua carreira em tecnologia com projetos reais")

    st.markdown(
        """
Plataforma inspirada no LinkedIn, focada em **habilidades**, **portfólio** 
e experiências práticas com empresas parceiras. Pensada para jovens e 
pessoas 50+ que querem entrar ou migrar para a área de tecnologia.
"""
    )

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown("### Como funciona")
        st.markdown(
            "- Preencha seu perfil e atinja o Cadastro Nível 3.\n"
            "- Participe de projetos práticos com empresas parceiras.\n"
            "- Ganhe reputação e destaque seu portfólio."
        )
    with col2:
        st.markdown("### Para quem é")
        st.markdown(
            "- Jovens em busca do primeiro emprego em tecnologia.\n"
            "- Profissionais 40+/50+ em transição de carreira."
        )
    with col3:
        st.info("Use o menu lateral para **Cadastrar/Login**, ver **Projetos** e gerar **Relatórios**.")


def pagina_login_cadastro():
    """
    Página que reúne login e cadastro.
    Demonstra:
    - Entrada (widgets do Streamlit)
    - Estrutura de condição (fluxo de login vs cadastro)
    """

    st.header("Login e Cadastro")

    col_login, col_cadastro = st.columns(2)

    # --- LOGIN ---
    with col_login:
        st.subheader("Entrar")

        with st.form("form_login"):
            email_login = st.text_input("E-mail", key="login_email")
            senha_login = st.text_input("Senha", type="password", key="login_senha")
            logar = st.form_submit_button("Entrar")

        if logar:
            usuario = autenticar_usuario(email_login, senha_login)
            if usuario:
                st.success(f"Bem-vindo(a), {usuario['nome']}! Você está logado.")
            else:
                st.error("Credenciais inválidas ou usuário não encontrado.")

    # --- CADASTRO ---
    with col_cadastro:
        st.subheader("Criar conta como talento")

        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo", key="cad_nome")
            email = st.text_input("E-mail", key="cad_email")
            faixa_etaria = st.selectbox(
                "Faixa etária",
                ["", "18–24", "25–34", "35–44", "45–54", "55+"],
                key="cad_faixa",
            )
            objetivo = st.text_area(
                "Objetivo na área de tecnologia (breve resumo)",
                key="cad_objetivo",
            )
            senha = st.text_input("Crie uma senha", type="password", key="cad_senha")
            cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if not nome or not email or not senha:
                st.warning("Preencha pelo menos nome, e-mail e senha.")
            else:
                usuario = cadastrar_usuario(nome, email, faixa_etaria, objetivo, senha)
                st.success(
                    f"Usuário {usuario['nome']} cadastrado com sucesso! "
                    f"Nível de cadastro: {usuario['nivel_cadastro']}."
                )


def pagina_projetos():
    """
    Lista os projetos e permite o usuário simular participação.
    Demonstra:
    - Estrutura de repetição (loop sobre projetos)
    - Condição: exige usuário logado para participar
    """
    st.header("Projetos de experiência")

    usuario = get_usuario_logado()
    if not usuario:
        st.warning("Você precisa estar logado para participar dos projetos.")
        st.info("Acesse a opção **Login e Cadastro** no menu lateral.")
        return

    st.write(f"Usuário logado: **{usuario['nome']}** – Reputação: {usuario['reputacao']} pontos")

    projetos = obter_projetos()

    for projeto in projetos:
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(projeto["titulo"])
                st.caption(f"{projeto['empresa']} · {projeto['area']}")
                st.write(
                    f"Nível: {projeto['nivel']} · Duração: {projeto['duracao']} · Formato: {projeto['formato']}"
                )
                st.write(
                    f"Conclusão gera **{projeto['pontos_reputacao']} pontos de reputação** e entra no portfólio."
                )

            with col2:
                st.write("")
                st.write("")
                if st.button(
                    "Simular conclusão de projeto",
                    key=f"btn_{projeto['id']}",
                ):
                    registrar_participacao(usuario["email"], projeto["id"], status="concluido")
                    st.success(
                        f"Concluído! Você ganhou {projeto['pontos_reputacao']} pontos de reputação."
                    )


def pagina_relatorios():
    """
    Mostra relatórios em DataFrame para a GS.
    Demonstra o uso de DataFrames e junções.
    """
    st.header("Relatórios de usuários, projetos e participações")

    df_usuarios, df_participacoes, df_projetos, df_geral = gerar_relatorio_geral()

    st.subheader("Usuários cadastrados")
    if df_usuarios.empty:
        st.info("Nenhum usuário cadastrado ainda.")
    else:
        st.dataframe(df_usuarios)

    st.subheader("Projetos disponíveis")
    st.dataframe(df_projetos)

    st.subheader("Participações registradas")
    if df_participacoes.empty:
        st.info("Nenhuma participação registrada ainda.")
    else:
        st.dataframe(df_participacoes)

    st.subheader("Visão geral (usuários x projetos)")
    if df_geral.empty:
        st.info("Ainda não há dados suficientes para gerar a visão geral.")
    else:
        st.dataframe(df_geral)


# ---------------------------
# MENU LATERAL (NAVEGAÇÃO)
# ---------------------------
menu = st.sidebar.radio(
    "Navegação",
    ["Home", "Login e Cadastro", "Projetos", "Relatórios"],
)

if menu == "Home":
    pagina_home()
elif menu == "Login e Cadastro":
    pagina_login_cadastro()
elif menu == "Projetos":
    pagina_projetos()
elif menu == "Relatórios":
    pagina_relatorios()