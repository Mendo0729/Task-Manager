#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a la base de datos y el modelo User
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.db import db
from app.models.user import User
from app.models.task import Tasks

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            # Probar conexión
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            
            # Probar modelo User
            users = User.query.all()
            print(f"✅ Modelo User funciona. Usuarios encontrados: {len(users)}")
            
            # Probar propiedad id
            if users:
                user = users[0]
                print(f"✅ Propiedad id funciona: {user.id}")
                print(f"✅ user_id: {user.user_id}")
                print(f"✅ username: {user.username}")
            
            # Probar modelo Tasks
            tasks = Tasks.query.all()
            print(f"✅ Modelo Tasks funciona. Tareas encontradas: {len(tasks)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos...")
    success = test_database_connection()
    
    if success:
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
    else:
        print("\n💥 Algunas pruebas fallaron.")
        sys.exit(1) 