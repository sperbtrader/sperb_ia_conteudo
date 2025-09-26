#!/bin/bash

# Script de Deploy Automatizado - Day Trade Content Generator
# Suporta múltiplas plataformas de hospedagem gratuita

set -e  # Para na primeira falha

echo "🚀 Day Trade Content Generator - Deploy Automatizado"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."
    
    if ! command -v git &> /dev/null; then
        log_error "Git não está instalado"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_warning "Docker não encontrado - alguns deploys podem falhar"
    fi
    
    log_success "Dependências verificadas"
}

# Preparar arquivos para deploy
prepare_files() {
    log_info "Preparando arquivos para deploy..."
    
    # Criar .gitignore se não existir
    if [ ! -f .gitignore ]; then
        cat > .gitignore << EOF
# Environment variables
.env
*.env

# Credentials
credentials.json
token.pickle
google_drive_credentials.json

# Generated content
generated_content/
logs/
*.log

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# OS
.DS_Store
Thumbs.db
EOF
        log_success "Arquivo .gitignore criado"
    fi
    
    # Criar arquivo .env.example
    cat > .env.example << EOF
# API Keys - Substitua pelos valores reais
OPENAI_API_KEY=sua_openai_api_key_aqui
GOOGLE_DRIVE_FOLDER_ID=id_da_sua_pasta_no_google_drive

# Configurações do sistema
CONTENT_GENERATION_INTERVAL=4
MAX_IMAGES_PER_CONTENT=3
LOG_LEVEL=INFO
TZ=America/Sao_Paulo

# Webhook (opcional)
WEBHOOK_SECRET=seu_webhook_secret_aqui
EOF
    
    log_success "Arquivos preparados"
}

# Configurar repositório Git
setup_git() {
    log_info "Configurando repositório Git..."
    
    if [ ! -d .git ]; then
        git init
        log_success "Repositório Git inicializado"
    fi
    
    # Adicionar arquivos
    git add .
    
    # Commit se houver mudanças
    if ! git diff --cached --quiet; then
        git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
        log_success "Commit realizado"
    else
        log_info "Nenhuma mudança para commit"
    fi
}

# Deploy para Railway
deploy_railway() {
    log_info "Iniciando deploy para Railway..."
    
    if ! command -v railway &> /dev/null; then
        log_warning "Railway CLI não instalado. Instalando..."
        npm install -g @railway/cli
    fi
    
    # Login no Railway (se necessário)
    if ! railway whoami &> /dev/null; then
        log_info "Faça login no Railway:"
        railway login
    fi
    
    # Deploy
    railway up
    
    log_success "Deploy para Railway concluído"
}

# Deploy para Render
deploy_render() {
    log_info "Deploy para Render..."
    log_info "Para Render, você precisa:"
    echo "1. Conectar seu repositório GitHub ao Render"
    echo "2. Configurar as variáveis de ambiente"
    echo "3. O deploy será automático a cada push"
    
    read -p "Pressione Enter para continuar..."
}

# Deploy para Google Cloud Run
deploy_gcloud() {
    log_info "Iniciando deploy para Google Cloud Run..."
    
    if ! command -v gcloud &> /dev/null; then
        log_error "Google Cloud SDK não instalado"
        log_info "Instale em: https://cloud.google.com/sdk/docs/install"
        return 1
    fi
    
    # Verificar autenticação
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 &> /dev/null; then
        log_info "Fazendo login no Google Cloud..."
        gcloud auth login
    fi
    
    # Configurar projeto
    read -p "Digite o ID do seu projeto Google Cloud: " PROJECT_ID
    gcloud config set project $PROJECT_ID
    
    # Build e deploy
    gcloud run deploy day-trade-generator \
        --source . \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1 \
        --timeout 300
    
    log_success "Deploy para Google Cloud Run concluído"
}

# Deploy para Fly.io
deploy_fly() {
    log_info "Iniciando deploy para Fly.io..."
    
    if ! command -v flyctl &> /dev/null; then
        log_warning "Fly CLI não instalado. Instalando..."
        curl -L https://fly.io/install.sh | sh
    fi
    
    # Login
    if ! flyctl auth whoami &> /dev/null; then
        flyctl auth login
    fi
    
    # Inicializar app se necessário
    if [ ! -f fly.toml ]; then
        flyctl launch --no-deploy
    fi
    
    # Deploy
    flyctl deploy
    
    log_success "Deploy para Fly.io concluído"
}

# Menu principal
main_menu() {
    echo ""
    echo "Escolha a plataforma para deploy:"
    echo "1) Railway (Recomendado - Fácil)"
    echo "2) Render (Simples)"
    echo "3) Google Cloud Run (Avançado)"
    echo "4) Fly.io (Intermediário)"
    echo "5) Preparar apenas (sem deploy)"
    echo "0) Sair"
    echo ""
    
    read -p "Digite sua escolha (0-5): " choice
    
    case $choice in
        1)
            deploy_railway
            ;;
        2)
            deploy_render
            ;;
        3)
            deploy_gcloud
            ;;
        4)
            deploy_fly
            ;;
        5)
            log_info "Arquivos preparados. Deploy manual necessário."
            ;;
        0)
            log_info "Saindo..."
            exit 0
            ;;
        *)
            log_error "Opção inválida"
            main_menu
            ;;
    esac
}

# Verificar configuração
check_config() {
    log_info "Verificando configuração..."
    
    if [ ! -f .env ] && [ ! -f .env.example ]; then
        log_warning "Arquivo .env não encontrado"
        log_info "Certifique-se de configurar suas API keys antes do deploy"
    fi
    
    if [ ! -f requirements.txt ]; then
        log_error "Arquivo requirements.txt não encontrado"
        exit 1
    fi
    
    if [ ! -f Dockerfile ]; then
        log_error "Dockerfile não encontrado"
        exit 1
    fi
    
    log_success "Configuração verificada"
}

# Função principal
main() {
    check_dependencies
    check_config
    prepare_files
    setup_git
    main_menu
    
    echo ""
    log_success "Deploy process completed!"
    log_info "Não se esqueça de:"
    echo "  • Configurar as variáveis de ambiente na plataforma"
    echo "  • Testar o endpoint /health"
    echo "  • Configurar monitoramento"
    echo "  • Verificar os logs após o deploy"
}

# Executar função principal
main "$@"
