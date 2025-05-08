import streamlit as st
import os
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from concurrent.futures import ProcessPoolExecutor

class DocumentIndexer:
    """Classe responsável por carregar e indexar documentos PDF"""
    
    def __init__(self, directory, index_path="faiss_index"):
        self.directory = directory
        self.index_path = index_path
        self.vector_store = None
        
    async def _load_pdf_async(self, file_path):
        """Carrega um PDF de forma assíncrona"""
        loader = PyPDFLoader(file_path)
        return await asyncio.to_thread(loader.load)
    
    def _load_pdf_sync(self, file_path):
        """Carrega um PDF de forma síncrona para uso em multiprocessing"""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    @st.cache_resource(show_spinner="Indexando documentos...")
    def _index_documents(_self, directory, index_path):
        """Método interno para indexação de documentos (com cache)"""
        # Verifica se o índice FAISS já existe
        if os.path.exists(index_path):
            embeddings = OpenAIEmbeddings()
            return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
        # Lista arquivos PDF
        pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]
        
        # Carrega PDFs em paralelo usando ProcessPoolExecutor
        documentos = []
        with ProcessPoolExecutor() as executor:
            results = executor.map(_self._load_pdf_sync, pdf_files)
            for result in results:
                documentos.extend(result)
        
        # Divide os documentos em pedaços
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=350,
            chunk_overlap=150  # Reduzido para menor sobreposição
        )
        textos = text_splitter.split_documents(documentos)
        
        # Gera embeddings em lotes
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(textos, embeddings)
        
        # Salva o índice para reutilização
        vector_store.save_local(index_path)
        return vector_store
    
    def get_vector_store(self):
        """Obtém o vector store dos documentos indexados"""
        self.vector_store = self._index_documents(self.directory, self.index_path)
        return self.vector_store
