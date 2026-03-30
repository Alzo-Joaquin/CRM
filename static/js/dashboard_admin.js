const alertaSolicitudes = document.getElementById("alerta-solicitudes-stock");
const alertaTitulo = document.getElementById("alerta-solicitudes-titulo");
const alertaTexto = document.getElementById("alerta-solicitudes-texto");

async function cargarAlertaSolicitudesStock() {
  try {
    const response = await fetch("/solicitudes-stock/pendientes-count");
    const data = await response.json();

    if (!response.ok) {
      return;
    }

    if (data.pendientes > 0) {
      alertaTitulo.textContent = `Tenés ${data.pendientes} solicitud${data.pendientes === 1 ? "" : "es"} de stock pendiente${data.pendientes === 1 ? "" : "s"}`;
      alertaTexto.textContent = "Hay pedidos de reposición o disponibilidad cargados por vendedores que todavía no fueron revisados.";
      // alertaSolicitudes.classList.remove("alerta-admin-oculta");
      alertaSolicitudes.classList.remove("db-alert-hidden");
    }
  } catch (error) {
    console.error("Error cargando alerta de solicitudes:", error);
  }
}

cargarAlertaSolicitudesStock();