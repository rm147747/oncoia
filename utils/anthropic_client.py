"""
Cliente para Anthropic Claude API
"""
import anthropic
from config.settings import ANTHROPIC_API_KEY, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE
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

INSTRUÇÕES:
1. Extraia APENAS informações presentes no texto
2. Use null para dados não encontrados
3. Seja preciso com números e unidades

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
