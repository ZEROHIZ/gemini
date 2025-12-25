"""Grok 请求处理器 - 适配 Hajimi 的请求到 GrokClient"""

from app.services.grok.client import GrokClient
from app.models.schemas import ChatCompletionRequest, ChatCompletionResponse
from app.core.grok.logger import logger
from fastapi.responses import StreamingResponse
import json

async def grok_chat_completions(request: ChatCompletionRequest):
    """处理 Grok 模型的聊天请求"""
    
    # 转换为字典格式，适配 GrokClient
    # 注意：ChatCompletionRequest 是 Pydantic 模型，可以使用 model_dump() 或 dict()
    request_dict = request.model_dump()
    
    # 确保 stream 字段存在
    request_dict["stream"] = request.stream
    
    logger.info(f"[GrokHandler] 接收请求: Model={request.model}, Stream={request.stream}")
    
    try:
        # 调用 GrokClient
        result = await GrokClient.openai_to_grok(request_dict)
        
        if request.stream:
            # 如果是流式，result 是一个异步生成器
            return StreamingResponse(
                result, 
                media_type="text/event-stream"
            )
        else:
            # 如果是非流式，result 是 OpenAIChatCompletionResponse 对象
            # 需要转换为 Hajimi 的 ChatCompletionResponse
            # 由于两者结构基本一致（都遵循 OpenAI 标准），我们可以尝试直接转换
            # 或者直接返回，FastAPI 会处理 Pydantic 模型
            return result
            
    except Exception as e:
        logger.error(f"[GrokHandler] 处理失败: {e}")
        # 这里可以让上层路由捕获异常并返回 HTTP 错误
        raise e
