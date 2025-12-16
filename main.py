import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from http import HTTPStatus
import dashscope

# --- 配置 ---
# 请确保环境变量 DASHSCOPE_API_KEY 已设置，或直接在此处填入（面试演示时可以直接填入，但在生产环境中不推荐）
# os.environ["DASHSCOPE_API_KEY"] = "sk-xxxxxxxxxxxxxx" 

app = FastAPI(title="职能沟通翻译助手")

# 挂载静态文件用于前端展示
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- 数据模型 ---
class TranslationRequest(BaseModel):
    direction: str  # "p2d" (产品转开发) or "d2p" (开发转产品)
    content: str

# --- 提示词设计 (Prompt Engineering) ---
SYSTEM_PROMPT_P2D = """
你是一位拥有10年经验的技术架构师。你的任务是将产品经理的“需求描述”翻译成开发工程师能理解的“技术规范”。
请按照以下结构输出翻译结果：
1. **核心技术拆解**：简述技术实现思路。
2. **算法/技术栈建议**：推荐具体的算法类型（如协同过滤、BERT等）或技术组件。
3. **数据流与处理**：数据来源、ETL流程、实时性/离线处理要求。
4. **性能与评估**：QPS预估、响应时间要求、开发工作量预估（人天）。
5. **潜在风险**：技术难点或边界情况。
注意：保持专业、客观，使用技术术语。
"""

SYSTEM_PROMPT_D2P = """
你是一位拥有商业敏锐度的资深产品总监。你的任务是将开发工程师的“技术方案/更新”翻译成产品经理能理解的“业务价值”。
请按照以下结构输出翻译结果：
1. **业务价值摘要**：用通俗易懂的语言解释这做了什么。
2. **用户体验提升**：具体对用户感知有什么影响（如加载变快、推荐更准）。
3. **商业增长空间**：如何支持DAU增长、留存率或转化率。
4. **成本与效率**：是否降低了服务器成本或提升了运营效率。
5. **下一步建议**：基于此技术优化，产品侧可以配合做什么。
注意：关注ROI（投资回报率）、用户体验和商业目标，避免过多技术黑话。
"""

# --- 核心逻辑 ---
def get_ai_stream(prompt: str, content: str):
    """调用千问API并返回生成器"""
    messages = [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': content}
    ]
    
    try:
        # 使用 qwen-turbo 或 qwen-plus
        responses = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            result_format='message',
            stream=True,
            top_p=0.8
        )
        
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                # 提取增量内容（Dashscope流式返回是全量还是增量取决于具体配置，这里做简易处理）
                # 注意：dashscope python SDK stream 模式下，content 通常是累积的或分段的
                # 为了简化前端处理，我们这里直接输出 content 的最后一段 delta，或者
                # 如果SDK返回的是全量更新，我们需要在前端或后端做 diff。
                # 实际上 Dashscope SDK 的 stream 返回的是逐步完整的 message。
                # 为了演示简单，我们取 content 直接发送，前端渲染可能会有闪烁，
                # 更好的做法是计算 delta，但在 2小时挑战中，直接返回当前完整文本覆盖前端也是一种策略。
                
                # 修正：为了流式效果更好，我们假设 response.output.choices[0].message.content 是累积文本
                # 在这里我们简单地将整个文本作为流发送，前端收到后全量替换(简单粗暴但有效)，
                # 或者你可以尝试只发送 delta，但 Dashscope SDK 标准返回通常是全量的。
                yield response.output.choices[0].message.content
            else:
                yield f"Error: {response.code} - {response.message}"
                
    except Exception as e:
        yield f"Server Error: {str(e)}"

@app.post("/api/translate")
async def translate(request: TranslationRequest):
    if request.direction == "p2d":
        prompt = SYSTEM_PROMPT_P2D
    elif request.direction == "d2p":
        prompt = SYSTEM_PROMPT_D2P
    else:
        raise HTTPException(status_code=400, detail="Invalid direction")

    # 使用 StreamingResponse 实现打字机效果
    # 注意：为了让前端简单地处理，这里我们演示最基础的流式：
    # 实际上 Dashscope 的流式通常返回完整的累积文本。
    # 为了模拟 ChatGPT 的 token 级流动，通常需要计算 delta。
    # 在这个面试 demo 中，为了稳定性，我们让前端处理“不断刷新的全量文本”或后端计算 delta。
    # 下面采用：后端产生数据，前端接收并渲染。
    
    return StreamingResponse(get_ai_stream(prompt, request.content), media_type="text/event-stream")

# 启动入口（方便调试）
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

