"""
Cliente para Anthropic Claude API
"""
import anthropic
from config.settings import ANTHROPIC_API_KEY, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE
from config.prompts import TUMOR_BOARD_PROMPT, COMPUTATIONAL_ONCOLOGY_PROMPT
import json
import streamlit as st

class ClaudeClient:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = DEFAULT_MODEL
    
    def extract_data(self, medical_record: str) -> dict:
        """Extrai dados estruturados de prontuário médico"""
        
        prompt = f"""Você é um assistente médico oncológico especializado.

Extraia dados estruturados deste prontuário em formato JSON.

FORMATO DE SAÍDA (JSON):
{{
  "patient_demographics": {{
    "age": number ou null,
    "sex": "M" | "F" | null,
    "weight_kg": number ou null,
    "height_cm": number ou null
  }},
  "diagnosis": {{
    "primary_tumor": string ou null,
    "histology": string ou null,
    "stage_tnm": {{
      "T": string ou null,
      "N": string ou null,
      "M": string ou null,
      "stage_group": string ou null
    }}
  }},
  "biomarkers": [
    {{"name": string, "value": string}}
  ],
  "performance_status": {{
    "ecog": 0-5 ou null
  }},
  "laboratory": {{
    "hemoglobin": number ou null,
    "wbc": number ou null,
    "platelets": number ou null,
    "creatinine": number ou null
  }},
  "extraction_confidence": 0-100
}}

PRONTUÁRIO:
{medical_record}

Retorne APENAS JSON válido."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # Limpar markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            response_text = response_text.strip()
            data = json.loads(response_text)
            return data
        
        except json.JSONDecodeError as e:
            st.error(f"Erro ao parsear JSON: {e}")
            return None
        except Exception as e:
            st.error(f"Erro na API: {e}")
            return None
    
    def tumor_board_discussion(self, prontuario: str, dados_estruturados: dict) -> str:
        """
        Realiza discussão de caso em formato Tumor Board
        """
        prompt = TUMOR_BOARD_PROMPT.format(
            prontuario=prontuario,
            dados_estruturados=json.dumps(dados_estruturados, indent=2, ensure_ascii=False)
        )
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=8000,  # Mais tokens para análise completa
                temperature=0.3,   # Pouco mais criativo que extração
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        
        except Exception as e:
            st.error(f"Erro na discussão do Tumor Board: {e}")
            return None
    
    def computational_analysis(self, prontuario: str, dados_estruturados: dict) -> str:
        """
        Realiza análise de oncologia computacional
        """
        prompt = COMPUTATIONAL_ONCOLOGY_PROMPT.format(
            prontuario=prontuario,
            dados_estruturados=json.dumps(dados_estruturados, indent=2, ensure_ascii=False)
        )
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=0.2,  # Mais rigor científico
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        
        except Exception as e:
            st.error(f"Erro na análise computacional: {e}")
            return None
