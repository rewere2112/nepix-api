"""
Nepix API Server
Provides REST endpoints for authentication
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import auth module from the same directory
import auth

# Set database path to current directory using os.path
auth.USERS_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')

app = Flask(__name__)

# CORS configuration for production
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://nepix.lat",
            "https://nepix.qzz.io",
            "https://nepix.eu.org",                 # Tu dominio personalizado
            "https://rewere2112.github.io",         # Tu GitHub Pages
            "http://localhost:8000",                # Tu servidor local de frontend
            "http://localhost:5000",
            "http://127.0.0.1:8000",
            "null"                                  # Para archivos locales (file://)
        ],
        "supports_credentials": True
    }
})


def validate_request_data(data, required_fields):
    """Validate request data has required fields"""
    if not data:
        return {"success": False, "message": "No se recibieron datos"}, 400
    
    for field in required_fields:
        if not data.get(field, '').strip() if isinstance(data.get(field), str) else not data.get(field):
            return {"success": False, "message": f"{field.capitalize()} es requerido"}, 400
    
    return None


@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user"""
    try:
        data = request.get_json()
        error = validate_request_data(data, ['username', 'password'])
        if error:
            return jsonify(error[0]), error[1]
        
        result = auth.register_user(
            data.get('username', '').strip(),
            data.get('password', ''),
            data.get('email', '').strip()
        )
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        app.logger.error(f"Register error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def api_login():
    """Validate login credentials"""
    try:
        data = request.get_json()
        error = validate_request_data(data, ['username', 'password'])
        if error:
            return jsonify(error[0]), error[1]
        
        user_data = auth.validate_login(
            data.get('username', '').strip(),
            data.get('password', '')
        )
        
        if user_data:
            return jsonify({"success": True, "user": user_data}), 200
        return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401
        
    except Exception as e:
        app.logger.error(f"Login error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/user/<user_id>', methods=['GET'])
def api_get_user(user_id):
    """Get user by ID"""
    try:
        user = auth.get_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
    except Exception as e:
        app.logger.error(f"Get user error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "database": auth.USERS_DB_PATH
    }), 200


@app.route('/')
def index():
    """API info"""
    return jsonify({
        "name": "Nepix API",
        "version": "2.0.0",
        "endpoints": {
            "POST /api/register": "Register user",
            "POST /api/login": "Login",
            "GET /api/user/<id>": "Get user",
            "GET /api/health": "Health check"
        }
    })


if __name__ == '__main__':
    # Ensure database exists
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
    
    if not os.path.exists(db_file):
        with open(db_file, 'w') as f:
            f.write('{"users":{}}')
    
    # Get port from environment variable (cloud platforms set this)
    port = int(os.environ.get("PORT", 5000))
    
    print(f"📁 Database: {db_file}")
    print(f"🚀 API: http://0.0.0.0:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
