#!/usr/bin/env python3
"""
GCM-BOT - Auto Setup Completo
Automatiza TUDO até o bot estar pronto no Discord
"""

import os
import sys
import json
import webbrowser
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_step(number, text):
    print(f"\n{'─'*70}")
    print(f"  PASSO {number}: {text}")
    print(f"{'─'*70}\n")

def create_env_file(token, prefix="!"):
    """Create .env file with token"""
    env_content = f"""# Discord Bot Configuration
DISCORD_TOKEN={token}
DISCORD_PREFIX={prefix}

# Database
DATABASE_URL=sqlite:///gcm_bot.db

# Optional
LOG_CHANNEL_ID=
ADMIN_ROLE_ID=
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print_success(".env criado com sucesso!")

def install_dependencies():
    """Install required packages"""
    print_step(1, "INSTALANDO DEPENDÊNCIAS")
    
    packages = [
        "discord.py==2.3.2",
        "python-dotenv==1.0.0",
        "aiohttp==3.9.1",
        "requests==2.31.0",
        "pymongo==4.6.0"
    ]
    
    print_info("Instalando pacotes necessários...\n")
    
    for package in packages:
        print(f"  📦 Instalando {package}...")
        os.system(f"pip install -q {package}")
    
    print_success("Todas as dependências instaladas!")

def get_bot_token():
    """Get bot token from user"""
    print_step(2, "OBTER TOKEN DO BOT")
    
    print("""
Para obter seu token do Discord Bot:

1. Acesse: https://discord.com/developers/applications
2. Clique em "New Application"
3. Nome: GCM-BOT
4. Vá para "Bot" → "Add Bot"
5. Clique em "Copy" (próximo ao token)
6. Cole abaixo:
""")
    
    while True:
        token = input("\n🔑 Cole seu DISCORD_TOKEN aqui: ").strip()
        
        if not token:
            print_error("Token não pode estar vazio!")
            continue
        
        if len(token) < 50:
            print_error("Token parece inválido (muito curto)")
            continue
        
        # Save token temporarily for validation
        create_env_file(token)
        print_success(f"Token salvo em .env")
        
        return token

def get_invite_url():
    """Generate and display invite URL"""
    print_step(3, "GERAR LINK DE CONVITE")
    
    print("""
Seu bot precisa de um link de convite especial para entrar no servidor.
Vou gerar automaticamente...

1. Acesse: https://discord.com/developers/applications
2. Selecione "GCM-BOT"
3. Vá para "OAuth2" → "URL Generator"
4. Em "SCOPES", marque:
   ✓ bot
5. Em "PERMISSIONS", marque TODAS:
   ✓ Send Messages
   ✓ Embed Links
   ✓ Read Message History
   ✓ Manage Messages
   ✓ Read Messages/View Channels
   ✓ Administrator (para facilitar)
6. Copie a URL gerada (parte inferior)
7. Abra no navegador
8. Escolha seu servidor
9. Autorize

Pressione ENTER quando estiver pronto para continuar...
""")
    
    input()
    print_info("Abrindo Discord Developer Portal...")
    webbrowser.open("https://discord.com/developers/applications")
    
    return True

def start_bot():
    """Start the bot"""
    print_step(4, "INICIANDO BOT")
    
    print("""
Agora vou iniciar o bot no seu servidor Discord.

Você deve ver mensagens como:
  ✓ Loaded TimesheetCog
  ✓ Loaded VehiclesCog
  ✓ Loaded IncidentsCog
  GCM-BOT#XXXX has connected to Discord!
  Synced XX command(s)

Se vir essas mensagens, significa que o bot está ONLINE! ✅

Pressione CTRL+C para parar o bot quando quiser.
""")
    
    input("Pressione ENTER para iniciar o bot...\n")
    
    print_info("Iniciando bot...\n")
    print("="*70)
    
    # Start the main bot
    os.system(f"{sys.executable} main.py")

def verify_bot_online():
    """Verify bot is online"""
    print_step(5, "VERIFICAR BOT ONLINE")
    
    print("""
Seu bot deve estar ONLINE agora no Discord!

