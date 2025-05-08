# Importa classes e funções necessárias para construir a cadeia de processamento
from langchain_openai import ChatOpenAI                          # Modelo LLM da OpenAI via LangChain
from langchain_core.prompts import PromptTemplate                # Classe para criação de prompts estruturados
from langchain_core.runnables import RunnablePassthrough         # Passa o valor recebido diretamente (usado em pipelines)
from langchain_core.output_parsers import StrOutputParser        # Parser que transforma a saída do modelo em string simples

# Importações utilitárias
import time                                                      # Usado para medir o tempo de execução
import asyncio                                                   # Permite chamadas assíncronas
from functools import lru_cache                                  # Decorador para cache de resultados (memoization)

class ChatAssistant:
    """Classe responsável pela configuração e execução do assistente de chat"""

    def __init__(self, vector_store):
        """
        Inicializa o assistente com a base de conhecimento (vector store).
        """
        self.vector_store = vector_store  # Armazena o vetor indexado dos documentos
        self.retriever = self.vector_store.as_retriever(          # Cria um recuperador de contexto a partir do índice
            search_type="similarity",                             # Busca baseada em similaridade vetorial
            search_kwargs={"k": 3, "fetch_k": 10}                 # Busca 10 vetores e retorna os 3 mais similares
        )
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)  # Inicializa o modelo LLM (menor custo e mais rápido)
        self.prompt_template = self._load_prompt_template()       # Carrega o template do prompt
        self.chain = self._setup_chain()                          # Configura a cadeia de execução LangChain

    def _load_prompt_template(self):
        """
        Carrega o template do prompt de um arquivo externo, se existir.
        Se o arquivo não for encontrado, retorna um prompt padrão.
        """
        try:
            with open("templates/prompt_template.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return (
                "Você é um assistente técnico em engenharia. "
                "Responda à pergunta com base no contexto fornecido:\n\n"
                "Contexto: {context}\n\nPergunta: {question}\n\nResposta:"
            )

    def _setup_chain(self):
        """
        Define a cadeia LangChain de entrada → prompt → modelo → parser de saída.
        """
        prompt = PromptTemplate.from_template(self.prompt_template)  # Usa o template carregado
        return (
            {"context": self._cached_retriever, "question": RunnablePassthrough()}  # Insere contexto recuperado e pergunta original
            | prompt                                                               # Aplica o prompt formatado
            | self.llm                                                             # Envia para o modelo de linguagem
            | StrOutputParser()                                                    # Extrai a resposta como string simples
        )

    @lru_cache(maxsize=100)
    def _cached_retriever(self, question):
        """
        Recuperador com cache: armazena até 100 chamadas anteriores para acelerar respostas repetidas.
        """
        return self.retriever.invoke(question)

    async def get_response(self, question):
        """
        Processa uma pergunta e retorna a resposta do modelo, medindo o tempo de execução.
        """
        start_time = time.time()                                           # Marca o início do tempo
        response = await asyncio.to_thread(self.chain.invoke, question)   # Executa a cadeia em uma thread assíncrona
        end_time = time.time()                                            # Marca o fim do tempo
        
        latency = end_time - start_time                                   # Calcula a latência
        print(f"Latência do modelo: {latency:.2f} segundos")              # Mostra no terminal
        return response, latency                                          # Retorna a resposta e o tempo gasto
