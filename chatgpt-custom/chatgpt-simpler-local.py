import sys
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All

# 1. Get query from command line
query = sys.argv[1]

# 2. Load document
loader = TextLoader("./data/data.txt")

# 3. Use local embeddings (free)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Use a local LLM (free)
llm = GPT4All(model="./models/mistral-7b-instruct-v0.1.Q4_0.gguf")  # Make sure this path points to your model

# 5. Create vector index
index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

# 6. Run query
print(index.query(query, llm=llm))

