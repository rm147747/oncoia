import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.anthropic_client import ClaudeClient

st.set_page_config(page_title="Oncologia Computacional", page_icon="🔬", layout="wide")

# CSS customizado
st.markdown("""
<style>
    .comp-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .analysis-section {
        background: #F9FAFB;
        border-left: 4px solid #3B82F6;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .analysis-section h3 {
        color: #1E40AF;
        margin-top: 0;
    }
    .warning-box {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="comp-header">
    <h1>🔬 Oncologia Clínica Computacional</h1>
    <p>Análise multi-ômica integrada inspirada em Dana-Farber/Harvard Medical School</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">
        <strong>Abordagem:</strong> Dr. Eliezer Van Allen - 
        Computational Biology, Bioinformatics, AI/ML em Oncologia
    </p>
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
with st.expander("📋 Dados do Caso", expanded=False):
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
    
    # Biomarcadores
    biomarkers = extracted_data.get("biomarkers", [])
    if biomarkers:
        st.write("**Biomarcadores:**")
        for bm in biomarkers:
            st.write(f"- {bm.get('name')}: {bm.get('value')}")

# Disclaimer científico
st.markdown("""
<div class="warning-box">
    <strong>⚠️ IMPORTANTE - Rigor Científico:</strong><br>
    Esta análise segue princípios de integridade científica:
    <ul>
        <li>✓ Analisa APENAS dados explicitamente fornecidos</li>
        <li>✓ Distingue achados estabelecidos de hipóteses</li>
        <li>✓ Declara quando dados são insuficientes</li>
        <li>✓ Quantifica incerteza e limitações estatísticas</li>
        <li>✓ NUNCA fabrica dados, estatísticas ou correlações</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# Botão de análise
if 'computational_result' not in st.session_state:
    st.info("""
    ### 📌 O que esperar desta análise:
    
    - **Avaliação crítica** da qualidade e completude dos dados
    - **Análise estatística e computacional** apropriada para o tipo de dados
    - **Interpretação biológica** de biomarcadores e vias moleculares
    - **Estratificação de risco** e insights prognósticos
    - **Hipóteses científicas** testáveis derivadas dos dados
    - **Recomendações metodológicas** para análises adicionais
    - **Avaliação de potencial** de pesquisa e publicação
    - **Declaração explícita** de limitações e incertezas
    """)
    
    if st.button("🚀 Iniciar Análise Computacional", type="primary", use_container_width=True):
        with st.spinner("🧬 Realizando análise multi-ômica integrada... (~90-120 segundos)"):
            try:
                client = ClaudeClient()
                result = client.computational_analysis(prontuario, extracted_data)
                
                if result:
                    st.session_state['computational_result'] = result
                    st.rerun()
                else:
                    st.error("❌ Erro ao gerar análise. Tente novamente.")
            
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                with st.expander("Ver detalhes do erro"):
                    st.exception(e)

# Mostrar resultado se já foi gerado
if 'computational_result' in st.session_state:
    st.success("✅ Análise computacional concluída!")
    
    # Botões de ação
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🔄 Refazer Análise"):
            del st.session_state['computational_result']
            st.rerun()
    
    with col2:
        if st.button("🏥 Ver Tumor Board"):
            st.session_state['analysis_type'] = 'tumor_board'
            st.switch_page("pages/2_Tumor_Board.py")
    
    with col3:
        if st.button("← Voltar"):
            st.switch_page("pages/1_Novo_Caso.py")
    
    st.divider()
    
    # Exibir a análise
    st.markdown("### 🔬 Análise Oncológica Computacional")
    
    # Mostrar resultado com formatação markdown
    st.markdown(st.session_state['computational_result'])
    
    # Opção de download
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Baixar Análise Completa (TXT)",
            data=st.session_state['computational_result'],
            file_name=f"analise_computacional_{demo.get('age', 'paciente')}anos.txt",
            mime="text/plain"
        )
    
    with col2:
        st.download_button(
            label="📄 Baixar Análise (Markdown)",
            data=st.session_state['computational_result'],
            file_name=f"analise_computacional_{demo.get('age', 'paciente')}anos.md",
            mime="text/markdown"
        )
    
    # Próximos passos sugeridos
    st.info("""
    💡 **Próximos Passos Científicos:**
    - Validar hipóteses em coortes independentes
    - Realizar análises estatísticas adicionais sugeridas
    - Considerar coleta de dados multi-ômicos complementares
    - Avaliar elegibilidade para ensaios clínicos biomarcador-dirigidos
    - Explorar colaborações para validação experimental
    - Considerar submissão para journals especializados
    """)
    
    # Métricas de pesquisa (exemplo)
    st.divider()
    st.subheader("📊 Potencial de Pesquisa")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Originalidade", "Alta", help="Baseado na combinação única de biomarcadores")
    with col2:
        st.metric("Tamanho Amostral", "n=1", delta="-99 para análise robusta", delta_color="inverse")
    with col3:
        st.metric("Qualidade Dados", "Moderada", help="Dados clínicos completos, molecular limitado")
    with col4:
        st.metric("Potencial Publicação", "Case Report", help="Adequado para relato de caso")

# Sidebar com informações
with st.sidebar:
    st.subheader("ℹ️ Sobre a Análise Computacional")
    
    st.write("""
    **Inspirado em:**
    - Dana-Farber Cancer Institute
    - Harvard Medical School
        
    **Integra:**
    - Dados clínicos
    - Biomarcadores moleculares
    - Laboratórios
    - Dados multi-ômicos (quando disponíveis)
    
    **Métodos:**
    - Bioinformática
    - Estatística computacional
    - Machine Learning (quando apropriado)
    - Análise de vias moleculares
    
    **Foco:**
    - Rigor científico
    - Integridade de dados
    - Hipóteses testáveis
    - Aplicabilidade clínica
    """)
    
    st.divider()
    
    st.caption("🔬 Oncologia Computacional")
    st.caption("Powered by Claude Sonnet 4")
    
    st.divider()
    
    st.write("""
    **⚠️ Limitações:**
    - Análise de caso único (n=1)
    - Requer validação em coortes
    - Dados ômicos limitados
    - Predições hipotéticas
    """)
