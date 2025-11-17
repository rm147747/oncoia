# 🎗️ OncoIA Clinical Copilot

Sistema de suporte à decisão clínica em oncologia com análise dual: **Tumor Board** e **Oncologia Computacional**.

---

## 👨‍⚕️ Desenvolvedor

**Dr. Raphael Brandão**  
CRM 147.757-SP  
First Oncologia - São Paulo
---

## ✨ Features Principais

### 📋 **Extração Automática de Dados**
- Cole prontuário completo
- Extração estruturada via Claude Sonnet 4
- Validação automática
- Cálculos clínicos (BSA, CrCl, NLR)
- Score de confiança da extração

### 🏥 **Tumor Board Virtual**
- Discussão clínica prática
- Baseado em guidelines (NCCN, ESMO, ASCO)
- Considerações de comorbidades e performance status
- Opções terapêuticas fundamentadas
- Formato de discussão multidisciplinar

### 🔬 **Oncologia Computacional**
- Análise multi-ômica integrada
- Inspirada em Dana-Farber/Harvard approach
- Interpretação de biomarcadores
- Geração de hipóteses científicas
- Avaliação de potencial de pesquisa
- Rigor científico e integridade de dados

---

## 🚀 Como Funciona
```
1. Cole prontuário → 2. Extração automática → 3. Escolha análise:
                                                    ├─ 🏥 Tumor Board
                                                    └─ 🔬 Análise Computacional
```

---

## 📊 Exemplo de Uso

### Input:
```
Paciente feminina, 62 anos, ex-tabagista.
Adenocarcinoma pulmonar T2bN3M1b
PD-L1: 85%, EGFR: wild-type
ECOG: 1
```

### Output Tumor Board:
- Estadiamento validado
- Opções: Pembrolizumab monoterapia (1ª linha)
- Evidências: KEYNOTE-024 (OS: 26.3 vs 13.4m, HR 0.62)
- Considerações práticas

### Output Oncologia Computacional:
- Análise de biomarcadores moleculares
- Estratificação de risco
- Hipóteses sobre resistência
- Sugestões de validação
- Potencial de publicação

---

## 🔒 Segurança & Privacidade

- ✅ Repositório privado
- ✅ Conformidade LGPD (Lei 13.709/2018)
- ✅ Anonimização de dados sensíveis
- ✅ API key nunca exposta (Streamlit Secrets)
- ✅ Disclaimer em todas as análises

---

## 🛠️ Stack Tecnológica

- **Frontend**: Streamlit
- **AI**: Claude Sonnet 4 (Anthropic API)
- **Language**: Python 3.10+
- **Deploy**: Streamlit Community Cloud (gratuito)

---

## 📦 Estrutura do Projeto
```
OncoIA/
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências Python
├── config/
│   ├── settings.py                 # Configurações globais
│   └── prompts.py                  # Prompts especializados
├── utils/
│   └── anthropic_client.py         # Cliente API Claude
├── modules/
│   └── calculations.py             # Cálculos clínicos (BSA, CrCl, NLR)
└── pages/
    ├── 1_Novo_Caso.py              # Extração de dados
    ├── 2_Tumor_Board.py            # Discussão clínica
    └── 3_Analise_Computacional.py  # Análise científica
```

---

## ⚠️ Disclaimer Médico

**Sistema de suporte à decisão clínica.**  
NÃO substitui julgamento clínico individualizado.  
Todas as recomendações devem ser interpretadas por oncologista qualificado,  
considerando contexto completo do paciente, preferências e objetivos de cuidado.

---

## 📖 Princípios Fundamentais

### Tumor Board:
- Guidelines atualizados (NCCN, ESMO, ASCO)
- Pensamento crítico construtivo
- Discussão multidisciplinar
- Considerações práticas

### Oncologia Computacional:
- **NUNCA fabricar dados** ou estatísticas
- Analisar APENAS dados fornecidos
- Declarar limitações explicitamente
- Quantificar incerteza
- Distinguir evidências de hipóteses

---

## 📈 Roadmap

- [x] MVP: Extração + Tumor Board + Análise Computacional
- [ ] Biblioteca de 20+ estudos pivotais
- [ ] Curvas de Kaplan-Meier interativas
- [ ] Comparação quantitativa de tratamentos (NNT/NNH)
- [ ] Parser de NGS/painéis moleculares
- [ ] Integração PubMed API
- [ ] Dashboard analytics
- [ ] Export para prontuário eletrônico

---

## 📄 License

Proprietary - Uso restrito

---

## 📧 Contato

Dr. Raphael Brandão  
CRM 147.757-SP  
First Oncologia - São Paulo

---

**Versão:** 1.0.0  
**Última atualização:** Novembro 2025  
**Powered by:** Claude Sonnet 4 (Anthropic)
```

4. **"Commit changes"** → escreva: `docs: Update README with complete project description`
5. **"Commit changes"**

---

## ✅ VERIFICAÇÃO FINAL

**Seu repositório OncoIA agora tem:**
```
OncoIA/
├── .gitignore
├── README.md ✅
├── app.py ✅
├── requirements.txt ✅
├── config/
│   ├── __init__.py ✅
│   ├── settings.py ✅
│   └── prompts.py ✅
├── utils/
│   ├── __init__.py ✅
│   └── anthropic_client.py ✅
├── modules/
│   ├── __init__.py ✅
│   └── calculations.py ✅
└── pages/
    ├── 1_Novo_Caso.py ✅
    ├── 2_Tumor_Board.py ✅
    └── 3_Analise_Computacional.py ✅
