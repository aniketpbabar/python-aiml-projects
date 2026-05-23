import os
import glob
from dotenv import load_dotenv
from anthropic import Anthropic
import chromadb

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("docs")

def chunk_text(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

def index_docs():
    for path in glob.glob("data/docs/*.md"):
        with open(path) as f:
            text = f.read()
        for i, chunk in enumerate(chunk_text(text)):
            collection.add(
                ids=[f"{path}-{i}"],
                documents=[chunk],
            )
    print(f"Indexed {collection.count()} chunks.")

def ask(question):
    hits = collection.query(query_texts=[question], n_results=3)
    context = "\n\n".join(hits["documents"][0])
    prompt = f"Answer the question using only this context:\n\n{context}\n\nQuestion: {question}"
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

if collection.count() == 0:
    index_docs()
print(ask("What is the refund policy?"))
