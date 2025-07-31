/**
 * TaskView - Maneja el renderizado y la manipulación visual de la interfaz
 */

export class TaskView {

    // ==================== RENDERIZADO DE TAREAS ====================

    /**
     * Renderiza la lista de tareas
     */
    renderTasks(tasks) {
        if (tasks.length === 0) {
            this.showEmptyState();
            return;
        }

        this.hideEmptyState();
        this.elements.tasksGrid.innerHTML = tasks.map(task => this.createTaskCard(task)).join('');
    }

    /**
     * Crea el HTML de una tarjeta de tarea
     */
    createTaskCard(task) {
        const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString('es-ES') : 'Sin fecha';
        const isCompleted = task.is_completed;
        
        return `
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 ${isCompleted ? 'border-green-500' : 'border-blue-500'}" data-task-id="${task.id}">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 ${isCompleted ? 'line-through text-gray-500' : ''}">
                        ${task.title}
                    </h3>
                    <div class="flex space-x-2">
                        <button class="toggle-task text-sm px-2 py-1 rounded ${isCompleted ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}" data-task-id="${task.id}">
                            ${isCompleted ? '✓' : '○'}
                        </button>
                    </div>
                </div>
                
                ${task.description ? `
                <p class="text-gray-600 mb-4 ${isCompleted ? 'line-through' : ''}">
                    ${task.description.length > 100 ? task.description.substring(0, 100) + '...' : task.description}
                </p>
                ` : ''}
                
                <div class="flex justify-between items-center text-sm text-gray-500">
                    <span>📅 ${dueDate}</span>
                    <div class="flex space-x-2">
                        <button class="edit-task text-primary-600 hover:text-primary-800" data-task-id="${task.id}">Editar</button>
                        <button class="delete-task text-red-600 hover:text-red-800" data-task-id="${task.id}">Eliminar</button>
                    </div>
                </div>
            </div>
        `;
    }

    // ==================== ESTADOS DE LA INTERFAZ ====================

    /**
     * Muestra el estado de carga
     */
    showLoading() {
        this.elements.loadingState.classList.remove('hidden');
        this.elements.tasksContainer.classList.add('hidden');
        this.elements.emptyState.classList.add('hidden');
    }

    /**
     * Oculta el estado de carga
     */
    hideLoading() {
        this.elements.loadingState.classList.add('hidden');
    }

    /**
     * Muestra el estado vacío
     */
    showEmptyState() {
        this.elements.tasksContainer.classList.add('hidden');
        this.elements.emptyState.classList.remove('hidden');
    }

    /**
     * Oculta el estado vacío
     */
    hideEmptyState() {
        this.elements.tasksContainer.classList.remove('hidden');
        this.elements.emptyState.classList.add('hidden');
    }

    // ==================== GESTIÓN DEL MODAL ====================

    /**
     * Abre el modal para crear una nueva tarea
     */
    openCreateModal() {
        this.elements.modalTitle.textContent = 'Nueva Tarea';
        this.elements.taskForm.reset();
        this.elements.taskId.value = '';
        this.setupModal();
        this.elements.taskModal.classList.remove('hidden');
    }

    /**
     * Abre el modal para editar una tarea existente
     */
    openEditModal(task) {
        this.elements.modalTitle.textContent = 'Editar Tarea';
        this.elements.taskId.value = task.id;
        this.elements.taskTitle.value = task.title;
        this.elements.taskDescription.value = task.description;
        this.elements.taskDueDate.value = task.due_date || '';
        this.elements.taskPriority.value = task.priority_id;
        this.elements.taskCategory.value = task.category_id;
        this.setupModal();
        this.elements.taskModal.classList.remove('hidden');
    }

    /**
     * Cierra el modal
     */
    closeModal() {
        this.elements.taskModal.classList.add('hidden');
    }

    /**
     * Configura el modal (fecha mínima, etc.)
     */
    setupModal() {
        const today = new Date().toISOString().split('T')[0];
        this.elements.taskDueDate.min = today;
    }

    // ==================== MENSAJES CON SWEETALERT2 ====================

