# EcoTech 1.5.17

- Redesign do formulário administrativo "Novo usuário" em grid responsivo.
- Campos obrigatórios identificados com um único asterisco.
- Removido o help text técnico padrão do campo Usuário.
- Adicionados CEP, Número e Bairro ao cadastro administrativo.
- CEP com máscara XXXXX-XXX e preenchimento automático de endereço, bairro, UF e cidade via ViaCEP.
- UF transformada em select com as 27 unidades federativas.
- Cidade carregada dinamicamente conforme a UF via API de localidades do IBGE.
- CPF/CNPJ e telefone com máscaras de digitação.
- Campo Senha com botão Gerar senha; senha fica visível ao administrador e é armazenada com hash pelo Django.
- Número do imóvel permanece editável, pois serviços de CEP não retornam esse dado de forma confiável.
