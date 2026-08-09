async function cargarKPIs() {
  try {
    const response = await fetch("/dashboard/kpis");
    const data = await response.json();

    const clientesEl = document.getElementById("kpi-clientes");
    const productosEl = document.getElementById("kpi-productos");
    const unidadesEl = document.getElementById("kpi-unidades");
    const ventasHoyEl = document.getElementById("kpi-ventas-hoy");

    if (clientesEl) clientesEl.textContent = data.clientes;
    if (productosEl) productosEl.textContent = data.productos;
    if (unidadesEl) unidadesEl.textContent = data.unidades_vendidas;
    if (ventasHoyEl) ventasHoyEl.textContent = data.ventas_del_dia;
  } catch (error) {
    console.error("Error cargando KPIs:", error);
  }
}

cargarKPIs();