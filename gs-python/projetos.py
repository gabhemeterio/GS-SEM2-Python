import pandas as pd
from storage import load_json, save_json
from usuarios import atualizar_reputacao, get_usuario_por_email

PROJETOS_FILE = "projetos.json"
PARTICIPACOES_FILE = "participacoes.json"

# Carrega dados já existentes
projetos = load_json(PROJETOS_FILE, [])
participacoes = load_json(PARTICIPACOES_FILE, [])


def _salvar_projetos():
    save_json(PROJETOS_FILE, projetos)


def _salvar_participacoes():
    save_json(PARTICIPACOES_FILE, participacoes)


def criar_projeto(titulo, descricao, area, nivel, duracao, empresa_email, pontos_reputacao):
    """
    Empresa cria um novo projeto de experiência.
    """
    novo_id = 1
    if projetos:
        novo_id = max(p["id"] for p in projetos) + 1

    projeto = {
        "id": novo_id,
        "titulo": titulo,
        "descricao": descricao,
        "area": area,
        "nivel": nivel,
        "duracao": duracao,
        "empresa_email": empresa_email,
        "status": "aberto",
        "pontos_reputacao": pontos_reputacao,
    }
    projetos.append(projeto)
    _salvar_projetos()
    return projeto


def obter_projeto_por_id(projeto_id):
    """
    Retorna um projeto específico pelo ID.
    """
    for p in projetos:
        if p["id"] == projeto_id:
            return p
    return None


def listar_projetos(aberto_only=True, filtro_area=None, filtro_nivel=None):
    """
    Lista projetos no terminal (com possíveis filtros).
    """
    print("\n=== PROJETOS DE EXPERIÊNCIA ===")
    if not projetos:
        print("Nenhum projeto cadastrado ainda.")
        return

    for projeto in projetos:
        if aberto_only and projeto.get("status") != "aberto":
            continue
        if filtro_area and projeto.get("area") != filtro_area:
            continue
        if filtro_nivel and projeto.get("nivel") != filtro_nivel:
            continue

        print(f"\nID: {projeto['id']}")
        print(f"Título : {projeto['titulo']}")
        print(f"Empresa: {projeto['empresa_email']} · Área: {projeto['area']}")
        print(
            f"Nível: {projeto['nivel']} · Duração estimada: {projeto['duracao']} · Status: {projeto['status']}"
        )
        print(
            f"Pontos de reputação ao concluir: {projeto['pontos_reputacao']} pontos"
        )


def listar_projetos_empresa(empresa_email):
    """
    Lista apenas os projetos daquela empresa parceira.
    """
    print("\n=== MEUS PROJETOS ===")
    encontrados = False
    for projeto in projetos:
        if projeto.get("empresa_email") == empresa_email:
            encontrados = True
            print(f"\nID: {projeto['id']} · Título: {projeto['titulo']}")
            print(
                f"Área: {projeto['area']} · Nível: {projeto['nivel']} · Status: {projeto['status']}"
            )
    if not encontrados:
        print("Nenhum projeto encontrado para esta empresa.")


def candidatar_a_projeto(email_talento, projeto_id):
    """
    Talento se candidata a um projeto.
    Garante:
    - projeto existe
    - projeto está aberto
    - talento não está duplicado na lista de participações
    """
    projeto = obter_projeto_por_id(projeto_id)
    if not projeto:
        return False, "Projeto não encontrado."
    if projeto.get("status") != "aberto":
        return False, "Projeto não está aberto para candidaturas."

    for p in participacoes:
        if p["projeto_id"] == projeto_id and p["email_talento"] == email_talento:
            return False, "Você já está candidatado(a) nesse projeto."

    participacoes.append(
        {
            "projeto_id": projeto_id,
            "email_talento": email_talento,
            "status": "candidatado",
        }
    )
    _salvar_participacoes()
    return True, "Candidatura registrada com sucesso."


def listar_candidatos_projeto(projeto_id):
    """
    Empresa visualiza todos os candidatos de um projeto específico.
    """
    projeto = obter_projeto_por_id(projeto_id)
    if not projeto:
        print("\nProjeto não encontrado.")
        return

    print(f"\n=== CANDIDATOS PARA O PROJETO {projeto_id} - {projeto['titulo']} ===")

    encontrados = False
    for part in participacoes:
        if part["projeto_id"] == projeto_id:
            encontrados = True
            talento = get_usuario_por_email(part["email_talento"])
            nome = talento["nome"] if talento else part["email_talento"]
            print(
                f"- {nome} ({part['email_talento']}) · Status: {part['status']}"
            )
    if not encontrados:
        print("Nenhum candidato para este projeto ainda.")


def atualizar_status_participacao(projeto_id, email_talento, novo_status):
    """
    Empresa atualiza status de uma participação:
    - 'candidatado'
    - 'selecionado'
    - 'concluido'

    Se virar 'concluido', aumenta reputação do talento
    e marca o projeto como concluído.
    """
    projeto = obter_projeto_por_id(projeto_id)
    if not projeto:
        return False, "Projeto não encontrado."

    alterado = False
    for part in participacoes:
        if (
            part["projeto_id"] == projeto_id
            and part["email_talento"] == email_talento
        ):
            part["status"] = novo_status
            alterado = True
            break

    if not alterado:
        return False, "Participação não encontrada."

    _salvar_participacoes()

    if novo_status == "concluido":
        atualizar_reputacao(email_talento, projeto["pontos_reputacao"])
        projeto["status"] = "concluido"
        _salvar_projetos()

    return True, "Status atualizado com sucesso."


def listar_participacoes_talento(email_talento):
    """
    Talento vê todos os projetos em que se candidatou/participou.
    """
    print("\n=== MINHAS PARTICIPAÇÕES EM PROJETOS ===")
    encontrados = False
    for part in participacoes:
        if part["email_talento"] == email_talento:
            projeto = obter_projeto_por_id(part["projeto_id"])
            titulo = projeto["titulo"] if projeto else "Projeto desconhecido"
            print(
                f"- Projeto ID {part['projeto_id']} · {titulo} · Status: {part['status']}"
            )
            encontrados = True
    if not encontrados:
        print("Nenhuma participação encontrada.")


def gerar_dataframe_projetos():
    """
    DataFrame com todos os projetos cadastrados.
    """
    if not projetos:
        return pd.DataFrame(
            columns=[
                "id",
                "titulo",
                "descricao",
                "area",
                "nivel",
                "duracao",
                "empresa_email",
                "status",
                "pontos_reputacao",
            ]
        )
    return pd.DataFrame(projetos)


def gerar_dataframe_participacoes():
    """
    DataFrame com todas as participações.
    """
    if not participacoes:
        return pd.DataFrame(
            columns=["projeto_id", "email_talento", "status"]
        )
    return pd.DataFrame(participacoes)