import discord
from discord.ext import commands
from discord import app_commands
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TimesheetCog(commands.Cog):
    """Timesheet commands for clock in/out"""
    
    def __init__(self, bot: commands.Bot, db):
        self.bot = bot
        self.db = db
    
    @app_commands.command(name="ponto_entrada", description="Registra entrada (bater ponto)")
    async def check_in(self, interaction: discord.Interaction):
        """Clock in"""
        try:
            user_id = interaction.user.id
            username = interaction.user.name
            
            # Check if already clocked in
            existing = await self.db.get_today_timesheet(user_id)
            if existing and existing['status'] == 'in_progress':
                await interaction.response.send_message(
                    f"❌ Você já bateu ponto hoje às {existing['check_in']}",
                    ephemeral=True
                )
                return
            
            # Register check-in
            await self.db.add_check_in(user_id, username)
            
            embed = discord.Embed(
                title="✅ Entrada Registrada",
                description=f"Hora: {datetime.now().strftime('%H:%M:%S')}",
                color=discord.Color.green()
            )
            embed.add_field(name="Usuário", value=username, inline=True)
            embed.set_footer(text="GCM-BOT • Sistema de Ponto")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Check-in: {username} ({user_id})")
            
        except Exception as e:
            logger.error(f"Check-in error: {e}")
            await interaction.response.send_message(f"❌ Erro ao registrar entrada: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="ponto_saida", description="Registra saída (bater ponto)")
    async def check_out(self, interaction: discord.Interaction):
        """Clock out"""
        try:
            user_id = interaction.user.id
            username = interaction.user.name
            
            # Check if clocked in
            existing = await self.db.get_today_timesheet(user_id)
            if not existing or existing['status'] != 'in_progress':
                await interaction.response.send_message(
                    "❌ Você precisa bater ponto de entrada primeiro!",
                    ephemeral=True
                )
                return
            
            # Register check-out
            success = await self.db.add_check_out(user_id)
            
            if success:
                # Calculate duration
                check_in = datetime.fromisoformat(existing['check_in'])
                check_out = datetime.now()
                duration = check_out - check_in
                hours = duration.total_seconds() / 3600
                
                embed = discord.Embed(
                    title="✅ Saída Registrada",
                    description=f"Hora: {check_out.strftime('%H:%M:%S')}",
                    color=discord.Color.green()
                )
                embed.add_field(name="Usuário", value=username, inline=True)
                embed.add_field(name="Tempo de Trabalho", value=f"{hours:.2f}h", inline=True)
                embed.add_field(name="Entrada", value=existing['check_in'], inline=False)
                embed.add_field(name="Saída", value=check_out.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
                embed.set_footer(text="GCM-BOT • Sistema de Ponto")
                
                await interaction.response.send_message(embed=embed)
                logger.info(f"Check-out: {username} ({user_id}) - Duration: {hours:.2f}h")
            else:
                await interaction.response.send_message(
                    "❌ Erro ao registrar saída",
                    ephemeral=True
                )
        
        except Exception as e:
            logger.error(f"Check-out error: {e}")
            await interaction.response.send_message(f"❌ Erro ao registrar saída: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="meu_ponto", description="Visualiza seu ponto do dia")
    async def my_timesheet(self, interaction: discord.Interaction):
        """View today's timesheet"""
        try:
            user_id = interaction.user.id
            timesheet = await self.db.get_today_timesheet(user_id)
            
            if not timesheet:
                await interaction.response.send_message(
                    "📋 Você ainda não bateu ponto hoje",
                    ephemeral=True
                )
                return
            
            embed = discord.Embed(
                title="📋 Seu Ponto Hoje",
                color=discord.Color.blue()
            )
            embed.add_field(name="Entrada", value=timesheet['check_in'] or "Não registrada", inline=True)
            embed.add_field(name="Saída", value=timesheet['check_out'] or "Ainda em trabalho", inline=True)
            embed.add_field(name="Status", value=timesheet['status'], inline=False)
            embed.set_footer(text="GCM-BOT • Sistema de Ponto")
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            logger.error(f"My timesheet error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
