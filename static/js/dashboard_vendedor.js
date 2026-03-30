const alertaVendedor = document.getElementById("alerta-vendedor-solicitudes");
const alertaVendedorLista = document.getElementById("alerta-vendedor-lista");

async function cargarNotificacionesSolicitudesVendedor() {
  try {
    const response = await fetch("/solicitudes-stock/mis-notificaciones");
    const solicitudes = await response.json();

    // Cambiamos "vo-alert-hidden" por "vs-alert-hidden"
    if (!response.ok || !solicitudes.length) {
      if (alertaVendedor) {
        alertaVendedor.classList.add("vs-alert-hidden");
      }
      return;
    }

    if (!alertaVendedorLista) return;

    alertaVendedorLista.innerHTML = "";

    solicitudes.forEach(solicitud => {
      const item = document.createElement("div");
      // Clase para el contenedor de la notificación (estilo profesional vs)
      item.className = "vs-notification-item"; 

      let statusColor = solicitud.estado === "aprobada" ? "#10b981" : "#ef4444";
      let textClass = solicitud.estado === "aprobada" ? "vs-text-success" : "vs-text-danger";

      item.innerHTML = `
          <div style="flex: 1; display: flex; align-items: center; gap: 12px;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: ${statusColor};"></div>
            <div>
              <p style="margin: 0; font-size: 0.9rem; color: var(--vs-text-main);">
                <strong>${solicitud.producto}</strong> (${solicitud.cantidad})
              </p>
              <small class="${textClass}" style="text-transform: uppercase; font-weight: 700; font-size: 0.7rem;">
                Ha sido ${solicitud.estado}
              </small>
            </div>
          </div>
          <button class="vs-btn-recibido boton-recibido" 
                  data-id="${solicitud.id}">
            Entendido
          </button>
      `;

      alertaVendedorLista.appendChild(item);
    });

    vincularBotonesRecibido();

    if (alertaVendedor) {
      // Cambiamos "vo-alert-hidden" por "vs-alert-hidden"
      alertaVendedor.classList.remove("vs-alert-hidden");
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