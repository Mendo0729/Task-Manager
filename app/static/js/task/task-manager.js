/**
 * TaskManager - Punto de entrada principal para la gestión de tareas
 * Utiliza ES6 modules para separar responsabilidades:
 * - task-model.js: Lógica de datos y comunicación con API
 * - task-view.js: Renderizado y manipulación visual
 * - task-controller.js: Eventos y coordinación
 */

import { TaskController } from './task-controller.js';

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    try {
        new TaskController();
        console.log('✅ TaskManager inicializado correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar TaskManager:', error);
    }
}); 