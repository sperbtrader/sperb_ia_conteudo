# Guia de Configuração - Pipedream para Day Trade Content

Este guia detalha como configurar o sistema automatizado de geração de conteúdo sobre day trade no Pipedream.

## Pré-requisitos

Antes de começar, você precisará de:

**Contas e APIs necessárias:**
- Conta no Pipedream (gratuita)
- API Key da OpenAI (para geração de texto)
- Conta Google com acesso ao Google Drive
- Pasta configurada no Google Drive

**Arquivos necessários:**
- `day_trade_content_generator_free.json` (workflow do Pipedream)
- Credenciais do Google Drive
- Configuração das variáveis de ambiente

## Passo 1: Configuração Inicial do Pipedream

### 1.1 Criar Conta no Pipedream
1. Acesse [pipedream.com](https://pipedream.com)
2. Crie uma conta gratuita
3. Confirme seu email
4. Acesse o dashboard

### 1.2 Importar o Workflow
1. No dashboard, clique em "New Workflow"
2. Selecione "Import from JSON"
3. Cole o conteúdo do arquivo `day_trade_content_generator_free.json`
4. Clique em "Import Workflow"

## Passo 2: Configuração das APIs

### 2.1 OpenAI API
**Obter API Key:**
1. Acesse [platform.openai.com](https://platform.openai.com/api-keys)
2. Faça login na sua conta OpenAI
3. Clique em "Create new secret key"
4. Copie a chave gerada (guarde com segurança)

**Configurar no Pipedream:**
1. No workflow, localize o nó "ROTEIRO"
2. Clique em "Connect Account"
3. Cole sua API Key da OpenAI
4. Teste a conexão

### 2.2 Google Drive API
**Configurar Credenciais:**
1. Acesse [console.developers.google.com](https://console.developers.google.com/)
2. Crie um novo projeto ou selecione existente
3. Ative a "Google Drive API"
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo JSON de credenciais

**Conectar no Pipedream:**
1. No workflow, localize o nó "Upload Google Drive"
2. Clique em "Connect Account"
3. Autorize o acesso ao Google Drive
4. Selecione a conta correta

## Passo 3: Configuração das Variáveis

### 3.1 Nó SETUP
Configure as seguintes variáveis no nó SETUP:

```json
{
  "g_googledrive_dir": "SEU_GOOGLE_DRIVE_FOLDER_ID",
  "g_qtdimagens": "3",
  "pollinations_api_url": "https://image.pollinations.ai/prompt/"
}
```

**Como obter o Google Drive Folder ID:**
1. Abra sua pasta no Google Drive
2. Copie o ID da URL: `https://drive.google.com/drive/folders/[ID_AQUI]`
3. Cole no campo `g_googledrive_dir`

### 3.2 Configuração do Agendamento
No nó "Schedule":
- **Intervalo**: A cada 4 horas
- **Timezone**: Seu fuso horário local
- **Status**: Ativo

## Passo 4: Teste do Workflow

### 4.1 Teste Manual
1. Clique em "Test" no workflow
2. Verifique cada nó individualmente
3. Confirme se as imagens são geradas
4. Verifique se o upload no Google Drive funciona

### 4.2 Verificação de Logs
1. Acesse a aba "Logs" no Pipedream
2. Verifique se não há erros
3. Confirme se o conteúdo está sendo gerado

## Passo 5: Otimizações e Monitoramento

### 5.1 Configurações Avançadas
**Rate Limiting:**
- OpenAI: Máximo 60 requests/minuto
- Pollinations: Sem limite específico
- Google Drive: 1000 requests/100 segundos

**Error Handling:**
- Configure retry automático em caso de falha
- Adicione notificações por email para erros
- Implemente fallbacks para APIs indisponíveis

### 5.2 Monitoramento
**Métricas importantes:**
- Taxa de sucesso na geração de conteúdo
- Tempo médio de execução
- Uso de cota das APIs
- Espaço utilizado no Google Drive

**Alertas recomendados:**
- Falha na geração de conteúdo
- Cota de API esgotada
- Erro no upload para Google Drive
- Workflow parado por mais de 8 horas

## Passo 6: Configurações de Produção

### 6.1 Ambiente de Produção
**Variáveis de ambiente:**
```
OPENAI_API_KEY=sua_chave_openai
GOOGLE_DRIVE_FOLDER_ID=id_da_pasta
PIPEDREAM_WEBHOOK_URL=url_do_webhook
```

**Backup e Recuperação:**
- Configure backup automático dos workflows
- Mantenha cópia das configurações
- Documente todas as alterações

### 6.2 Escalabilidade
**Para aumentar a produção:**
- Reduza o intervalo para 2 horas
- Aumente o número de imagens por execução
- Configure múltiplos workflows para temas diferentes

## Troubleshooting

### Problemas Comuns

**Erro: "OpenAI API quota exceeded"**
- Solução: Verifique sua cota na OpenAI
- Alternativa: Implemente rate limiting

**Erro: "Google Drive permission denied"**
- Solução: Reautorize a conexão
- Verifique as permissões da pasta

**Erro: "Pollinations API timeout"**
- Solução: Adicione retry automático
- Use prompts mais simples

**Workflow não executa no horário**
- Verifique se está ativo
- Confirme o timezone
- Verifique logs de erro

### Logs e Debugging

**Ativar logs detalhados:**
1. No workflow, ative "Debug mode"
2. Adicione logs customizados nos nós
3. Monitore a execução em tempo real

**Análise de performance:**
- Tempo médio por nó
- Taxa de erro por API
- Uso de recursos do Pipedream

## Custos e Limites

### Pipedream (Plano Gratuito)
- 10.000 invocações/mês
- 30 segundos timeout por step
- 512MB memória por execução

### APIs Utilizadas
- **OpenAI**: ~$0.002 por request (GPT-4o-mini)
- **Pollinations**: Gratuito
- **Google Drive**: Gratuito (até 15GB)

### Estimativa Mensal
- Execuções: 180/mês (a cada 4 horas)
- Custo OpenAI: ~$0.36/mês
- Custo total: Menos de $1/mês

## Próximos Passos

Após a configuração:

1. **Monitore por 48 horas** para garantir estabilidade
2. **Ajuste os prompts** baseado na qualidade das imagens
3. **Configure integrações** com redes sociais (opcional)
4. **Implemente analytics** para medir performance
5. **Escale o sistema** conforme necessário

## Suporte

Para dúvidas ou problemas:
- Documentação oficial do Pipedream
- Logs detalhados do sistema
- Comunidade Pipedream no Discord
- Suporte técnico via email

---

**Última atualização**: 25/09/2025  
**Versão**: 1.0  
**Compatibilidade**: Pipedream, OpenAI API, Google Drive API, Pollinations AI
