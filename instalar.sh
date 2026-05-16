#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════╗
# ║   Agente de Comunicação LigueLead — Setup Automático     ║
# ║   Uso: bash instalar.sh API_TOKEN APP_ID                 ║
# ╚══════════════════════════════════════════════════════════╝
set -e

TEAL='\033[38;2;27;204;174m'
WHITE='\033[0m'
BOLD='\033[1m'
RED='\033[0;31m'

print() { echo -e "${TEAL}${BOLD}$1${WHITE}"; }
err()   { echo -e "${RED}✗ $1${WHITE}"; exit 1; }

API_TOKEN="${1:-$LIGUELEAD_API_TOKEN}"
APP_ID="${2:-$LIGUELEAD_APP_ID}"

print "⚡ Agente de Comunicação LigueLead"
echo ""

# ── 1. Verificar Claude CLI ──────────────────────────────────
print "1/4  Verificando Claude CLI..."
command -v claude &>/dev/null || err "Claude CLI não encontrado. Instale em: claude.ai/code"
print "     ✓ Claude CLI encontrado"

# ── 2. Verificar Node/npx ────────────────────────────────────
command -v npx &>/dev/null || err "npx não encontrado. Instale Node.js em: nodejs.org"

# ── 3. Instalar MCP da LigueLead ────────────────────────────
print "2/4  Instalando MCP da LigueLead..."

if [ -z "$API_TOKEN" ] || [ -z "$APP_ID" ]; then
  echo ""
  err "Informe API_TOKEN e APP_ID como argumentos:
  bash instalar.sh SEU_TOKEN SEU_APP_ID
  (Obtenha em: areadocliente.liguelead.app.br → Integrações → API Token)"
fi

claude mcp add -s user liguelead \
  -e LIGUELEAD_API_TOKEN="$API_TOKEN" \
  -e LIGUELEAD_APP_ID="$APP_ID" \
  -e TRANSPORT=stdio \
  -- npx -y @liguelead/mcp-server

print "     ✓ MCP instalado"

# ── 4. Criar estrutura de pastas ────────────────────────────
print "3/4  Criando estrutura do projeto..."
mkdir -p memoria relatorios

# CLAUDE.md
if [ ! -f CLAUDE.md ]; then
  curl -fsSL https://raw.githubusercontent.com/liguelead/agente-comunicacao/main/CLAUDE.md -o CLAUDE.md
fi
print "     ✓ CLAUDE.md criado"

# memoria/reguas.md
cat > memoria/reguas.md << 'EOF'
# Réguas de Comunicação

> Arquivo gerenciado pelo Agente de Comunicação LigueLead.

---

## Régua de Cobrança (exemplo)
**Objetivo:** Recuperar inadimplentes sem perder o relacionamento
**Gatilho:** D+1 após vencimento
**Critério de parada:** Pagamento confirmado ou D+30

| Etapa | Gatilho | Canal | Mensagem |
|-------|---------|-------|----------|
| 1 | D+1 | SMS | "Olá [Nome]! Sua fatura venceu ontem. Regularize: [link]" |
| 2 | D+3 | Voz | "Olá [Nome], sua fatura está em aberto. Ligue [tel]." |
| 3 | D+7 | SMS Flash | "⚠️ [Nome], última chance antes do bloqueio: [link]" |

---
EOF
print "     ✓ memoria/reguas.md criado"

cat > memoria/comunicacoes.md << 'EOF'
# Log de Comunicações

| Data/Hora | Canal | Destinatário | Régua | Status |
|-----------|-------|--------------|-------|--------|
EOF

cat > memoria/contatos.md << 'EOF'
# Contatos e Segmentos

## Formato
Nome: João Silva
Telefone: +5511999999999
Segmento: inadimplente / cliente-ativo / lead

---
EOF

cat > memoria/aprendizados.md << 'EOF'
# Aprendizados e Otimizações

- SMS de cobrança no D+1 têm maior taxa que no D+0
- Voz aumenta conversão ~30% vs SMS isolado
- SMS Flash: máx 1x por semana por contato

---
EOF
print "     ✓ Arquivos de memória criados"

# ── 5. Verificar ────────────────────────────────────────────
print "4/4  Verificando instalação..."
claude mcp list 2>/dev/null | grep -q liguelead && print "     ✓ liguelead MCP ativo" || echo "     ⚠ Verifique: claude mcp list"

echo ""
echo -e "${TEAL}${BOLD}╔══════════════════════════════════════════╗${WHITE}"
echo -e "${TEAL}${BOLD}║  ✅  Agente pronto!                      ║${WHITE}"
echo -e "${TEAL}${BOLD}╠══════════════════════════════════════════╣${WHITE}"
echo -e "${TEAL}${BOLD}║  Execute: claude                         ║${WHITE}"
echo -e "${TEAL}${BOLD}║  Diga: "Crie uma régua de cobrança"      ║${WHITE}"
echo -e "${TEAL}${BOLD}╚══════════════════════════════════════════╝${WHITE}"
echo ""
