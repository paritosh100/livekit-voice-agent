# ingest.py
import os, pickle, numpy as np, faiss
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

DOC_DIR = "../docs"
IDX_PATH = "../rag/faiss.index"
META_PATH = "../rag/meta.pkl"
EMBED_MODEL = "text-embedding-3-small"

def read_docs():
    items=[]
    for r,_,fs in os.walk(DOC_DIR):
        for f in fs:
            p=os.path.join(r,f)
            if f.lower().endswith(".pdf"):
                t=""; 
                for pg in PdfReader(p).pages:
                    t += pg.extract_text() or ""
                items.append((f,t))
            elif f.lower().endswith((".md",".txt")):
                items.append((f, open(p,encoding="utf-8").read()))
    return items

def chunk(s, size=1200, overlap=200):
    out=[]; i=0
    while i < len(s):
        out.append(s[i:i+size]); i += size - overlap
    return out

def main():
    os.makedirs("rag", exist_ok=True)
    client = OpenAI()
    meta=[]; vecs=[]
    for fname, text in read_docs():
        for c in chunk(text):
            emb = client.embeddings.create(model=EMBED_MODEL, input=c).data[0].embedding
            vecs.append(emb); meta.append({"file": fname, "text": c})
    arr = np.array(vecs, dtype="float32"); faiss.normalize_L2(arr)
    idx = faiss.IndexFlatIP(arr.shape[1]); idx.add(arr)
    faiss.write_index(idx, IDX_PATH); pickle.dump(meta, open(META_PATH,"wb"))
    print(f"Indexed {len(meta)} chunks from {len(set(m['file'] for m in meta))} files.")

if __name__ == "__main__":
    main()
