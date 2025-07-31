/**
 * TaskController - Maneja los eventos y coordina entre el modelo y la vista
 */

import { TaskModel } from './task-model.js';
import { TaskView } from './task-view.js';

export class TaskController {
    constructor() {
        this.model = new TaskModel();
        this.view = new TaskView();
        this.init();
    }

    /**
     * Inicializa el controlador
     */
    init() {
        this.loadTasks();
        this.bindEvents();
    }

    /**
     * Vincula todos los eventos del DOM
     */
    bindEvents() {
        // Filtros
        document.getElementById('filterSelect').addEventListener('change', (e) => {
            this.handleFilterChange(e.target.value);
        });

        // Botones principales
        document.getElementById('newTaskBtn').addEventListener('click', () => {
            this.handleNewTaskClick();
        });
        
        document.getElementById('createFirstTaskBtn').addEventListener('click', () => {
            this.handleNewTaskClick();
        });

        // Modal
        document.getElementById('closeModal').addEventListener('click', () => {
            this.handleCloseModal();
        });
        
        document.getElementById('cancelTask').addEventListener('click', () => {
            this.handleCloseModal();
        });
        
        document.getElementById('taskForm').addEventListener('submit', (e) => {
            this.handleFormSubmit(e);
        });

        // Cerrar modal al hacer clic fuera
        document.getElementById('taskModal').addEventListener('click', (e) => {
            if (e.target.id === 'taskModal') {
                this.handleCloseModal();
            }
        });

        // Eventos de mensajes flash
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('flash-close')) {
                this.handleCloseFlashMessage(e.target);
            }
        });
    }

    /**
     * Vincula eventos a las tarjetas de tareas
     */
    bindTaskEvents() {
        // Toggle completion
        document.querySelectorAll('.toggle-task').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = e.currentTarget.dataset.taskId;
                this.handleToggleTask(taskId);
            });
        });

        // Edit task
        document.querySelectorAll('.edit-task').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = e.currentTarget.dataset.taskId;
                this.handleEditTask(taskId);
            });
        });

        // Delete task
        document.querySelectorAll('.delete-task').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = e.currentTarget.dataset.taskId;
                this.handleDeleteTask(taskId);
            });
        });
    }

    // ==================== MANEJADORES DE EVENTOS ====================

    /**
     * Maneja el cambio de filtro
     */
    handleFilterChange(filter) {
        this.model.setFilter(filter);
        this.renderTasks();
    }

    /**
     * Maneja el clic en "Nueva Tarea"
     */
    handleNewTaskClick() {
        this.view.openCreateModal();
    }

    /**
     * Maneja el cierre del modal
     */
    handleCloseModal() {
        this.view.closeModal();
    }

    /**
     * Maneja el envío del formulario
     */
    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const taskData = this.model.prepareTaskData(formData);
        
        // Validar datos
        const validation = this.model.validateTaskData(taskData);
        if (!validation.isValid) {
            this.view.showValidationError(validation.errors);
            return;
        }

        const taskId = formData.get('taskId');
        const isEdit = taskId !== '';

        try {
            // Mostrar modal de carga
            if (isEdit) {
                this.view.showEditLoading();
            } else {
                this.view.showCreateLoading();
            }

            let result;
            if (isEdit) {
                result = await this.model.updateTask(taskId, taskData);
            } else {
                result = await this.model.createTask(taskData);
            }

            if (result.success) {
                this.view.closeModal();
                this.renderTasks();
                // Mostrar flujo de mensajes después del modal de carga
                this.view.hideLoadingModal();
                this.view.showSuccessAfterLoading(result.message);
            } else {
                this.view.showError(result.error);
                this.view.hideLoadingModal();
            }
        } catch (error) {
            console.error('Error:', error);
            this.view.showError('Error al guardar la tarea');
            // En caso de error, forzar el ocultamiento del modal
            this.view.forceHideLoadingModal();
            return;
        }
    }

    /**
     * Maneja el toggle de una tarea
     */
    async handleToggleTask(taskId) {
        try {
            // Mostrar modal de carga
            this.view.showToggleLoading();
            
            const result = await this.model.toggleTask(taskId);
            
            if (result.success) {
                this.renderTasks();
                // Mostrar flujo de mensajes después del modal de carga
                this.view.hideLoadingModal();
                this.view.showSuccessAfterLoading(result.message);
            } else {
                this.view.showError(result.error);
                this.view.hideLoadingModal();
            }
        } catch (error) {
            console.error('Error:', error);
            this.view.showError('Error al cambiar el estado de la tarea');
            // En caso de error, forzar el ocultamiento del modal
            this.view.forceHideLoadingModal();
            return;
        }
    }

    /**
     * Maneja la edición de una tarea
     */
    handleEditTask(taskId) {
        const task = this.model.getTaskById(taskId);
        if (task) {
            this.view.openEditModal(task);
        }
    }

    /**
     * Maneja la eliminación de una tarea
     */
    async handleDeleteTask(taskId) {
        const confirmed = await this.view.showConfirmation(
            '¿Eliminar tarea?',
            'Esta acción no se puede deshacer. ¿Estás seguro de que quieres eliminar esta tarea?'
        );
        
        if (!confirmed) {
            return;
        }

        try {
            // Mostrar modal de carga
            this.view.showDeleteLoading();
            
            const result = await this.model.deleteTask(taskId);
            
            if (result.success) {
                this.renderTasks();
                // Mostrar flujo de mensajes después del modal de carga
                this.view.hideLoadingModal();
                this.view.showSuccessAfterLoading(result.message);
            } else {
                this.view.showError(result.error);
                this.view.hideLoadingModal();
            }
        } catch (error) {
            console.error('Error:', error);
            this.view.showError('Error al eliminar la tarea');
            // En caso de error, forzar el ocultamiento del modal
            this.view.forceHideLoadingModal();
            return;
        }
    }

    /**
     * Maneja el cierre de mensajes flash
     */
    handleCloseFlashMessage(button) {
        const flashMessage = button.closest('.flash-message');
        if (flashMessage) {
            flashMessage.style.opacity = '0';
            flashMessage.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (flashMessage.parentNode) {
                    flashMessage.parentNode.removeChild(flashMessage);
                }
            }, 500);
        }
    }

    // ==================== OPERACIONES PRINCIPALES ====================

    /**
     * Carga las tareas desde la API
     */
    async loadTasks() {
        this.view.showLoading();
        this.view.showInitialLoading();
        
        try {
            const result = await this.model.loadTasks();
            
            if (result.success) {
                this.renderTasks();
            } else {
                this.view.showError(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            this.view.showError('Error de conexión');
            // En caso de error, forzar el ocultamiento del modal
            this.view.forceHideLoadingModal();
            return;
        }
        
        // Ocultar modal de carga solo si no hubo error
        this.view.hideLoading();
        this.view.hideLoadingModal();
    }

    /**
     * Renderiza las tareas en la vista
     */
    renderTasks() {
        const filteredTasks = this.model.getFilteredTasks();
        this.view.renderTasks(filteredTasks);
        this.bindTaskEvents();
    }
} 