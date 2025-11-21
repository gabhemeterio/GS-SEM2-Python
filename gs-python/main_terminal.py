from usuarios import (
    cadastrar_talento,
    cadastrar_empresa,
    autenticar_usuario,
    get_usuario_logado,
    logout,
)
from projetos import (
    listar_projetos,
    criar_projeto,
    candidatar_a_projeto,
    listar_candidatos_projeto,
    atualizar_status_participacao,
    listar_participacoes_talento,
    listar_projetos_empresa,
)
from relatorios import gerar_relatorios, gerar_top_talentos


def pausar():
    input("\nPressione ENTER para continuar...")


def fluxo_cadastro_talento():
    print("\n=== CADASTRO DE TALENTO ===")
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    faixa_etaria = input("Faixa etária (ex.: 18–24, 25–34, 55+): ")
    objetivo = input("Objetivo na área de tecnologia: ")
    area_interesse = input("Área de interesse (Front-end, Dados, UX, etc.): ")
    skills = input("Liste algumas skills separadas por vírgula: ")
    senha = input("Crie uma senha: ")

    try:
        usuario = cadastrar_talento(
            nome, email, faixa_etaria, objetivo, area_interesse, skills, senha
        )
        print("\nTalento cadastrado com sucesso!")
        print(f"Nome             : {usuario['nome']}")
        print(f"E-mail           : {usuario['email']}")
        print(f"Área de interesse: {usuario['area_interesse']}")
        print(f"Nível de cadastro: {usuario['nivel_cadastro']}")
    except ValueError as e:
        print(f"\nErro: {e}")


def fluxo_cadastro_empresa():
    print("\n=== CADASTRO DE EMPRESA PARCEIRA ===")
    nome = input("Nome fantasia da empresa: ")
    email = input("E-mail corporativo: ")
    segmento = input("Segmento (ex.: Fintech, EdTech, Consultoria...): ")
    porte = input("Porte (ex.: Startup, PME, Grande): ")
    descricao = input("Breve descrição da empresa: ")
    senha = input("Crie uma senha: ")

    try:
        empresa = cadastrar_empresa(nome, email, segmento, porte, descricao, senha)
        print("\nEmpresa cadastrada com sucesso!")
        print(f"Nome    : {empresa['nome']}")
        print(f"E-mail  : {empresa['email']}")
        print(f"Segmento: {empresa['segmento']} · Porte: {empresa['porte']}")
    except ValueError as e:
        print(f"\nErro: {e}")


def fluxo_login():
    print("\n=== LOGIN ===")
    email = input("E-mail: ")
    senha = input("Senha: ")
    usuario = autenticar_usuario(email, senha)
    if usuario:
        print(f"\nBem-vindo(a), {usuario['nome']}! Tipo de conta: {usuario.get('tipo', 'talento')}")
    else:
        print("\nCredenciais inválidas ou usuário não encontrado.")


def fluxo_logout():
    usuario = get_usuario_logado()
    if not usuario:
        print("\nNenhum usuário está logado.")
        return
    logout()
    print("\nLogout realizado com sucesso.")


