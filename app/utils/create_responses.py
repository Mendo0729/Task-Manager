from datetime import datetime

#-------------------------------RESPONSES-------------------------------
# metodo para estrcturar el patron de las respuestas
def create_response(success=True, data=None, message="", errors=None, status_code=200):
        """Versión mejorada con código de estado HTTP."""
        response = {
            "success": success,
            "data": data if data is not None else {},
            "message": message,
            "errors": errors if errors else {},
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code
        }
        return response