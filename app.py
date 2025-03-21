import streamlit as st

from tokenizacao import processar_texto
from analise_sintatica import analisar_sintaxe
from armazenamento import inserir_frase, recuperar_frases

# Configuração da página em modo escuro e layout de duas colunas
st.set_page_config(page_title="Processador de Frases", layout="wide")

# CSS para customização
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>input {
            background-color: #1e1e1e;
            color: white;
            border-radius: 20px;
            padding: 15px;
            font-size: 18px;
            border: 1px solid #444;
            width: 100%;
        }
        .stButton>button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border-radius: 20px;
            padding: 12px 25px;
            font-size: 18px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #2575fc, #6a11cb);
            transform: scale(1.05);
        }
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        }
        .doc-button-container {
            position: fixed;
            bottom: 20px;
            left: 10px;
            width: 100%;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Layout de duas colunas
st.sidebar.markdown("<div class='sidebar-title'>🔎 Pesquisa</div>", unsafe_allow_html=True)
frase = st.sidebar.text_input("Digite uma frase ou texto para análise:")

buscar = st.sidebar.button("🔍 Analisar")

# Botão de documentação fixado na parte inferior e mais à esquerda
st.sidebar.markdown("""
    <div class='doc-button-container'>
        <a href="https://github.com/alansms/2TIAPY-GRUPO-01-Software" target="_blank">
            <button style='background: linear-gradient(135deg, #6a11cb, #2575fc); color: white; border-radius: 20px; padding: 12px 25px; font-size: 18px; border: none; transition: 0.3s;'>📄 Documentação</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Painel principal
st.title("📊 Resultados da Análise")

if buscar and frase:
    # Executando as etapas do processamento
    tokens_processados = processar_texto(frase)
    analise_sintatica = analisar_sintaxe(tokens_processados)

    # Armazenando no banco de dados
    inserir_frase(frase, " ".join(tokens_processados), "|".join(tokens_processados), str(analise_sintatica))

    # Estatísticas básicas
    num_letras = len(frase.replace(" ", ""))
    num_palavras = len(tokens_processados)
    num_frases = frase.count(".") + frase.count("!") + frase.count("?")

    st.markdown("### 📌 Estatísticas da frase")
    col1, col2, col3 = st.columns(3)
    col1.metric("Letras", num_letras)
    col2.metric("Palavras", num_palavras)
    col3.metric("Frases", num_frases)

    # Seções de processamento
    with st.expander("🔹 Tokenização e Pré-processamento"):
        st.write("Tokens:", tokens_processados)

    with st.expander("🔹 Análise Sintática"):
        st.write("Estrutura Sintática:", analise_sintatica)

    with st.expander("🔹 Armazenamento e Recuperação"):
        frases_armazenadas = recuperar_frases()
        st.write("Frases salvas no banco de dados:", frases_armazenadas)
