import streamlit as st
import os
from datetime import datetime

ARQUIVO_JOGOS = "jogos.txt"
ARQUIVO_VENDAS = "vendas.txt"


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



st.set_page_config(page_title="🎮 Loja dos Fuleiros", page_icon="🎮")
st.title("🎮 Loja dos Fuleiros")

menu = st.sidebar.selectbox(
    "|Escolha uma opção|",
    ["Início", "Cadastrar Jogo", "Listar Jogos", "Buscar Jogo", "Atualizar Jogo", "Registrar Venda",
     "Visualizar Vendas"]
)

if menu == "Início":
    st.header(" Bem-vindo ao sistema da Loja dos Fuleiros!")
    st.markdown(
        """  
        Você pode:
        - **Cadastrar** novos jogos
        - **Listar** todos os jogos
        - **Buscar** por nome ou gênero
        - **Atualizar** informações
        - **Registrar vendas**
        - **Visualizar histórico de vendas**

        Use o menu lateral para navegar!
        """
    )
    jogos = listar_jogos()
    vendas = carregar_vendas()
    st.subheader(f" Jogos cadastrados: {len(jogos)} |  Vendas realizadas: {len(vendas)}")


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
            st.write(f"**{j['nome']}** |  {j['genero']} |  R$ {j['preco']:.2f}")
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
                    st.write(f"**{j['nome']}** |  {j['genero']} |  R$ {j['preco']:.2f}")
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
            st.write(f"**{v['nome']}** |  {v['genero']} |  R$ {v['preco']:.2f} |  {v['data_hora']}")
    else:
        st.info("Nenhuma venda registrada ainda.")