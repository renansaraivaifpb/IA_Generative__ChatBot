# Importa as bibliotecas necessárias
import streamlit as st  # Biblioteca para criar interfaces web interativas
import os               # Módulo para interações com o sistema operacional
import asyncio          # Permite operações assíncronas
from document_indexer import DocumentIndexer  # Classe personalizada para indexar documentos
from chat_assistant import ChatAssistant      # Classe personalizada para interagir com o modelo
import time             # Usado para medir tempo de execução

class NormaGPTApp:
    """Classe principal da aplicação Streamlit"""

    def __init__(self):
        # Inicializa o ambiente, interface e estado da sessão
        self._setup_environment()
        self._setup_ui()
        self._setup_session_state()
    
    def _setup_environment(self):
        """Configura variáveis de ambiente"""
        # Define a chave da API do OpenAI a partir dos segredos do Streamlit
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    
    def _setup_ui(self):
        """Configura a interface do usuário"""
        st.title("Normas - Assistente Técnico em Engenharia")  # Título principal
        st.write("Carregue suas normas técnicas e faça perguntas diretamente com base nos documentos.")
        # Campo de entrada para o diretório de PDFs
        self.directory = st.text_input("Caminho para o diretório de PDFs:", value="normas")
        self.index_path = "faiss_index"  # Caminho fixo onde o índice vetorial será salvo
    
    def _setup_session_state(self):
        """Inicializa o estado da sessão"""
        # Cria a variável de mensagens se ainda não existir no estado da sessão
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def _display_chat_history(self):
        """Exibe o histórico de mensagens"""
        # Mostra todas as mensagens anteriores, organizadas por papel (usuário ou assistente)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    async def _process_user_input(self, assistant):
        """Processa a entrada do usuário e gera a resposta"""
        # Verifica se o usuário digitou algo no campo de chat
        if user_input := st.chat_input("Digite sua dúvida técnica aqui..."):
            # Armazena a entrada do usuário no histórico
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Exibe a entrada do usuário
            with st.chat_message("user"):
                st.markdown(user_input)

            # Processa a resposta do assistente com indicador de carregamento
            with st.chat_message("assistant"):
                with st.spinner("Buscando nas normas..."):
                    start_time = time.time()  # Marca o início do tempo
                    resposta, latency = await assistant.get_response(user_input)  # Chama o assistente
                    end_time = time.time()    # Marca o fim do tempo
                    
                    total_latency = end_time - start_time  # Calcula tempo total de resposta
                    st.markdown(resposta)  # Exibe a resposta na interface
                    st.session_state.messages.append({"role": "assistant", "content": resposta})  # Armazena resposta
                    
                    # Mostra o tempo de resposta na interface e imprime no terminal
                    st.caption(f"⏱️ Tempo de resposta: {total_latency:.2f} segundos")
                    print(f"Latência total: {total_latency:.2f} segundos | "
                          f"Modelo: {latency:.2f} segundos | "
                          f"Processamento: {total_latency - latency:.2f} segundos")
    
    async def run(self):
        """Executa a aplicação principal"""
        # Verifica se o diretório informado existe
        if os.path.exists(self.directory):
            # Indexa os documentos encontrados no diretório
            indexer = DocumentIndexer(self.directory, self.index_path)
            vector_store = indexer.get_vector_store()
            
            # Cria uma instância do assistente com os documentos indexados
            assistant = ChatAssistant(vector_store)
            
            # Exibe o histórico e processa a nova entrada do usuário
            self._display_chat_history()
            await self._process_user_input(assistant)
        else:
            # Alerta o usuário caso o diretório seja inválido
            st.warning("Por favor, insira um diretório válido contendo arquivos PDF.")

# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = NormaGPTApp()      # Instancia o app
    asyncio.run(app.run())   # Executa a aplicação de forma assíncrona
