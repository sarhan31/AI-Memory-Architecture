import time
import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("orchestrator")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Generate request ID
        request_id = f"{int(time.time() * 1000)}"
        
        # Log request
        logger.info(json.dumps({
            "event": "request_received",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown"
        }))
        
        # Process request
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Log response
            logger.info(json.dumps({
                "event": "request_completed",
                "request_id": request_id,
                "status_code": response.status_code,
                "latency_ms": latency_ms
            }))
            
            return response
            
        except Exception as e:
            # Log error
            logger.error(json.dumps({
                "event": "request_failed",
                "request_id": request_id,
                "error": str(e)
            }))
            raise
