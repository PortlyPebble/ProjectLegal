from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
import chromadb

PROMPT_TEMPLATE = """
Explain why the following 3 cases are similiar to the question below, reference the specif parts of the cases that make them similiar to the question:
{context}
+++
Only anwser the following question. What makes the following case similar to the context cases?: 
{question}
"""
 
def query_rag(query_text: str):
    model = OllamaEmbeddings(model="nomic-embed-text")
    query_embedding = model.embed_query([query_text])
    chroma_client = chromadb.PersistentClient(path=".\Website\static\data\my_vectordb") 

    collection = chroma_client.get_collection(name="my_hele_rechtzaak_collection")
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=['documents', 'distances']
    )  
    id = results['ids'][0]
    rechtzaken = results['documents'][0]
 
    formatted_lines = []
    for i in range(len(id)):
        formatted_lines.append(id[i])
        formatted_lines.append("-")
        formatted_lines.append(rechtzaken[i])
        formatted_lines.append("-")

    formatted_lines.pop()
    formatted_string = "\n".join(str(item) for item in formatted_lines)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=formatted_string, question=query_text)

    model = Ollama(model="geitje:7b", base_url="http://ml.hihva.nl:11434")
    response_text = model.invoke(prompt)
    sources = results['ids'][0]
    formatted_response = f"Response: {response_text}\nSources: {sources}\nDistances: {results['distances']}"
    return formatted_response