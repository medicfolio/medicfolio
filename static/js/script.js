// # js/Scripts.js

// Mensaje de bienvenida en consola
console.log("Bienvenido a MedicFolio");

// Confirmación antes de eliminar el perfil
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-profile");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            if (!confirm("¿Estás seguro de que deseas eliminar tu perfil?")) {
                event.preventDefault();
            }
        });
    });
});

// Ejemplo de interacción con Bootstrap (opcional)
const toastTrigger = document.getElementById('liveToastBtn');
const toastLive = document.getElementById('liveToast');

if (toastTrigger) {
    toastTrigger.addEventListener('click', () => {
        const toast = new bootstrap.Toast(toastLive);
        toast.show();
    });
}
