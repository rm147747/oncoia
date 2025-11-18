import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.anthropic_client import ClaudeClient

st.set_page_config(page_title="Tumor Board", page_icon="🏥", layout="wide")

# CSS customizado
st.markdown("""
<style>
    .tumor-board-header {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .discussion-section {
        background: #F9FAFB;
        border-left: 4px solid #10B981;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .discussion-section h3 {
        color: #059669;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="tumor-board-header">
    <h1>🏥 Tumor Board Multidisciplinar</h1>
    <p>Discussão clínica baseada em guidelines (NCCN, ESMO, ASCO)</p>
</div>
""", unsafe_allow_html=True)

# Verificar se tem dados
if 'extracted_data' not in st.session_state or 'prontuario_original' not in st.session_state:
    st.error("⚠️ Nenhum caso carregado. Por favor, volte e extraia os dados primeiro.")
    if st.button("← Voltar para Novo Caso"):
        st.switch_page("pages/1_Novo_Caso.py")
    st.stop()

# Dados do caso
extracted_data = st.session_state['extracted_data']
prontuario = st.session_state['prontuario_original']

# Mostrar resumo do caso
with st.expander("📋 Resumo do Caso", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    demo = extracted_data.get("patient_demographics", {})
    diag = extracted_data.get("diagnosis", {})
    
    with col1:
        st.metric("Idade", f"{demo.get('age', 'N/A')} anos" if demo.get('age') else "N/A")
    with col2:
        st.metric("Sexo", demo.get('sex', 'N/A'))
    with col3:
        st.metric("ECOG", extracted_data.get("performance_status", {}).get('ecog', 'N/A'))
    with col4:
        tnm = diag.get('stage_tnm', {})
        st.metric("Stage", tnm.get('stage_group', 'N/A'))
    
    st.write(f"**Diagnóstico:** {diag.get('primary_tumor', 'N/A')}")

# Botão de análise
st.divider()

if 'tumor_board_result' not in st.session_state:
    st.info("""
    ### 📌 O que esperar desta análise:
    
    - **Discussão crítica** do estadiamento e diagnóstico diferencial
    - **Opções terapêuticas** baseadas em guidelines atualizados
    - **Considerações práticas** sobre comorbidades e performance status
    - **Pontos para discussão** multidisciplinar
    - **Evidências científicas** quando disponíveis
    """)
    
    if st.button("🚀 Iniciar Discussão do Tumor Board", type="primary", use_container_width=True):
        with st.spinner("🤖 Realizando discussão de caso... (~60-90 segundos)"):
            try:
                client = ClaudeClient()
                result = client.tumor_board_discussion(prontuario, extracted_data)
                
                if result:
                    st.session_state['tumor_board_result'] = result
                    st.rerun()
                else:
                    st.error("❌ Erro ao gerar discussão. Tente novamente.")
            
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                with st.expander("Ver detalhes do erro"):
                    st.exception(e)

# Mostrar resultado se já foi gerado
if 'tumor_board_result' in st.session_state:
    st.success("✅ Discussão do Tumor Board concluída!")
    
    # Botões de ação
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🔄 Refazer Discussão"):
            del st.session_state['tumor_board_result']
            st.rerun()
    
    with col2:
        if st.button("🔬 Fazer Análise Computacional"):
            st.session_state['analysis_type'] = 'computational'
            st.switch_page("pages/3_Analise_Computacional.py")
    
    with col3:
        if st.button("← Voltar"):
            st.switch_page("pages/1_Novo_Caso.py")
    
    st.divider()
    
   # Exibir a discussão
st.markdown("### 📝 Discussão Clínica")
st.divider()

# Mostrar o resultado com markdown processado
st.markdown(st.session_state['tumor_board_result'])
    
    # Opção de download
    st.divider()
    st.download_button(
        label="📥 Baixar Discussão (TXT)",
        data=st.session_state['tumor_board_result'],
        file_name=f"tumor_board_{demo.get('age', 'paciente')}anos.txt",
        mime="text/plain"
    )
    
    # Informações adicionais
    st.info("""
    💡 **Próximos Passos Sugeridos:**
    - Validar recomendações com equipe multidisciplinar
    - Verificar disponibilidade de tratamentos sugeridos
    - Considerar ensaios clínicos disponíveis
    - Avaliar preferências e objetivos de cuidado do paciente
    """)

# Sidebar com informações
with st.sidebar:
    st.subheader("ℹ️ Sobre o Tumor Board")
    
    st.write("""
    **Baseado em:**
    - NCCN Guidelines
    - ESMO Clinical Practice Guidelines
    - ASCO Recommendations
    
    **Considera:**
    - Estadiamento adequado
    - Performance status
    - Comorbidades
    - Função orgânica
    - Evidências científicas
    
    **Formato:**
    - Discussão estruturada
    - Pensamento crítico
    - Recomendações práticas
    """)
    
    st.divider()
    
    st.caption("🏥 Tumor Board Virtual")
    st.caption("Powered by Claude Sonnet 4")
