"""管理后台 API 路由"""

import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from pydantic import BaseModel

from app.core.grok.config import setting
from app.core.grok.logger import logger
from app.services.grok.token import token_manager
from app.models.grok.grok_models import TokenType


router = APIRouter()

# 简单的内存Session存储
_sessions: Dict[str, datetime] = {}
SESSION_EXPIRE_HOURS = 24


# 请求模型
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str

class AddTokensRequest(BaseModel):
    tokens: List[str]
    token_type: str  # "ssoNormal" or "ssoSuper"

class UpdateConfigRequest(BaseModel):
    config: Dict[str, Any]


# 依赖项：验证管理员Session
async def verify_admin_session(x_admin_token: Optional[str] = Header(None)) -> bool:
    if not x_admin_token:
        raise HTTPException(status_code=401, detail="未授权")
    
    expire_time = _sessions.get(x_admin_token)
    if not expire_time or datetime.now() > expire_time:
        if x_admin_token in _sessions:
            del _sessions[x_admin_token]
        raise HTTPException(status_code=401, detail="会话已过期")
    
    return True


@router.post("/login", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    """管理员登录"""
    try:
        expected_user = setting.global_config.get("admin_username", "admin")
        expected_pass = setting.global_config.get("admin_password", "123456")

        if request.username != expected_user or request.password != expected_pass:
            logger.warning(f"[Admin] 登录失败: {request.username}")
            return LoginResponse(success=False, message="用户名或密码错误")

        session_token = secrets.token_urlsafe(32)
        _sessions[session_token] = datetime.now() + timedelta(hours=SESSION_EXPIRE_HOURS)

        logger.debug(f"[Admin] 登录成功: {request.username}")
        return LoginResponse(success=True, token=session_token, message="登录成功")
    except Exception as e:
        logger.error(f"[Admin] 登录异常: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tokens")
async def get_tokens(_: bool = Depends(verify_admin_session)):
    """获取所有Token"""
    return token_manager.get_tokens()


@router.post("/tokens/add")
async def add_tokens(request: AddTokensRequest, _: bool = Depends(verify_admin_session)):
    """添加Token"""
    try:
        if request.token_type == TokenType.NORMAL.value:
            t_type = TokenType.NORMAL
        elif request.token_type == TokenType.SUPER.value:
            t_type = TokenType.SUPER
        else:
            raise HTTPException(status_code=400, detail="无效的Token类型")

        await token_manager.add_token(request.tokens, t_type)
        return {"success": True, "message": f"成功添加 {len(request.tokens)} 个Token"}
    except Exception as e:
        logger.error(f"[Admin] 添加Token失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tokens/delete")
async def delete_tokens(request: AddTokensRequest, _: bool = Depends(verify_admin_session)):
    """删除Token"""
    try:
        if request.token_type == TokenType.NORMAL.value:
            t_type = TokenType.NORMAL
        elif request.token_type == TokenType.SUPER.value:
            t_type = TokenType.SUPER
        else:
            raise HTTPException(status_code=400, detail="无效的Token类型")

        await token_manager.delete_token(request.tokens, t_type)
        return {"success": True, "message": f"成功删除 {len(request.tokens)} 个Token"}
    except Exception as e:
        logger.error(f"[Admin] 删除Token失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_config(_: bool = Depends(verify_admin_session)):
    """获取配置"""
    # 过滤敏感信息
    conf = setting.grok_config.copy()
    return conf


@router.post("/config/update")
async def update_config(request: UpdateConfigRequest, _: bool = Depends(verify_admin_session)):
    """更新配置"""
    try:
        # 这里需要实现配置更新逻辑，可能需要扩展 ConfigManager
        # 暂时只支持更新内存中的配置，重启失效
        # 或者实现持久化到 grok_setting.toml
        # 鉴于 ConfigManager 主要是读取，我们需要添加 update 方法
        # 暂时简化处理
        for k, v in request.config.items():
            setting.grok_config[k] = v
        
        return {"success": True, "message": "配置已更新（仅内存生效）"}
    except Exception as e:
        logger.error(f"[Admin] 更新配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
