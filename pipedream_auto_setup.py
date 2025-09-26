#!/usr/bin/env python3
"""
Script de Configuração Automática para Pipedream
Configura o workflow de day trade automaticamente
"""

import json
import requests
import os
from datetime import datetime

class PipedreamAutoSetup:
    def __init__(self):
        self.pipedream_api_key = os.getenv('PIPEDREAM_API_KEY', '')
        self.base_url = "https://api.pipedream.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.pipedream_api_key}",
            "Content-Type": "application/json"
        }
        
    def check_api_connection(self):
        """Verifica se a conexão com a API do Pipedream está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Conectado ao Pipedream como: {user_data.get('email', 'Usuário')}")
                return True
            else:
                print(f"❌ Erro na conexão: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    def create_workflow(self, workflow_data):
        """Cria um novo workflow no Pipedream"""
        try:
            response = requests.post(
                f"{self.base_url}/workflows",
                headers=self.headers,
                json=workflow_data
            )
            
            if response.status_code == 201:
                workflow = response.json()
                workflow_id = workflow.get('id')
                print(f"✅ Workflow criado com sucesso! ID: {workflow_id}")
                return workflow_id
            else:
                print(f"❌ Erro ao criar workflow: {response.status_code}")
                print(f"Resposta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na criação do workflow: {e}")
            return None
    
    def configure_environment_variables(self, workflow_id, variables):
        """Configura variáveis de ambiente do workflow"""
        try:
            for key, value in variables.items():
                env_data = {
                    "key": key,
                    "value": value
                }
                
                response = requests.post(
                    f"{self.base_url}/workflows/{workflow_id}/environment_variables",
                    headers=self.headers,
                    json=env_data
                )
                
                if response.status_code == 201:
                    print(f"✅ Variável configurada: {key}")
                else:
                    print(f"❌ Erro ao configurar {key}: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Erro na configuração de variáveis: {e}")
    
    def activate_workflow(self, workflow_id):
        """Ativa o workflow para execução automática"""
        try:
            response = requests.patch(
                f"{self.base_url}/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": True}
            )
            
            if response.status_code == 200:
                print("✅ Workflow ativado com sucesso!")
                return True
            else:
                print(f"❌ Erro ao ativar workflow: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na ativação: {e}")
            return False
    
    def load_workflow_template(self):
        """Carrega o template do workflow"""
        try:
            with open('day_trade_content_generator_free.json', 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # Adapta para o formato da API do Pipedream
            pipedream_workflow = {
                "name": workflow_data.get("name", "Day Trade Content Generator"),
                "description": "Gerador automatizado de conteúdo sobre day trade",
                "nodes": workflow_data.get("nodes", []),
                "connections": workflow_data.get("connections", {}),
                "active": False  # Será ativado depois
            }
            
            return pipedream_workflow
            
        except FileNotFoundError:
            print("❌ Arquivo day_trade_content_generator_free.json não encontrado")
            return None
        except json.JSONDecodeError:
            print("❌ Erro ao ler o arquivo JSON")
            return None
    
    def setup_api_connections(self):
        """Configura as conexões com APIs externas"""
        print("🔧 Configurando conexões com APIs...")
        
        connections_needed = [
            {
                "name": "OpenAI",
                "type": "openai",
                "description": "Para geração de roteiros e prompts"
            },
            {
                "name": "Google Drive",
                "type": "google_drive",
                "description": "Para upload de imagens e arquivos"
            }
        ]
        
        for conn in connections_needed:
            print(f"📋 Configure manualmente: {conn['name']} - {conn['description']}")
    
    def generate_setup_report(self, workflow_id, success=True):
        """Gera relatório de configuração"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            "setup_date": timestamp,
            "workflow_id": workflow_id,
            "status": "success" if success else "failed",
            "configuration": {
                "schedule": "Every 4 hours",
                "apis_used": ["OpenAI", "Pollinations AI", "Google Drive"],
                "estimated_monthly_cost": "$0.36",
                "estimated_executions": 180
            },
            "next_steps": [
                "Configure OpenAI API key",
                "Setup Google Drive connection", 
                "Test workflow execution",
                "Monitor for 24 hours",
                "Adjust prompts if needed"
            ]
        }
        
        with open('pipedream_setup_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo em: pipedream_setup_report.json")
        return report
    
    def run_full_setup(self):
        """Executa o processo completo de configuração"""
        print("🚀 Iniciando configuração automática do Pipedream...")
        print("=" * 60)
        
        # Verifica API key
        if not self.pipedream_api_key:
            print("❌ PIPEDREAM_API_KEY não configurada!")
            print("📋 Para obter sua API key:")
            print("1. Acesse https://pipedream.com/settings/account")
            print("2. Gere uma nova API key")
            print("3. Execute: export PIPEDREAM_API_KEY=sua_chave_aqui")
            return False
        
        # Testa conexão
        if not self.check_api_connection():
            return False
        
        # Carrega template do workflow
        workflow_data = self.load_workflow_template()
        if not workflow_data:
            return False
        
        # Cria o workflow
        workflow_id = self.create_workflow(workflow_data)
        if not workflow_id:
            return False
        
        # Configura variáveis de ambiente
        env_vars = {
            "OPENAI_API_KEY": "CONFIGURE_SUA_CHAVE_AQUI",
            "GOOGLE_DRIVE_FOLDER_ID": "CONFIGURE_ID_DA_PASTA_AQUI",
            "CONTENT_GENERATION_INTERVAL": "4",
            "MAX_IMAGES_PER_CONTENT": "3"
        }
        
        self.configure_environment_variables(workflow_id, env_vars)
        
        # Configura conexões com APIs
        self.setup_api_connections()
        
        # Gera relatório
        report = self.generate_setup_report(workflow_id, True)
        
        print("\n🎉 CONFIGURAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print(f"🔗 Workflow ID: {workflow_id}")
        print(f"📊 URL: https://pipedream.com/workflows/{workflow_id}")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Configure sua OpenAI API key no workflow")
        print("2. Configure a conexão com Google Drive")
        print("3. Teste o workflow manualmente")
        print("4. Ative o agendamento automático")
        
        return True

def main():
    """Função principal"""
    print("🔧 Configurador Automático - Pipedream Day Trade Content")
    print("=" * 60)
    
    setup = PipedreamAutoSetup()
    
    # Verifica se os arquivos necessários existem
    required_files = ['day_trade_content_generator_free.json']
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Arquivo necessário não encontrado: {file}")
            return
    
    # Executa a configuração
    success = setup.run_full_setup()
    
    if success:
        print("\n✅ Setup concluído com sucesso!")
        print("📖 Consulte o guia pipedream_setup_guide.md para detalhes")
    else:
        print("\n❌ Setup falhou. Verifique os erros acima.")

if __name__ == "__main__":
    main()
