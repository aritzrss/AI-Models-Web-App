document.addEventListener('DOMContentLoaded', function() {
    
    console.log("JS Cargado correctamente");

    // 1. EFECTO GLOBAL
    document.body.style.opacity = 0;
    document.body.style.transition = 'opacity 1s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = 1;
    }, 100);

    // VALIDACIÓN DE FORMULARIO
    const formularioCrear = document.getElementById('form-crear');

    if (formularioCrear) {
        formularioCrear.addEventListener('submit', function(event) {
            const campoNombre = document.querySelector('input[name="nombre"]');
            const campoAnio = document.querySelector('input[name="anio_inventado"]');
            
            let errores = [];

            // Validación 1: El nombre no puede estar vacío ni ser muy corto
            if (campoNombre.value.trim().length < 3) {
                errores.push("El nombre debe tener al menos 3 caracteres.");
                campoNombre.style.border = "2px solid red";
            } else {
                campoNombre.style.border = "1px solid #ccc";
            }

            // Validación 2: El año debe ser realista (entre 1950 y el año actual)
            const anioActual = new Date().getFullYear();
            if (campoAnio.value < 1950 || campoAnio.value > anioActual) {
                errores.push(`El año debe ser entre 1950 y ${anioActual}.`);
                campoAnio.style.border = "2px solid red";
            } else {
                campoAnio.style.border = "1px solid #ccc";
            }

            if (errores.length > 0) {
                event.preventDefault();
                alert("Errores detectados:\n" + errores.join("\n"));
            }
        });
    }


    // 3. INTERACCIÓN EN BORRADO (Confirmación JS)
    const botonesBorrar = document.querySelectorAll('.btn-borrar-js');

    botonesBorrar.forEach(boton => {
        boton.addEventListener('click', function(event) {
            // Función nativa de JS para confirmar
            const confirmacion = confirm("¿Seguro que quieres ir a la página de borrado?");
            
            if (!confirmacion) {
                event.preventDefault(); // Si dice "Cancelar", no sigue el enlace
            }
        });
    });

    // VALIDACIÓN DE FILTROS (formulario.html)
    const formFiltros = document.querySelector('.form-filters');

    if (formFiltros) {
        formFiltros.addEventListener('submit', function(event) {
            // Obtenemos los inputs de años
            const inputDesde = document.querySelector('input[name="anio_desde"]');
            const inputHasta = document.querySelector('input[name="anio_hasta"]');
            
            // Verificamos si ambos tienen valores
            if (inputDesde.value && inputHasta.value) {
                const desde = parseInt(inputDesde.value);
                const hasta = parseInt(inputHasta.value);

                // Si el año de inicio es mayor que el final, es un error lógico
                if (desde > hasta) {
                    event.preventDefault(); // IMPORTANTE: Detiene el filtrado
                    alert("⚠️ Error en los años: \nEl año 'Desde' no puede ser mayor que el año 'Hasta'.");
                    
                    // Efecto visual de error
                    inputDesde.style.border = "2px solid red";
                    inputHasta.style.border = "2px solid red";
                } else {
                    // Si lo corrige, quitamos el rojo
                    inputDesde.style.border = "1px solid #ccc";
                    inputHasta.style.border = "1px solid #ccc";
                }
            }
        });
    }

});