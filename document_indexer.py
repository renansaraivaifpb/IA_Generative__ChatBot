import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class DocumentIndexer:
    """Classe responsável por carregar e indexar documentos PDF"""
    
    def __init__(self, directory):
        self.directory = directory
        
    @st.cache_resource(show_spinner="Indexando documentos...")
    def _index_documents(_self, directory):
        """Método interno para indexação de documentos (com cache)"""
        documentos = []
        for arquivo in os.listdir(directory):
            if arquivo.endswith(".pdf"):
                caminho = os.path.join(directory, arquivo)
                loader = PyPDFLoader(caminho)
                documentos.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=350,
            chunk_overlap=220
        )
        textos = text_splitter.split_documents(documentos)
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(textos, embeddings)
    
    def get_vector_store(self):
        """Obtém o vector store dos documentos indexados"""
        return self._index_documents(self.directory)
