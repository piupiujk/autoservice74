from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user_service_url: str = "http://host.docker.internal:8001"
    product_service_url: str = "http://host.docker.internal:8003"
    order_service_url: str = "http://host.docker.internal:8002"
    timeout: int = 30
    
    model_config = {"env_file": ".env"}

settings = Settings()