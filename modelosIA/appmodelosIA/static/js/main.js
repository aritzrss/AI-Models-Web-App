document.addEventListener('DOMContentLoaded', function() {
    
    console.log("JS Cargado correctamente");

    // ==========================================================================
    // 1. EFECTO FADE-IN GLOBAL AL CARGAR PÁGINA
    // ==========================================================================
    document.body.style.opacity = 0;
    document.body.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = 1;
    }, 50);

    // ==========================================================================
    // 2. VALIDACIÓN DEL FORMULARIO DE CREAR MODELO (crear_modelo.html)
    // ==========================================================================
    const formularioCrear = document.getElementById('form-crear');

    if (formularioCrear) {
        formularioCrear.addEventListener('submit', function(event) {
            const campoNombre = document.querySelector('input[name="nombre"]');
            const campoAnio = document.querySelector('input[name="anio_inventado"]');
            
            let errores = [];

            // Reset de estilos
            campoNombre.style.border = "1px solid #ccc";
            campoAnio.style.border = "1px solid #ccc";

            // Validación 1: El nombre no puede estar vacío ni ser muy corto
            if (campoNombre.value.trim().length < 3) {
                errores.push("El nombre debe tener al menos 3 caracteres.");
                campoNombre.style.border = "2px solid red";
            }

            // Validación 2: El año debe ser realista
            const anioActual = new Date().getFullYear();
            if (campoAnio.value && (campoAnio.value < 1950 || campoAnio.value > anioActual)) {
                errores.push(`El año debe ser un valor realista entre 1950 y ${anioActual}.`);
                campoAnio.style.border = "2px solid red";
            }

            if (errores.length > 0) {
                event.preventDefault();
                alert("Errores detectados:\n" + errores.join("\n"));
            }
        });
    }

    // ==========================================================================
    // 3. VALIDACIÓN DE FILTROS DE AÑO (formulario.html)
    // ==========================================================================
    const formFiltros = document.querySelector('.form-filters');

    if (formFiltros) {
        formFiltros.addEventListener('submit', function(event) {
            const inputDesde = document.querySelector('input[name="anio_desde"]');
            const inputHasta = document.querySelector('input[name="anio_hasta"]');
            
            if (inputDesde.value && inputHasta.value) {
                const desde = parseInt(inputDesde.value);
                const hasta = parseInt(inputHasta.value);
                
                inputDesde.style.border = "1px solid #ccc";
                inputHasta.style.border = "1px solid #ccc";

                if (desde > hasta) {
                    event.preventDefault();
                    alert("⚠️ Error en los años: \nEl año 'Desde' no puede ser mayor que el año 'Hasta'.");
                    inputDesde.style.border = "2px solid red";
                    inputHasta.style.border = "2px solid red";
                }
            }
        });
    }

    // ==========================================================================
    // 4. LÓGICA DE CONFIRMACIÓN DE BORRADO (Dos Pasos)
    // ==========================================================================
    
    // Paso 1: Aviso al hacer clic en el enlace "Eliminar" en la página de detalle.
    const linkBorrar = document.getElementById('link-borrar');
    if (linkBorrar) {
        linkBorrar.addEventListener('click', function(event) {
            event.preventDefault();
            const confirmacionInicial = confirm("¿Estás seguro de que quieres ir a la pantalla de eliminación?");
            if (confirmacionInicial) {
                window.location.href = this.href;
            }
        });
    }

    // Paso 2: Aviso final en la página de confirmación.
    const botonConfirmarBorrado = document.querySelector('.btn-borrar-js');
    if (botonConfirmarBorrado) {
        botonConfirmarBorrado.addEventListener('click', function(event) {
            const confirmacionFinal = confirm("¡ACCIÓN IRREVERSIBLE! ⚠️\n\n¿Estás completamente seguro de que quieres eliminar este modelo para siempre?");
            if (!confirmacionFinal) {
                event.preventDefault(); 
            }
        });
    }

    // ==========================================================================
    // 5. AJAX PARA EL LABORATORIO DE ML (reporte.html)
    // ==========================================================================
    const formLaboratorio = document.getElementById('form-laboratorio');
    
    if (formLaboratorio) {
        const resultadoContainer = document.getElementById('resultado-container');
        const botonEjecutar = document.getElementById('btn-ejecutar');

        formLaboratorio.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const botonTextoOriginal = botonEjecutar.innerHTML;
            botonEjecutar.innerHTML = '⏳ Procesando...';
            botonEjecutar.disabled = true;
            resultadoContainer.style.opacity = '0.5';

            const formData = new FormData(formLaboratorio);
            const params = new URLSearchParams(formData).toString();
            const url = formLaboratorio.action + '?' + params;

            fetch(url, {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                resultadoContainer.innerHTML = data.html;
            })
            .catch(error => {
                console.error('Error en la petición AJAX:', error);
                resultadoContainer.innerHTML = '<div class="error-box">Ocurrió un error de conexión. Inténtalo de nuevo.</div>';
            })
            .finally(() => {
                botonEjecutar.innerHTML = botonTextoOriginal;
                botonEjecutar.disabled = false;
                resultadoContainer.style.opacity = '1';
            });
        });
    }

    // ==========================================================================
    // 6. AJAX PARA LA VALORACIÓN DE MODELOS (modelo_detail.html)
    // ==========================================================================
    const valoracionContainer = document.getElementById('valoracion-container');

    if (valoracionContainer) {
        // Usamos delegación de eventos porque el formulario de dentro se reemplaza
        valoracionContainer.addEventListener('submit', function(event) {
            
            if (event.target && event.target.id === 'form-votar') {
                event.preventDefault();
                
                const form = event.target;
                const button = form.querySelector('button[type="submit"]');
                button.disabled = true;
                button.innerHTML = '⏳';

                fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: new FormData(form)
                })
                .then(response => response.json())
                .then(data => {
                    valoracionContainer.innerHTML = data.html;
                })
                .catch(error => {
                    console.error('Error al procesar el voto:', error);
                    // Si falla, el usuario verá el HTML original y el botón se reactivará
                    // en la siguiente interacción, ya que no se habrá reemplazado el HTML.
                    alert("Hubo un error al enviar el voto. Por favor, inténtalo de nuevo.");
                    button.disabled = false;
                    button.innerHTML = 'Enviar';
                });
            }
        });
    }
});