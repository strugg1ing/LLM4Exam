from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

MODEL_DIR = "./models/paraphrase-multilingual-MiniLM-L12-v2"
# 如果本地没有模型，则自动下载
if not os.path.exists(MODEL_DIR):
    SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2").save(MODEL_DIR)

model = SentenceTransformer(MODEL_DIR)
index = faiss.read_index("vector.index")
with open("id2question.pkl", "rb") as f:
    id2question = pickle.load(f)

def search_similar_questions(query, top_k=5):
    try:
        vec = model.encode([query])
        D, I = index.search(vec, top_k)
        return [id2question[i] for i in I[0] if i >=0]
    except Exception as e:
        print(f"检索失败: {e}")
        return []
