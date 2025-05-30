from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import search_similar_questions
from generator import generate_questions
from docgen import generate_word_doc
import uuid, os
from typing import List
import uvicorn

app = FastAPI()

# 允许本地静态页面跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 中文序号列表
QUESTION_TYPE_PREFIXES = ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、']

# 定义请求体的数据模型
class QuestionTypeItem(BaseModel):
    type: str
    count: int

class GenerationRequest(BaseModel):
    subject: str
    grade: str
    question_types: List[QuestionTypeItem]  # 题目类型列表
    prompt: str

# 生成试卷接口
@app.post("/generate")
def generate_exam(request: GenerationRequest):
    print(f"-----Received request: {request}----------")
    all_questions = ""
    for index,item in enumerate(request.question_types):
        # 获取对应的中文序号前缀
        if index < len(QUESTION_TYPE_PREFIXES):
            prefix = QUESTION_TYPE_PREFIXES[index]
        else:
            # 如果超过10个题型，使用数字序号
            prefix = f"{index+1}、"
        
        # 检索相似问题作为上下文
        context = search_similar_questions(request.prompt)
        # 判断是否有检索到上下文
        if context:
            prompt = f"{request.prompt}。如无参考题库，请根据常识和通用知识生成。"
            generated = generate_questions(prompt, context, item.count, request.subject,request.grade,item.type)
        else:
            # 没有检索到相关内容，提示模型根据通用知识生成
            prompt = f"{request.prompt}。如无参考题库，请根据常识和通用知识生成。"
            generated = generate_questions(prompt, [], item.count)
        # 添加题型前缀
        all_questions += f"{prefix}{item.type}\n\n{generated}\n\n"

    print(f"all_questions：\n{all_questions}")
    doc_path = generate_word_doc(all_questions, request.subject, request.grade)
    print(f"生成的Word文档路径：{doc_path}")
    return {"file": doc_path}

# 文件下载接口
@app.get("/download")
def download_file(path: str = Query(..., description="Word文档路径")):
    # 返回Word文档文件
    return FileResponse(
        path,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        filename=os.path.basename(path)
    )

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)