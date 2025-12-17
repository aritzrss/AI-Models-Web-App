document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('form-laboratorio');
    const resultadoContainer = document.getElementById('resultado-container');
    const boton = document.getElementById('btn-ejecutar');

    if (form) {
        form.addEventListener('submit', function(event) {
            // 1. Evitar recarga completa
            event.preventDefault();
            
            // 2. Feedback visual inmediato
            const botonTextoOriginal = boton.innerHTML;
            boton.innerHTML = 'Procesando...';
            boton.disabled = true;
            if (resultadoContainer) {
                resultadoContainer.style.opacity = '0.5';
            }

            // 3. Preparar datos
            const formData = new FormData(form);
            const params = new URLSearchParams(formData).toString();
            // Aseguramos que la URL sea correcta
            const url = form.getAttribute('action') + '?' + params;

            // 4. Petición AJAX
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Cabecera clave para Django
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                // 5. Actualizar DOM
                if (resultadoContainer) {
                    resultadoContainer.innerHTML = data.html;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (resultadoContainer) {
                    resultadoContainer.innerHTML = `
                        <div class="alert-error">
                             Ocurrió un error al procesar la solicitud. Inténtalo de nuevo.
                        </div>`;
                }
            })
            .finally(() => {
                // 6. Restaurar estado
                boton.innerHTML = botonTextoOriginal;
                boton.disabled = false;
                if (resultadoContainer) {
                    resultadoContainer.style.opacity = '1';
                }
            });
        });
    }
});