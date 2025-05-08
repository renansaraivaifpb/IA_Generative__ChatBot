
# Chat de Norma - Assistente Técnico Baseado em Normas de Engenharia

---

## Descrição

O Chat de Norma é um assistente virtual inteligente especializado em normas técnicas de engenharia elétrica e mecânica. Utilizando processamento de linguagem natural e modelos avançados de IA, o sistema permite:

- Carregar e interpretar normas técnicas em formato PDF

- Responder perguntas técnicas com base no conteúdo dos documentos

- Identificar e citar trechos relevantes das normas

- Oferecer explicações claras e contextualizadas

---

## Visual do ChatBot

Veja a implementação rodando em localhost:

![Tela do Chat Bot no Streamlit](https://raw.githubusercontent.com/renansaraivaifpb/IA_Generative__ChatBot/refs/heads/main/Chat.png)

---

## Funcionalidades

1. Indexação automática de documentos PDF

2. Busca semântica nas normas técnicas

3. Citação de fontes (norma, seção e página)

4. Interface conversacional amigável

5. Respostas rápidas com cache inteligente

---

## Tecnologias Utilizadas

- Python (3.8+)

- Streamlit (Interface web)

- LangChain (Framework para aplicações LLM)

- OpenAI API (Modelos GPT)

- FAISS (Armazenamento vetorial)

## Instalação
- Pré-requisitos
- Python 3.8 ou superior

Conta na OpenAI com chave API válida

### Passo a Passo
1. Clone o repositório (ou baixe diretamente nesse link: (https://github.com/renansaraivaifpb/IA_Generative__ChatBot)

```
git clone https://github.com/renansaraivaifpb/IA_Generative__ChatBot.git
```

2. Crie e ative um ambiente virtual: (opcional)

```
python -m venv venv
source venv/bin/activate  # Linux/MacOS
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Configure suas credenciais:

Substitua # do arquivo /.streamlit/secrets.toml  pelo código abaixo

Mas antes, faça:

**(Remova o caracter (#) inicial e o (#) segundo da key abaixo)** antes de substituir no arquivo:

(OpenAI não permite salvar keys no github).

```
#s#k-proj-rJ7Q8FbkjD1M3vphEZB_M2lG5FDObzDJvcXvSMqoWrzO_j02pZqvQYTDOhOYZc15EDWjx7UYkAT3BlbkFJ6y365c1ltK-UucyEYhCML0c0TzZwodSam7n5RWZCwSHwp89fuPyHzH7ZC2X66ulEQ6sreEr-MA
```

## Como Executar

1. Coloque seus arquivos PDF na pasta normas/

2. Inicie o aplicativo:

```
streamlit run CaseB.py
```

Ou exectur o arquivo normalmente:

```
python run_App.py
```

3. Acesse http://localhost:8501 no seu navegador
