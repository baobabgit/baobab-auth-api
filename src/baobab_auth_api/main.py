"""Point d'entrée uvicorn pour baobab-auth-api.

:spec: BL-API-010-001
"""

from baobab_auth_api.app import create_app

app = create_app()
