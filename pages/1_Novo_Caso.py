import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.anthropic_client import ClaudeClient
from modules.calculations import calculate_bsa, calculate_creatinine_clearance

st.set_page_config(page_title="Novo Caso", page_icon="📋", layout="wide")

st.title("📋 Novo Caso Clínico")
st.write("Cole o prontuário completo do paciente")

# ========== NOVO: SEÇÃO DE UPLOAD ==========
st.subheader("📎 Anexar Exames (Opcional)")
st.write("Faça upload de laudos em PDF ou imagens (NGS, germline, metabolômica, anatomopatológico, etc)")

uploaded_files = st.file_uploader(
    "Escolha os arquivos",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
    help="Aceita: PDF, PNG, JPG"
)

# Mostrar arquivos anexados
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} arquivo(s) anexado(s)")
    
    with st.expander("📋 Ver arquivos anexados"):
        for file in uploaded_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"📄 {file.name}")
            col2.write(f"{file.size/1024:.1f} KB")
            col3.write(file.type.split('/')[-1].upper())

st.divider()
# ========== FIM DA SEÇÃO NOVA ==========

# Textarea para prontuário
prontuario = st.text_area(
    "Prontuário Clínico",
    height=400,
    placeholder="""Cole o prontuário completo aqui...

Exemplo:
Paciente feminina, 62 anos, ex-tabagista (40 maços-ano).
Peso: 68kg, Altura: 165cm.

DIAGNÓSTICO: Adenocarcinoma pulmonar
Estadiamento TNM8: T2bN3M1b (Stage IV)
PD-L1 (22C3): TPS 85%
EGFR: wild-type
ECOG: 1

Labs (05/04/2024):
Hemoglobina: 12.3 g/dL
Creatinina: 0.9 mg/dL
Leucócitos: 7.800/mm³
...
"""
)

char_count = len(prontuario)
st.caption(f"📝 {char_count} caracteres")

if char_count < 100 and char_count > 0:
    st.warning("⚠️ Prontuário muito curto. Recomendado: mínimo 300 caracteres.")

# Botões
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("← Voltar"):
        st.switch_page("app.py")

with col2:
    extract_button = st.button(
        "✨ Extrair Dados", 
        type="primary", 
        disabled=(char_count < 50),
        use_container_width=True
    )

# EXTRAÇÃO DOS DADOS
if extract_button:
    with st.spinner("🤖 Extraindo dados estruturados... (~30s)"):
        try:
            client = ClaudeClient()
            extracted_data = client.extract_data(prontuario)
            
            if not extracted_data:
                st.error("❌ Falha na extração. Tente novamente.")
                st.stop()
            
            # Calcular métricas adicionais
            demo = extracted_data.get("patient_demographics", {})
            
            # BSA
            if demo.get("height_cm") and demo.get("weight_kg"):
                bsa = calculate_bsa(demo["height_cm"], demo["weight_kg"])
                demo["bsa_m2"] = bsa
            
            # CrCl
            labs = extracted_data.get("laboratory", {})
            if all([demo.get("age"), demo.get("weight_kg"), 
                   labs.get("creatinine"), demo.get("sex")]):
                crcl = calculate_creatinine_clearance(
                    demo["age"],
                    demo["weight_kg"],
                    labs["creatinine"],
                    demo["sex"]
                )
                labs["crcl_ml_min"] = crcl
            
            # Salvar em session state
            st.session_state['extracted_data'] = extracted_data
            st.session_state['prontuario_original'] = prontuario
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro durante extração: {str(e)}")
            with st.expander("Ver detalhes do erro"):
                st.exception(e)

