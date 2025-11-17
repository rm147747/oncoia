"""
Configurações globais do OncoIA
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
STUDIES_DIR = DATA_DIR / "studies"

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model settings
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
TEMPERATURE = 0.1

# App metadata
APP_VERSION = "1.0.0"
APP_NAME = "OncoIA Clinical Copilot"
DEVELOPER_NAME = "Dr. Raphael Brandão"
DEVELOPER_CRM = "CRM 147.757-SP"
INSTITUTION = "First Oncologia"
