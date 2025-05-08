# Bibliotecas principais
import streamlit as st                           # Usada para interface web
import os                                        # Permite manipulação de arquivos e diretórios
import asyncio                                   # Suporte a programação assíncrona

# LangChain: carregamento e processamento de documentos
from langchain_community.document_loaders import PyPDFLoader  # Carregador de PDFs
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Divisor de texto inteligente

# LangChain: embeddings e indexação vetorial
from langchain_openai import OpenAIEmbeddings                  # Geração de embeddings usando OpenAI
from langchain_community.vectorstores import FAISS            # Armazena vetores usando FAISS (indexação eficiente)

# Execução paralela para aceleração da carga de arquivos
from concurrent.futures import ProcessPoolExecutor


class DocumentIndexer:
    """Classe responsável por carregar e indexar documentos PDF"""

    def __init__(self, directory, index_path="faiss_index"):
        """
        Inicializa a instância com o diretório onde estão os PDFs
        e o caminho onde o índice FAISS será salvo ou carregado.
        """
        self.directory = directory
        self.index_path = index_path
        self.vector_store = None  # Será preenchido com o FAISS index após o carregamento

    async def _load_pdf_async(self, file_path):
        """
        Método assíncrono para carregar PDFs. 
        Usa uma thread separada para não travar a execução principal.
        """
        loader = PyPDFLoader(file_path)
        return await asyncio.to_thread(loader.load)

    def _load_pdf_sync(self, file_path):
        """
        Método síncrono usado para leitura de arquivos em multiprocessamento.
        """
        loader = PyPDFLoader(file_path)
        return loader.load()

    @st.cache_resource(show_spinner="Indexando documentos...")
    def _index_documents(_self, directory, index_path):
        """
        Indexa documentos PDF de um diretório e retorna o vetor FAISS.
        Usa cache do Streamlit para evitar reprocessamento desnecessário.
        """

        # Se já existe um índice salvo, apenas carrega o FAISS
        if os.path.exists(index_path):
            embeddings = OpenAIEmbeddings()
            return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

        # Lista todos os arquivos PDF no diretório
        pdf_files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.endswith(".pdf")
        ]

        # Carrega os documentos PDF em paralelo usando ProcessPoolExecutor
        documentos = []
        with ProcessPoolExecutor() as executor:
            results = executor.map(_self._load_pdf_sync, pdf_files)
            for result in results:
                documentos.extend(result)  # Cada PDF pode ter múltiplas páginas ou seções

        # Divide os documentos em partes menores com sobreposição
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=350,        # Tamanho máximo de cada pedaço
            chunk_overlap=150      # Sobreposição para manter o contexto
        )
        textos = text_splitter.split_documents(documentos)

        # Gera embeddings dos textos usando OpenAI
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(textos, embeddings)  # Cria o índice FAISS

        # Salva o índice FAISS localmente para uso futuro
        vector_store.save_local(index_path)

        return vector_store  # Retorna o índice vetorial construído

    def get_vector_store(self):
        """
        Retorna o vetor FAISS (índice vetorial) com base nos documentos processados.
        """
        self.vector_store = self._index_documents(self.directory, self.index_path)
        return self.vector_store
