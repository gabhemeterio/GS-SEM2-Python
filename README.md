## Integrantes

- Felippe Nascimento Silva | RM 562123
- Gabriel S. Hemeterio | RM 566243
- Matheus Hideki Doroszewski Yoshimura | RM 564970
---

# LinkTech – Plataforma de Experiências em Tecnologia  
Global Solution – Futuro do Trabalho

## Sumário

1. [Visão geral do projeto](#1-visão-geral-do-projeto)  
2. [Problema e oportunidade](#2-problema-e-oportunidade)  
3. [Solução proposta](#3-solução-proposta)  
4. [Público-alvo](#4-público-alvo)  
5. [Como a solução endereça o problema](#5-como-a-solução-endereça-o-problema)  
6. [Arquitetura da solução em Python](#6-arquitetura-da-solução-em-python)  
7. [Documentação das funções por módulo](#7-documentação-das-funções-por-módulo)  
8. [Guia de uso – Aplicação principal em Python (modo texto)](#8-guia-de-uso--aplicação-principal-em-python-modo-texto)  
9. [Guia de uso – Protótipo em Streamlit](#9-guia-de-uso--protótipo-em-streamlit)  
10. [Conclusão](#10-conclusão)

---

## 1. Visão geral do projeto

A **LinkTech** é uma plataforma inspirada em redes profissionais (como o LinkedIn), mas com foco central em **empregabilidade em tecnologia por meio de projetos reais**.  

O projeto foi desenvolvido em duas interfaces em Python:
- **Aplicação principal em linha de comando** (modo texto), com persistência em JSON e relatórios estruturados em `pandas`;
- **Protótipo em Streamlit**, simulando uma interface web mais amigável para demonstração.

Ambas as versões compartilham o mesmo conceito central: conectar **talentos** (jovens e pessoas 50+) a **empresas parceiras** por meio de **projetos de experiência**, construindo reputação e portfólio de forma prática.

---

## 2. Problema e oportunidade

### 2.1 Dor principal

No contexto do **futuro do trabalho**, a área de tecnologia enfrenta simultaneamente:

- Déficit de profissionais qualificados;
- Pessoas em início de carreira ou em transição (especialmente 40+/50+) com dificuldade de comprovar experiência;
- Plataformas focadas em currículo estático, com ênfase em cargos e histórico formal, e pouca visibilidade para:
  - habilidades práticas,
  - participação em projetos,
  - reputação baseada em entregas reais.

Isso gera um descompasso entre **quem quer entrar na área** e **empresas que precisam de talentos testados em problemas do mundo real**.

### 2.2 Oportunidade

A solução proposta atua exatamente na interseção entre:

- **Upskilling/Reskilling em tecnologia**  
- **Projetos reais de curta duração com empresas parceiras**  
- **Construção de reputação e portfólio verificáveis**  

permitindo que talentos mostrem valor antes mesmo de um vínculo CLT, e que empresas reduzam o risco de contratação.

---

## 3. Solução proposta

A LinkTech propõe uma plataforma onde:

- Pessoas se cadastram como **talentos**:
  - Preenchem perfil com faixa etária, objetivo de carreira e área de interesse (Front-end, Dados, etc.);
  - Informam skills iniciais e evoluem seu **nível de cadastro** (1, 2 ou 3) conforme completam o perfil;
  - Participam de **projetos de experiência** oferecidos por empresas parceiras.

- Empresas se cadastram como **empresas parceiras**:
  - Criam **projetos de experiência** com escopo definido, área, nível e pontos de reputação;
  - Recebem candidaturas,
  - Selecionam talentos e registram conclusão, o que gera pontos de reputação para o talento.

Cada projeto concluído:

- **Aumenta a reputação do talento**;
- Incrementa o número de **projetos concluídos**;
- Entra na visão consolidada de relatórios (DataFrames), simulando o “portfólio” e a “rede de talentos”.

---

## 4. Público-alvo

- **Talentos em tecnologia**:
  - Jovens em busca do primeiro emprego ou estágio na área;
  - Profissionais em **transição de carreira**, especialmente **40+/50+**, que precisam comprovar capacidade prática sem depender apenas de cargos anteriores.

- **Empresas parceiras**:
  - Startups, fintechs, edtechs, consultorias e PMEs que desejam:
    - Testar talentos em desafios reais de tecnologia;
    - Construir um **banco de talentos** alinhado à sua realidade;
    - Aumentar sua visibilidade como marca empregadora em tecnologia.

---

## 5. Como a solução endereça o problema

A LinkTech ataca o problema de forma prática:

1. **Foca em habilidades e projetos**, não apenas em cargos e tempo de empresa.
2. Usa **projetos de curta duração** como “freelas de experiência” para gerar:
   - evidência prática,
   - portfólio,
   - reputação numérica.
3. Integra dois lados do ecossistema:
   - Talentos que precisam provar capacidade,
   - Empresas que querem reduzir a incerteza na contratação.
4. Oferece uma base técnica clara (em Python), com:
   - persistência de dados (JSON),
   - relatórios estruturados (DataFrames),
   - menus específicos para talentos e empresas,
   - possibilidade de crescimento futuro (API, interface web, integração com cursos).

## 6. Arquitetura da solução em Python

A solução foi organizada em módulos, separados por responsabilidade:

- `storage.py`  
  Utilitário para salvar e carregar dados em **JSON**, garantindo persistência entre execuções.

- `usuarios.py`  
  Gerencia todos os tipos de usuários:
  - talentos,
  - empresas parceiras,
  - login/logout,
  - reputação,
  - DataFrame de usuários.

- `projetos.py`  
  Gerencia a oferta e o ciclo de vida dos projetos:
  - criação de projetos (empresas),
  - candidaturas (talentos),
  - atualização de status (candidatado, selecionado, concluído),
  - atualização de reputação,
  - DataFrames de projetos e participações.

- `relatorios.py`  
  Consolida dados em **DataFrames** (`pandas`), gerando:
  - visão de talentos,
  - visão de empresas,
  - visão de projetos,
  - log de participações,
  - visão consolidada talento x projeto x status,
  - ranking de talentos por reputação.

- `main_terminal.py`  
  Apresenta a **aplicação principal em modo texto**, com menus:
  - menu raiz,
  - menu de talento,
  - menu de empresa parceira.

Além disso, existe uma **versão em Streamlit** que reutiliza a lógica de negócio em um formato de aplicativo web simples (`app.py` + módulos de apoio), permitindo uma demonstração visual alinhada ao conceito da plataforma online.

---

## 7. Documentação das funções por módulo

### 7.1 `storage.py`

- `load_json(filename, default)`  
  Lê um arquivo JSON e retorna os dados carregados.  
  Se o arquivo não existir ou estiver corrompido, retorna o valor `default`.  
  É utilizado por outros módulos para restaurar usuários, projetos e participações.

- `save_json(filename, data)`  
  Salva os dados em um arquivo JSON com indentação, garantindo facilidade de leitura e debug dos arquivos `.json`.

---

### 7.2 `usuarios.py` (gestão de talentos e empresas)

- `cadastrar_talento(nome, email, faixa_etaria, objetivo, area_interesse, skills_texto, senha)`  
  Cria um novo perfil de talento.  
  Utiliza uma **função interna (`calcular_nivel_cadastro`)** para determinar o nível do cadastro (1, 2 ou 3) com base na quantidade de campos preenchidos.  
  Garante que não haja duplicidade de e-mail e inicializa reputação e projetos concluídos.

- `cadastrar_empresa(nome_fantasia, email, segmento, porte, descricao, senha)`  
  Cadastra um usuário do tipo empresa, com dados de segmento e porte.  
  Também garante unicidade de e-mail e separa as estruturas de dados entre talento e empresa.

- `autenticar_usuario(email, senha)`  
  Percorre a lista de usuários, comparando e-mail e senha.  
  Em caso de sucesso, atualiza a variável global `usuario_logado_email` e retorna o dicionário do usuário.

- `get_usuario_logado()`  
  Retorna o dicionário do usuário atualmente logado, consultando `usuario_logado_email`.  
  Caso não haja nenhum usuário logado, retorna `None`.

- `logout()`  
  Limpa a informação de usuário logado, simulando o logout da sessão.

- `get_usuario_por_email(email)`  
  Busca e retorna um usuário específico pelo e-mail (apoio utilizado no módulo de projetos, por exemplo, ao listar candidatos).

- `atualizar_reputacao(email, pontos)`  
  Localiza um talento pelo e-mail, incrementa a reputação e o número de projetos concluídos, e salva a lista de usuários no JSON.  
  É o elo entre a conclusão de projetos e a evolução do talento na plataforma.

- `gerar_dataframe_usuarios()`  
  Gera um `DataFrame` com todos os usuários (talentos e empresas), removendo o campo de senha para segurança.  
  Garante colunas consistentes para permitir análises e relatórios.

- `get_dataframe_talentos()` / `get_dataframe_empresas()`  
  Especializações de `gerar_dataframe_usuarios()` que filtram apenas talentos ou apenas empresas, facilitando a geração de relatórios e ranking.

---

### 7.3 `projetos.py` (gestão de projetos e participações)

- `criar_projeto(titulo, descricao, area, nivel, duracao, empresa_email, pontos_reputacao)`  
  Permite que uma empresa parceira crie um novo projeto de experiência.  
  Gera um `id` incremental, associa o projeto à empresa criadora e define um valor de reputação a ser atribuído ao talento na conclusão.

- `obter_projeto_por_id(projeto_id)`  
  Função utilitária que retorna um projeto específico com base no ID informado.

- `listar_projetos(aberto_only=True, filtro_area=None, filtro_nivel=None)`  
  Lista, no modo texto, os projetos da plataforma, com opções de filtro por área e nível.  
  Quando `aberto_only=True`, mostra apenas projetos com status “aberto”.

- `listar_projetos_empresa(empresa_email)`  
  Lista, para a empresa logada, somente os projetos criados por ela, com informações resumidas de status.

- `candidatar_a_projeto(email_talento, projeto_id)`  
  Registra a candidatura de um talento a um projeto.  
  Verifica se o projeto existe, se está aberto, e se o talento já não está candidatado.  
  Armazena a participação com status inicial `candidatado` em JSON, retornando mensagem de sucesso ou erro.

- `listar_candidatos_projeto(projeto_id)`  
  Permite que a empresa veja, em modo texto, todos os talentos que se candidataram ao projeto indicado, com nome, e-mail e status atual.

- `atualizar_status_participacao(projeto_id, email_talento, novo_status)`  
  Atualiza o status de uma participação específica (por exemplo, de `candidatado` para `selecionado` ou `concluido`).  
  Quando o status passa a `concluido`, a função:
  - chama `atualizar_reputacao` (módulo `usuarios`);
  - atualiza o status do projeto para `concluido` (simulando encerramento da vaga);
  - persiste tudo em JSON.

- `listar_participacoes_talento(email_talento)`  
  Mostra, para o talento, um histórico de todos os projetos em que ele se candidatou/participou, junto com o status de cada participação.

- `gerar_dataframe_projetos()` / `gerar_dataframe_participacoes()`  
  Geração de DataFrames específicos de projetos e participações, usados posteriormente nos relatórios consolidados.

### 7.4 `relatorios.py` (visão analítica)

- `gerar_relatorios()`  
  Produz e retorna cinco DataFrames principais:
  - `df_talentos`: talentos com reputação, área de interesse etc.;
  - `df_empresas`: empresas parceiras e seus dados de segmento;
  - `df_projetos`: catálogo de projetos cadastrados;
  - `df_participacoes`: log das participações de talentos;
  - `df_consolidado`: junção de talentos x participações x projetos, permitindo visualizar quem participou de qual projeto, em qual área, com qual status.

- `gerar_top_talentos(df_talentos, n=5)`  
  Recebe um DataFrame de talentos e retorna os `n` talentos com maior reputação, simulando um ranking interno de destaques da plataforma.

---

## 8. Guia de uso – Aplicação principal em Python

### 8.1 Pré-requisitos

- Python 3.11 instalado;
- Biblioteca pandas instalada no ambiente:
  - Comando: pip install pandas
- Todos os arquivos do projeto (storage.py, usuarios.py, projetos.py, relatorios.py, main_terminal.py) na mesma pasta.

---

### 8.2 Execução

No diretório do projeto, executar:

  python main_terminal.py

A aplicação iniciará o menu principal em modo texto.

---

### 8.3 Fluxo geral de uso

#### 8.3.1 Etapas para Talento

1. Cadastrar TALENTO  
   - Escolher a opção "1 - Cadastrar TALENTO" no menu principal;  
   - Informar nome completo, e-mail, faixa etária, objetivo, área de interesse, skills e senha;  
   - Ao finalizar, o sistema calcula automaticamente o nível de cadastro do talento (1, 2 ou 3).

2. Login  
   - Selecionar a opção "3 - Login";  
   - Informar e-mail e senha cadastrados;  
   - Após login bem-sucedido, o talento é identificado pelo sistema.

3. Acessar o menu TALENTO  
   - Escolher a opção "5 - Entrar no menu TALENTO";  
   - As opções disponíveis incluem:
     - Listar projetos abertos na plataforma;
     - Candidatar-se a um projeto específico, informando o ID;
     - Visualizar suas participações e seus status;
     - Ver um resumo em formato de DataFrames com seus dados e suas participações.

4. Candidatar-se e evoluir reputação  
   - Ao candidatar-se, o status inicial da participação é "candidatado";  
   - Quando a empresa altera o status para "concluido", o talento:
     - recebe pontos de reputação;
     - incrementa o número de projetos concluídos;
     - melhora sua posição no ranking de talentos.

---

#### 8.3.2 Etapas para Empresa Parceira

1. Cadastrar EMPRESA  
   - No menu principal, selecionar "2 - Cadastrar EMPRESA parceira";  
   - Informar nome fantasia, e-mail corporativo, segmento, porte, descrição e senha.

2. Login como empresa  
   - Acessar a opção "3 - Login" com as credenciais da empresa.

3. Acessar o menu EMPRESA  
   - Selecionar "6 - Entrar no menu EMPRESA";  
   - O menu oferece:
     - Criação de novos projetos de experiência;
     - Listagem dos projetos da própria empresa;
     - Visualização dos candidatos de um determinado projeto;
     - Atualização do status das participações (candidatado, selecionado, concluido);
     - Acesso a relatórios gerais (talentos, projetos, participações, ranking de reputação).

4. Encerrar projetos e alimentar a reputação  
   - Ao marcar uma participação como "concluido", a empresa:
     - valida a entrega do talento;
     - alimenta o mecanismo de reputação da plataforma, que passa a refletir melhor a experiência prática do talento.

---

### 8.4 Arquivos JSON gerados

Durante o uso, os seguintes arquivos são criados ou atualizados automaticamente:

- usuarios.json  
  Armazena todos os talentos e empresas cadastrados, com seus dados de perfil e credenciais.

- projetos.json  
  Armazena os projetos de experiência criados pelas empresas, com status e pontos de reputação associados.

- participacoes.json  
  Registra a relação entre talentos e projetos, incluindo o status da participação (candidatado, selecionado, concluido).

Esses arquivos permitem continuar a utilização da plataforma em execuções futuras, simulando um banco de dados simples baseado em arquivos.

## 9. Guia de uso – Protótipo em Streamlit

A aplicação em Streamlit foi construída como um protótipo visual da LinkTech, reaproveitando a lógica de negócio em uma interface web simples.

---

### 9.1 Pré-requisitos

- Python 3.11 instalado;
- Bibliotecas necessárias instaladas no ambiente:
  - pip install streamlit pandas
- Arquivos principais:
  - app.py (arquivo principal do Streamlit);
  - módulos de apoio (usuarios.py, projetos.py, relatorios.py) ajustados para o uso com st.session_state.

---

### 9.2 Execução

No diretório onde está o arquivo app.py, executar:

  streamlit run app.py

O navegador abrirá automaticamente (ou será exibida uma URL local, como http://localhost:8501).

---

### 9.3 Fluxo de navegação

O protótipo em Streamlit apresenta, de forma resumida:

- Página inicial  
  - Explica o conceito da LinkTech;
  - Apresenta a ideia de cadastro de talentos, empresas parceiras, projetos de experiência, reputação e portfólio.

- Área de Login e Cadastro  
  - Permite cadastrar talentos com informações básicas (nome, faixa etária, objetivo);
  - Permite realizar login simplificado para acesso à área de projetos.

- Tela de projetos de experiência  
  - Exibe uma lista dos projetos disponíveis;
  - Permite simular participação e conclusão de projetos;
  - Ao simular a conclusão, a reputação do talento é incrementada e a participação é registrada.

- Tela de relatórios  
  - Exibe DataFrames diretamente no navegador, permitindo visualizar:
    - talentos cadastrados;
    - projetos disponíveis;
    - participações registradas;
    - visão consolidada de quem participou de qual projeto.

O foco desta versão é a demonstração de conceito (experiência de uso), enquanto a aplicação principal em modo texto oferece um conjunto mais completo de funcionalidades, incluindo:
- cadastro de empresas parceiras;
- criação de projetos;
- fluxo detalhado de candidatura e atualização de status;
- relatórios mais completos.

## 10. Conclusão

A LinkTech, mesmo em formato acadêmico e simplificado, materializa uma proposta concreta para o futuro do trabalho em tecnologia:

- Reposiciona o talento no centro, valorizando habilidades, projetos e reputação em vez de apenas cargos formais;
- Cria um espaço em que talentos em início de carreira e profissionais 50+ podem comprovar experiência por meio de projetos aplicados, reduzindo a barreira de entrada na área de tecnologia;
- Permite que empresas parceiras experimentem um modelo de relacionamento com talentos baseado em desafios reais e evidências de entrega, reduzindo o risco de contratação e aumentando a qualidade do banco de talentos;
- Utiliza uma base técnica organizada (Python, JSON, DataFrames) que:
  - demonstra domínio das estruturas fundamentais exigidas na disciplina (entrada, saída, repetição, condição, funções, função dentro de função);
  - aplica boas práticas de organização de código (separação em módulos, persistência de dados, relatórios estruturados).

A aplicação principal em linha de comando e o protótipo em Streamlit funcionam como duas camadas da mesma solução:

1. Um núcleo de regras de negócio bem estruturado em Python, com persistência simples e relatórios analíticos;
2. Interfaces de interação (texto e web) adaptadas aos objetivos da Global Solution, demonstrando tanto o funcionamento do fluxo quanto a experiência do usuário final.

Em um cenário real, a solução poderia evoluir para:

- uma API REST consumida por aplicações web e mobile;
- uma interface completa em React/Next.js integrada à plataforma;
- conexão com trilhas de cursos, testes técnicos e módulos de recomendação por IA generativa;

mantendo a mesma lógica central: usar projetos de experiência e reputação como ponte entre talentos em formação e empresas que buscam profissionais qualificados na área de tecnologia.
