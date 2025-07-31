/**
 * TaskModel - Maneja la lógica de datos y comunicación con la API
 */

export class TaskModel {
    constructor() {
        this.tasks = [];
        this.currentFilter = 'all';
        this.authToken = window.authToken || '';
    }

    // Método helper para obtener headers con autenticación
    getAuthHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.authToken}`
        };
    }

    // ==================== GESTIÓN DE DATOS ====================

    /**
     * Carga todas las tareas desde la API
     */
    async loadTasks() {
        try {
            const response = await fetch('/api/tasks', {
                headers: this.getAuthHeaders()
            });
            const data = await response.json();
            
            if (data.success) {
                this.tasks = data.data;
                return { success: true, data: this.tasks };
            } else {
                return { success: false, error: 'Error al cargar las tareas' };
            }
        } catch (error) {
            console.error('Error:', error);
            return { success: false, error: 'Error de conexión' };
        }
    }

    /**
     * Obtiene las tareas filtradas según el filtro actual
     */
    getFilteredTasks() {
        switch (this.currentFilter) {
            case 'pending':
                return this.tasks.filter(task => !task.is_completed);
            case 'completed':
                return this.tasks.filter(task => task.is_completed);
            default:
                return this.tasks;
        }
    }

    /**
     * Obtiene una tarea específica por ID
     */
    getTaskById(taskId) {
        return this.tasks.find(task => task.id == taskId);
    }

    /**
     * Actualiza el filtro actual
     */
    setFilter(filter) {
        this.currentFilter = filter;
    }

    // ==================== OPERACIONES CRUD ====================

    /**
     * Crea una nueva tarea
     */
    async createTask(taskData) {
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(taskData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.tasks.push(data.data);
                return { success: true, data: data.data, message: data.message };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Error:', error);
            return { success: false, error: 'Error al crear la tarea' };
        }
    }

    /**
     * Actualiza una tarea existente
     */
    async updateTask(taskId, taskData) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(taskData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                const taskIndex = this.tasks.findIndex(t => t.id == taskId);
                if (taskIndex !== -1) {
                    this.tasks[taskIndex] = data.data;
                }
                return { success: true, data: data.data, message: data.message };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Error:', error);
            return { success: false, error: 'Error al actualizar la tarea' };
        }
    }

    /**
     * Elimina una tarea
     */
    async deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE',
                headers: this.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.tasks = this.tasks.filter(t => t.id != taskId);
                return { success: true, message: data.message };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Error:', error);
            return { success: false, error: 'Error al eliminar la tarea' };
        }
    }

    /**
     * Cambia el estado de completado de una tarea
     */
    async toggleTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}/toggle`, {
                method: 'PATCH',
                headers: this.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (data.success) {
                const taskIndex = this.tasks.findIndex(t => t.id == taskId);
                if (taskIndex !== -1) {
                    this.tasks[taskIndex].is_completed = data.data.is_completed;
                }
                return { success: true, data: data.data, message: data.message };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Error:', error);
            return { success: false, error: 'Error al cambiar el estado de la tarea' };
        }
    }

    // ==================== VALIDACIONES ====================

    /**
     * Valida los datos de una tarea
     */
    validateTaskData(taskData) {
        const errors = [];

        if (!taskData.title || !taskData.title.trim()) {
            errors.push('El título es requerido');
        }

        if (!taskData.priority_id) {
            errors.push('La prioridad es requerida');
        }

        if (!taskData.category_id) {
            errors.push('La categoría es requerida');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Prepara los datos de la tarea para enviar a la API
     */
    prepareTaskData(formData) {
        return {
            title: formData.get('title'),
            description: formData.get('description'),
            due_date: formData.get('due_date') || null,
            priority_id: parseInt(formData.get('priority_id')),
            category_id: parseInt(formData.get('category_id'))
        };
    }
} 