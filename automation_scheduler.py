#!/usr/bin/env python3
"""
Agendador de Automação para Day Trade Content
Executa o gerador de conteúdo em intervalos regulares
"""

import schedule
import time
import subprocess
import os
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

class AutomationScheduler:
    def __init__(self):
        self.script_path = '/home/ubuntu/day_trade_generator.py'
        self.content_dir = '/home/ubuntu/generated_content'
        
        # Cria diretório para conteúdo gerado
        os.makedirs(self.content_dir, exist_ok=True)
    
    def run_content_generator(self):
        """Executa o gerador de conteúdo"""
        try:
            logging.info("🚀 Iniciando geração de conteúdo...")
            
            # Muda para o diretório de conteúdo
            os.chdir(self.content_dir)
            
            # Executa o script
            result = subprocess.run(
                ['python3', self.script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos de timeout
            )
            
            if result.returncode == 0:
                logging.info("✅ Conteúdo gerado com sucesso!")
                logging.info(f"Output: {result.stdout}")
            else:
                logging.error(f"❌ Erro na geração: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logging.error("⏰ Timeout na geração de conteúdo")
        except Exception as e:
            logging.error(f"💥 Erro inesperado: {e}")
    
    def cleanup_old_files(self):
        """Remove arquivos antigos para economizar espaço"""
        try:
            # Remove arquivos com mais de 7 dias
            cutoff_time = time.time() - (7 * 24 * 60 * 60)
            
            for filename in os.listdir(self.content_dir):
                filepath = os.path.join(self.content_dir, filename)
                
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        logging.info(f"🗑️ Arquivo removido: {filename}")
                        
        except Exception as e:
            logging.error(f"Erro na limpeza: {e}")
    
    def start_scheduler(self):
        """Inicia o agendador"""
        logging.info("📅 Iniciando agendador de automação...")
        
        # Agenda execução a cada 4 horas
        schedule.every(4).hours.do(self.run_content_generator)
        
        # Agenda limpeza diária às 02:00
        schedule.every().day.at("02:00").do(self.cleanup_old_files)
        
        # Executa uma vez imediatamente
        self.run_content_generator()
        
        logging.info("⏰ Agendador configurado:")
        logging.info("  - Geração de conteúdo: a cada 4 horas")
        logging.info("  - Limpeza de arquivos: diariamente às 02:00")
        
        # Loop principal
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
            except KeyboardInterrupt:
                logging.info("🛑 Agendador interrompido pelo usuário")
                break
            except Exception as e:
                logging.error(f"Erro no agendador: {e}")
                time.sleep(60)

if __name__ == "__main__":
    scheduler = AutomationScheduler()
    scheduler.start_scheduler()
