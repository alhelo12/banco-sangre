<template>
  <div class="login-page">
    <div class="login-card">

      <div class="logo">🩸</div>
      <h1>Banco de Sangre</h1>
      <p class="subtitle">Inicia sesión para continuar</p>

      <div class="field">
        <label>Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="correo@ejemplo.com"
        />
      </div>

      <div class="field">
        <label>Contraseña</label>
        <input
          v-model="password"
          type="password"
          placeholder="••••••••"
          @keyup.enter="handleLogin"
        />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button @click="handleLogin" :disabled="loading">
        {{ loading ? "Entrando..." : "Iniciar sesión" }}
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/authStore";

const email    = ref("");
const password = ref("");
const error    = ref("");
const loading  = ref(false);
const router   = useRouter();
const auth     = useAuthStore();

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
  width: 360px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  text-align: center;
}

.logo {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

h1 {
  margin: 0 0 0.25rem;
  color: #b71c1c;
  font-size: 1.5rem;
}

.subtitle {
  color: #999;
  margin: 0 0 1.5rem;
  font-size: 0.9rem;
}

.field {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 1rem;
}

label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.3rem;
}

input {
  padding: 0.65rem 0.9rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #e53935;
}

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

button:hover:not(:disabled) {
  background: #b71c1c;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #e53935;
  font-size: 0.85rem;
  margin: 0.25rem 0;
}
</style>
