"""Grok V1 API 路由"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse

from app.models.grok.openai_schema import OpenAIChatRequest
from app.services.grok.client import GrokClient
from app.core.grok.logger import logger
from app.core.grok.exception import GrokApiException
from app.models.grok.grok_models import Models

router = APIRouter()


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, raw_request: Request):
    """OpenAI 兼容的聊天完成接口"""
    try:
        # 记录请求
        logger.info(f"[API] 收到请求: {request.model}, 流式: {request.stream}")
        
        # 调用客户端
        response = await GrokClient.chat_completions(request)

        if request.stream:
            return StreamingResponse(
                response,
                media_type="text/event-stream"
            )
        else:
            return JSONResponse(content=response.model_dump())

    except GrokApiException as e:
        logger.error(f"[API] 业务异常: {e.message}")
        return JSONResponse(
            status_code=e.status_code,
            content=e.to_dict()
        )
    except Exception as e:
        logger.error(f"[API] 系统异常: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": f"内部服务器错误: {str(e)}",
                    "type": "server_error",
                    "code": "INTERNAL_ERROR"
                }
            }
        )


@router.get("/models")
async def list_models():
    """获取可用模型列表"""
    models = []
    for model_name in Models.get_all_model_names():
        info = Models.get_model_info(model_name)
        models.append({
            "id": model_name,
            "object": "model",
            "created": 1677610602,
            "owned_by": "xai",
            "permission": [],
            "root": model_name,
            "parent": None,
        })
    
    return {
        "object": "list",
        "data": models
    }
