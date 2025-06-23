# API - Diagrams Serverless

## 1. Register User

**Endpoint:** `POST /user/register`

**Link:** https://lnvew987t4.execute-api.us-east-1.amazonaws.com/dev/user/register

**Descripción:** Registra un nuevo usuario en el sistema.

**Cuerpo esperado (JSON):**

```json
{
  "email": "usuario@correo.com",
  "password": "clave_segura",
  "name": "Nombre del usuario"
}
```

**Respuesta exitosa:**

```json
{
  "message": "Usuario registrado exitosamente",
  "user_id": "uuid-generado"
}
```

---

## 2. Login Usuario

**Endpoint:** `POST /user/login`

**Link:** https://lnvew987t4.execute-api.us-east-1.amazonaws.com/dev/user/login

**Descripción:** Autentica a un usuario existente y devuelve un token.
**Cuerpo esperado (JSON):**

```json
{
  "email": "usuario@correo.com",
  "password": "clave_segura"
}
```

**Respuesta exitosa:**

```json
{
  "token": "uuid-token-generado",
  "expires": "2025-06-30 23:59:59"
}
```

---

## 3. Verificar Token

**Endpoint:** `POST /user/verify`

**Link:** https://lnvew987t4.execute-api.us-east-1.amazonaws.com/dev/user/verify

**Descripción:** Verifica si un token enviado es válido y no ha expirado.
**Cuerpo esperado (JSON):**

```json
{
  "token": "uuid-token-generado",
  "user": {...info_usuario}
}
```

**Respuesta exitosa:**

```json
{
  "message": "Token válido"
}
```

---

## 4. Generar Diagrama con JSON

**Endpoint:** `POST /diagrams/with-json`

**Link:** https://lnvew987t4.execute-api.us-east-1.amazonaws.com/dev/diagrams/with-json

**Descripción:** Recibe un objeto JSON y genera un grafo - diagrama representativo (como imagen JPG).
**Cuerpo esperado (JSON):**

```json
{
  "json": {
    "persona": {
      "nombre": "Ana",
      "edad": 30
    }
  }
}
```

**Respuesta exitosa:**
Imagen generada almacenada en un bucket S3, donde esta su URL respectivo.
