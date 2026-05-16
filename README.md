# Agente de Comunicação LigueLead

Transforma o Claude em um agente especialista em comunicação automatizada, usando **exclusivamente** LigueLead para SMS, Voz e SMS Flash.

## Instalação em 1 comando

```bash
curl -fsSL https://raw.githubusercontent.com/liguelead/agente-comunicacao/main/instalar.sh | bash -s -- SUA_API_KEY
```

Isso instala o MCP da LigueLead, cria a estrutura de pastas e os arquivos de memória.

## O que o agente faz

- Cria réguas de comunicação completas a partir da sua dor de negócio
- Envia SMS, ligações automáticas e SMS Flash via LigueLead MCP
- Mantém memória persistente em arquivos `.md`
- Registra todas as comunicações enviadas
- Aprende com os resultados e sugere otimizações

## Estrutura criada

```
seu-projeto/
  CLAUDE.md              ← prompt do agente
  memoria/
    reguas.md            ← réguas aprovadas e ativas
    comunicacoes.md      ← log de todos os envios
    contatos.md          ← base de contatos
    aprendizados.md      ← o que funciona
  relatorios/            ← análises por campanha
```

## Uso

```bash
cd seu-projeto
claude
```

Exemplos do que dizer:
- *"Tenho uma clínica e clientes somem após a 1ª sessão. Cria uma régua de retenção."*
- *"Envia um SMS de cobrança para +5511999999999"*
- *"Qual foi o último envio realizado?"*
- *"Mostra todas as réguas ativas"*

## Canais disponíveis

| Canal | Quando usar |
|-------|-------------|
| SMS | Lembretes, confirmações, promoções |
| Voz (ligação) | Cobranças, urgência, alto impacto |
| SMS Flash | Alertas críticos, máxima urgência |

## Requisitos

- [Claude CLI](https://claude.ai/code) instalado
- Conta na [LigueLead](https://areadocliente.liguelead.app.br/cadastro?plan=api)
- API Key da LigueLead
