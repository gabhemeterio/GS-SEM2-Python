import pandas as pd
from storage import load_json, save_json

USUARIOS_FILE = "usuarios.json"

# Carrega usuários do JSON se já existir
usuarios = load_json(USUARIOS_FILE, [])
usuario_logado_email = None


def _salvar_usuarios():
    save_json(USUARIOS_FILE, usuarios)


def cadastrar_talento(nome, email, faixa_etaria, objetivo, area_interesse, skills_texto, senha):
    """
    Cadastra um usuário do tipo 'talento'.
    Usa uma FUNÇÃO INTERNA para calcular o nível de cadastro.
    """

    def calcular_nivel_cadastro():
        """
        Função dentro da função.
        Quanto mais campos preenchidos, maior o nível.
        """
        campos_preenchidos = sum(
            [
                1 if nome else 0,
                1 if email else 0,
                1 if faixa_etaria else 0,
                1 if objetivo else 0,
                1 if area_interesse else 0,
            ]
        )
        if campos_preenchidos >= 5:
            return 3
        elif campos_preenchidos >= 3:
            return 2
        else:
            return 1

    # evita e-mail duplicado
    for u in usuarios:
        if u["email"] == email:
            raise ValueError("Já existe um usuário cadastrado com esse e-mail.")

    skills = [s.strip() for s in skills_texto.split(",") if s.strip()]

    usuario = {
        "tipo": "talento",
        "nome": nome,
        "email": email,
        "faixa_etaria": faixa_etaria,
        "objetivo": objetivo,
        "area_interesse": area_interesse,
        "skills": skills,
        "senha": senha,
        "nivel_cadastro": calcular_nivel_cadastro(),
        "reputacao": 0,
        "projetos_concluidos": 0,
    }

    usuarios.append(usuario)
    _salvar_usuarios()

    global usuario_logado_email
    usuario_logado_email = email

    return usuario


def cadastrar_empresa(nome_fantasia, email, segmento, porte, descricao, senha):
    """
    Cadastra um usuário do tipo 'empresa parceira'.
    """
    for u in usuarios:
        if u["email"] == email:
            raise ValueError("Já existe um usuário cadastrado com esse e-mail.")

    usuario = {
        "tipo": "empresa",
        "nome": nome_fantasia,
        "email": email,
        "segmento": segmento,
        "porte": porte,
        "descricao": descricao,
        "senha": senha,
    }

    usuarios.append(usuario)
    _salvar_usuarios()

    global usuario_logado_email
    usuario_logado_email = email

    return usuario


def autenticar_usuario(email, senha):
    """
    Simula autenticação: percorre a lista de usuários
    e compara e-mail + senha.
    """
    global usuario_logado_email
    for user in usuarios:
        if user["email"] == email and user["senha"] == senha:
            usuario_logado_email = email
            return user
    return None


def get_usuario_logado():
    """
    Retorna o dicionário do usuário logado (ou None).
    """
    if not usuario_logado_email:
        return None
    for user in usuarios:
        if user["email"] == usuario_logado_email:
            return user
    return None


def logout():
    """
    Faz logout limpando o e-mail logado.
    """
    global usuario_logado_email
    usuario_logado_email = None


def get_usuario_por_email(email):
    """
    Busca usuário específico pelo e-mail.
    """
    for user in usuarios:
        if user["email"] == email:
            return user
    return None


def atualizar_reputacao(email, pontos):
    """
    Aumenta a reputação e o número de projetos concluídos
    de um TALENTO e salva no JSON.
    """
    alterado = False
    for user in usuarios:
        if user["email"] == email and user.get("tipo") == "talento":
            user["reputacao"] = user.get("reputacao", 0) + pontos
            user["projetos_concluidos"] = user.get("projetos_concluidos", 0) + 1
            alterado = True
            break
    if alterado:
        _salvar_usuarios()


def gerar_dataframe_usuarios():
    """
    Gera um DataFrame com todos os usuários (talentos + empresas),
    sem expor as senhas.
    """
    if not usuarios:
        return pd.DataFrame(
            columns=[
                "tipo",
                "nome",
                "email",
                "faixa_etaria",
                "objetivo",
                "area_interesse",
                "skills",
                "nivel_cadastro",
                "reputacao",
                "projetos_concluidos",
                "segmento",
                "porte",
                "descricao",
            ]
        )

    processed = []
    for u in usuarios:
        base = {
            "tipo": u.get("tipo"),
            "nome": u.get("nome"),
            "email": u.get("email"),
        }
        if u.get("tipo") == "talento":
            base.update(
                {
                    "faixa_etaria": u.get("faixa_etaria"),
                    "objetivo": u.get("objetivo"),
                    "area_interesse": u.get("area_interesse"),
                    "skills": ", ".join(u.get("skills", [])),
                    "nivel_cadastro": u.get("nivel_cadastro"),
                    "reputacao": u.get("reputacao"),
                    "projetos_concluidos": u.get("projetos_concluidos"),
                    "segmento": None,
                    "porte": None,
                    "descricao": None,
                }
            )
        else:  # empresa
            base.update(
                {
                    "faixa_etaria": None,
                    "objetivo": None,
                    "area_interesse": None,
                    "skills": None,
                    "nivel_cadastro": None,
                    "reputacao": None,
                    "projetos_concluidos": None,
                    "segmento": u.get("segmento"),
                    "porte": u.get("porte"),
                    "descricao": u.get("descricao"),
                }
            )
        processed.append(base)

    return pd.DataFrame(processed)


def get_dataframe_talentos():
    df = gerar_dataframe_usuarios()
    if df.empty:
        return df
    return df[df["tipo"] == "talento"]


def get_dataframe_empresas():
    df = gerar_dataframe_usuarios()
    if df.empty:
        return df
    return df[df["tipo"] == "empresa"]