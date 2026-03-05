# Certificados SSL

Esta carpeta contiene los certificados SSL utilizados por el servidor.
Los archivos `key.pem` y `cert.pem` estan ignorados en Git por seguridad.

---

## Desarrollo local (certificado autofirmado)

Genera un certificado autofirmado para desarrollo local con OpenSSL:

```powershell
# Windows
$env:OPENSSL_CONF = "C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"
& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

```bash
# Linux / Mac
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

> El navegador mostrara una advertencia de certificado no confiable al ser autofirmado.
> Haz click en "Avanzado" → "Continuar de todas formas" para acceder.

---

## Produccion (Let's Encrypt)

Para produccion en un servidor con dominio propio usa **Certbot** con Let's Encrypt,
que genera certificados gratuitos y reconocidos por todos los navegadores.

### Instalar Certbot (Ubuntu/Debian)

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d tu-dominio.com
```

Los certificados se generan en:
```
/etc/letsencrypt/live/tu-dominio.com/privkey.pem   → key.pem
/etc/letsencrypt/live/tu-dominio.com/fullchain.pem  → cert.pem
```

Actualiza las rutas en `backend/run.py` y `frontend/vite.config.js` con las rutas correctas.

> Los certificados de Let's Encrypt se renuevan cada 90 dias.
> Configura la renovacion automatica con: `sudo certbot renew --dry-run`
