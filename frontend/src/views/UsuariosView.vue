<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">👥 Usuarios</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Nuevo usuario</button>
    </div>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in usuarios" :key="u.id">
            <td>{{ u.nombre }}</td>
            <td>{{ u.email }}</td>
            <td><span :class="['badge-rol', u.rol]">{{ u.rol }}</span></td>
            <td class="acciones">
              <button class="btn-sm" @click="abrirFormulario(u)">✏️ Editar</button>
              <button class="btn-sm danger" @click="eliminar(u.id)">🗑️ Eliminar</button>
            </td>
          </tr>
          <tr v-if="usuarios.length === 0">
            <td colspan="4" class="empty">Sin usuarios registrados</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>{{ form.id ? "Editar usuario" : "Nuevo usuario" }}</h3>

        <div class="grid2">
          <div class="field full">
            <label>Nombre</label>
            <input v-model="form.nombre" placeholder="Nombre completo" />
          </div>
          <div class="field full">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="correo@ejemplo.com" />
          </div>
          <div class="field">
            <label>Rol</label>
            <select v-model="form.rol">
              <option value="admin">Admin</option>
              <option value="enfermero">Enfermero</option>
              <option value="medico">Médico</option>
            </select>
          </div>
          <div class="field">
            <label>{{ form.id ? "Nueva contraseña (opcional)" : "Contraseña" }}</label>
            <input v-model="form.password" type="password" placeholder="••••••••" />
          </div>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="modal-actions">
          <button @click="modal = false">Cancelar</button>
          <button class="btn-primary" @click="guardar">Guardar</button>
        </div>
      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import api from "@/apiServices/authService";

const usuarios = ref([]);
const modal    = ref(false);
const error    = ref("");
const form     = ref({});

async function cargar() {
  const { data } = await api.get("/api/usuarios/");
  usuarios.value = data;
}

function abrirFormulario(u = null) {
  error.value = "";
  form.value  = u
    ? { ...u, password: "" }
    : { nombre: "", email: "", rol: "enfermero", password: "" };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    if (form.value.id) {
      await api.put(`/api/usuarios/${form.value.id}`, form.value);
    } else {
      await api.post("/api/usuarios/", form.value);
    }
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al guardar";
  }
}

async function eliminar(id) {
  if (confirm("¿Eliminar este usuario?")) {
    await api.delete(`/api/usuarios/${id}`);
    cargar();
  }
}

onMounted(cargar);
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-title { margin: 0; color: #333; font-size: 1.4rem; }

.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

table { width: 100%; border-collapse: collapse; }

th {
  background: #f9f9f9;
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.85rem;
  color: #666;
}

td {
  padding: 0.75rem 1rem;
  border-top: 1px solid #f0f0f0;
  font-size: 0.9rem;
  color: #333;
}

.empty { text-align: center; color: #aaa; }

.badge-rol {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}
.badge-rol.admin     { background: #fde8e8; color: #b71c1c; }
.badge-rol.enfermero { background: #e8f4fd; color: #1565c0; }
.badge-rol.medico    { background: #e8fde8; color: #1b5e20; }

.acciones { display: flex; gap: 0.4rem; }

.btn-primary {
  background: #e53935;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}
.btn-primary:hover { background: #b71c1c; }

.btn-sm {
  background: #f0f0f0;
  border: none;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}
.btn-sm.danger { background: #fde8e8; color: #b71c1c; }
.btn-sm:hover { opacity: 0.8; }

/* ── Modal ───────────────────────────────────────── */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  width: 460px;
  max-width: 95vw;
}

.modal h3 { margin: 0 0 1.5rem; color: #333; }

.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.field.full { grid-column: 1 / -1; }

label { font-size: 0.8rem; font-weight: 600; color: #555; }

input, select {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
}
input:focus, select:focus { border-color: #e53935; }

.error { color: #e53935; font-size: 0.85rem; margin: 0.5rem 0 0; }

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}
</style>