    /**
     * Muestra un mensaje de éxito con SweetAlert2
     */
    showSuccess(message) {
        Swal.fire({
            icon: 'success',
            title: '¡Éxito!',
            text: message,
            timer: 3000,
            timerProgressBar: true,
            showConfirmButton: false,
            toast: true,
            position: 'top-end'
        });
    }

    /**
     * Muestra un mensaje de error con SweetAlert2
     */
    showError(message) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: message,
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#ef4444'
        });
    }

    /**
     * Muestra un mensaje de validación con SweetAlert2
     */
    showValidationError(errors) {
        const errorList = Array.isArray(errors) ? errors.join('<br>') : errors;
        Swal.fire({
            icon: 'warning',
            title: 'Validación',
            html: errorList,
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#f59e0b'
        });
    }

    /**
     * Muestra una confirmación con SweetAlert2
     */
    async showConfirmation(title, text) {
        const result = await Swal.fire({
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#ef4444',
            cancelButtonColor: '#6b7280'
        });
        return result.isConfirmed;
    }

    // ==================== MODAL DE CARGA CON SWEETALERT2 ====================

    constructor() {
        this.elements = {
            tasksGrid: document.getElementById('tasksGrid'),
            loadingState: document.getElementById('loadingState'),
            tasksContainer: document.getElementById('tasksContainer'),
            emptyState: document.getElementById('emptyState'),
            taskModal: document.getElementById('taskModal'),
            modalTitle: document.getElementById('modalTitle'),
            taskForm: document.getElementById('taskForm'),
            taskId: document.getElementById('taskId'),
            taskTitle: document.getElementById('taskTitle'),
            taskDescription: document.getElementById('taskDescription'),
            taskDueDate: document.getElementById('taskDueDate'),
            taskPriority: document.getElementById('taskPriority'),
            taskCategory: document.getElementById('taskCategory'),
            flashMessages: document.getElementById('flash-messages')
        };
    }

    /**
     * Muestra el modal de carga con SweetAlert2
     */
    showLoadingModal(title = 'Procesando...', message = 'Por favor espera mientras se procesa tu solicitud.') {
        Swal.fire({
            title: title,
            text: message,
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    }

    /**
     * Oculta el modal de carga
     */
    hideLoadingModal() {
        Swal.close();
    }

    /**
     * Fuerza el ocultamiento del modal de carga (para casos de error)
     */
    forceHideLoadingModal() {
        Swal.close();
    }

    /**
     * Muestra el modal de carga para crear tarea
     */
    showCreateLoading() {
        this.showLoadingModal('Creando tarea...', 'Guardando tu nueva tarea, por favor espera.');
    }

    /**
     * Muestra el modal de carga para editar tarea
     */
    showEditLoading() {
        this.showLoadingModal('Actualizando tarea...', 'Guardando los cambios, por favor espera.');
    }

    /**
     * Muestra el modal de carga para eliminar tarea
     */
    showDeleteLoading() {
        this.showLoadingModal('Eliminando tarea...', 'Eliminando la tarea, por favor espera.');
    }

    /**
     * Muestra el modal de carga para cambiar estado
     */
    showToggleLoading() {
        this.showLoadingModal('Cambiando estado...', 'Actualizando el estado de la tarea, por favor espera.');
    }

    /**
     * Muestra el modal de carga para cargar tareas iniciales
     */
    showInitialLoading() {
        this.showLoadingModal('Cargando tareas...', 'Obteniendo tus tareas, por favor espera.');
    }

    /**
     * Muestra el flujo de mensajes después del modal de carga
     * Primero muestra "¡Listo!" y luego el mensaje específico de la acción
     */
    showSuccessAfterLoading(actionMessage) {
        // Primero mostrar "¡Listo!"
        Swal.fire({
            icon: 'success',
            title: '¡Listo!',
            text: 'Operación completada exitosamente',
            timer: 1500,
            timerProgressBar: true,
            showConfirmButton: false
        }).then(() => {
            // Después mostrar el mensaje específico de la acción
            this.showSuccess(actionMessage);
        });
    }
} 