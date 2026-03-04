<template>
  <div class="layout">

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="brand">🩸 Banco de Sangre</div>

      <nav>
        <RouterLink to="/">
          <i class="pi pi-home" /> Dashboard
        </RouterLink>
        <RouterLink to="/donantes">
          <i class="pi pi-users" /> Donantes
        </RouterLink>
        <RouterLink to="/donaciones">
          <i class="pi pi-heart" /> Donaciones
        </RouterLink>
        <RouterLink to="/inventario">
          <i class="pi pi-box" /> Inventario
        </RouterLink>
        <RouterLink to="/solicitudes">
          <i class="pi pi-file" /> Solicitudes
        </RouterLink>
        <RouterLink to="/transfusiones">
          <i class="pi pi-sync" /> Transfusiones
        </RouterLink>
      </nav>

      <div class="user-info">
        <span class="user-name">{{ auth.user?.nombre }}</span>
        <span class="user-rol">{{ auth.user?.rol }}</span>
        <button @click="handleLogout">
          <i class="pi pi-sign-out" /> Cerrar sesión
        </button>
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="main">
      <slot />
    </main>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore";

const auth   = useAuthStore();
const router = useRouter();

function handleLogout() {
  auth.logout();
  router.push("/login");
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  font-family: sans-serif;
}

/* ── Sidebar ─────────────────────────────────────── */
.sidebar {
  width: 220px;
  background: #b71c1c;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  gap: 1rem;
  flex-shrink: 0;
}

.brand {
  font-size: 1rem;
  font-weight: 700;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

nav a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.55rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  transition: background 0.2s;
}

nav a:hover,
nav a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* ── Usuario ─────────────────────────────────────── */
.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  padding-top: 1rem;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
}

.user-rol {
  font-size: 0.75rem;
  opacity: 0.7;
  text-transform: capitalize;
  margin-bottom: 0.4rem;
}

.user-info button {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: background 0.2s;
}

.user-info button:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* ── Main ────────────────────────────────────────── */
.main {
  flex: 1;
  background: #f5f5f5;
  padding: 2rem;
  overflow-y: auto;
}
</style>
