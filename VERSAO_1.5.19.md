# EcoTech 1.5.19

## Login de usuário bloqueado
- Usuários com `is_active=False` continuam impedidos de autenticar.
- Quando a conta existe e a senha informada está correta, a tela de login exibe: **Usuário Bloqueado. Entre em contato com o seu supervisor ou administrador.**
- Senhas incorretas continuam exibindo apenas o erro genérico de credenciais, evitando revelar a existência de contas.
