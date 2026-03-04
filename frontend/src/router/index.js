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
    meta: { requiresAuth: true },
  },
  {
    path: "/usuarios",
    name: "Usuarios",
    component: () => import("@/views/UsuariosView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/donantes",
    name: "Donantes",
    component: () => import("@/views/DonantesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/donaciones",
    name: "Donaciones",
    component: () => import("@/views/DonacionesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/inventario",
    name: "Inventario",
    component: () => import("@/views/InventarioView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/solicitudes",
    name: "Solicitudes",
    component: () => import("@/views/SolicitudesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/transfusiones",
    name: "Transfusiones",
    component: () => import("@/views/TransfusionesView.vue"),
    meta: { requiresAuth: true },
  },
  // Redirige cualquier ruta desconocida al dashboard
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard: si la ruta requiere auth y no hay token, manda al login
router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "Login" };
  }
  // Si ya esta autenticado y va al login, manda al dashboard
  if (to.name === "Login" && auth.isAuthenticated) {
    return { name: "Dashboard" };
  }
});

export default router;
