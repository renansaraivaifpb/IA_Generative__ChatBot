"""
Chat de Normas - Assistente Técnico em Engenharia

Um sistema avançado para consulta e interpretação de normas técnicas com:
- Suporte a múltiplos formatos de documentos (PDF, DOCX, XLSX)
- Recuperação de informação semântica
- Interface conversacional natural
- Referência precisa a normas técnicas
"""

__version__ = "1.2.0"
__author__ = "Renan Saraiva dos Santos"
__email__ = "renan.saraiva@academico.ifpb.edu.br"

# Exportações públicas
from .document_indexer import DocumentIndexer
from .chat_assistant import ChatAssistant
from .CaseB import NormaGPTApp
