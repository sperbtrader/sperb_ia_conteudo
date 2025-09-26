# 🚀 Gerador de Conteúdo Automatizado sobre Day Trade

**Versão**: 1.0.0  
**Autor**: Manus AI  
**Data**: 25/09/2025

## 📖 Visão Geral

Este projeto é um sistema completo e automatizado para a **criação e postagem de conteúdo sobre day trade e mercado financeiro**. Ele foi projetado para funcionar 24/7 em servidores gratuitos, utilizando APIs de inteligência artificial para gerar roteiros educativos e imagens de alta qualidade, com integração total ao Google Drive e Pipedream.

O sistema é capaz de gerar conteúdo sobre:
- **Estratégias de Day Trade**: Scalping, breakouts, etc.
- **Aulas sobre Indicadores**: MACD, IFR, Bandas de Bollinger, etc.
- **Dicas para Iniciantes**: Gerenciamento de risco, psicologia do trader, etc.

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição | Status |
| :--- | :--- | :--- |
| **Geração de Roteiros** | Cria roteiros curtos e educativos usando a API da OpenAI (GPT-4o-mini). | ✅ Completo |
| **Geração de Imagens** | Gera imagens profissionais e temáticas com a API gratuita **Pollinations AI**. | ✅ Completo |
| **Automação 24/7** | Executa automaticamente a cada 4 horas para gerar novo conteúdo. | ✅ Completo |
| **Integração Google Drive** | Organiza e salva todo o conteúdo gerado em uma estrutura de pastas otimizada. | ✅ Completo |
| **Workflow para Pipedream** | Inclui um arquivo JSON pronto para ser importado no Pipedream. | ✅ Completo |
| **Deploy em Servidor Gratuito** | Suporte completo para deploy em plataformas como **Railway**, Render e Google Cloud Run. | ✅ Completo |
| **Containerização** | O sistema é totalmente containerizado com **Docker** para fácil portabilidade. | ✅ Completo |
| **CI/CD com GitHub Actions** | Inclui um workflow de deploy contínuo e monitoramento para manter o serviço ativo. | ✅ Completo |

## 📁 Estrutura do Projeto

Este pacote contém todos os arquivos necessários para configurar e executar o sistema.

```
/
├── 📂 .github/                    # Configuração do GitHub Actions para CI/CD
│   └── workflows/
│       └── deploy.yml
├── 📂 google_drive_structure/      # Estrutura e scripts para o Google Drive
│   ├── config/
│   │   └── google_drive_config.json
│   ├── publicacoes/
│   │   └── Controle_Publicacoes.csv
│   ├── README.md
│   └── setup_google_drive.py
├── 📜 .env.example                # Exemplo de arquivo para variáveis de ambiente
├── 📜 .gitignore                  # Arquivos a serem ignorados pelo Git
├── 📜 Dockerfile                  # Define o container da aplicação
├── 📜 Eli_Rigobeli_IA___Historias_Aliens.json # Arquivo original de referência
├── 📜 EstruturaparaGoogleDrive-20250925T233137Z-1-001.zip # Arquivo original
├── 📜 README.md                   # Este arquivo
├── 📜 automation_scheduler.py     # Script principal que agenda e executa a automação
├── 📜 day_trade_content_generator.json # Workflow Pipedream (com API paga)
├── 📜 day_trade_content_generator_free.json # Workflow Pipedream (com API gratuita - recomendado)
├── 📜 day_trade_generator.py      # Script de geração de conteúdo (com API paga)
├── 📜 day_trade_generator_free.py # Script de geração de conteúdo (com API gratuita - recomendado)
├── 📜 deploy.sh                   # Script de deploy automatizado
├── 📜 deploy_guide.md             # Guia de deploy para servidores gratuitos
├── 📜 docker-compose.yml          # Orquestração de containers para deploy local
├── 📜 pipedream_auto_setup.py     # Script para configuração automática no Pipedream
├── 📜 pipedream_config.json       # Arquivo de configuração detalhado para Pipedream
├── 📜 pipedream_setup_guide.md    # Guia completo de configuração do Pipedream
├── 📜 requirements.txt            # Dependências Python do projeto
├── 📜 setup_env.sh                # Script para configuração inicial do ambiente
└── 📜 webhook_server.py           # Servidor webhook opcional para triggers externos
```

