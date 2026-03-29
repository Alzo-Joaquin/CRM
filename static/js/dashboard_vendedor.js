const alertaVendedor = document.getElementById("alerta-vendedor-solicitudes");
const alertaVendedorLista = document.getElementById("alerta-vendedor-lista");

async function cargarNotificacionesSolicitudesVendedor() {
  try {
    const response = await fetch("/solicitudes-stock/mis-notificaciones");
    const solicitudes = await response.json();

    if (!response.ok || !solicitudes.length) {
      if (alertaVendedor) {
        alertaVendedor.classList.add("alerta-vendedor-oculta");
      }
      return;
    }

    if (!alertaVendedorLista) return;

    alertaVendedorLista.innerHTML = "";

    solicitudes.forEach(solicitud => {
      const item = document.createElement("div");
      item.className = "alerta-vendedor-item";

      let html = "";

      if (solicitud.estado === "aprobada") {
        html = `
          <div class="alerta-vendedor-item-contenido">
            <p>
              ${solicitud.producto} (${solicitud.cantidad})
              <span class="texto-aprobado">ha sido aprobada</span>
            </p>
            <button class="boton vendedor-boton boton-recibido" data-id="${solicitud.id}">
              Recibido
            </button>
          </div>
        `;
      }

      if (solicitud.estado === "rechazada") {
        html = `
          <div class="alerta-vendedor-item-contenido">
            <p>
              ${solicitud.producto} (${solicitud.cantidad})
              <span class="texto-rechazado">ha sido rechazada</span>
            </p>
            <button class="boton vendedor-boton boton-recibido" data-id="${solicitud.id}">
              Recibido
            </button>
          </div>
        `;
      }

      item.innerHTML = html;
      alertaVendedorLista.appendChild(item);
    });

    vincularBotonesRecibido();

    if (alertaVendedor) {
      alertaVendedor.classList.remove("alerta-vendedor-oculta");
    }
  } catch (error) {
    console.error("Error cargando notificaciones del vendedor:", error);
  }
}

function vincularBotonesRecibido() {
  document.querySelectorAll(".boton-recibido").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      await marcarComoRecibido(id);
    });
  });
}

async function marcarComoRecibido(id) {
  try {
    const response = await fetch(`/solicitudes-stock/${id}/recibido`, {
      method: "PATCH"
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || "No se pudo marcar como recibido.");
      return;
    }

    await cargarNotificacionesSolicitudesVendedor();
  } catch (error) {
    console.error("Error marcando solicitud como recibida:", error);
  }
}

cargarNotificacionesSolicitudesVendedor();

// La dejamos explícitamente global para que socket_vendedor.js la vea sí o sí
window.cargarNotificacionesSolicitudesVendedor = cargarNotificacionesSolicitudesVendedor;