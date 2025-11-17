import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.anthropic_client import ClaudeClient
from modules.calculations import calculate_bsa, calculate_creatinine_clearance

st.set_page_config(page_title="Novo Caso", page_icon="📋", layout="wide")

st.title("📋 Novo Caso Clínico")
st.write("Cole o prontuário completo do paciente")

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
            
            st.success("✅ Dados extraídos com sucesso!")
            
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
            
            # Salvar em session state PRIMEIRO
            st.session_state['extracted_data'] = extracted_data
            st.session_state['prontuario_original'] = prontuario
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro durante extração: {str(e)}")
            with st.expander("Ver detalhes do erro"):
                st.exception(e)
            st.stop()

# ==========================================
# MOSTRAR DADOS SE JÁ FORAM EXTRAÍDOS
# ==========================================
if 'extracted_data' in st.session_state:
    extracted_data = st.session_state['extracted_data']
    demo = extracted_data.get("patient_demographics", {})
    
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
