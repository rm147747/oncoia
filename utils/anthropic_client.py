import anthropic
import os
import json
import re

# Schema para extração estruturada
DATA_EXTRACTION_SCHEMA = {
    "patient_demographics": {
        "age": "int",
        "sex": "string (M/F)",
        "weight_kg": "float",
        "height_cm": "float"
    },
    "diagnosis": {
        "primary_tumor": "string",
        "histology": "string",
        "stage_tnm": {
            "T": "string",
            "N": "string",
            "M": "string",
            "stage_group": "string"
        }
    },
    "biomarkers": [
        {
            "name": "string",
            "value": "string",
            "date": "string"
        }
    ],
    "performance_status": {
        "ecog": "int (0-4)"
    },
    "laboratory": {
        "hemoglobin": "float",
        "wbc": "float",
        "creatinine": "float"
    },
    "extraction_confidence": "int (0-100)"
}

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY não encontrada")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def extract_data(self, prontuario):
        """
        Extrai dados estruturados do prontuário em texto
        """
        prompt = f"""Extraia dados estruturados deste prontuário oncológico.

PRONTUÁRIO:
{prontuario}

Retorne JSON seguindo este schema:
{json.dumps(DATA_EXTRACTION_SCHEMA, indent=2)}

INSTRUÇÕES:
- Se um dado não estiver presente, use null
- Seja preciso com números (idade, peso, altura, labs)
- extraction_confidence: 0-100% baseado na clareza dos dados
- Inclua TODOS os biomarcadores encontrados

Retorne APENAS o JSON, sem texto adicional."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        response_text = message.content[0].text
        
        # Extrair JSON da resposta
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text
        
        extracted_data = json.loads(json_str)
        return extracted_data
    
    def extract_data_with_files(self, prontuario_text, uploaded_files):
        """
        Extrai dados estruturados do prontuário texto + arquivos PDF/imagens
        """
        import base64
        
        # Preparar conteúdo da mensagem
        message_content = []
        
        # Adicionar os arquivos primeiro
        for file in uploaded_files:
            # Reset file pointer
            file.seek(0)
            file_bytes = file.read()
            file_base64 = base64.standard_b64encode(file_bytes).decode("utf-8")
            
            if file.type == "application/pdf":
                message_content.append({
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": file_base64
                    }
                })
            elif file.type.startswith("image/"):
                message_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": file.type,
                        "data": file_base64
                    }
                })
            
            # Adicionar contexto sobre o arquivo
            message_content.append({
                "type": "text",
                "text": f"[Arquivo anexado: {file.name}]"
            })
        
        # Adicionar o prontuário texto e instruções
        message_content.append({
            "type": "text",
            "text": f"""Analise TODOS os documentos anexados acima E o prontuário texto abaixo.

PRONTUÁRIO TEXTO:
{prontuario_text}

---

INSTRUÇÕES:
1. Extraia dados de TODOS os documentos (PDFs e imagens)
2. Se encontrar laudos NGS: extraia TODAS mutações, TMB, MSI, PD-L1
3. Se encontrar germline: extraia variantes patogênicas e VUS
4. Se encontrar metabolômica: extraia metabólitos alterados
5. Se encontrar anatomopatológico: extraia IHQ completa (ER, PR, HER2, Ki-67, etc)
6. Se encontrar labs: extraia todos valores com datas
7. Consolide com o prontuário texto

Retorne JSON estruturado conforme o schema:
{json.dumps(DATA_EXTRACTION_SCHEMA, indent=2)}

Retorne APENAS o JSON, sem texto adicional."""
        })
        
        # Chamar Claude
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )
        
        # Processar resposta
        response_text = message.content[0].text
        
        # Extrair JSON
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text
        
        # Parse JSON
        extracted_data = json.loads(json_str)
        
        return extracted_data
    
    def tumor_board_discussion(self, prontuario, extracted_data):
        """Discussão de tumor board"""
        from config.prompts import TUMOR_BOARD_PROMPT
        
        prompt = TUMOR_BOARD_PROMPT.format(
            prontuario=prontuario,
            dados_estruturados=json.dumps(extracted_data, indent=2, ensure_ascii=False)
        )
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def computational_analysis(self, prontuario, extracted_data):
        """Análise oncológica computacional"""
        from config.prompts import COMPUTATIONAL_ONCOLOGY_PROMPT
        
        prompt = COMPUTATIONAL_ONCOLOGY_PROMPT.format(
            prontuario=prontuario,
            dados_estruturados=json.dumps(extracted_data, indent=2, ensure_ascii=False)
        )
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
