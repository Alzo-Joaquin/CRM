const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const menuLinks = document.querySelectorAll('.navigation-menu .menu-item');

function openSidebar() {
  if (!sidebar || !sidebarOverlay) return;
  sidebar.classList.add('is-open');
  sidebarOverlay.classList.add('is-visible');
  document.body.classList.add('sidebar-open');
}

function closeSidebar() {
  if (!sidebar || !sidebarOverlay) return;
  sidebar.classList.remove('is-open');
  sidebarOverlay.classList.remove('is-visible');
  document.body.classList.remove('sidebar-open');
}

function toggleSidebar() {
  if (!sidebar) return;
  if (sidebar.classList.contains('is-open')) {
    closeSidebar();
  } else {
    openSidebar();
  }
}

if (sidebar && sidebarToggle) {
  sidebarToggle.addEventListener('click', toggleSidebar);
}

if (sidebarOverlay) {
  sidebarOverlay.addEventListener('click', closeSidebar);
}

menuLinks.forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 1000) {
      closeSidebar();
    }
  });
});

window.addEventListener('resize', () => {
  if (window.innerWidth > 1000) {
    closeSidebar();
  }
});

const header = document.querySelector('.page-header');

window.addEventListener('scroll', () => {
  if (!header) return;

  if (window.scrollY > 10) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
});