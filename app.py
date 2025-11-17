"""
OncoIA Clinical Copilot
Desenvolvido por: Dr. Raphael Brandão (CRM 147.757-SP)
"""

import streamlit as st
from config.settings import ANTHROPIC_API_KEY, APP_VERSION

st.set_page_config(
    page_title="OncoIA Clinical Copilot",
    page_icon="🎗️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎗️ OncoIA Clinical Copilot</h1>
    <p>Extração Inteligente de Dados Clínicos Oncológicos</p>
</div>
""", unsafe_allow_html=True)

# Check API
if not ANTHROPIC_API_KEY:
    st.error("""
    ⚠️ **API Key não configurada**
    
    Configure nos secrets do Streamlit Cloud:
    Settings → Secrets → Add ANTHROPIC_API_KEY
    """)
    st.stop()

st.success("✅ Sistema configurado!")

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📋 Extração")
    st.write("Cole prontuário e extraia dados estruturados")
    if st.button("🚀 Novo Caso", type="primary"):
        st.switch_page("pages/1_Novo_Caso.py")

with col2:
    st.success("### 📊 Predições")
    st.write("Curvas KM e IC95%")
    st.caption("Em breve")

with col3:
    st.warning("### 🔬 Computational Biology")
    st.write("Análise de NGS")
    st.caption("Em breve")

st.divider()
st.caption(f"Dr. Raphael Brandão - CRM 147.757-SP - v{APP_VERSION}")
