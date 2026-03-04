<template>
  <div class="login-page">
    <div class="login-card">

      <div class="logo">🩸</div>
      <h1>Banco de Sangre</h1>
      <p class="subtitle">{{ modo === 'login' ? 'Inicia sesión para continuar' : 'Crea tu cuenta' }}</p>

      <!-- ── LOGIN ── -->
      <template v-if="modo === 'login'">
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="correo@ejemplo.com" />
        </div>
        <div class="field">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" @keyup.enter="handleLogin" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button @click="handleLogin" :disabled="loading">
          {{ loading ? "Entrando..." : "Iniciar sesión" }}
        </button>
        <p class="toggle">
          ¿No tienes cuenta?
          <span @click="cambiarModo('registro')">Regístrate aquí</span>
        </p>
      </template>

      <!-- ── REGISTRO ── -->
      <template v-else>
        <div class="field">
          <label>Nombre completo</label>
          <input v-model="nombre" placeholder="Juan Pérez" />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="correo@ejemplo.com" />
        </div>
        <div class="field">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" />
        </div>
        <div class="field">
          <label>Matrícula</label>
          <input v-model="matricula" placeholder="Ej: MED-4821" @input="validarMatricula" />
          <span v-if="rolDetectado" class="rol-detectado">
            ✅ Rol detectado: <strong>{{ rolDetectado }}</strong>
          </span>
          <span v-if="matriculaError" class="hint-error">{{ matriculaError }}</span>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button @click="handleRegistro" :disabled="loading || !rolDetectado">
          {{ loading ? "Registrando..." : "Crear cuenta" }}
        </button>
        <p class="toggle">
          ¿Ya tienes cuenta?
          <span @click="cambiarModo('login')">Inicia sesión</span>
        </p>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore";
import axios from "axios";

const modo           = ref("login");
const email          = ref("");
const password       = ref("");
const nombre         = ref("");
const matricula      = ref("");
const rolDetectado   = ref("");
const matriculaError = ref("");
const error          = ref("");
const loading        = ref(false);
const router         = useRouter();
const auth           = useAuthStore();

function cambiarModo(m) {
  modo.value           = m;
  error.value          = "";
  matriculaError.value = "";
  rolDetectado.value   = "";
  email.value          = "";
  password.value       = "";
  nombre.value         = "";
  matricula.value      = "";
}

// Valida la matricula en tiempo real mientras el usuario escribe
let timeout = null;
async function validarMatricula() {
  rolDetectado.value   = "";
  matriculaError.value = "";
  if (!matricula.value || matricula.value.length < 2) return;

  clearTimeout(timeout);
  timeout = setTimeout(async () => {
    try {
      const { data } = await axios.get(`/api/configuracion-roles/validar/${matricula.value}`);
      rolDetectado.value = data.rol;
    } catch {
      matriculaError.value = "Matrícula no reconocida";
    }
  }, 500);
}

async function handleLogin() {
  error.value   = "";
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    router.push("/");
  } catch {
    error.value = "Email o contraseña incorrectos";
  } finally {
    loading.value = false;
  }
}

async function handleRegistro() {
  error.value   = "";
  loading.value = true;
  try {
    await axios.post("/api/auth/register", {
      nombre:    nombre.value,
      email:     email.value,
      password:  password.value,
      matricula: matricula.value,
    });
    // Login automatico tras registro exitoso
    await auth.login(email.value, password.value);
    router.push("/");
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al registrarse";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #b71c1c, #e53935);
  font-family: sans-serif;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  width: 380px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  text-align: center;
}

.logo { font-size: 3rem; margin-bottom: 0.5rem; }

h1 { margin: 0 0 0.25rem; color: #b71c1c; font-size: 1.5rem; }

.subtitle { color: #999; margin: 0 0 1.5rem; font-size: 0.9rem; }

.field {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 1rem;
}

label { font-size: 0.8rem; font-weight: 600; color: #555; margin-bottom: 0.3rem; }

input {
  padding: 0.65rem 0.9rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}
input:focus { border-color: #e53935; }

button {
  width: 100%;
  padding: 0.75rem;
  background: #e53935;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
button:hover:not(:disabled) { background: #b71c1c; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

.error { color: #e53935; font-size: 0.85rem; margin: 0.25rem 0; }

.rol-detectado {
  font-size: 0.8rem;
  color: #2e7d32;
  margin-top: 0.25rem;
}

.hint-error {
  font-size: 0.8rem;
  color: #e53935;
  margin-top: 0.25rem;
}

.toggle {
  margin-top: 1.25rem;
  font-size: 0.85rem;
  color: #888;
}

.toggle span {
  color: #e53935;
  cursor: pointer;
  font-weight: 600;
}
.toggle span:hover { text-decoration: underline; }
</style>
