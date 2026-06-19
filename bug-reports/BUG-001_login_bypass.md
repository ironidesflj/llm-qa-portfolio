# BUG-001 — Login permite acesso com conta desativada

**ID:** BUG-001  
**Data:** 2024-01-15  
**Reportado por:** Iron (QA Engineer)  
**Severidade:** 🔴 Crítica  
**Prioridade:** Alta  
**Status:** Aberto  
**Ambiente:** Staging — v2.3.1  

---

## Resumo
Usuários com conta desativada pelo admin conseguem realizar login com sucesso e acessar o dashboard normalmente.

---

## Impacto no Negócio
Risco de segurança crítico: ex-funcionários ou clientes com acesso revogado ainda conseguem acessar dados da plataforma.

---

## Passos para Reproduzir

1. Admin desativa o usuário `iron@teste.com` via painel admin em `/admin/users`
2. Confirmar que o status aparece como `INACTIVE` no banco: `SELECT status FROM users WHERE email = 'iron@teste.com';`
3. Acessar `http://localhost:3000/login`
4. Inserir email `iron@teste.com` e senha `Senha@123`
5. Clicar em "Entrar"

**Resultado Obtido:**  
Usuário é autenticado e redirecionado para `/dashboard` normalmente.

**Resultado Esperado:**  
Sistema deve retornar erro HTTP 403 com mensagem: *"Sua conta foi desativada. Entre em contato com o suporte."*

---

## Evidências

```
POST /api/auth/login HTTP/1.1
Body: {"email":"iron@teste.com","password":"Senha@123"}

Response: 200 OK
{"token":"eyJhbGc...","user":{"id":42,"status":"INACTIVE"}}
```

> **Nota:** O token JWT é gerado mesmo com `status: INACTIVE` — a validação de status não ocorre no endpoint de login.

---

## Análise Técnica
A API de login verifica apenas email e senha, mas não valida o campo `status` do usuário antes de gerar o token. A validação deveria ocorrer na query de autenticação:

```sql
-- Query atual (incorreta)
SELECT * FROM users WHERE email = ? AND password_hash = ?

-- Query corrigida (sugerida)
SELECT * FROM users WHERE email = ? AND password_hash = ? AND status = 'ACTIVE'
```

---

## Critério de Aceite para Correção
- [ ] Login com conta `INACTIVE` retorna HTTP 403
- [ ] Mensagem de erro amigável exibida ao usuário
- [ ] Log de tentativa de acesso registrado para auditoria
- [ ] Teste TC-001-09 adicionado à suite de regressão
