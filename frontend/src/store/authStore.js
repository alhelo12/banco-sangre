import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/apiServices/authService";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || null);
  const user  = ref(JSON.parse(localStorage.getItem("user") || "null"));

  const isAuthenticated = computed(() => !!token.value);

  async function login(email, password) {
    // FastAPI OAuth2 espera form-data, no JSON
    const form = new URLSearchParams({ username: email, password });
    const { data } = await api.post("/api/auth/token", form);

    token.value = data.access_token;
    localStorage.setItem("token", data.access_token);

    // Obtener datos del usuario autenticado
    const me = await api.get("/api/auth/me");
    user.value = me.data;
    localStorage.setItem("user", JSON.stringify(me.data));
  }

  function logout() {
    token.value = null;
    user.value  = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  return { token, user, isAuthenticated, login, logout };
});
