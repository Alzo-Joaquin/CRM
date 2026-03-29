const socketAdmin = io();

socketAdmin.on("connect", () => {
  console.log("Admin socket conectado");
});

socketAdmin.on("solicitud_stock_nueva", () => {
  if (typeof cargarAlertaSolicitudesStock === "function") {
    cargarAlertaSolicitudesStock();
  }

  if (typeof cargarSolicitudesAdmin === "function") {
    cargarSolicitudesAdmin();
  }
});

socketAdmin.on("solicitud_stock_actualizada", () => {
  if (typeof cargarAlertaSolicitudesStock === "function") {
    cargarAlertaSolicitudesStock();
  }

  if (typeof cargarSolicitudesAdmin === "function") {
    cargarSolicitudesAdmin();
  }
});

socketAdmin.on("solicitud_stock_recibida", () => {
  if (typeof cargarAlertaSolicitudesStock === "function") {
    cargarAlertaSolicitudesStock();
  }

  if (typeof cargarSolicitudesAdmin === "function") {
    cargarSolicitudesAdmin();
  }
});