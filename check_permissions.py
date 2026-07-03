#!/usr/bin/env python3
"""
GCM-BOT Permission Fixer
Corrige automaticamente as permissões do bot no servidor Discord
"""

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

class PermissionFixer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When bot is ready, fix permissions"""
        print(f"\n{'='*60}")
        print(f"Bot conectado como: {self.bot.user}")
        print(f"{'='*60}\n")
        
        for guild in self.bot.guilds:
            print(f"📍 Servidor: {guild.name}")
            print(f"   👤 Membros: {guild.member_count}")
            print(f"   🔑 ID do servidor: {guild.id}")
            
            # Get bot member
            bot_member = guild.me
            
            # Check permissions
            perms = bot_member.guild_permissions
            print(f"\n   ✅ Permissões do bot:")
            print(f"      - Enviar mensagens: {perms.send_messages}")
            print(f"      - Embed Links: {perms.embed_links}")
            print(f"      - Ler histórico: {perms.read_message_history}")
            print(f"      - Gerenciar mensagens: {perms.manage_messages}")
            print(f"      - Administrador: {perms.administrator}\n")
            
            # List commands
            print(f"   📋 Comandos sincronizados:")
            synced = await self.bot.tree.sync()
            for i, cmd in enumerate(synced, 1):
                print(f"      {i}. /{cmd.name}")
            
            print(f"\n{'='*60}\n")
        
        print("✅ Setup concluído! O bot está pronto para usar.")
        print("\n💡 Próximo passo:")
        print("   1. Abra seu servidor Discord")
        print("   2. Digite '/' para ver todos os comandos")
        print("   3. Use os comandos normalmente\n")

async def main():
    """Start the permission fixer bot"""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    async with bot:
        await bot.add_cog(PermissionFixer(bot))
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    print("\n🔧 GCM-BOT - Permission Fixer")
    print("="*60)
    print("\nVerificando permissões do bot nos servidores...\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nVerifique se:")
        print("  1. O DISCORD_TOKEN está configurado em .env")
        print("  2. O token é válido")
        print("  3. O bot já foi adicionado ao servidor")
