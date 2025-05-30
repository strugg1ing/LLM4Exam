from sentence_transformers import SentenceTransformer
import faiss, pickle
import os

MODEL_DIR = "./models/paraphrase-multilingual-MiniLM-L12-v2"
# 如果本地没有模型，则自动下载
if not os.path.exists(MODEL_DIR):
    SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2").save(MODEL_DIR)

questions = [
    "什么是勾股定理？它的数学表达式是什么？",
    "如何证明直角三角形斜边上的中线等于斜边的一半？",
    "完全平方公式的展开式是什么？",
    "如何用因式分解法解一元二次方程？",
    "平行四边形有哪些判定方法？",
    "什么是一次函数？它的标准形式是什么？",
    "如何求两个点的中点坐标？",
    "分式的基本性质是什么？",
    "如何计算一组数据的加权平均数？",
    "三角形全等的判定方法有哪些？",
    "什么是算术平方根？如何表示？",
    "二次根式的乘法法则是什么？",
    "如何用代入消元法解二元一次方程组？",
    "菱形的对角线有什么特殊性质？",
    "如何求一次函数图像与坐标轴的交点？",
    "方差的计算公式是什么？它表示什么意义？",
    "如何用尺规作线段的垂直平分线？",
    "分式方程的一般解法步骤是什么？",
    "立方差公式的因式分解形式是什么？",
    "如何判断一个四边形是矩形？",
    "直角坐标系中两点间距离公式是什么？",
    "如何用图像法解二元一次方程组？",
    "等腰三角形有哪些性质？",
    "二次根式加减法的运算步骤是什么？",
    "如何用配方法解一元二次方程？",
    "中位数和众数有什么区别？",
    "如何求多边形的内角和？",
    "轴对称图形有哪些基本性质？",
    "如何用待定系数法求一次函数解析式？",
    "方差和标准差之间有什么关系？"
]
model = SentenceTransformer(MODEL_DIR)
embeddings = model.encode(questions)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

with open("id2question.pkl", "wb") as f:
    pickle.dump({i: q for i, q in enumerate(questions)}, f)

faiss.write_index(index, "vector.index")
