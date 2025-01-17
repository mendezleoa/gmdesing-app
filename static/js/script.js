// Función para alternar la visibilidad del menú
function toggleMenu() {
    const menu = document.getElementById('sidebar');
    menu.classList.toggle('hidden');
}

// Escucha el evento DOMContentLoaded para asegurarte de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Aquí puedes agregar más funcionalidad, como el menú hamburguesa
    const menuButton = document.getElementById('menu-button'); // Asegúrate de que este ID exista en tu HTML

    // Verifica si el botón de menú existe antes de agregar el evento
    if (menuButton) {
        menuButton.addEventListener('click', toggleMenu);
    }
});

function openModal(id, nombre, eliminarUrl) {
    // Actualiza el contenido del modal
    document.getElementById('modalMessage').innerText = `¿Está seguro de que desea eliminar ${nombre}?`;
    document.getElementById('deleteLink').setAttribute('href', eliminarUrl);

    // Muestra el modal
    const modal = document.getElementById('confirmDeleteModal');
    modal.classList.remove('hidden'); // Quita la clase 'hidden'
    modal.classList.add('flex'); // Agrega la clase 'flex'
}

function closeModal() {
    // Oculta el modal
    const modal = document.getElementById('confirmDeleteModal');
    modal.classList.add('hidden'); // Agrega la clase 'hidden'
    modal.classList.remove('flex'); // Quita la clase 'flex'
}