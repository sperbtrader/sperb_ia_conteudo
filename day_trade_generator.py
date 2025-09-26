#!/usr/bin/env python3
"""
Gerador de Conteúdo para Day Trade
Sistema automatizado para criar roteiros e imagens sobre mercado financeiro
"""

import json
import random
import requests
import os
from datetime import datetime
import time

class DayTradeContentGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'SUA_OPENAI_API_KEY')
        self.replicate_api_token = os.getenv('REPLICATE_API_TOKEN', 'SEU_REPLICATE_API_TOKEN')
        
        # Tópicos para variação de conteúdo
        self.topics = [
            "Estratégia de Scalping para mini-índice",
            "Como usar o indicador MACD para identificar tendências",
            "A importância do Stop Loss no day trade",
            "Análise de suporte e resistência",
            "Como usar médias móveis no day trade",
            "Padrões de candlestick mais eficazes",
            "Gerenciamento de risco no mercado financeiro",
            "Como identificar breakouts verdadeiros",
            "Estratégias para operar no mini-dólar",
            "Psicologia do trader: controlando as emoções"
        ]
        
        # Indicadores técnicos para aulas
        self.indicators = [
            "MACD", "RSI", "Bandas de Bollinger", "Estocástico",
            "IFR", "Volume", "ADX", "Williams %R", "CCI", "ROC"
        ]
    
    def generate_script(self):
        """Gera um roteiro sobre day trade"""
        topic = random.choice(self.topics)
        
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        Crie um roteiro educativo para um vídeo curto sobre: {topic}
        
        Requisitos:
        - Máximo 500 caracteres
        - Linguagem acessível para iniciantes
        - Conteúdo prático e direto
        - Inclua uma dica específica
        """
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um especialista em mercado financeiro e day trade."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                script = result['choices'][0]['message']['content']
                return self.clean_text(script)
            else:
                print(f"Erro ao gerar roteiro: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def clean_text(self, text):
        """Limpa o texto removendo caracteres especiais"""
        # Remove aspas externas
        text = text.replace('"', '').replace("'", "")
        
        # Remove quebras de linha e múltiplos espaços
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        # Remove caracteres de controle
        text = ''.join(char for char in text if ord(char) >= 32)
        
        return text.strip()
    
    def generate_image_prompts(self, script):
        """Gera prompts para imagens baseados no roteiro"""
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        A partir do roteiro sobre day trade abaixo, crie 3 prompts em inglês para gerar imagens.
        
        Roteiro: {script}
        
        Requisitos:
        - Cada prompt deve ter 1-2 sentenças
        - Imagens limpas e modernas com tema corporativo
        - Cores: azul, verde, dourado, preto e branco
        - Sem texto nas imagens
        - Representar conceitos de mercado financeiro
        
        Retorne apenas um JSON no formato:
        {{"image_prompts": [{{"prompt": "prompt_1", "image": "image_1"}}, {{"prompt": "prompt_2", "image": "image_2"}}, {{"prompt": "prompt_3", "image": "image_3"}}]}}
        """
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um diretor de arte especializado em imagens financeiras."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 400,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Limpa e parseia o JSON
                content = content.replace('```json', '').replace('```', '').strip()
                prompts_data = json.loads(content)
                return prompts_data['image_prompts']
            else:
                print(f"Erro ao gerar prompts: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao processar prompts: {e}")
            return None
    
    def generate_image(self, prompt):
        """Gera uma imagem usando a API da Replicate"""
        headers = {
            'Authorization': f'Bearer {self.replicate_api_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "input": {
                "prompt": f"{prompt}, professional financial trading concept, clean modern design, corporate style, blue and green color scheme",
                "width": 1024,
                "height": 1024,
                "num_outputs": 1,
                "scheduler": "K_EULER",
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        }
        
        try:
            # Inicia a geração
            response = requests.post(
                'https://api.replicate.com/v1/models/stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf/predictions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction['id']
                
                # Aguarda a conclusão
                while True:
                    status_response = requests.get(
                        f'https://api.replicate.com/v1/predictions/{prediction_id}',
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        
                        if status_data['status'] == 'succeeded':
                            return status_data['output'][0]
                        elif status_data['status'] == 'failed':
                            print("Falha na geração da imagem")
                            return None
                        else:
                            time.sleep(2)  # Aguarda 2 segundos antes de verificar novamente
                    else:
                        print(f"Erro ao verificar status: {status_response.status_code}")
                        return None
            else:
                print(f"Erro ao iniciar geração: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro na geração de imagem: {e}")
            return None
    
    def save_content(self, script, image_urls):
        """Salva o conteúdo gerado em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        content = {
            "timestamp": timestamp,
            "script": script,
            "images": image_urls,
            "topic": "Day Trade Content",
            "status": "generated"
        }
        
        filename = f"content_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print(f"Conteúdo salvo em: {filename}")
        return filename
    
    def run(self):
        """Executa o processo completo de geração de conteúdo"""
        print("🚀 Iniciando geração de conteúdo sobre Day Trade...")
        
        # Gera o roteiro
        print("📝 Gerando roteiro...")
        script = self.generate_script()
        
        if not script:
            print("❌ Falha ao gerar roteiro")
            return
        
        print(f"✅ Roteiro gerado: {script[:100]}...")
        
        # Gera prompts para imagens
        print("🎨 Gerando prompts para imagens...")
        image_prompts = self.generate_image_prompts(script)
        
        if not image_prompts:
            print("❌ Falha ao gerar prompts")
            return
        
        print(f"✅ {len(image_prompts)} prompts gerados")
        
        # Gera as imagens
        print("🖼️ Gerando imagens...")
        image_urls = []
        
        for i, prompt_data in enumerate(image_prompts):
            print(f"  Gerando imagem {i+1}/3...")
            image_url = self.generate_image(prompt_data['prompt'])
            
            if image_url:
                image_urls.append({
                    "prompt": prompt_data['prompt'],
                    "url": image_url,
                    "name": prompt_data['image']
                })
                print(f"  ✅ Imagem {i+1} gerada")
            else:
                print(f"  ❌ Falha na imagem {i+1}")
        
        # Salva o conteúdo
        if image_urls:
            filename = self.save_content(script, image_urls)
            print(f"🎉 Processo concluído! Arquivo: {filename}")
        else:
            print("❌ Nenhuma imagem foi gerada com sucesso")

if __name__ == "__main__":
    generator = DayTradeContentGenerator()
    generator.run()
