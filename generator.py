from openai import OpenAI

client = OpenAI(
    api_key = "sk-xxxxxx", #替换为真实的key
    base_url = "http://xxxx.xxx.xxx/v1" #替换为ai_url
)

def generate_questions(prompt, context_list, count,subject, grade,type):
    print("==========开始生成试题========")
    # print(f"========Prompt: {prompt}")
    context = "\n".join(context_list)
    # print(f"========Context: {context}")
    full_prompt = f"""你是一名经验丰富的命题老师。参考以下题库与提示并根据你自身的经验生成生成{grade}{subject}的{count}道{type}试题，如果题库与生成要求明显不匹配，则按照你自身的经验。

要求：
1. 题目内容要符合题型要求，不能出现明显错误
2. 知识点分布合理
3. 题目内容要符合{subject}学科的知识体系
4. 题目内容要符合{grade}年级的知识水平 

提示: {prompt}
参考题库:
{context}

输出格式：
1. 每道题目单独一行，题目前加上题目序号
2. 选择题需要包含选项（A、B、C、D），生成的选择题和判断题目题目后面带上空白的（）,生成选项时另起一行
3. 生成的填空题需要给出____
4. 如果是生成内容包含数字或公式，请使用latex代码,避免使用度数的符号表示°，请使用汉字度
5. 只需给出题目内容，不需要其他说明，不要包含markdown的标识符号（例如**，##，```等）
6. 生成题目之前，根据{type}写一段题型描述，例如：判断题（请判断下列陈述是否正确，正确的在题后括号内打“√”，错误的打“×”）；单项选择题(下列每题均有四个选项，其中只有一个选项符合题意。）

"""
    print(f"========Full Prompt: {full_prompt}")
    response = client.chat.completions.create(
        # model="qwen-turbo",
        model="qwen",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7
    )
    print("==========试题生成完成========", response.choices[0].message.content)
    return response.choices[0].message.content

# # 测试用例
# if __name__ == "__main__":
#     prompt = "请生成一道关于机器学习的选择题，包含四个选项和正确答案。"
#     context_list = [
#         "机器学习是人工智能的一个分支，它使计算机能够从数据中学习和改进。",
#         "监督学习和无监督学习是机器学习的两种主要类型。",
#         "常见的机器学习算法包括线性回归、决策树和支持向量机。"
#     ]
#     count = 1
    
#     questions = generate_questions(prompt, context_list, count)
#     print(questions)
