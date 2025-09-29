
import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF

st.set_page_config(page_title="Brandskyddsbot", page_icon="🔥", layout="wide")
st.title("🔥 Brandskyddsbot (källa-låst)")

@st.cache_resource
def get_state():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    idx = None
    texts = []
    meta = []
    return model, idx, texts, meta

model, index, texts, meta = get_state()

with st.sidebar:
    st.header("Dokument")
    uploaded_files = st.file_uploader("Ladda upp PDF (BFS/AFS/BSB)", type=["pdf"], accept_multiple_files=True)
    build = st.button("Bygg index")

def add_pdf_to_index(file, filename):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    chunks, metas = [], []
    for pno in range(len(doc)):
        txt = (doc[pno].get_text("text") or "").strip()
        if not txt:
            continue
        words = txt.split()
        for i in range(0, len(words), 200):
            piece = " ".join(words[i:i+200])
            chunks.append(piece)
            metas.append((filename, pno+1))
    return chunks, metas

if build and uploaded_files:
    new_chunks, new_metas = [], []
    for f in uploaded_files:
        c, m = add_pdf_to_index(f, f.name)
        new_chunks.extend(c); new_metas.extend(m)
        st.success(f"📄 {f.name}: indexerat {len(c)} textbitar")
    if new_chunks:
        embs = model.encode(new_chunks, normalize_embeddings=True)
        if index is None:
            dim = embs.shape[1]
            idx = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(embs)
            idx.add(embs.astype(np.float32))
            index = idx
        else:
            faiss.normalize_L2(embs)
            index.add(embs.astype(np.float32))
        texts.extend(new_chunks); meta.extend(new_metas)
        st.session_state["index"] = index
        st.session_state["texts"] = texts
        st.session_state["meta"] = meta

index = st.session_state.get("index", index)
texts = st.session_state.get("texts", texts)
meta = st.session_state.get("meta", meta)

st.divider()
q = st.text_input("❓ Ställ en fråga (boten svarar ENDAST utifrån dina källor):")

if q:
    if index is None:
        st.warning("⚠ Ladda upp PDF:er och klicka 'Bygg index' först.")
    else:
        q_emb = model.encode([q], normalize_embeddings=True).astype(np.float32)
        sims, ids = index.search(q_emb, 10)
        sims, ids = sims[0], ids[0]

        COS_MIN, MIN_HITS = 0.25, 2
        ctx = []
        used = set()
        for s, i in zip(sims, ids):
            if i == -1 or s < COS_MIN or i in used:
                continue
            used.add(i)
            src, page = meta[i]
            ctx.append({"source": src, "page": int(page), "excerpt": texts[i]})

        if len(ctx) < MIN_HITS:
            st.warning("⚠ Jag kan inte bedöma detta utan relevant källa. Ladda upp rätt handlingar.")
        else:
            st.subheader("📑 Källunderlag (urval)")
            for c in ctx[:5]:
                st.markdown(f"**Källa:** {c['source']} (s. {c['page']})")
                st.write(c['excerpt'])
                st.divider()
