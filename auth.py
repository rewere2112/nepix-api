"""
Módulo de Autenticación para Nepix
Gestiona el registro de usuarios, validación de login y persistencia de datos.
"""

import json
import hashlib
import uuid
import os
from typing import Optional, Dict
from datetime import datetime


# Ruta a la base de datos de usuarios (en el mismo directorio para cloud deployment)
USERS_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')


def _load_users_db() -> Dict:
    """Carga la base de datos de usuarios desde el archivo JSON."""
    if not os.path.exists(USERS_DB_PATH):
        return {"users": {}}
    
    try:
        with open(USERS_DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"users": {}}


def _save_users_db(data: Dict) -> None:
    """Guarda la base de datos de usuarios en el archivo JSON."""
    db_dir = os.path.dirname(USERS_DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    with open(USERS_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_user_id() -> str:
    """Genera un ID de usuario único usando UUID v4."""
    return str(uuid.uuid4())


def validate_password_strength(password: str) -> Dict:
    """
    Valida que la contraseña cumpla con los requisitos de seguridad.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un carácter especial
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Dict con 'valid' (bool) y 'message' (str)
    """
    if len(password) < 8:
        return {
            "valid": False,
            "message": "La contraseña debe tener al menos 8 caracteres"
        }
    
    if not any(c.isupper() for c in password):
        return {
            "valid": False,
            "message": "La contraseña debe contener al menos una letra mayúscula"
        }
    
    if not any(c.islower() for c in password):
        return {
            "valid": False,
            "message": "La contraseña debe contener al menos una letra minúscula"
        }
    
    if not any(c.isdigit() for c in password):
        return {
            "valid": False,
            "message": "La contraseña debe contener al menos un número"
        }
    
    # Caracteres especiales comunes
    special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    if not any(c in special_chars for c in password):
        return {
            "valid": False,
            "message": "La contraseña debe contener al menos un carácter especial (!@#$%^&*...)"
        }
    
    return {
        "valid": True,
        "message": "Contraseña válida"
    }


def hash_password(password: str) -> str:
    """Hashea la contraseña usando SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def register_user(username: str, password: str, email: str = "") -> Dict:
    """
    Registra un nuevo usuario.
    
    Args:
        username: Unique username
        password: Plain text password (will be hashed)
        email: User email (optional)
    
    Returns:
        Dict with 'success' bool and 'message' or 'user' data
    """
    # Validar entrada
    if not username or len(username) < 3:
        return {"success": False, "message": "El usuario debe tener al menos 3 caracteres"}
    
    # Validar fortaleza de contraseña
    password_validation = validate_password_strength(password)
    if not password_validation["valid"]:
        return {"success": False, "message": password_validation["message"]}
    
    # Cargar base de datos
    db = _load_users_db()
    
    # Verificar si el usuario ya existe
    if username in db["users"]:
        return {"success": False, "message": "El usuario ya existe"}
    
    # Crear usuario
    user_id = generate_user_id()
    user_data = {
        "id": user_id,
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    # Guardar en base de datos
    db["users"][username] = user_data
    _save_users_db(db)
    
    return {
        "success": True,
        "message": "Usuario registrado exitosamente",
        "user": {
            "id": user_id,
            "username": username,
            "email": email
        }
    }


def validate_login(username: str, password: str) -> Optional[Dict]:
    """
    Valida las credenciales del usuario.
    
    Args:
        username: Username to validate
        password: Plain text password
    
    Returns:
        User data dict if valid, None if invalid
    """
    db = _load_users_db()
    
    # Verificar si el usuario existe
    if username not in db["users"]:
        return None
    
    user = db["users"][username]
    
    # Validar contraseña
    if user["password_hash"] != hash_password(password):
        return None
    
    # Actualizar último login
    user["last_login"] = datetime.now().isoformat()
    db["users"][username] = user
    _save_users_db(db)
    
    # Retornar datos del usuario (sin hash de contraseña)
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"],
        "last_login": user["last_login"]
    }


def get_user_by_id(user_id: str) -> Optional[Dict]:
    """
    Obtiene datos del usuario por ID.
    
    Args:
        user_id: User ID to search for
    
    Returns:
        User data dict if found, None otherwise
    """
    db = _load_users_db()
    
    for user in db["users"].values():
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"],
                "last_login": user["last_login"]
            }
    
    return None


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Obtiene datos del usuario por nombre de usuario.
    
    Args:
        username: Username to search for
    
    Returns:
        User data dict if found, None otherwise
    """
    db = _load_users_db()
    
    if username in db["users"]:
        user = db["users"][username]
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        }
    
    return None
