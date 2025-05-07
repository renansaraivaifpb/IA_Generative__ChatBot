from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

class ChatAssistant:
    """Classe responsável pela configuração e execução do assistente de chat"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.chain = self._setup_chain()
        
    def _load_prompt_template(self):
        """Carrega o template do prompt de um arquivo externo"""
        with open("templates/prompt_template.txt", "r", encoding="utf-8") as file:
            return file.read()
        
    def _setup_chain(self):
        """Configura a cadeia de processamento do LangChain"""
        prompt_template = self._load_prompt_template()
        prompt = PromptTemplate.from_template(prompt_template)
        
        return (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def get_response(self, question):
        """Obtém a resposta para uma pergunta do usuário"""
        return self.chain.invoke(question)
