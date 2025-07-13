# 🔧 Sistema de Controle de Acesso - Backend

Backend Django para controle de acesso com ESP32.

## Tecnologias
- Django 5.2.4
- Django REST Framework
- SQLite

## Instalação
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Endpoints principais
- POST /api/access/verify/
- POST /api/login/
- GET /api/users/
- GET /api/logs/

## Configuração
- Edite `core/settings.py` para ajustar `ALLOWED_HOSTS`.

## Integração
- O ESP32 e o frontend Vue.js consomem esta API. 