## 🚀 Guia de Início Rápido

Siga estes passos para colocar o sistema no ar em **menos de 10 minutos** usando o **Railway** (recomendado).

### Passo 1: Preparar o Ambiente

1.  **Crie um repositório no GitHub** e envie todos os arquivos deste projeto.
2.  **Obtenha suas API Keys**:
    *   **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    *   **Railway Token**: Gere um token na sua conta Railway.
3.  **Configure os Secrets no GitHub** (em `Settings` > `Secrets and variables` > `Actions`):
    *   `OPENAI_API_KEY`: Sua chave da OpenAI.
    *   `GOOGLE_DRIVE_FOLDER_ID`: O ID da pasta que você criará no Google Drive.
    *   `RAILWAY_TOKEN`: Seu token do Railway.
    *   `RAILWAY_URL`: A URL pública do seu serviço no Railway (após o primeiro deploy).

### Passo 2: Configurar o Google Drive

1.  Crie uma pasta principal no seu Google Drive para o projeto.
2.  Copie o ID da pasta da URL (ex: `https://drive.google.com/drive/folders/ESTE_É_O_ID`).
3.  Adicione este ID ao secret `GOOGLE_DRIVE_FOLDER_ID` no GitHub.

### Passo 3: Deploy no Railway

1.  Crie uma conta no [Railway](https://railway.app) e conecte seu GitHub.
2.  Crie um "New Project" e selecione "Deploy from GitHub repo".
3.  Escolha o repositório que você criou.
4.  O Railway detectará o `Dockerfile` e fará o deploy automaticamente.
5.  Após o primeiro deploy, adicione a URL pública do serviço ao secret `RAILWAY_URL` no GitHub para habilitar o monitoramento.

O sistema de CI/CD configurado no arquivo `.github/workflows/deploy.yml` cuidará do resto, incluindo testes, deploy e monitoramento para manter o serviço sempre ativo.

## ⚙️ Uso Alternativo com Pipedream

Se preferir usar o Pipedream em vez de um servidor dedicado, siga o guia detalhado `pipedream_setup_guide.md` e importe o arquivo `day_trade_content_generator_free.json`.

## 🔧 Tecnologias Utilizadas

| Tecnologia | Propósito | Custo |
| :--- | :--- | :--- |
| **Python** | Linguagem principal para automação e scripts. | Gratuito |
| **Docker** | Containerização para portabilidade e deploy. | Gratuito |
| **GitHub Actions** | CI/CD, testes e monitoramento 24/7. | Gratuito |
| **Railway** | Hospedagem gratuita do container Docker. | Gratuito (500h/mês) |
| **OpenAI API** | Geração de roteiros e prompts (GPT-4o-mini). | ~ $0.36/mês |
| **Pollinations AI** | Geração de imagens de alta qualidade. | **Totalmente Gratuito** |
| **Google Drive** | Armazenamento e organização dos arquivos. | Gratuito (15GB) |
| **Pipedream** | Plataforma de automação (alternativa ao deploy). | Gratuito |

## 📈 Potenciais Melhorias

- **Postagem Automática**: Integrar com APIs de redes sociais (Instagram, TikTok) para postar o conteúdo gerado.
- **Análise de Performance**: Criar um dashboard para analisar o engajamento do conteúdo postado.
- **Geração de Vídeo**: Utilizar ferramentas como Remotion ou a API da RunwayML para gerar vídeos completos a partir das imagens e roteiros.
- **Variação de Voz**: Integrar com a API da ElevenLabs para gerar narrações com diferentes vozes.

## 📞 Suporte

Este é um projeto complexo e completo. Para qualquer dúvida, consulte a documentação específica de cada arquivo ou siga os guias detalhados incluídos no pacote.

