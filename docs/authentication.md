# Autenticação e Segurança

O projeto utiliza **JWT (JSON Web Tokens)** para autenticação e **Argon2** (via `pwdlib`) para hashing de senhas.

- Os endpoints protegidos requerem o envio do token no header `Authorization: Bearer <token>`.
