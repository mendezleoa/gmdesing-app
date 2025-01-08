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