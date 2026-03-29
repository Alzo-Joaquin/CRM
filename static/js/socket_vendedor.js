const socketVendedor = io();

socketVendedor.on("connect", () => {
  console.log("Vendedor socket conectado");
});

socketVendedor.on("solicitud_stock_actualizada", () => {
  console.log("Evento solicitud_stock_actualizada recibido en vendedor");

  if (typeof window.cargarNotificacionesSolicitudesVendedor === "function") {
    window.cargarNotificacionesSolicitudesVendedor();
  }

  if (typeof window.cargarSolicitudes === "function") {
    window.cargarSolicitudes();
  }

  if (typeof window.cargarProductos === "function") {
    window.cargarProductos();
  }
});

socketVendedor.on("solicitud_stock_recibida", () => {
  console.log("Evento solicitud_stock_recibida recibido en vendedor");

  if (typeof window.cargarNotificacionesSolicitudesVendedor === "function") {
    window.cargarNotificacionesSolicitudesVendedor();
  }

  if (typeof window.cargarSolicitudes === "function") {
    window.cargarSolicitudes();
  }
});

socketVendedor.on("solicitud_stock_nueva", () => {
  console.log("Evento solicitud_stock_nueva recibido en vendedor");

  if (typeof window.cargarSolicitudes === "function") {
    window.cargarSolicitudes();
  }
});