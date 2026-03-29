const tablaSolicitudesAdmin = document.getElementById("tabla-solicitudes-admin");
const mensajeSolicitudesAdmin = document.getElementById("mensaje-solicitudes-admin");
const btnRecargarSolicitudesAdmin = document.getElementById("btn-recargar-solicitudes-admin");

async function cargarSolicitudesAdmin() {
  try {
    const response = await fetch("/solicitudes-stock");
    const solicitudes = await response.json();

    tablaSolicitudesAdmin.innerHTML = "";

    solicitudes.forEach(solicitud => {
      const fila = document.createElement("tr");

      let acciones = "";

      if (solicitud.estado === "pendiente") {
        acciones = `
          <button class="boton boton-tabla aprobar-btn" data-id="${solicitud.id}">Aprobar</button>
          <button class="boton secundario boton-tabla rechazar-btn" data-id="${solicitud.id}">Rechazar</button>
        `;
      } else {
        acciones = `<span class="estado-finalizado">Sin acciones</span>`;
      }

      fila.innerHTML = `
        <td>${solicitud.id}</td>
        <td>${solicitud.usuario ?? ""}</td>
        <td>${solicitud.producto ?? ""}</td>
        <td>${solicitud.cantidad}</td>
        <td>${solicitud.estado}</td>
        <td>${solicitud.observaciones ?? ""}</td>
        <td>${solicitud.fecha_creacion ?? ""}</td>
        <td class="acciones-tabla">${acciones}</td>
      `;

      tablaSolicitudesAdmin.appendChild(fila);
    });

    vincularEventosSolicitudes();
  } catch (error) {
    mensajeSolicitudesAdmin.textContent = "Error al cargar solicitudes.";
    mensajeSolicitudesAdmin.style.color = "red";
  }
}

function vincularEventosSolicitudes() {
  document.querySelectorAll(".aprobar-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      await aprobarSolicitud(id);
    });
  });

  document.querySelectorAll(".rechazar-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      await rechazarSolicitud(id);
    });
  });
}

async function aprobarSolicitud(id) {
  try {
    const response = await fetch(`/solicitudes-stock/${id}/aprobar`, {
      method: "PATCH"
    });

    const data = await response.json();

    if (!response.ok) {
      mensajeSolicitudesAdmin.textContent = data.error || "No se pudo aprobar la solicitud.";
      mensajeSolicitudesAdmin.style.color = "red";
      return;
    }

    mensajeSolicitudesAdmin.textContent = "Solicitud aprobada correctamente.";
    mensajeSolicitudesAdmin.style.color = "green";

    await cargarSolicitudesAdmin();
  } catch (error) {
    mensajeSolicitudesAdmin.textContent = "Error de conexión al aprobar la solicitud.";
    mensajeSolicitudesAdmin.style.color = "red";
  }
}

async function rechazarSolicitud(id) {
  try {
    const response = await fetch(`/solicitudes-stock/${id}/rechazar`, {
      method: "PATCH"
    });

    const data = await response.json();

    if (!response.ok) {
      mensajeSolicitudesAdmin.textContent = data.error || "No se pudo rechazar la solicitud.";
      mensajeSolicitudesAdmin.style.color = "red";
      return;
    }

    mensajeSolicitudesAdmin.textContent = "Solicitud rechazada correctamente.";
    mensajeSolicitudesAdmin.style.color = "green";

    await cargarSolicitudesAdmin();
  } catch (error) {
    mensajeSolicitudesAdmin.textContent = "Error de conexión al rechazar la solicitud.";
    mensajeSolicitudesAdmin.style.color = "red";
  }
}

btnRecargarSolicitudesAdmin.addEventListener("click", cargarSolicitudesAdmin);

cargarSolicitudesAdmin();