#!/usr/bin/env python3
"""
Gerador de Conteúdo para Day Trade - Versão Gratuita
Sistema automatizado usando APIs gratuitas (Pollinations AI)
"""

import json
import random
import requests
import os
from datetime import datetime
import time
import urllib.parse

class DayTradeContentGeneratorFree:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'SUA_OPENAI_API_KEY')
        
        # URLs das APIs gratuitas
        self.pollinations_image_api = "https://image.pollinations.ai/prompt/"
        
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
            "Psicologia do trader: controlando as emoções",
            "Volume como confirmação de tendência",
            "Fibonacci no day trade",
            "Horários de maior volatilidade",
            "Como definir metas de lucro",
            "Análise de fluxo de ordens"
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
        - Foque em conceitos visuais que podem ser ilustrados
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
                # Fallback para roteiro manual se a API falhar
                return self.get_fallback_script()
                
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return self.get_fallback_script()
    
    def get_fallback_script(self):
        """Roteiros de fallback caso a API falhe"""
        fallback_scripts = [
            "O MACD é um dos indicadores mais poderosos do day trade. Quando as linhas se cruzam acima de zero, temos um sinal de compra. Quando cruzam abaixo, sinal de venda. Use sempre com stop loss!",
            "No scalping, velocidade é tudo! Opere apenas nos primeiros 30 minutos após a abertura. Use gráfico de 1 minuto e sempre defina seu stop antes de entrar. Lucros pequenos, mas consistentes!",
            "Stop Loss não é opcional no day trade! Defina sempre antes de entrar na operação. Uma boa regra: nunca arrisque mais de 1% do seu capital por trade. Preserve seu dinheiro para operar outro dia!"
        ]
        return random.choice(fallback_scripts)
    
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
        - Incluir elementos como gráficos, candlesticks, setas de tendência
        
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
                return self.get_fallback_prompts()
                
        except Exception as e:
            print(f"Erro ao processar prompts: {e}")
            return self.get_fallback_prompts()
    
    def get_fallback_prompts(self):
        """Prompts de fallback para imagens"""
        return [
            {
                "prompt": "Professional financial trading concept, modern stock market chart with candlesticks, blue and green color scheme, corporate style, clean design",
                "image": "image_1"
            },
            {
                "prompt": "Trading indicators dashboard, MACD and RSI charts, professional financial interface, blue corporate colors, modern design",
                "image": "image_2"
            },
            {
                "prompt": "Day trading workspace, multiple monitors with financial charts, professional trader setup, clean modern office, blue lighting",
                "image": "image_3"
            }
        ]
    
    def generate_image_pollinations(self, prompt):
        """Gera uma imagem usando a API gratuita Pollinations"""
        try:
            # Adiciona elementos específicos para melhorar a qualidade
            enhanced_prompt = f"{prompt}, professional financial trading concept, clean modern design, corporate style, high quality, detailed"
            
            # Codifica o prompt para URL
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # Constrói a URL da API
            image_url = f"{self.pollinations_image_api}{encoded_prompt}?width=1024&height=1024&model=flux&enhance=true"
            
            print(f"  Gerando imagem via Pollinations...")
            print(f"  URL: {image_url}")
            
            # A API Pollinations retorna diretamente a imagem
            return image_url
            
        except Exception as e:
            print(f"Erro na geração de imagem: {e}")
            return None
    
    def download_image(self, image_url, filename):
        """Baixa uma imagem da URL"""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"  ✅ Imagem salva: {filename}")
                return filename
            else:
                print(f"  ❌ Erro ao baixar imagem: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Erro no download: {e}")
            return None
    
    def save_content(self, script, image_data):
        """Salva o conteúdo gerado em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        content = {
            "timestamp": timestamp,
            "script": script,
            "images": image_data,
            "topic": "Day Trade Content",
            "status": "generated",
            "generator": "Pollinations AI (Free)",
            "api_used": "pollinations.ai"
        }
        
        filename = f"content_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Conteúdo salvo em: {filename}")
        return filename
    
    def run(self):
        """Executa o processo completo de geração de conteúdo"""
        print("🚀 Iniciando geração de conteúdo sobre Day Trade (Versão Gratuita)...")
        print("🔧 Usando Pollinations AI para geração de imagens")
        
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
        print("🖼️ Gerando imagens com Pollinations AI...")
        image_data = []
        
        for i, prompt_data in enumerate(image_prompts):
            print(f"  Gerando imagem {i+1}/3...")
            
            # Gera a URL da imagem
            image_url = self.generate_image_pollinations(prompt_data['prompt'])
            
            if image_url:
                # Baixa a imagem
                filename = f"image_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                local_file = self.download_image(image_url, filename)
                
                if local_file:
                    image_data.append({
                        "prompt": prompt_data['prompt'],
                        "url": image_url,
                        "local_file": local_file,
                        "name": prompt_data['image']
                    })
                    print(f"  ✅ Imagem {i+1} gerada e salva")
                else:
                    # Mesmo se o download falhar, mantém a URL
                    image_data.append({
                        "prompt": prompt_data['prompt'],
                        "url": image_url,
                        "local_file": None,
                        "name": prompt_data['image']
                    })
                    print(f"  ⚠️ Imagem {i+1} gerada (URL disponível, download falhou)")
            else:
                print(f"  ❌ Falha na imagem {i+1}")
        
        # Salva o conteúdo
        if image_data:
            filename = self.save_content(script, image_data)
            print(f"🎉 Processo concluído! Arquivo: {filename}")
            print(f"📊 Imagens geradas: {len(image_data)}")
            print("💡 Dica: As imagens estão disponíveis via URL mesmo se o download falhar")
        else:
            print("❌ Nenhuma imagem foi gerada com sucesso")

if __name__ == "__main__":
    generator = DayTradeContentGeneratorFree()
    generator.run()
