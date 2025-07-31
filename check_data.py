#!/usr/bin/env python3
"""
Script para verificar categorías y prioridades en la base de datos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.db import db
from app.models.categories import Categories
from app.models.priorities import Priorities

def check_data():
    """Verifica las categorías y prioridades en la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar categorías
            categories = Categories.query.all()
            print(f"📋 Categorías ({len(categories)}):")
            for cat in categories:
                print(f"   - {cat.category_name} (ID: {cat.category_id})")
            
            print()
            
            # Verificar prioridades
            priorities = Priorities.query.all()
            print(f"🎯 Prioridades ({len(priorities)}):")
            for pri in priorities:
                print(f"   - {pri.priority_name} (ID: {pri.priority_id}, Nivel: {pri.priority_level})")
            
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

if __name__ == "__main__":
    print("🔍 Verificando datos en la base de datos...")
    success = check_data()
    
    if success:
        print("\n✅ Verificación completada!")
    else:
        print("\n💥 Error en la verificación.")
        sys.exit(1) 