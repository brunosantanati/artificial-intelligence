import os
import sys

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

query = sys.argv[1]

embeddings = OpenAIEmbeddings()
loader = TextLoader("data/data.txt")
#loader = DirectoryLoader(".", global="*.txt")
index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

print(index.query(query, llm=ChatOpenAI()))
