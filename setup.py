#!/usr/bin/env python3
"""
GCM-BOT Setup Script
Configura automaticamente o bot Discord
"""

import os
import sys
from dotenv import load_dotenv

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def setup_env():
    """Configure .env file"""
    print_header("CONFIGURAÇÃO DE AMBIENTE")
    
    env_file = ".env"
    
    # Check if .env exists
    if os.path.exists(env_file):
        print_info("Arquivo .env já existe")
        response = input("Deseja atualizar? (s/n): ").strip().lower()
        if response != 's':
            return
    
    print_info("Preencha as informações abaixo:\n")
    
    token = input("🔑 Cole seu DISCORD_TOKEN: ").strip()
    if not token:
        print_error("Token não pode estar vazio!")
        return False
    
    prefix = input("📝 Prefixo do bot (padrão '!'): ").strip() or "!"
    
    # Validate token format
    if len(token) < 20:
        print_error("Token parece inválido!")
        return False
    
    # Create .env file
    env_content = f"""# Discord Bot Configuration
DISCORD_TOKEN={token}
DISCORD_PREFIX={prefix}

# Database
DATABASE_URL=sqlite:///gcm_bot.db

# Optional
LOG_CHANNEL_ID=
ADMIN_ROLE_ID=
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print_success(f"Arquivo {env_file} criado com sucesso!")
    print_info("⚠️  NUNCA compartilhe seu token com ninguém!")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print_header("VERIFICAÇÃO DE DEPENDÊNCIAS")
    
    required_packages = {
        'discord': 'discord.py',
        'dotenv': 'python-dotenv',
        'aiohttp': 'aiohttp',
        'requests': 'requests',
    }
    
    missing = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print_success(f"{pip_name} já está instalado")
        except ImportError:
            print_error(f"{pip_name} não está instalado")
            missing.append(pip_name)
    
    if missing:
        print_info(f"\nInstalando pacotes faltantes...")
        os.system(f"pip install {' '.join(missing)}")
        print_success("Dependências instaladas!")
    
    return True

def check_bot_token():
    """Validate bot token"""
    print_header("VALIDAÇÃO DE TOKEN")
    
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print_error("DISCORD_TOKEN não configurado em .env")
        return False
    
    if token == "your_bot_token_here":
        print_error("Token ainda está com valor padrão!")
        print_info("Execute este script novamente e configure o token real")
        return False
    
    print_success("Token configurado!")
    return True

def display_invite_link_instructions():
    """Display instructions for getting invite link"""
    print_header("LINK DE CONVITE DO BOT")
    
    print_info("Para adicionar o bot ao seu servidor, siga estes passos:\n")
    
    instructions = """
1. Acesse: https://discord.com/developers/applications

2. Selecione sua aplicação "GCM-BOT"

3. No menu esquerdo, clique em "OAuth2" > "URL Generator"

4. Em "SCOPES", marque:
   ☑ bot

5. Em "PERMISSIONS", marque TODAS estas:
   ☑ Send Messages
   ☑ Embed Links
   ☑ Read Message History
   ☑ Manage Messages
   ☑ Read Messages/View Channels

6. Copie a URL gerada (parte inferior)

7. Cole a URL no seu navegador

8. Selecione seu servidor Discord

9. Clique em "Autorizar"

10. Complete o CAPTCHA (se aparecer)
"""
    
    print(instructions)
    
    input("Pressione ENTER após adicionar o bot ao servidor...")
    print_success("Ótimo! Continuando...")

def test_bot_connection():
    """Test bot connection"""
    print_header("TESTE DE CONEXÃO")
    
    print_info("Para testar o bot, execute:")
    print("\n  python main.py\n")
    print_info("Você deve ver:")
    print("""
  ✓ Loaded TimesheetCog
  ✓ Loaded VehiclesCog
  ✓ Loaded IncidentsCog
  GCM-BOT#XXXX has connected to Discord!
  Synced XX command(s)
""")
    
    test_response = input("Já executou o bot e ele conectou? (s/n): ").strip().lower()
    
    if test_response == 's':
        print_success("Bot conectado com sucesso! ✅")
        return True
    else:
        print_error("Verifique os erros acima")
        return False

def display_commands():
    """Display available commands"""
    print_header("COMANDOS DISPONÍVEIS")
    
    commands_info = """
📋 CONTROLE DE PONTO:
  /ponto_entrada        - Registra entrada
  /ponto_saida          - Registra saída
  /meu_ponto            - Visualiza ponto do dia

🚗 GESTÃO DE VIATURAS:
  /adicionar_viatura    - Adiciona nova viatura (ADMIN)
  /pegar_viatura        - Atribui viatura a você
  /devolver_viatura     - Devolve viatura
  /listar_viaturas      - Lista todas as viaturas
  /info_viatura         - Info de uma viatura

🚨 OCORRÊNCIAS:
  /criar_ocorrencia     - Cria nova ocorrência
  /ver_ocorrencia       - Visualiza detalhes
  /atribuir_ocorrencia  - Atribui a um guarda (ADMIN)
  /atualizar_ocorrencia - Adiciona atualização
  /fechar_ocorrencia    - Marca como fechada
  /ocorrencias_abertas  - Lista abertas

💡 DICA: Digite "/" no Discord para ver todos os comandos!
"""
    
    print(commands_info)

def main():
    """Main setup routine"""
    print_header("SETUP DO GCM-BOT")
    
    print("""
Bem-vindo ao GCM-BOT! 🤖
Este script vai configurar tudo automaticamente.

Vamos começar...
""")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return
    
    # Step 2: Setup environment
    if not setup_env():
        print_error("Falha na configuração de ambiente")
        return
    
    # Step 3: Check token
    if not check_bot_token():
        return
    
    # Step 4: Display invite link instructions
    display_invite_link_instructions()
    
    # Step 5: Test connection
    if test_bot_connection():
        # Step 6: Display commands
        display_commands()
        
        print_header("SETUP CONCLUÍDO! ✅")
        print("""
Seu bot GCM-BOT está pronto para usar!

Próximos passos:
1. Mantenha o bot rodando: python main.py
2. Use os comandos no Discord
3. Consulte o README.md para mais detalhes

Para suporte:
- GitHub: https://github.com/luixrp2006-cmyk/GCM-BOT
- Issues: Abra uma issue no repositório

Divirta-se! 🚀
""")
    else:
        print_error("Falha ao conectar ao Discord")
        print_info("Verifique o token e tente novamente")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
