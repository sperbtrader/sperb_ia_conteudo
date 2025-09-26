#!/usr/bin/env python3
"""
Servidor Webhook para Day Trade Content Generator
Permite triggering manual e integração com serviços externos
"""

from flask import Flask, request, jsonify
import subprocess
import os
import logging
import hmac
import hashlib
from datetime import datetime

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/webhook.log'),
        logging.StreamHandler()
    ]
)

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default_secret')

def verify_signature(payload, signature, secret):
    """Verifica a assinatura do webhook"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'day-trade-content-generator'
    })

@app.route('/webhook/generate', methods=['POST'])
def webhook_generate():
    """Endpoint para trigger manual de geração de conteúdo"""
    try:
        # Verifica assinatura se configurada
        signature = request.headers.get('X-Hub-Signature-256')
        if signature and WEBHOOK_SECRET != 'default_secret':
            if not verify_signature(request.data, signature, WEBHOOK_SECRET):
                logging.warning("Assinatura inválida no webhook")
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Log da requisição
        logging.info(f"Webhook recebido de {request.remote_addr}")
        
        # Executa o gerador de conteúdo
        result = subprocess.run(
            ['python', '/app/day_trade_generator_free.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            logging.info("Conteúdo gerado com sucesso via webhook")
            return jsonify({
                'status': 'success',
                'message': 'Content generated successfully',
                'timestamp': datetime.now().isoformat(),
                'output': result.stdout
            })
        else:
            logging.error(f"Erro na geração via webhook: {result.stderr}")
            return jsonify({
                'status': 'error',
                'message': 'Content generation failed',
                'error': result.stderr
            }), 500
            
    except subprocess.TimeoutExpired:
        logging.error("Timeout na geração de conteúdo via webhook")
        return jsonify({
            'status': 'error',
            'message': 'Content generation timeout'
        }), 408
        
    except Exception as e:
        logging.error(f"Erro inesperado no webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@app.route('/webhook/status', methods=['GET'])
def webhook_status():
    """Endpoint para verificar status do sistema"""
    try:
        # Verifica se os arquivos necessários existem
        required_files = [
            '/app/day_trade_generator_free.py',
            '/app/.env'
        ]
        
        missing_files = [f for f in required_files if not os.path.exists(f)]
        
        # Verifica espaço em disco
        disk_usage = os.statvfs('/app')
        free_space_gb = (disk_usage.f_frsize * disk_usage.f_bavail) / (1024**3)
        
        # Verifica últimos logs
        log_file = '/app/logs/automation.log'
        last_execution = None
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in reversed(lines[-50:]):  # Últimas 50 linhas
                    if 'Processo concluído' in line:
                        last_execution = line.split(' - ')[0]
                        break
        
        status = {
            'system_status': 'healthy' if not missing_files else 'degraded',
            'missing_files': missing_files,
            'free_space_gb': round(free_space_gb, 2),
            'last_execution': last_execution,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        logging.error(f"Erro ao verificar status: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to check system status',
            'error': str(e)
        }), 500

@app.route('/webhook/logs', methods=['GET'])
def webhook_logs():
    """Endpoint para visualizar logs recentes"""
    try:
        lines = int(request.args.get('lines', 50))
        log_type = request.args.get('type', 'automation')
        
        log_files = {
            'automation': '/app/logs/automation.log',
            'webhook': '/app/logs/webhook.log'
        }
        
        log_file = log_files.get(log_type)
        if not log_file or not os.path.exists(log_file):
            return jsonify({
                'error': f'Log file not found: {log_type}'
            }), 404
        
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return jsonify({
            'log_type': log_type,
            'lines_returned': len(recent_lines),
            'logs': [line.strip() for line in recent_lines],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Erro ao recuperar logs: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve logs',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logging.info("Iniciando servidor webhook...")
    app.run(host='0.0.0.0', port=8000, debug=False)
