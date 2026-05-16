#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════╗
# ║   Agente de Comunicação LigueLead — Setup Automático     ║
# ║   Uso: bash instalar.sh [LIGUELEAD_API_KEY]             ║
# ╚══════════════════════════════════════════════════════════╝
set -e

TEAL='\033[38;2;27;204;174m'
WHITE='\033[0m'
BOLD='\033[1m'
RED='\033[0;31m'

print() { echo -e "${TEAL}${BOLD}$1${WHITE}"; }
err()   { echo -e "${RED}✗ $1${WHITE}"; exit 1; }

API_KEY="${1:-$LIGUELEAD_API_KEY}"

print "⚡ Agente de Comunicação LigueLead"
echo ""

# ── 1. Verificar Claude CLI ──────────────────────────────────
print "1/4  Verificando Claude CLI..."
command -v claude &>/dev/null || err "Claude CLI não encontrado. Instale em: claude.ai/code"
print "     ✓ Claude CLI encontrado"

# ── 2. Instalar MCP da LigueLead ────────────────────────────
print "2/4  Instalando MCP da LigueLead..."
if [ -n "$API_KEY" ]; then
  claude mcp add --transport http liguelead https://mcp.liguelead.com.br \
    --header "Authorization: Bearer ${API_KEY}"
else
  claude mcp add --transport http liguelead https://mcp.liguelead.com.br
fi
print "     ✓ MCP instalado"

# ── 3. Criar estrutura de pastas ────────────────────────────
print "3/4  Criando estrutura do projeto..."
mkdir -p memoria relatorios 2>/dev/null || true

# CLAUDE.md — prompt principal do agente
if [ ! -f CLAUDE.md ]; then
  curl -fsSL https://raw.githubusercontent.com/liguelead/agente-comunicacao/main/CLAUDE.md -o CLAUDE.md
  print "     ✓ CLAUDE.md criado"
fi

# memoria/reguas.md
cat > memoria/reguas.md << 'EOF'
# Réguas de Comunicação

> Arquivo gerenciado pelo Agente de Comunicação LigueLead.
> Cada régua aprovada é salva aqui automaticamente.

---

## Exemplos de Réguas

### Régua de Cobrança
**Objetivo:** Recuperar inadimplentes sem perder o relacionamento
**Gatilho:** D+1 após vencimento
**Critério de parada:** Pagamento confirmado ou D+30

| Etapa | Gatilho | Canal | Mensagem |
|-------|---------|-------|----------|
| 1 | D+1 | SMS | "Olá [Nome]! Sua fatura venceu ontem. Regularize agora: [link]" |
| 2 | D+3 | Voz | "Olá [Nome], aqui é a [Empresa]. Sua fatura está em aberto. Ligue [tel] para regularizar." |
| 3 | D+7 | SMS Flash | "⚠️ [Nome], última chance antes do bloqueio. Pague agora: [link]" |

---
EOF
print "     ✓ memoria/reguas.md criado"

# memoria/comunicacoes.md
cat > memoria/comunicacoes.md << 'EOF'
# Log de Comunicações

> Registro automático de todas as mensagens enviadas pelo agente.

| Data/Hora | Canal | Destinatário | Régua | Status |
|-----------|-------|--------------|-------|--------|
EOF
print "     ✓ memoria/comunicacoes.md criado"

# memoria/contatos.md
cat > memoria/contatos.md << 'EOF'
# Contatos e Segmentos

> Base de contatos cadastrada pelo usuário.

## Formato de contato
```
Nome: João Silva
Telefone: +5511999999999
Segmento: inadimplente / cliente-ativo / lead
```

---

## Contatos

<!-- Adicione contatos abaixo -->
EOF
print "     ✓ memoria/contatos.md criado"

# memoria/aprendizados.md
cat > memoria/aprendizados.md << 'EOF'
# Aprendizados e Otimizações

> O agente registra aqui o que funciona e o que não funciona.

## Melhores práticas identificadas

- SMS de cobrança no D+1 têm maior taxa de pagamento que no D+0
- Voz aumenta conversão em ~30% versus SMS isolado
- SMS Flash deve ser usado com moderação (máx 1x por semana por contato)

---
EOF
print "     ✓ memoria/aprendizados.md criado"

# ── 4. Verificar instalação ─────────────────────────────────
print "4/4  Verificando MCP..."
claude mcp list 2>/dev/null | grep -q liguelead && print "     ✓ liguelead MCP ativo" || echo "     ⚠ Verifique com: claude mcp list"

echo ""
echo -e "${TEAL}${BOLD}╔══════════════════════════════════════════╗${WHITE}"
echo -e "${TEAL}${BOLD}║  ✅  Agente pronto para uso!             ║${WHITE}"
echo -e "${TEAL}${BOLD}╠══════════════════════════════════════════╣${WHITE}"
echo -e "${TEAL}${BOLD}║  Execute: claude                         ║${WHITE}"
echo -e "${TEAL}${BOLD}║  Diga: "Crie uma régua de cobrança"      ║${WHITE}"
echo -e "${TEAL}${BOLD}╚══════════════════════════════════════════╝${WHITE}"
echo ""