Você pode verificar:
1. Vá para seu servidor Discord
2. Olhe na lista de membros (lado direito)
3. Procure por "GCM-BOT"
4. Deve estar com status ONLINE (ponto verde)

Viu o bot online? Ótimo! 🎉
""")

def show_available_commands():
    """Show available commands"""
    print_header("COMANDOS DISPONÍVEIS")
    
    commands = """
DIGITE ESTES COMANDOS NO SEU SERVIDOR DISCORD:

📋 CONTROLE DE PONTO:
   /ponto_entrada        - Registra sua entrada
   /ponto_saida          - Registra sua saída
   /meu_ponto            - Vê seu ponto do dia

🚗 GESTÃO DE VIATURAS:
   /adicionar_viatura    - Adiciona nova viatura
   /pegar_viatura        - Pega uma viatura
   /devolver_viatura     - Devolve uma viatura
   /listar_viaturas      - Lista todas as viaturas
   /info_viatura         - Vê info de uma viatura

🚨 OCORRÊNCIAS:
   /criar_ocorrencia     - Cria novo incidente
   /ver_ocorrencia       - Vê detalhes
   /atribuir_ocorrencia  - Atribui a alguém
   /atualizar_ocorrencia - Adiciona comentário
   /fechar_ocorrencia    - Marca como fechada
   /ocorrencias_abertas  - Lista abertas

💡 DICA: Digite "/" no Discord para ver todos os comandos!
"""
    
    print(commands)

def show_next_steps():
    """Show what to do next"""
    print_header("PRÓXIMOS PASSOS")
    
    print("""
✅ SEU BOT ESTÁ PRONTO!

Para manter o bot online:
  • Execute: python main.py
  • Deixe rodando enquanto quiser usar

Estrutura do projeto:
  main.py ................... Arquivo principal
  setup.py .................. Setup automático
  check_permissions.py ...... Verificar permissões
  start.py .................. Menu de início
  src/database.py ........... Banco de dados
  src/cogs/timesheet.py .... Controle de ponto
  src/cogs/vehicles.py ..... Gestão de viaturas
  src/cogs/incidents.py .... Registro de ocorrências

Documentação:
  README.md ................. Guia completo
  CONTRIBUTING.md .......... Como contribuir

Precisa de ajuda?
  • GitHub: https://github.com/luixrp2006-cmyk/GCM-BOT
  • Issues: Abra uma issue para bugs/sugestões

Aproveite seu bot! 🚀
""")

def ask_continue():
    """Ask user to continue"""
    response = input("\nContinuar com o próximo passo? (s/n): ").strip().lower()
    return response == 's'

def main():
    """Main setup routine"""
    print_header("🤖 GCM-BOT - AUTO SETUP COMPLETO")
    
    print("""
Bem-vindo! 👋

Este script vai configurar TUDO automaticamente:
  1. Instalar dependências
  2. Obter seu token do Discord
  3. Gerar link de convite
  4. Iniciar o bot
  5. Mostrar comandos disponíveis

⏱️  Tempo estimado: 5-10 minutos

Vamos começar?
""")
    
    input("Pressione ENTER para começar...\n")
    
    try:
        # Step 1: Install dependencies
        install_dependencies()
        if not ask_continue():
            print_warning("Instalação cancelada")
            return
        
        # Step 2: Get bot token
        token = get_bot_token()
        if not ask_continue():
            print_warning("Setup cancelado")
            return
        
        # Step 3: Get invite URL
        get_invite_url()
        if not ask_continue():
            print_warning("Setup cancelado")
            return
        
        # Step 4: Start bot
        start_bot()
        
        # Step 5: Show success
        print_header("✅ SUCESSO!")
        
        print("""
Seu bot GCM-BOT foi criado e configurado com sucesso!

O que você pode fazer agora:

1. NO DISCORD:
   • Digite "/" para ver todos os comandos
   • Use /ponto_entrada para bater ponto
   • Use /criar_ocorrencia para registrar incidentes
   • Use /pegar_viatura para usar uma viatura

2. PARA MANTER O BOT ONLINE:
   • Execute: python main.py
   • Deixe o terminal aberto
   • O bot ficará online enquanto isso

3. PARA PARAR O BOT:
   • Pressione CTRL+C no terminal

Divirta-se! 🚀
""")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
