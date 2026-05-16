# Agente de Comunicação LigueLead

Transforma o Claude em um agente especialista em comunicação automatizada, usando **exclusivamente** LigueLead para SMS, Voz e SMS Flash.

## Passo a passo

### 1. Pegue as credenciais
Acesse **areadocliente.liguelead.app.br → Integrações → API Token → crie um App**
Copie o **API Token** e o **App ID**

### 2. Instale o MCP (no terminal)
```bash
claude mcp add -s user liguelead \
  -e LIGUELEAD_API_TOKEN=SEU_TOKEN \
  -e LIGUELEAD_APP_ID=SEU_APP_ID \
  -e TRANSPORT=stdio \
  -- npx -y @liguelead/mcp-server
```

### 3. Crie e abra o agente
```bash
mkdir -p agente-liguelead && cd agente-liguelead && \
curl -fsSL https://raw.githubusercontent.com/liguelead/agente-comunicacao/main/CLAUDE.md -o CLAUDE.md && \
claude
```

### 4. Use o agente
Digite sua dor de negócio. Exemplos:
- *"Clientes somem após a primeira sessão. Cria uma régua de retenção."*
- *"Tenho 20% de inadimplência. Quero recuperar sem perder o cliente."*
- *"Agenda visitas e metade não aparece. Reduz as faltas."*

O agente cria a régua e pode enviar SMS, Voz e SMS Flash diretamente via LigueLead.

## Canais disponíveis

| Canal | Quando usar |
|-------|-------------|
| SMS | Lembretes, confirmações, promoções |
| SMS Flash | Alertas críticos, 100% visualização |
| Voz (ligação) | Cobranças, urgência, alto impacto |

## Requisitos
- [Claude CLI](https://claude.ai/code) instalado
- Conta na [LigueLead](https://areadocliente.liguelead.app.br/cadastro?plan=api) com API Token e App ID
- Node.js instalado (para npx)
