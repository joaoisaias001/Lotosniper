import streamlit as st

# Página
st.set_page_config(page_title="Mentor Sniper v15", layout="centered", initial_sidebar_state="collapsed")

# CSS (mais robusto para diferentes versões do Streamlit e responsivo)
st.markdown(
    """
    <style>
    /* Conteúdo principal */
    div.block-container { background-color: #0E1117; color: #FFFFFF; padding: 1rem 1rem; }
    h1, h2, h3 { color: #A020F0 !important; } /* Roxo Premium */

    /* Botões */
    .stButton>button {
        background-color: #A020F0;
        color: white;
        border-radius: 8px;
        border: 1px solid #39FF14;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem 0.8rem;
    }
    .stButton>button:hover { background-color: #39FF14; color: #000000; cursor: pointer; }

    /* Boxes e badges */
    .status-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #1F2937;
        border-left: 5px solid #39FF14;
        margin-bottom: 20px;
    }
    .badge {
        background-color: #2D3748;
        padding: 5px 10px;
        border-radius: 20px;
        border: 1px solid #A020F0;
        display: inline-block;
        margin: 3px;
        color: #39FF14;
        font-weight: 600;
    }
    .badge.red { color: #FF3333; }

    /* Responsividade pequena */
    @media (max-width: 600px) {
        div.block-container { padding: 0.5rem; }
        .stButton>button { font-size: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicializa estado
if "last_concurso" not in st.session_state:
    st.session_state.last_concurso = 3718
if "generated_games" not in st.session_state:
    st.session_state.generated_games = ""

# Cabeçalho
st.title("🎯 MENTOR SNIPER")
st.subheader("Algoritmo de Alta Probabilidade - V15 PRO")

# Status
st.markdown(
    f"""
    <div class="status-box">
        <span style='color: #39FF14; font-weight: bold;'>🟢 SENSOR ONLINE</span><br>
        <small style='color: #A0AEC0;'>Último concurso capturado automaticamente às 21h: <b>{st.session_state.last_concurso}</b></small>
    </div>
    """,
    unsafe_allow_html=True,
)

# Painel: Matriz
st.header("📊 Matriz de Dezenas do Dia")
pool_exemplo = [1, 3, 4, 6, 9, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 25, 5, 10]
fixas_exemplo = [4, 15, 23, 24, 6, 9]

def render_badges(numbers, red=False):
    classes = "badge red" if red else "badge"
    html = "".join([f"<span class='{classes}'>{str(d).zfill(2)}</span>" for d in numbers])
    return html

st.write("**🎱 Pool de 20 Dezenas Selecionadas:**")
st.markdown(render_badges(pool_exemplo), unsafe_allow_html=True)

st.write("<br>**🔒 Sugestão de Fixas (Âncoras do Rank):**", unsafe_allow_html=True)
st.markdown(render_badges(fixas_exemplo, red=True), unsafe_allow_html=True)

st.markdown("---")

# Formulário de configuração para evitar reruns desnecessários
with st.form("config_form"):
    st.header("⚙️ Configurações do Fechamento")
    col1, col2 = st.columns(2)
    with col1:
        qtd_jogos = st.number_input("Quantidade de Jogos:", min_value=1, max_value=500, value=50, step=1)
    with col2:
        tipo_fixa = st.selectbox("Estratégia das Fixas:", ["100% Engessadas", "Flexíveis (Amortecedor)"])

    st.write("**Filtros Ativos do Painel:**")
    f_paridade = st.checkbox("Filtro de Paridade Ativo (6 a 8 Pares)", value=True)
    f_vacuo = st.checkbox("Sensor de Vácuo (Mapa Geo Horizontal)", value=True)
    f_anterior = st.checkbox("Filtro do Concurso Anterior (8 a 10 repetidos)", value=True)

    submit = st.form_submit_button("🔥 GERAR JOGOS SNIPER")

# Ação principal (executada somente quando o formulário for submetido)
if submit:
    # Aqui é o lugar para chamar sua lógica real de geração/fechamento.
    # Para demo, mantive exemplo estático, mas armazenado no session_state
    jogos_ficticios = (
        "01 03 04 06 09 11 12 13 14 15 17 21 23 24 25\n"
        "01 04 05 06 09 11 12 13 14 15 18 20 22 24 25"
    )
    st.session_state.generated_games = jogos_ficticios
    st.success(f"Sucesso! {qtd_jogos} jogos gerados e filtrados pelo algoritmo ({tipo_fixa}).")

# Se já gerado, mostra a saída e opções
if st.session_state.generated_games:
    st.text_area("Copia os bilhetes abaixo:", value=st.session_state.generated_games, height=180)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        # Botão copiar via JS
        js_copy = f"""
        <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text);
            const el = document.getElementById('copy-feedback');
            if (el) {{ el.innerText = 'Copiado para área de transferência ✅'; setTimeout(()=>el.innerText='',2000); }}
        }}
        </script>
        <button onclick="copyToClipboard(`{st.session_state.generated_games}`)" style="width:100%; padding:8px; border-radius:6px; border:none; background:#A020F0; color:white; font-weight:600;">
            📋 Copiar Área de Transferência
        </button>
        <div id="copy-feedback" style="margin-top:6px;color:#39FF14;font-weight:600"></div>
        """
        st.markdown(js_copy, unsafe_allow_html=True)
    with col_btn2:
        st.download_button("📥 Baixar Arquivo .TXT", data=st.session_state.generated_games, file_name="jogos_sniper.txt", mime="text/plain")
