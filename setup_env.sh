#!/bin/bash

# Script de Configuração de Ambiente para Day Trade Content Generator
# Execute este script para configurar as variáveis de ambiente necessárias

echo "🔧 Configurando ambiente para Day Trade Content Generator..."

# Cria arquivo de configuração
cat > /home/ubuntu/.env << 'EOF'
# API Keys - Substitua pelos seus valores reais
OPENAI_API_KEY=sua_openai_api_key_aqui
REPLICATE_API_TOKEN=seu_replicate_token_aqui

# Configurações do Google Drive
GOOGLE_DRIVE_FOLDER_ID=id_da_sua_pasta_no_google_drive

# Configurações do sistema
CONTENT_GENERATION_INTERVAL=4  # horas
MAX_IMAGES_PER_CONTENT=3
LOG_LEVEL=INFO
EOF

echo "✅ Arquivo .env criado em /home/ubuntu/.env"
echo ""
echo "📝 IMPORTANTE: Edite o arquivo .env e adicione suas API keys:"
echo "   - OpenAI API Key (para geração de texto)"
echo "   - Replicate API Token (para geração de imagens)"
echo "   - Google Drive Folder ID (opcional)"
echo ""
echo "🔗 Links para obter as chaves:"
echo "   OpenAI: https://platform.openai.com/api-keys"
echo "   Replicate: https://replicate.com/account/api-tokens"
echo ""

# Cria diretórios necessários
mkdir -p /home/ubuntu/generated_content
mkdir -p /home/ubuntu/logs

echo "📁 Diretórios criados:"
echo "   - /home/ubuntu/generated_content (para conteúdo gerado)"
echo "   - /home/ubuntu/logs (para logs do sistema)"
echo ""

# Torna os scripts executáveis
chmod +x /home/ubuntu/day_trade_generator.py
chmod +x /home/ubuntu/automation_scheduler.py

echo "🚀 Scripts configurados como executáveis"
echo ""
echo "⚡ Para iniciar o sistema:"
echo "   1. Edite o arquivo .env com suas API keys"
echo "   2. Execute: python3 /home/ubuntu/automation_scheduler.py"
echo ""
echo "🔄 O sistema irá:"
echo "   - Gerar conteúdo a cada 4 horas"
echo "   - Limpar arquivos antigos diariamente"
echo "   - Salvar logs em automation.log"
echo ""