def menu_talento():
    """
    Menu quando um TALENTO está logado.
    """
    while True:
        usuario = get_usuario_logado()
        if not usuario or usuario.get("tipo") != "talento":
            print("\nNenhum talento logado. Voltando ao menu principal.")
            return

        print("\n===== MENU TALENTO =====")
        print(f"Logado como: {usuario['nome']} · Reputação: {usuario.get('reputacao', 0)} pts")
        print("1 - Listar projetos disponíveis")
        print("2 - Candidatar-se a um projeto")
        print("3 - Ver minhas participações")
        print("4 - Ver relatórios/resumo")
        print("0 - Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            listar_projetos(aberto_only=True)
            pausar()
        elif opcao == "2":
            try:
                projeto_id = int(input("Digite o ID do projeto para se candidatar: "))
            except ValueError:
                print("ID inválido.")
                pausar()
                continue
            ok, msg = candidatar_a_projeto(usuario["email"], projeto_id)
            print("\n" + msg)
            pausar()
        elif opcao == "3":
            listar_participacoes_talento(usuario["email"])
            pausar()
        elif opcao == "4":
            df_talentos, df_empresas, df_projetos, df_participacoes, df_consolidado = gerar_relatorios()
            print("\n--- Meus dados (visão rápida) ---")
            if not df_talentos.empty:
                meu_registro = df_talentos[df_talentos["email"] == usuario["email"]]
                if not meu_registro.empty:
                    print(meu_registro.to_string(index=False))
                else:
                    print("Não encontrado no DataFrame (erro inesperado).")
            else:
                print("Nenhum talento cadastrado no DataFrame.")

            print("\n--- Meus projetos/candidaturas (consolidado) ---")
            if not df_consolidado.empty:
                meus = df_consolidado[df_consolidado["email_talento"] == usuario["email"]]
                if meus.empty:
                    print("Nenhuma participação registrada ainda.")
                else:
                    print(meus.to_string(index=False))
            else:
                print("Ainda não há dados suficientes para gerar o consolidado.")
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_empresa():
    """
    Menu quando uma EMPRESA está logada.
    """
    while True:
        usuario = get_usuario_logado()
        if not usuario or usuario.get("tipo") != "empresa":
            print("\nNenhuma empresa logada. Voltando ao menu principal.")
            return

        print("\n===== MENU EMPRESA PARCEIRA =====")
        print(f"Logado como: {usuario['nome']} ({usuario.get('segmento', '')})")
        print("1 - Criar novo projeto de experiência")
        print("2 - Listar meus projetos")
        print("3 - Ver candidatos de um projeto")
        print("4 - Atualizar status de participação (selecionar/concluir)")
        print("5 - Ver relatórios gerais")
        print("0 - Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            titulo = input("Título do projeto: ")
            descricao = input("Descrição (resumo do desafio): ")
            area = input("Área (Front-end, Dados, UX, etc.): ")
            nivel = input("Nível recomendado (Iniciante, Júnior, etc.): ")
            duracao = input("Duração estimada (ex.: 10–15h): ")
            try:
                pontos = int(input("Pontos de reputação oferecidos ao concluir: "))
            except ValueError:
                print("Valor inválido. Usando padrão de 10 pontos.")
                pontos = 10
            projeto = criar_projeto(
                titulo, descricao, area, nivel, duracao, usuario["email"], pontos
            )
            print("\nProjeto criado com sucesso!")
            print(f"ID: {projeto['id']} · Título: {projeto['titulo']}")
            pausar()
        elif opcao == "2":
            listar_projetos_empresa(usuario["email"])
            pausar()
        elif opcao == "3":
            try:
                projeto_id = int(input("Digite o ID do projeto para ver candidatos: "))
            except ValueError:
                print("ID inválido.")
                pausar()
                continue
            listar_candidatos_projeto(projeto_id)
            pausar()
        elif opcao == "4":
            try:
                projeto_id = int(input("ID do projeto: "))
            except ValueError:
                print("ID inválido.")
                pausar()
                continue
            email_talento = input("E-mail do talento: ")
            print("Novo status: candidatado, selecionado ou concluido")
            novo_status = input("Digite o novo status: ").strip().lower()
            if novo_status not in {"candidatado", "selecionado", "concluido"}:
                print("Status inválido.")
                pausar()
                continue
            ok, msg = atualizar_status_participacao(projeto_id, email_talento, novo_status)
            print("\n" + msg)
            pausar()
        elif opcao == "5":
            df_talentos, df_empresas, df_projetos, df_participacoes, df_consolidado = gerar_relatorios()
            print("\n--- Talentos cadastrados ---")
            if df_talentos.empty:
                print("Nenhum talento cadastrado.")
            else:
                print(df_talentos.to_string(index=False))

            print("\n--- Projetos cadastrados ---")
            if df_projetos.empty:
                print("Nenhum projeto cadastrado.")
            else:
                print(df_projetos.to_string(index=False))

            print("\n--- Participações registradas ---")
            if df_participacoes.empty:
                print("Nenhuma participação registrada.")
            else:
                print(df_participacoes.to_string(index=False))

            print("\n--- Top talentos por reputação ---")
            top = gerar_top_talentos(df_talentos, n=5)
            if top.empty:
                print("Sem dados de reputação ainda.")
            else:
                print(top.to_string(index=False))
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def menu_principal():
    """
    Menu raiz: daqui você acessa cadastro, login
    e os menus específicos de talento/empresa.
    """
    while True:
        usuario = get_usuario_logado()
        print("\n==============================")
        print(" LINKTECH - FUTURO DO TRABALHO")
        print("==============================")
        if usuario:
            print(f"Usuário logado: {usuario['nome']} ({usuario.get('tipo', 'talento')})")
        else:
            print("Nenhum usuário logado.")
        print("\n1 - Cadastrar TALENTO")
        print("2 - Cadastrar EMPRESA parceira")
        print("3 - Login")
        print("4 - Logout")
        print("5 - Entrar no menu TALENTO")
        print("6 - Entrar no menu EMPRESA")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            fluxo_cadastro_talento()
            pausar()
        elif opcao == "2":
            fluxo_cadastro_empresa()
            pausar()
        elif opcao == "3":
            fluxo_login()
            pausar()
        elif opcao == "4":
            fluxo_logout()
            pausar()
        elif opcao == "5":
            menu_talento()
        elif opcao == "6":
            menu_empresa()
        elif opcao == "0":
            print("\nObrigado por utilizar a LinkTech!")
            break
        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":
    menu_principal()