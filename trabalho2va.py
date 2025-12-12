import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Loja dos Fuleiros", page_icon="🎮")


def add_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap');

        /* Fundo suave e profundo */
        .stApp {
            background: linear-gradient(135deg, #1a1f25, #232a36);
            color: #e0e0e8;
            font-family: 'Roboto', sans-serif;
        }

        /* Títulos: fonte moderna, sem brilho */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: #a0c4e8; /* azul-acinzentado suave */
            text-shadow: none;
        }

        /* Texto comum */
        p, div, span, label, .stMarkdown {
            color: #d0d5db;
        }

        /* Inputs */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
            background-color: rgba(35, 42, 54, 0.8);
            color: #f0f2f6;
            border: 1px solid #4a5568;
            border-radius: 8px;
        }

        .stTextInput > div > div > input::placeholder {
            color: #718096;
        }

        /* Botões: suaves, sem neon */
        .stButton > button {
            background: linear-gradient(90deg, #2c3e50, #3a506b);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.2rem;
            font-family: 'Montserrat', sans-serif;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #3a506b, #4a6285);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(26, 31, 37, 0.95);
            border-right: 1px solid #2d3748;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #a0c4e8;
        }

        /* Cards */
        .jogo-card, .venda-card {
            background: rgba(35, 42, 54, 0.6);
            padding: 1rem;
            border-radius: 10px;
            border-left: 3px solid #3a506b;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        }

        /* Métricas */
        [data-testid="stMetricValue"] {
            color: #a0c4e8 !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600;
        }
        [data-testid="stMetricLabel"] {
            color: #cbd5e0 !important;
        }

        /* Divider */
        hr {
            border-color: #2d3748;
        }

        /* Botão de logout: destaque suave */
        .logout-button > button {
            background: linear-gradient(90deg, #553c4d, #7a5c6e) !important;
        }
        .logout-button > button:hover {
            background: linear-gradient(90deg, #7a5c6e, #553c4d) !important;
        }

        /* Selectbox */
        .stSelectbox > div > div > div {
            background-color: rgba(35, 42, 54, 0.8);
            color: #f0f2f6;
            border: 1px solid #4a5568;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)


add_custom_css()

ARQUIVO_JOGOS = "jogos.txt"
ARQUIVO_VENDAS = "vendas.txt"

CREDENCIAIS = {
    "admin": {"senha": "admin123", "funcao": "admin"},
    "cliente": {"senha": "cliente123", "funcao": "cliente"}
}


def carregar_jogos():
    jogos = []
    if os.path.exists(ARQUIVO_JOGOS):
        with open(ARQUIVO_JOGOS, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 3:
                    try:
                        preco = float(partes[2])
                    except ValueError:
                        preco = 0.0
                    jogos.append({
                        "nome": partes[0],
                        "genero": partes[1],
                        "preco": preco
                    })
    return jogos


def salvar_jogos(jogos):
    with open(ARQUIVO_JOGOS, "w", encoding="utf-8") as f:
        for j in jogos:
            f.write(f"{j['nome']};{j['genero']};{j['preco']:.2f}\n")


def cadastrar_jogo(nome, genero, preco):
    jogos = carregar_jogos()
    if not any(j["nome"].lower() == nome.lower() for j in jogos):
        jogos.append({"nome": nome, "genero": genero, "preco": float(preco)})
        salvar_jogos(jogos)
        return True
    return False


def listar_jogos():
    return carregar_jogos()


def buscar_jogo(termo):
    jogos = carregar_jogos()
    termo = termo.lower()
    return [j for j in jogos if termo in j["nome"].lower() or termo in j["genero"].lower()]


def atualizar_jogo(nome_antigo, novo_nome, novo_genero, novo_preco):
    jogos = carregar_jogos()
    for j in jogos:
        if j["nome"] == nome_antigo:
            j["nome"] = novo_nome
            j["genero"] = novo_genero
            j["preco"] = float(novo_preco)
            break
    salvar_jogos(jogos)


def registrar_venda(nome_jogo, genero, preco):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARQUIVO_VENDAS, "a", encoding="utf-8") as f:
        f.write(f"{nome_jogo};{genero};{preco:.2f};{data_hora}\n")


def carregar_vendas():
    vendas = []
    if os.path.exists(ARQUIVO_VENDAS):
        with open(ARQUIVO_VENDAS, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 4:
                    try:
                        preco = float(partes[2])
                        data_hora = partes[3]
                    except (ValueError, IndexError):
                        continue
                    vendas.append({
                        "nome": partes[0],
                        "genero": partes[1],
                        "preco": preco,
                        "data_hora": data_hora
                    })
    return vendas


if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.funcao = None


def fazer_logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.funcao = None
    st.rerun()


if not st.session_state.logado:
    st.title(" Login - Loja dos Fuleiros")
    st.write("Digite suas credenciais para acessar:")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in CREDENCIAIS and CREDENCIAIS[usuario]["senha"] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.funcao = CREDENCIAIS[usuario]["funcao"]
            st.success(f"Bem-vindo, {usuario}!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.info("Credenciais de teste:\n\n- **Admin**: `admin` / `admin123`\n- **Cliente**: `cliente` / `cliente123`")

else:
    st.title("🎮 Loja dos Fuleiros")

    with st.sidebar:
        st.write(f"**Logado como:** {st.session_state.usuario} ({st.session_state.funcao})")
        st.markdown('<div class="logout-button">', unsafe_allow_html=True)
        st.button("🚪 Logout", on_click=fazer_logout)
        st.markdown('</div>', unsafe_allow_html=True)

    # Menu com base na função
    if st.session_state.funcao == "admin":
        opcoes_menu = ["Início", "Cadastrar Jogo", "Listar Jogos", "Buscar Jogo", "Atualizar Jogo", "Registrar Venda",
                       "Visualizar Vendas"]
    else:
        opcoes_menu = ["Início", "Listar Jogos", "Buscar Jogo"]

    menu = st.sidebar.selectbox("|Escolha uma opção|", opcoes_menu)

    if menu == "Início":
        st.header(" Bem-vindo ao sistema da Loja dos Fuleiros!")

        if st.session_state.funcao == "admin":
            st.markdown(
                """  
                Você pode:
                - **Cadastrar** novos jogos
                - **Listar** todos os jogos
                - **Buscar** por nome ou gênero
                - **Atualizar** informações de jogos
                - **Registrar vendas**
                - **Visualizar histórico de vendas**

                Use o menu lateral para navegar!
                """
            )
        else:
            st.markdown(
                """  
                Você pode:
                - **Listar** todos os jogos
                - **Buscar** por nome ou gênero

                Use o menu lateral para explorar nosso catálogo!
                """
            )

        jogos = listar_jogos()
        vendas = carregar_vendas()
        if st.session_state.funcao == "admin":
            st.subheader(f" Jogos cadastrados: {len(jogos)} |  Vendas realizadas: {len(vendas)}")
        else:
            st.subheader(f" Jogos cadastrados: {len(jogos)}")

    elif menu == "Cadastrar Jogo":
        st.header(" Cadastrar Novo Jogo")
        nome = st.text_input("Nome do Jogo")
        genero = st.text_input("Gênero (ex: RPG, Ação, Esporte)")
        preco = st.number_input("Preço (R$)", min_value=0.0, step=1.0, format="%.2f")

        if st.button("Cadastrar Jogo"):
            if nome.strip() and genero.strip():
                if cadastrar_jogo(nome.strip(), genero.strip(), preco):
                    st.success("Jogo cadastrado com sucesso!")
                else:
                    st.warning(" Jogo já existe com esse nome!")
            else:
                st.error(" Preencha o nome e o gênero!")

    elif menu == "Listar Jogos":
        st.header(" Todos os Jogos Cadastrados")
        jogos = listar_jogos()
        if jogos:
            for j in jogos:
                st.markdown(
                    f"""
                    <div class="jogo-card">
                        <strong>{j['nome']}</strong> | {j['genero']} | R$ {j['preco']:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Nenhum jogo cadastrado ainda.")

    elif menu == "Buscar Jogo":
        st.header(" Buscar Jogo")
        termo = st.text_input("Digite parte do nome ou gênero")
        if st.button("Buscar"):
            if termo.strip():
                resultados = buscar_jogo(termo.strip())
                if resultados:
                    for j in resultados:
                        st.markdown(
                            f"""
                            <div class="jogo-card">
                                <strong>{j['nome']}</strong> | {j['genero']} | R$ {j['preco']:.2f}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("Nenhum jogo encontrado.")
            else:
                st.error("Digite um termo para buscar!")

    elif menu == "Atualizar Jogo":
        st.header(" Atualizar Jogo")
        jogos = listar_jogos()
        if jogos:
            nomes = [j["nome"] for j in jogos]
            nome_selecionado = st.selectbox("Selecione o jogo para atualizar", nomes)
            jogo_atual = next(j for j in jogos if j["nome"] == nome_selecionado)

            novo_nome = st.text_input("Novo nome", value=jogo_atual["nome"])
            novo_genero = st.text_input("Novo gênero", value=jogo_atual["genero"])
            novo_preco = st.number_input(
                "Novo preço (R$)",
                value=float(jogo_atual["preco"]),
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )

            if st.button("Atualizar Jogo"):
                atualizar_jogo(nome_selecionado, novo_nome, novo_genero, novo_preco)
                st.success(" Jogo atualizado com sucesso!")
        else:
            st.info("Não há jogos para atualizar.")

    elif menu == "Registrar Venda":
        st.header(" Registrar Nova Venda")
        jogos = listar_jogos()
        if not jogos:
            st.warning("Nenhum jogo cadastrado. Cadastre pelo menos um jogo antes de vender.")
        else:
            nomes_jogos = [j["nome"] for j in jogos]
            jogo_selecionado = st.selectbox("Selecione o jogo vendido", nomes_jogos)
            jogo = next(j for j in jogos if j["nome"] == jogo_selecionado)
            st.write(f"**Gênero:** {jogo['genero']} | **Preço:** R$ {jogo['preco']:.2f}")

            if st.button(" Confirmar Venda"):
                registrar_venda(jogo["nome"], jogo["genero"], jogo["preco"])
                st.success(f"Venda de **{jogo['nome']}** registrada com sucesso!")

    elif menu == "Visualizar Vendas":
        st.header(" Histórico de Vendas")
        vendas = carregar_vendas()
        if vendas:
            total_vendas = sum(v["preco"] for v in vendas)
            st.metric("Total em Vendas", f"R$ {total_vendas:.2f}")
            st.divider()
            for v in vendas:
                st.markdown(
                    f"""
                    <div class="venda-card">
                        <strong>{v['nome']}</strong> | {v['genero']} | R$ {v['preco']:.2f} | {v['data_hora']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Nenhuma venda registrada ainda.")
            st.info("Nenhuma venda registrada ainda.")
     

