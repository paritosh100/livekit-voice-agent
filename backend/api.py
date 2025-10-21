from livekit.agents import llm
from livekit.agents.llm import FunctionContext
import faiss, pickle, numpy as np, os
from openai import OpenAI

IDX_PATH = "../rag/faiss.index"
META_PATH = "../rag/meta.pkl"
EMBED_MODEL = "text-embedding-3-small"
SIM_THRESH = 0.30
TOP_K = 4

class AssistantFnc(FunctionContext):
    def __init__(self):
        super().__init__()
        if not (os.path.exists(IDX_PATH) and os.path.exists(META_PATH)):
            raise RuntimeError("RAG index missing. Run `python ingest.py`.")
        self.idx = faiss.read_index(IDX_PATH)
        self.meta = pickle.load(open(META_PATH, "rb"))
        self.client = OpenAI()

    @llm.ai_callable(name="doc_search", description="Retrieve top-k snippets from indexed documents.")
    async def doc_search(self, query: str, k: int = TOP_K) -> str:
        q = self.client.embeddings.create(model=EMBED_MODEL, input=query).data[0].embedding
        q = np.array([q], dtype="float32"); faiss.normalize_L2(q)
        D, I = self.idx.search(q, int(k))
        pairs = [(float(d), int(i)) for d, i in zip(D[0], I[0]) if i != -1 and float(d) >= SIM_THRESH]
        if not pairs:
            return ""
        blocks = []
        for d, i in pairs:
            m = self.meta[i]
            blocks.append(f"[{m['file']}] score={d:.2f}\n{m['text']}")
        return "\n\n---\n\n".join(blocks)

    @llm.ai_callable(name="doc_answer", description="Answer strictly from documents or refuse.")
    async def doc_answer(self, query: str, max_words: int = 80) -> str:
        if not query.strip() or len(query.split()) < 2:
            return "REFUSE: Please ask a specific question about the documents."

        ctx = await self.doc_search(query, k=TOP_K)
        if not ctx:
            return "REFUSE: I can only answer questions about the provided documents."

        clean_ctx = []
        for block in ctx.split("---"):
            lines = block.strip().split("\n")
            if lines and lines[0].startswith("[") and "]" in lines[0]:
                lines = lines[1:]
            clean_ctx.append(" ".join(lines))
        context = "\n".join(clean_ctx)

        return (
            "Use only the following context to answer the user's question."
            "Summarize in under three short sentences."
            "Do not mention sources or filenames."
            f"\n\nContext:\n{context}\n\nQuestion: {query}"
        )
