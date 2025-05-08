import streamlit as st
import os
import asyncio
from document_indexer import DocumentIndexer
from chat_assistant import ChatAssistant
import time

class NormaGPTApp:
    """Classe principal da aplicação Streamlit"""
    
    def __init__(self):
        self._setup_environment()
        self._setup_ui()
        self._setup_session_state()
    
    def _setup_environment(self):
        """Configura variáveis de ambiente"""
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    
    def _setup_ui(self):
        """Configura a interface do usuário"""
        st.title("Normas - Assistente Técnico em Engenharia")
        st.write("Carregue suas normas técnicas e faça perguntas diretamente com base nos documentos.")
        self.directory = st.text_input("Caminho para o diretório de PDFs:", value="normas")
        self.index_path = "faiss_index"  # Caminho fixo para o índice FAISS
    
    def _setup_session_state(self):
        """Inicializa o estado da sessão"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def _display_chat_history(self):
        """Exibe o histórico de mensagens"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    async def _process_user_input(self, assistant):
        """Processa a entrada do usuário e gera a resposta"""
        if user_input := st.chat_input("Digite sua dúvida técnica aqui..."):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Buscando nas normas..."):
                    start_time = time.time()
                    resposta, latency = await assistant.get_response(user_input)
                    end_time = time.time()
                    
                    total_latency = end_time - start_time
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    
                    # Exibe a latência no Streamlit e no terminal
                    st.caption(f"⏱️ Tempo de resposta: {total_latency:.2f} segundos")
                    print(f"Latência total: {total_latency:.2f} segundos | "
                          f"Modelo: {latency:.2f} segundos | "
                          f"Processamento: {total_latency - latency:.2f} segundos")
    
    async def run(self):
        """Executa a aplicação principal"""
        if os.path.exists(self.directory):
            # Indexar documentos
            indexer = DocumentIndexer(self.directory, self.index_path)
            vector_store = indexer.get_vector_store()
            
            # Inicializar assistente
            assistant = ChatAssistant(vector_store)
            
            # Exibir histórico e processar entrada
            self._display_chat_history()
            await self._process_user_input(assistant)
        else:
            st.warning("Por favor, insira um diretório válido contendo arquivos PDF.")

# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = NormaGPTApp()
    asyncio.run(app.run())
