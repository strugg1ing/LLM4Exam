# LLM4Exam
LLM4Exam is a system designed to help users efficiently and conveniently create exam questions.

## Key Features
- Automatically generates exam questions using large language models
- Supports customizable question types and difficulty levels
- Simplifies the test creation process and improves productivity

## Start
```
# generator.py中替换可用的key和url

pip install -r requirement.txt

python main.py

# 首次启动会自动加载paraphrase-multilingual-MiniLM-L12-v2模型，响应较慢
# 访问本地http://127.0.0.1:8000/
```

## Environment
```
Python==3.8
fastapi>=0.68.0
uvicorn>=0.15.0
python-docx>=0.8.11
sentence-transformers>=0.4.1
faiss-cpu>=1.7.2
openai==1.8.2
pydantic>=1.8.2
python-multipart>=0.0.5
numpy>=1.21.0
```

## Structure
```
LLM4Exam/
├── build_index.py              # Script to build vector index from exam data
├── docgen.py                   # Word layout settings
├── generator.py                # Question or answer generator logic(prompt)
├── id2question.pkl             # Serialized mapping of IDs to questions (pickle format)
├── main.py                     # Main entry point for running the application
├── rag.py                      # Retrieval-Augmented Generation pipeline implementation
├── README.md                   # Project overview and usage instructions
├── requirement.txt             # Python dependencies (note: should be 'requirements.txt')
├── vector.index                # Precomputed vector index for semantic search or retrieval
├── models/                     # Directory for storing  models
├── static/                     # Frontend static assets (HTML, CSS, JS)
│   └── index.html              # Web interface entry point
```