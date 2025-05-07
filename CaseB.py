import streamlit as st
import os
from document_indexer import DocumentIndexer
from chat_assistant import ChatAssistant

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
    
    def _setup_session_state(self):
        """Inicializa o estado da sessão"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def _display_chat_history(self):
        """Exibe o histórico de mensagens"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def _process_user_input(self, assistant):
        """Processa a entrada do usuário e gera a resposta"""
        if user_input := st.chat_input("Digite sua dúvida técnica aqui..."):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Buscando nas normas..."):
                    resposta = assistant.get_response(user_input)
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    def run(self):
        """Executa a aplicação principal"""
        if os.path.exists(self.directory):
            # Indexar documentos
            indexer = DocumentIndexer(self.directory)
            vector_store = indexer.get_vector_store()
            
            # Inicializar assistente
            assistant = ChatAssistant(vector_store)
            
            # Exibir histórico e processar entrada
            self._display_chat_history()
            self._process_user_input(assistant)
        else:
            st.warning("Por favor, insira um diretório válido contendo arquivos PDF.")

# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = NormaGPTApp()
    app.run()
