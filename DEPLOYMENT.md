# Nepix Backend - Deployment Guide

## ✅ Production-Ready Configuration

This backend has been refactored for cloud deployment with the following improvements:

### Files Changed

1. **server.py → app.py** (Standard Flask convention)
2. **auth.py** - Updated to use `os.path` instead of `pathlib`
3. **requirements.txt** - Added `gunicorn` for production
4. **Procfile** - Created for cloud platforms (Render, Railway, Heroku)
5. **start.sh** - Updated to use `app.py`

### Key Features

✅ **No external dependencies** - All imports are local
✅ **Environment-aware PORT** - Uses `PORT` env variable
✅ **Production CORS** - Configured for `https://nepix.qzz.io` and localhost
✅ **Gunicorn ready** - Production WSGI server included
✅ **Database auto-creation** - Creates `users.json` if missing

---

## Local Development

### Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
# Option 1: Direct
python app.py

# Option 2: Using start script
./start.sh

# Option 3: Production mode
gunicorn app:app
```

Server will run on `http://localhost:5000`

---

## Cloud Deployment

### Render.com

1. Create new **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `nepix-deploy/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

### Railway.app

1. Create new project
2. Add service from GitHub
3. Configure:
   - **Root Directory**: `nepix-deploy/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Heroku

1. Create new app
2. Add Python buildpack
3. Configure:
   - **Procfile**: Already included
   - Deploy via Git or GitHub integration

---

## Environment Variables

Set these in your cloud platform:

```bash
PORT=5000                    # Auto-set by most platforms
FLASK_ENV=production         # Optional
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/api/health` | Health check |
| POST | `/api/register` | Register new user |
| POST | `/api/login` | User login |
| GET | `/api/user/<id>` | Get user by ID |

---

## CORS Configuration

Currently allows:
- `https://nepix.qzz.io`
- `http://localhost`
- `http://localhost:*` (any port)

To modify, edit `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["your-domain.com"]
    }
})
```

---

## Database

Uses `users.json` flat file database. For production, consider:

1. **PostgreSQL** - Via cloud provider's add-on
2. **MongoDB Atlas** - Free tier available
3. **SQLite** - Built-in, but requires persistent storage

### Persistent Storage

On Render/Railway, add a **Disk** volume:
- Mount path: `/app/users.json`
- This prevents data loss on redeploy

---

## Testing

```bash
# Health check
curl https://your-app.onrender.com/api/health

# Register
curl -X POST https://your-app.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!@#","email":"test@test.com"}'

# Login
curl -X POST https://your-app.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!@#"}'
```

---

## Troubleshooting

### Import errors
- Ensure `auth.py` is in the same directory as `app.py`
- Check Python version (requires 3.7+)

### CORS issues
- Add your frontend domain to allowed origins
- Check browser console for specific errors

### Database not persisting
- Add persistent disk/volume on your cloud platform
- Check file permissions

---

## Next Steps

1. ✅ Code is ready - Deploy to Render/Railway
2. ⚙️ Configure environment variables
3. 🔒 Add HTTPS (automatic on most platforms)
4. 📊 Monitor logs and health endpoint
5. 🗄️ Consider migrating to PostgreSQL for production
