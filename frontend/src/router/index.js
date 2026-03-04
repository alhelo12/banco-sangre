import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/authStore";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/",
    name: "Dashboard",
    component: () => import("@/views/DashboardView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero", "medico"] },
  },
  {
    path: "/configuracion-roles",
    name: "ConfiguracionRoles",
    component: () => import("@/views/ConfiguracionRolesView.vue"),
    meta: { requiresAuth: true, roles: ["admin"] },
  },
  {
    path: "/usuarios",
    name: "Usuarios",
    component: () => import("@/views/UsuariosView.vue"),
    meta: { requiresAuth: true, roles: ["admin"] },
  },
  {
    path: "/donantes",
    name: "Donantes",
    component: () => import("@/views/DonantesView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero"] },
  },
  {
    path: "/donaciones",
    name: "Donaciones",
    component: () => import("@/views/DonacionesView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero"] },
  },
  {
    path: "/inventario",
    name: "Inventario",
    component: () => import("@/views/InventarioView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero"] },
  },
  {
    path: "/solicitudes",
    name: "Solicitudes",
    component: () => import("@/views/SolicitudesView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero", "medico"] },
  },
  {
    path: "/transfusiones",
    name: "Transfusiones",
    component: () => import("@/views/TransfusionesView.vue"),
    meta: { requiresAuth: true, roles: ["admin", "enfermero", "medico"] },
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  // Sin token → login
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "Login" };
  }

  // Ya autenticado va al login → dashboard
  if (to.name === "Login" && auth.isAuthenticated) {
    return { name: "Dashboard" };
  }

  // Rol sin permiso para esa ruta → dashboard
  if (to.meta.roles && auth.user) {
    if (!to.meta.roles.includes(auth.user.rol)) {
      return { name: "Dashboard" };
    }
  }
});

export default router;
