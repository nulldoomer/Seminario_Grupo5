# 🔧 Configuración de Entornos para Deployment

## Variables de Entorno

Para configurar el cliente API en diferentes entornos, usa las siguientes variables:

### Local Development
```bash
# No requiere configuración - usa http://127.0.0.1:8000 por defecto
```

### Docker Local
```bash
export API_URL=http://localhost:8000
```

### Railway Deployment
```bash
# Variables en Railway Dashboard
API_URL=https://tu-app.up.railway.app
```

### Render Deployment
```bash
# Variables en Render Dashboard
API_URL=https://tu-app.onrender.com
```

### Streamlit Cloud
```toml
# En .streamlit/secrets.toml
api_url = "https://tu-api-url.com"
```

### Google Cloud Run (Actual)
```bash
API_URL=https://bank-api-service-216433300622.us-central1.run.app
```

## Configuración por Archivo

### 1. Variables de Entorno (.env)
```bash
# .env
API_URL=http://127.0.0.1:8000
STREAMLIT_RUNTIME_ENV=development
```

### 2. Streamlit Secrets (.streamlit/secrets.toml)
```toml
[api]
url = "http://127.0.0.1:8000"

[database]
# Configuraciones futuras
```

### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      
  dashboard:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api
```

## Prioridad de Configuración

El cliente API usa el siguiente orden de prioridad:

1. **Parámetro directo**: `APIClient(base_url="...")`
2. **Variable de entorno**: `API_URL`
3. **Streamlit secrets**: `st.secrets["api_url"]`
4. **Detección automática**: Streamlit Cloud → URL de producción
5. **Default local**: `http://127.0.0.1:8000`

## Verificación de Conectividad

El cliente API incluye verificación automática:

```python
# En el código
client = get_api_client()
connection_info = client.test_connection()

if connection_info["connected"]:
    print(f"✅ API disponible en {connection_info['url']}")
else:
    print(f"❌ {connection_info['message']}")
```

## URLs por Entorno

| Entorno | URL | Puerto | Notas |
|---------|-----|---------|-------|
| **Local Dev** | `http://127.0.0.1:8000` | 8000 | Default |
| **Docker Local** | `http://localhost:8000` | 8000 | Host local |
| **Railway** | `https://app.up.railway.app` | 443 | HTTPS |
| **Render** | `https://app.onrender.com` | 443 | HTTPS |
| **Google Cloud** | `https://bank-api-service-...` | 443 | Actual |
| **Vercel** | `https://app.vercel.app` | 443 | Solo frontend |

## Troubleshooting

### Error: "Connection refused"
- Verificar que el API esté ejecutándose
- Confirmar puerto correcto (8000)
- Revisar firewall/antivirus

### Error: "404 Not Found" 
- Verificar endpoints del API
- Confirmar versión correcta
- Revisar logs del servidor

### Error: "CORS"
- Configurar CORS en FastAPI
- Agregar origen de Streamlit

### Error: "Timeout"
- Aumentar timeout en cliente
- Verificar red/VPN
- Revisar performance del API