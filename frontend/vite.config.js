import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const isDev = process.env.NODE_ENV !== "production";

const certPath = path.resolve(__dirname, "../certs/cert.pem");
const keyPath  = path.resolve(__dirname, "../certs/key.pem");
const hasCerts = isDev && fs.existsSync(certPath) && fs.existsSync(keyPath);

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
    https: hasCerts
      ? { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }
      : false,
    proxy: {
      "/api": {
        target: hasCerts ? "https://localhost:8000" : "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
