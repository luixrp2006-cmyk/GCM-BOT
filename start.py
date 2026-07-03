#!/usr/bin/env python3
"""
GCM-BOT Quick Start Guide
Guia rápido de início
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    print(f"\n{'─'*70}")
    print(f"  {text}")
    print(f"{'─'*70}\n")

def main():
    print_header("GCM-BOT - GUIA DE INÍCIO RÁPIDO")
    
    print("""
Bem-vindo ao GCM-BOT! Este script vai ajudá-lo a começar.

Escolha uma opção abaixo:
""")
    
    menu = """
1. 🚀 SETUP COMPLETO (Configure tudo do zero)
2. ▶️  EXECUTAR BOT (Iniciar o bot agora)
3. 🔧 VERIFICAR PERMISSÕES (Ver permissões do servidor)
4. 📖 DOCUMENTAÇÃO (Ver guia completo)
5. ❌ SAIR

Digite o número da opção (1-5):
"""
    
    while True:
        choice = input(menu).strip()
        
        if choice == '1':
            print_section("INICIANDO SETUP COMPLETO")
            print("Executando setup.py...\n")
            os.system(f"{sys.executable} setup.py")
            
        elif choice == '2':
            print_section("INICIANDO BOT")
            print("Executando main.py...\n")
            print("⏳ Aguarde a conexão...\n")
            os.system(f"{sys.executable} main.py")
            
        elif choice == '3':
            print_section("VERIFICANDO PERMISSÕES")
            print("Executando check_permissions.py...\n")
            print("⏳ Aguarde a verificação...\n")
            os.system(f"{sys.executable} check_permissions.py")
            
        elif choice == '4':
            print_section("DOCUMENTAÇÃO COMPLETA")
            
            doc = """
╔════════════════════════════════════════════════════════════════════╗
║                     GCM-BOT - DOCUMENTAÇÃO                         ║
╚════════════════════════════════════════════════════════════════════╝

📋 PRIMEIROS PASSOS
─────────────────────────────────────────────────────────────────────

1️⃣  OBTER TOKEN DO BOT
   • Acesse: https://discord.com/developers/applications
   • Clique em "New Application"
   • Nome: "GCM-BOT"
   • Vá para "Bot" e clique "Add Bot"
   • Copie o TOKEN


2️⃣  CONFIGURAR ARQUIVO .env
   • Execute: python setup.py
   • Cole o token quando pedido
   • Salve o arquivo


3️⃣  ADICIONAR BOT AO SERVIDOR
   • Acesse: https://discord.com/developers/applications
   • Selecione "GCM-BOT"
   • OAuth2 > URL Generator
   • Marque: ✓ bot
   • Marque permissões:
     ✓ Send Messages
     ✓ Embed Links
     ✓ Read Message History
     ✓ Manage Messages
     ✓ Read Messages/View Channels
   • Copie URL gerada
   • Cole no navegador
   • Selecione seu servidor


4️⃣  INICIAR BOT
   • Execute: python main.py
   • Veja a mensagem "connected to Discord!"


5️⃣  USAR COMANDOS
   • No Discord, digite: /
   • Veja todos os comandos disponíveis


📊 COMANDOS PRINCIPAIS
─────────────────────────────────────────────────────────────────────

PONTO (Controle de Chegada/Saída):
  /ponto_entrada  ......... Registra sua chegada
  /ponto_saida    ......... Registra sua saída
  /meu_ponto      ......... Vê seu ponto do dia


VIATURAS (Gestão da Frota):
  /adicionar_viatura ....... Adiciona nova viatura [ADMIN]
  /pegar_viatura ........... Atribui viatura a você
  /devolver_viatura ........ Devolve a viatura
  /listar_viaturas ......... Vê todas as viaturas
  /info_viatura ............ Info detalhada de uma viatura


OCORRÊNCIAS (Registro de Incidentes):
  /criar_ocorrencia ........ Registra novo incidente
  /ver_ocorrencia .......... Vê detalhes de um incidente
  /atribuir_ocorrencia ..... Atribui a um guarda [ADMIN]
  /atualizar_ocorrencia .... Adiciona comentário
  /fechar_ocorrencia ....... Marca como resolvida
  /ocorrencias_abertas .... Lista incidentes abertos


🔒 SEGURANÇA
─────────────────────────────────────────────────────────────────────

⚠️  NUNCA compartilhe seu token!

Proteções já configuradas:
  ✅ .env está no .gitignore (não será enviado ao Git)
  ✅ Token fica apenas localmente
  ✅ Permissões limitadas por padrão
  ✅ Validação de entrada em todos os comandos


🆘 SOLUÇÃO DE PROBLEMAS
─────────────────────────────────────────────────────────────────────

Problema: Bot não conecta
Solução:  1. Verifique token em .env
          2. Verifique conexão com internet
          3. Regenere token no Developer Portal

Problema: Comandos não aparecem
Solução:  1. Aguarde 1 minuto após iniciar bot
          2. Reinicie o Discord (Ctrl+R)
          3. Verifique permissões do bot

Problema: Mensagem de erro ao usar comando
Solução:  1. Verifique permissões do bot no servidor
          2. Verifique argumentos do comando
          3. Veja o arquivo de logs para detalhes


📚 ARQUIVOS IMPORTANTES
─────────────────────────────────────────────────────────────────────

main.py .................. Arquivo principal do bot
setup.py ................. Setup automático
check_permissions.py .... Verificador de permissões
requirements.txt ........ Dependências do projeto
.env ..................... Configurações (não compartilhar!)
src/database.py ......... Banco de dados SQLite
src/cogs/timesheet.py .. Comandos de ponto
src/cogs/vehicles.py ... Comandos de viaturas
src/cogs/incidents.py .. Comandos de ocorrências
README.md ............... Documentação completa


📞 SUPORTE
─────────────────────────────────────────────────────────────────────

GitHub: https://github.com/luixrp2006-cmyk/GCM-BOT
Issues: Abra uma issue para bugs e sugestões


🎉 PRONTO PARA COMEÇAR!
─────────────────────────────────────────────────────────────────────

Próximas ações:
  1. Execute: python setup.py
  2. Execute: python main.py
  3. Teste os comandos no Discord!

Divirta-se! 🚀
"""
            
            print(doc)
            input("\nPressione ENTER para voltar ao menu...")
            
        elif choice == '5':
            print("\n👋 Até logo! Boa sorte com seu bot!\n")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido pelo usuário")
        sys.exit(0)
