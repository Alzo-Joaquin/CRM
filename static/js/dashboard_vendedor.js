const alerta = document.getElementById("alerta-vendedor-solicitudes");
const lista = document.getElementById("alerta-vendedor-lista");

async function cargar() {
  try {
    const res = await fetch("/solicitudes-stock/mis-notificaciones");
    const data = await res.json();

    if (!res.ok || data.length === 0) {
      alerta.classList.add("alerta-vendedor-oculta");
      return;
    }

    lista.innerHTML = "";

    data.forEach(s => {
      const div = document.createElement("div");
      div.className = "alerta-vendedor-item";

      let html = "";

      if (s.estado === "aprobada") {
        html = `
          <div class="alerta-vendedor-item-contenido">
            <p>
              ${s.producto} (${s.cantidad})
              <span class="ok">APROBADA</span>
            </p>
            <button class="btn-recibido" data-id="${s.id}">
              Recibido
            </button>
          </div>
        `;
      }

      if (s.estado === "rechazada") {
        html = `
          <div class="alerta-vendedor-item-contenido">
            <p>
              ${s.producto} (${s.cantidad})
              <span class="error">RECHAZADA</span>
            </p>
            <button class="btn-recibido" data-id="${s.id}">
              Recibido
            </button>
          </div>
        `;
      }

      div.innerHTML = html;
      lista.appendChild(div);
    });

    bind();
    alerta.classList.remove("alerta-vendedor-oculta");

  } catch (e) {
    console.error(e);
  }
}

function bind() {
  document.querySelectorAll(".btn-recibido").forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;

      const res = await fetch(`/solicitudes-stock/${id}/recibido`, {
        method: "PATCH"
      });

      if (!res.ok) {
        alert("Error al marcar como recibido");
        return;
      }

      cargar(); // refresca
    };
  });
}

cargar();