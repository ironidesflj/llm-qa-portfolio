# TC-001 — Login de Usuário

**Módulo:** Autenticação  
**Tipo:** Funcional  
**Prioridade:** Alta  
**Status:** ✅ Aprovado  

---

## Objetivo
Verificar que o fluxo de login aceita credenciais válidas e rejeita inválidas com mensagens adequadas.

---

## Pré-condições
- Usuário `iron@teste.com` cadastrado no sistema com senha `Senha@123`
- Sistema acessível em `http://localhost:3000`

---

## Casos

| ID | Cenário | Entrada | Resultado Esperado | Status |
|----|---------|---------|-------------------|--------|
| TC-001-01 | Login válido | email: iron@teste.com / senha: Senha@123 | Redireciona para /dashboard | ✅ Pass |
| TC-001-02 | Senha incorreta | email: iron@teste.com / senha: errada | Mensagem "Credenciais inválidas" | ✅ Pass |
| TC-001-03 | Email inexistente | email: nao@existe.com / senha: qualquer | Mensagem "Credenciais inválidas" | ✅ Pass |
| TC-001-04 | Campos em branco | email: vazio / senha: vazia | Mensagem de campo obrigatório | ✅ Pass |
| TC-001-05 | Email sem @ | email: emailinvalido / senha: qualquer | Validação de formato de email | ✅ Pass |
| TC-001-06 | SQL Injection | email: `' OR '1'='1` | Rejeita — não autentica | ✅ Pass |
| TC-001-07 | Brute force (6 tentativas) | senha errada x6 | Conta bloqueada por 5 min | ✅ Pass |
| TC-001-08 | Lembrar sessão | login com "lembrar-me" marcado | Token persiste após fechar browser | ✅ Pass |

---

## Evidências
- Screenshots em `/docs/evidencias/TC-001/`
- Log de rede capturado no Postman

---

## Observações
> O campo senha não possui limite máximo de caracteres — recomenda-se adicionar validação para prevenir DoS.
