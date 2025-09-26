# Estrutura do Google Drive - Day Trade Content

Esta é a estrutura organizacional recomendada para o seu Google Drive, otimizada para o sistema automatizado de geração de conteúdo sobre day trade.

## 📁 Estrutura de Pastas

### `/videos`
- **Propósito**: Armazenar vídeos finalizados
- **Subpastas sugeridas**:
  - `2025/01/` - Organização por ano/mês
  - `estrategias/` - Vídeos sobre estratégias
  - `indicadores/` - Vídeos sobre indicadores técnicos
  - `iniciantes/` - Conteúdo para iniciantes

### `/imagens`
- **Propósito**: Imagens geradas automaticamente
- **Organização**: Por data de criação
- **Formato**: `day_trade_image_YYYY-MM-DD_HH-mm-ss.jpg`
- **Uso**: Thumbnails, posts para redes sociais, ilustrações

### `/roteiros`
- **Propósito**: Scripts e roteiros gerados
- **Formato**: Arquivos JSON com metadados
- **Conteúdo**: Texto do roteiro, prompts usados, timestamps

### `/assets`
- **Propósito**: Recursos reutilizáveis
- **Conteúdo**:
  - Logos e marcas d'água
  - Fontes personalizadas
  - Templates de vídeo
  - Música de fundo
  - Elementos gráficos

### `/publicacoes`
- **Propósito**: Controle de publicações
- **Conteúdo**:
  - Planilha de controle
  - Histórico de posts
  - Performance analytics
  - Calendário editorial

## 🔧 Configuração Automática

O sistema irá:

1. **Criar conteúdo automaticamente** a cada 4 horas
2. **Organizar arquivos** por data e tipo
3. **Fazer backup** de todo conteúdo gerado
4. **Manter histórico** para análise de performance

## 📊 Planilha de Controle

Localização: `/publicacoes/Controle_Publicacoes.xlsx`

Colunas recomendadas:
- ID único
- Data/Hora de criação
- Roteiro (texto)
- Imagens geradas (links)
- Status (gerado/publicado/arquivado)
- Plataforma (Instagram/TikTok/YouTube)
- Performance (views/likes/comentários)
- Tags utilizadas

## 🚀 Integração com Automação

### IDs Importantes
- **Pasta Principal**: `[SEU_GOOGLE_DRIVE_FOLDER_ID]`
- **Pasta Imagens**: `[ID_PASTA_IMAGENS]`
- **Pasta Roteiros**: `[ID_PASTA_ROTEIROS]`

### Permissões Necessárias
- Leitura e escrita na pasta principal
- Criação de subpastas
- Upload de arquivos
- Compartilhamento (opcional)

## 📱 Uso com Redes Sociais

### Instagram/TikTok
- Formato: 1080x1080 ou 1080x1920
- Duração: 15-60 segundos
- Hashtags: #daytrade #mercadofinanceiro #investimentos

### YouTube Shorts
- Formato: 1080x1920
- Duração: até 60 segundos
- Título otimizado para SEO

## 🔄 Manutenção

### Limpeza Automática
- Arquivos com mais de 30 dias são movidos para pasta "Arquivo"
- Backup semanal em pasta separada
- Relatório mensal de uso de espaço

### Monitoramento
- Log de atividades em `/logs/`
- Alertas por email em caso de erro
- Dashboard de performance

## 📞 Suporte

Para dúvidas sobre a estrutura ou configuração:
1. Verifique os logs em `/logs/`
2. Consulte a documentação técnica
3. Entre em contato com o suporte

---

**Última atualização**: 25/09/2025
**Versão**: 1.0
**Compatibilidade**: Pipedream, n8n, Google Drive API
