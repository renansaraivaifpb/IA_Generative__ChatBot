from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import time
import asyncio
from functools import lru_cache

class ChatAssistant:
    """Classe responsável pela configuração e execução do assistente de chat"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3, "fetch_k": 10}  # Otimizado para busca mais rápida
        )
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)  # Usa modelo mais leve
        self.prompt_template = self._load_prompt_template()
        self.chain = self._setup_chain()
        
    def _load_prompt_template(self):
        """Carrega o template do prompt de um arquivo externo"""
        try:
            with open("templates/prompt_template.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "Você é um assistente técnico em engenharia. Responda à pergunta com base no contexto fornecido:\n\nContexto: {context}\n\nPergunta: {question}\n\nResposta:"
        
    def _setup_chain(self):
        """Configura a cadeia de processamento do LangChain"""
        prompt = PromptTemplate.from_template(self.prompt_template)
        
        return (
            {"context": self._cached_retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    @lru_cache(maxsize=100)
    def _cached_retriever(self, question):
        """Cache para resultados de recuperação"""
        return self.retriever.invoke(question)
    
    async def get_response(self, question):
        """Obtém a resposta para uma pergunta do usuário de forma assíncrona"""
        start_time = time.time()
        response = await asyncio.to_thread(self.chain.invoke, question)
        end_time = time.time()
        
        latency = end_time - start_time
        print(f"Latência do modelo: {latency:.2f} segundos")  # Exibe no terminal
        return response, latency
