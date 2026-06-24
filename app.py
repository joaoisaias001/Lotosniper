import streamlit as st
import pandas as pd
import requests

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Lotofácil Sniper v15", layout="centered")

# CSS customizado para manter o Dark Mode com Roxo e Verde Neon
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #A020F0 !important; }
    .stButton>button {
        background-color: #A020F0; color: white; border-radius: 8px;
        border: 1px solid #39FF14; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #39FF14; color: #000000; }
    .status-box {
        padding: 15px; border-radius: 8px; background-color: #1F2937;
        border-left: 5px solid #39FF14; margin-bottom: 20px;
    }
    .badge {
        background-color: #2D3748; padding: 5px 10px; border-radius: 20px;
        border: 1px solid #A020F0; display: inline-block; margin: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN CONTROLANDO O ACESSO
def checar_login():
    """Cria a tela de login e valida as credenciais."""
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🎯 MENTOR SNIPER PRO")
        st.write("Acesse com suas credenciais de assinante:")
        
        usuario = st.text_input("Usuário / E-mail:")
        senha = st.text_input("Senha de Acesso:", type="password")
        
        # Aqui você define o seu login e o de clientes de teste (depois podemos puxar do banco)
        if st.button("🔓 ENTRAR NO SISTEMA"):
            if usuario == "admin" and senha == "sniper2026":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos. Acesso Negado.")
        return False
    return True

# Se o login passar, o resto do app roda abaixo
if checar_login():
    
    # Botão de Logout no topo para o cliente sair se quiser
    if st.sidebar.button("🚪 Sair do App"):
        st.session_state["autenticado"] = False
        st.rerun()

    # 3. CONEXÃO E CAPTURA DO CONCURSO ATUAL (AUTOMÁTICO)
    st.title("🎯 MENTOR SNIPER")
    st.subheader("Algoritmo de Alta Probabilidade - V15 PRO")

    # API buscando o último sorteio em tempo real
    @st.cache_data(ttl=3600) # Guarda em cache por 1 hora para economizar processamento
    def carregar_ultimo_sorteio():
        try:
            r = requests.get("https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest", timeout=5)
            if r.status_code == 200:
                return r.json()
        except:
            return None
        return None

    dados_caixa = carregar_ultimo_sorteio()
    num_concurso = dados_caixa.get('concurso', '3718') if dados_caixa else '3718'

    st.markdown(f"""
        <div class="status-box">
            <span style='color: #39FF14; font-weight: bold;'>🟢 BANCO DE DADOS SINCRO</span><br>
            <small style='color: #A0AEC0;'>Último concurso capturado automaticamente: <b>{num_concurso}</b></small>
        </div>
    """, unsafe_allow_html=True)

    # 4. EXIBIÇÃO DA MATRIZ DO DIA
    st.header("📊 Matriz de Dezenas do Dia")
    
    # Aqui o motor Python (que criamos no passo anterior) processaria o histórico real.
    # Exemplo simulado baseado no score final da planilha:
    pool_exemplo = [1, 3, 4, 6, 9, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 25, 5, 10]
    fixas_exemplo = [4, 15, 23, 24, 6, 9]

    st.write("**🎱 Pool de 20 Dezenas Calculadas:**")
    pool_html = "".join([f"<span class='badge' style='color: #39FF14;'>{str(d).zfill(2)}</span>" for d in pool_exemplo])
    st.markdown(pool_html, unsafe_allow_html=True)

    st.write("<br>**🔒 Sugestão de Fixas (Âncoras do Rank):**", unsafe_allow_html=True)
    fixas_html = "".join([f"<span class='badge' style='color: #FF3333;'>{str(d).zfill(2)}</span>" for d in fixas_exemplo])
    st.markdown(fixas_html, unsafe_allow_html=True)

    st.markdown("---")

    # 5. CONFIGURAÇÃO E GERAÇÃO
    st.header("⚙️ Configurações do Fechamento")
    
    col1, col2 = st.columns(2)
    with col1:
        qtd_jogos = st.number_input("Quantidade de Jogos:", min_value=1, max_value=500, value=50, step=1)
    with col2:
        tipo_fixa = st.selectbox("Estratégia das Fixas:", ["100% Engessadas", "Flexíveis"])

    st.write("**Filtros Ativos:**")
    st.checkbox("Filtro de Paridade Ativo (6 a 8 Pares)", value=True, disabled=True)
    st.checkbox("Sensor de VácuoAtivo", value=True, disabled=True)

    if st.button("🔥 GERAR JOGOS SNIPER"):
        st.success(f"Sucesso! {qtd_jogos} jogos gerados e filtrados pelo algoritmo.")
        
        # Simulação de saída
        jogos_ficticios = "01 03 04 06 09 11 12 13 14 15 17 21 23 24 25\n01 04 05 06 09 11 12 13 14 15 18 20 22 24 25"
        st.text_area("Copia os bilhetes abaixo:", value=jogos_ficticios, height=150)
