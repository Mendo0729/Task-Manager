#!/usr/bin/env python3
"""
Script para agregar datos por defecto a la base de datos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.db import db
from app.models.categories import Categories
from app.models.priorities import Priorities

def add_default_data():
    """Agrega categorías y prioridades por defecto"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existen categorías
            existing_categories = Categories.query.count()
            if existing_categories == 0:
                # Agregar categorías por defecto
                default_categories = [
                    "Trabajo",
                    "Personal",
                    "Estudio",
                    "Salud",
                    "Finanzas",
                    "Hogar",
                    "Proyectos",
                    "Otros"
                ]
                
                for category_name in default_categories:
                    category = Categories(category_name=category_name)
                    db.session.add(category)
                
                db.session.commit()
                print(f"✅ Se agregaron {len(default_categories)} categorías por defecto")
            else:
                print(f"✅ Ya existen {existing_categories} categorías en la base de datos")
            
            # Verificar si ya existen prioridades
            existing_priorities = Priorities.query.count()
            if existing_priorities == 0:
                # Agregar prioridades por defecto
                default_priorities = [
                    {"priority_name": "Baja", "priority_level": 1},
                    {"priority_name": "Media", "priority_level": 2},
                    {"priority_name": "Alta", "priority_level": 3}
                ]
                
                for priority_data in default_priorities:
                    priority = Priorities(**priority_data)
                    db.session.add(priority)
                
                db.session.commit()
                print(f"✅ Se agregaron {len(default_priorities)} prioridades por defecto")
            else:
                print(f"✅ Ya existen {existing_priorities} prioridades en la base de datos")
            
            # Mostrar datos actuales
            print("\n📊 Datos actuales en la base de datos:")
            print(f"   Categorías: {Categories.query.count()}")
            print(f"   Prioridades: {Priorities.query.count()}")
            
            # Mostrar categorías
            categories = Categories.query.all()
            print("\n📋 Categorías disponibles:")
            for cat in categories:
                print(f"   - {cat.category_name} (ID: {cat.category_id})")
            
            # Mostrar prioridades
            priorities = Priorities.query.all()
            print("\n🎯 Prioridades disponibles:")
            for pri in priorities:
                print(f"   - {pri.priority_name} (ID: {pri.priority_id}, Nivel: {pri.priority_level})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🔧 Agregando datos por defecto a la base de datos...")
    success = add_default_data()
    
    if success:
        print("\n🎉 Datos agregados exitosamente!")
    else:
        print("\n💥 Error al agregar datos.")
        sys.exit(1) 