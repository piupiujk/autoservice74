from fastapi import APIRouter, Request, HTTPException
import httpx

from app.config import settings

router = APIRouter()

class ServiceProxy:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
    
    async def proxy(self, method: str, path: str, request: Request):
        # Удаляем начальный слеш из path, так как он уже есть в base_url
        clean_path = path.lstrip('/')
        url = f"{self.base_url}/{clean_path}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url,
                params=request.query_params,
                json=await request.json() if request.method in ("POST", "PUT", "PATCH") else None,
                headers={key: value for key, value in request.headers.items() 
                        if key.lower() not in ["host", "content-length"]}
            )
            
            # Для DELETE запросов возвращаем None при успешном выполнении
            if response.status_code == 204:  # No Content
                return None
                
            if response.status_code >= 400:
                raise HTTPException(response.status_code, response.text)
            
            # Пытаемся распарсить JSON, но если не получается, возвращаем текст
            try:
                return response.json()
            except Exception:
                return {"message": response.text, "status": response.status_code}

# Прокси
user_proxy = ServiceProxy(settings.user_service_url)
product_proxy = ServiceProxy(settings.product_service_url)
order_proxy = ServiceProxy(settings.order_service_url)

@router.api_route("/users{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(path: str, request: Request):
    # Для всех запросов передаем полный путь
    target_path = f"/users{path}"
    return await user_proxy.proxy(request.method, target_path, request)

@router.api_route("/products{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_products(path: str, request: Request):
    # Для POST запросов убираем /products из пути, так как он уже включен в base_url
    target_path = f"/products{path}"
    return await product_proxy.proxy(request.method, target_path, request)

@router.api_route("/orders{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_orders(path: str, request: Request):
    # Для всех запросов передаем полный путь
    target_path = f"/orders{path}"
    return await order_proxy.proxy(request.method, target_path, request)