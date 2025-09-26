#!/usr/bin/env python3
"""
Script para configurar automaticamente a estrutura no Google Drive
Cria todas as pastas necessárias e configura permissões
"""

import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

class GoogleDriveSetup:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.service = None
        self.main_folder_id = None
        
    def authenticate(self):
        """Autentica com o Google Drive"""
        creds = None
        
        # Token salvo anteriormente
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Se não há credenciais válidas, faz login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salva as credenciais para próxima execução
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Autenticado com sucesso no Google Drive")
    
    def create_folder(self, name, parent_id='root'):
        """Cria uma pasta no Google Drive"""
        try:
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            print(f"📁 Pasta criada: {name} (ID: {folder_id})")
            return folder_id
            
        except Exception as e:
            print(f"❌ Erro ao criar pasta {name}: {e}")
            return None
    
    def setup_folder_structure(self):
        """Cria toda a estrutura de pastas"""
        print("🚀 Iniciando configuração da estrutura no Google Drive...")
        
        # Cria pasta principal
        main_folder_id = self.create_folder("Day Trade Content Generator")
        if not main_folder_id:
            print("❌ Falha ao criar pasta principal")
            return False
        
        self.main_folder_id = main_folder_id
        
        # Estrutura de subpastas
        folders = {
            'videos': 'Vídeos finalizados',
            'imagens': 'Imagens geradas automaticamente', 
            'roteiros': 'Scripts e roteiros',
            'assets': 'Recursos reutilizáveis',
            'publicacoes': 'Controle de publicações',
            'logs': 'Logs do sistema',
            'backup': 'Backup automático',
            'arquivo': 'Arquivos antigos'
        }
        
        folder_ids = {}
        
        for folder_name, description in folders.items():
            folder_id = self.create_folder(folder_name, main_folder_id)
            if folder_id:
                folder_ids[folder_name] = folder_id
        
        # Cria subpastas organizacionais em videos
        if 'videos' in folder_ids:
            video_subfolders = ['estrategias', 'indicadores', 'iniciantes', '2025']
            for subfolder in video_subfolders:
                self.create_folder(subfolder, folder_ids['videos'])
        
        # Salva configuração
        config = {
            'main_folder_id': main_folder_id,
            'folder_ids': folder_ids,
            'setup_date': '2025-09-25',
            'status': 'configured'
        }
        
        with open('google_drive_setup.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Estrutura criada com sucesso!")
        print(f"📋 ID da pasta principal: {main_folder_id}")
        print("💾 Configuração salva em: google_drive_setup.json")
        
        return True
    
    def upload_initial_files(self):
        """Faz upload dos arquivos iniciais"""
        if not self.main_folder_id:
            print("❌ Pasta principal não configurada")
            return
        
        # Lista de arquivos para upload
        files_to_upload = [
            ('README.md', 'README.md'),
            ('Controle_Publicacoes.csv', 'publicacoes/Controle_Publicacoes.csv'),
            ('google_drive_config.json', 'config/google_drive_config.json')
        ]
        
        print("📤 Fazendo upload dos arquivos iniciais...")
        
        for filename, local_path in files_to_upload:
            if os.path.exists(local_path):
                try:
                    with open(local_path, 'rb') as f:
                        media_body = f.read()
                    
                    file_metadata = {
                        'name': filename,
                        'parents': [self.main_folder_id]
                    }
                    
                    # Upload do arquivo
                    file = self.service.files().create(
                        body=file_metadata,
                        media_body=media_body,
                        fields='id'
                    ).execute()
                    
                    print(f"✅ Upload: {filename}")
                    
                except Exception as e:
                    print(f"❌ Erro no upload de {filename}: {e}")
    
    def generate_instructions(self):
        """Gera instruções para o usuário"""
        instructions = f"""
🎉 CONFIGURAÇÃO CONCLUÍDA!

Sua estrutura do Google Drive foi criada com sucesso.

📁 PASTA PRINCIPAL: {self.main_folder_id}

🔧 PRÓXIMOS PASSOS:

1. Copie o ID da pasta principal: {self.main_folder_id}

2. Cole este ID nos seguintes arquivos:
   - day_trade_content_generator_free.json (campo g_googledrive_dir)
   - .env (campo GOOGLE_DRIVE_FOLDER_ID)

3. Configure suas API keys no arquivo .env:
   - OPENAI_API_KEY=sua_chave_aqui
   - GOOGLE_DRIVE_FOLDER_ID={self.main_folder_id}

4. Execute o sistema:
   python3 automation_scheduler.py

🔗 LINKS ÚTEIS:
- Pasta no Drive: https://drive.google.com/drive/folders/{self.main_folder_id}
- Documentação: README.md na pasta principal

✅ SISTEMA PRONTO PARA USO!
        """
        
        with open('INSTRUCOES_FINAIS.txt', 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(instructions)
    
    def run(self):
        """Executa todo o processo de configuração"""
        try:
            self.authenticate()
            
            if self.setup_folder_structure():
                self.upload_initial_files()
                self.generate_instructions()
                return True
            else:
                print("❌ Falha na configuração")
                return False
                
        except Exception as e:
            print(f"💥 Erro geral: {e}")
            return False

if __name__ == "__main__":
    print("🔧 Configurador do Google Drive - Day Trade Content")
    print("=" * 50)
    
    setup = GoogleDriveSetup()
    
    if not os.path.exists('credentials.json'):
        print("❌ Arquivo credentials.json não encontrado!")
        print("📋 Instruções:")
        print("1. Acesse: https://console.developers.google.com/")
        print("2. Crie um projeto ou selecione um existente")
        print("3. Ative a Google Drive API")
        print("4. Crie credenciais (OAuth 2.0)")
        print("5. Baixe o arquivo JSON e renomeie para 'credentials.json'")
        exit(1)
    
    success = setup.run()
    
    if success:
        print("🎉 Configuração finalizada com sucesso!")
    else:
        print("❌ Configuração falhou. Verifique os logs acima.")