# ==========================================
# MOSTRAR DADOS EXTRAÍDOS E BOTÕES
# ==========================================
if 'extracted_data' in st.session_state:
    extracted_data = st.session_state['extracted_data']
    demo = extracted_data.get("patient_demographics", {})
    
    st.success("✅ Dados extraídos com sucesso!")
    
    st.subheader("📊 Dados Estruturados")
    
    # Demografia
    with st.expander("👤 Demografia", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Idade", f"{demo.get('age', 'N/A')} anos" if demo.get('age') else "N/A")
        col2.metric("Sexo", demo.get('sex', 'N/A'))
        col3.metric("Peso", f"{demo.get('weight_kg', 'N/A')} kg" if demo.get('weight_kg') else "N/A")
        col4.metric("Altura", f"{demo.get('height_cm', 'N/A')} cm" if demo.get('height_cm') else "N/A")
        if demo.get("bsa_m2"):
            col5.metric("BSA", f"{demo['bsa_m2']} m²")
    
    # Diagnóstico
    with st.expander("🔬 Diagnóstico", expanded=True):
        diag = extracted_data.get("diagnosis", {})
        st.write(f"**Tumor:** {diag.get('primary_tumor', 'N/A')}")
        st.write(f"**Histologia:** {diag.get('histology', 'N/A')}")
        
        tnm = diag.get('stage_tnm', {})
        if tnm and any(tnm.values()):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("T", tnm.get('T', '?'))
            col2.metric("N", tnm.get('N', '?'))
            col3.metric("M", tnm.get('M', '?'))
            col4.metric("Stage", tnm.get('stage_group', '?'))
    
    # Biomarcadores
    biomarkers = extracted_data.get("biomarkers", [])
    if biomarkers:
        with st.expander("🧬 Biomarcadores"):
            for bm in biomarkers:
                st.write(f"• **{bm.get('name')}:** {bm.get('value')}")
    
    # Performance Status
    ps = extracted_data.get("performance_status", {})
    if ps and ps.get('ecog') is not None:
        with st.expander("💪 Performance Status"):
            st.metric("ECOG", ps.get('ecog'))
    
    # Laboratório
    labs = extracted_data.get("laboratory", {})
    if labs and any(labs.values()):
        with st.expander("🧪 Laboratório"):
            col1, col2, col3, col4 = st.columns(4)
            if labs.get('hemoglobin'):
                col1.metric("Hb", f"{labs['hemoglobin']} g/dL")
            if labs.get('wbc'):
                col2.metric("Leuco", f"{labs['wbc']} /mm³")
            if labs.get('creatinine'):
                col3.metric("Creat", f"{labs['creatinine']} mg/dL")
            if labs.get('crcl_ml_min'):
                col4.metric("CrCl", f"{labs['crcl_ml_min']} mL/min")
    
    # Confiança
    st.divider()
    conf = extracted_data.get("extraction_confidence", 0)
    if conf >= 80:
        st.success(f"🎯 Confiança da extração: **{conf}%**")
    elif conf >= 60:
        st.warning(f"⚠️ Confiança da extração: **{conf}%**")
    else:
        st.error(f"❌ Confiança da extração: **{conf}%** (revisar)")
    
    # JSON completo
    with st.expander("🔍 Ver JSON completo"):
        st.json(extracted_data)
    
    # ==========================================
    # BOTÕES DE NAVEGAÇÃO
    # ==========================================
    
    st.divider()
    st.subheader("🎯 Próxima Etapa: Escolha o Tipo de Análise")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                   padding: 1.5rem; border-radius: 10px; color: white; height: 200px;">
            <h3>🏥 Tumor Board</h3>
            <p><strong>Discussão Clínica Prática</strong></p>
            <ul style="font-size: 0.9rem;">
                <li>Guidelines (NCCN, ESMO, ASCO)</li>
                <li>Tomada de decisão terapêutica</li>
                <li>Discussão multidisciplinar</li>
                <li>Considerações práticas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏥 Discutir em Tumor Board", 
                   type="primary", 
                   use_container_width=True,
                   key="tumor_board"):
            st.switch_page("pages/2_Tumor_Board.py")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%); 
                   padding: 1.5rem; border-radius: 10px; color: white; height: 200px;">
            <h3>🔬 Oncologia Computacional</h3>
            <p><strong>Análise Multi-Ômica Profunda</strong></p>
            <ul style="font-size: 0.9rem;">
                <li>Análise bioinformática avançada</li>
                <li>Integração multi-ômica</li>
                <li>Hipóteses científicas</li>
                <li>Potencial de publicação</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Análise Computacional", 
                   use_container_width=True,
                   key="comp_onco"):
            st.switch_page("pages/3_Analise_Computacional.py")
    
    st.info("💡 **Dica:** Você pode fazer ambas as análises. Cada uma oferece perspectivas complementares.")
    
    # Botão para novo caso
    st.divider()
    if st.button("🆕 Analisar Novo Caso"):
        del st.session_state['extracted_data']
        del st.session_state['prontuario_original']
        st.rerun()

# Exemplo
st.divider()
with st.expander("📄 Ver exemplo de prontuário"):
    st.code("""Paciente feminina, 62 anos, ex-tabagista (40 maços-ano).
Peso: 68kg, Altura: 165cm.

DIAGNÓSTICO: Adenocarcinoma pulmonar, lobo superior direito
Data: 15/03/2024
Estadiamento TNM8: T2bN3M1b (Stage IV)

BIOMARCADORES (01/04/2024):
- PD-L1 (22C3): TPS 85%
- EGFR: wild-type
- ALK: negativo
- TMB: 12 mut/Mb

PERFORMANCE STATUS: ECOG 1

LABORATÓRIO (05/04/2024):
- Hemoglobina: 12.3 g/dL
- Leucócitos: 7.800/mm³
- Creatinina: 0.9 mg/dL""", language="text")
