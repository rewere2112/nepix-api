# 🚀 Guía Rápida: Servidor API

## Iniciar el Servidor API

### Opción 1: Usando el script (Recomendado)
```bash
cd server/api
./start.sh
```

### Opción 2: Manual
```bash
cd server/api
source venv/bin/activate
python app.py
```

El servidor se iniciará en: **http://localhost:5000**

## ⚠️ IMPORTANTE

**DEBES tener el servidor API corriendo para usar las páginas HTML** (Register.html y Login.html).

Si el servidor no está corriendo, verás el mensaje:
```
Error: No se puede conectar con el servidor API
```

## 📋 Verificar que funciona

### 1. Abrir en navegador
http://localhost:5000

Deberías ver:
```json
{
  "name": "Nepix API",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

### 2. Health check
http://localhost:5000/api/health

Deberías ver:
```json
{
  "status": "healthy",
  "message": "Nepix API is running",
  "database": "/path/to/database/users.json"
}
```

## 🎮 Usar la Aplicación

### Páginas Web
1. **Iniciar el servidor API** (ver arriba)
2. Abrir `client/Register.html` o `client/Login.html`
3. Usar normalmente

### Aplicación Python
```bash
cd minecraft_launcher
source venv/bin/activate
python main.py
```

La app Python **NO necesita** el servidor API, accede directamente a `database/users.json`.

## 🔍 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/api/health` | Health check |
| POST | `/api/register` | Registrar usuario |
| POST | `/api/login` | Iniciar sesión |
| GET | `/api/user/<id>` | Obtener usuario por ID |

## 📝 Ejemplos de Uso

### Registrar Usuario (curl)
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123!","email":"test@example.com"}'
```

### Login (curl)
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123!"}'
```

## 🛑 Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está corriendo

## 🐛 Solución de Problemas

### "Address already in use"
El puerto 5000 ya está en uso. Mata el proceso:
```bash
lsof -i :5000
kill -9 <PID>
```

### "Module not found"
Reinstala dependencias:
```bash
cd server/api
source venv/bin/activate
pip install -r requirements.txt
```

### "Database not found"
El servidor crea automáticamente `database/users.json` si no existe.
# nepix-backend
# nepix-backend
# nepix-backend
# nepix-backend
# nepix-backend
# nepix-backend
# nepix-api
# nepix-api
