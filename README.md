
# Proyecto Integrador · Aplicación Web con IA (Análisis de Sentimientos)

Plataforma web con **Flask** que integra la **API de Hugging Face** para analizar el sentimiento de un texto (multilingüe).

## Características
- Frontend accesible vía navegador (TailwindCDN + HTML).
- Backend en Flask.
- Integración con Hugging Face Inference API (modelo configurable por variable de entorno).
- Validaciones y manejo de errores.

## Requisitos
- Python 3.10+
- Token de Hugging Face (gratuito al crear cuenta): `HUGGINGFACE_API_KEY`

## Instalación y ejecución local
```bash
# 1) Crear entorno virtual (opcional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Variables de entorno
cp .env.example .env
# Edita .env y coloca tu HUGGINGFACE_API_KEY

# 4) Ejecutar
python app.py
# Abrir: http://localhost:5000
```

## Despliegue rápido (Render/railway/otros)
- Define variables: `HUGGINGFACE_API_KEY`, `HF_MODEL`, `PORT`.
- Usa `gunicorn` si lo prefieres, o el servidor de Flask para pruebas.

## Entregables (según rúbrica)
- Código fuente (este repo).
- Video explicativo (problema, demo, API usada e integración, reflexión).
- Manual de Usuario (docs/MANUAL_USUARIO.md).
- Manual del Programador (docs/MANUAL_PROGRAMADOR.md).
