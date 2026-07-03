import discord
from discord.ext import commands
from discord import app_commands
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class IncidentsCog(commands.Cog):
    """Incident management commands"""
    
    def __init__(self, bot: commands.Bot, db):
        self.bot = bot
        self.db = db
    
    @app_commands.command(name="criar_ocorrencia", description="Cria uma nova ocorrência")
    @app_commands.describe(
        titulo="Título da ocorrência",
        descricao="Descrição detalhada",
        local="Local da ocorrência",
        prioridade="Nível de prioridade (baixa, normal, alta, critica)"
    )
    async def create_incident(self, interaction: discord.Interaction, titulo: str, descricao: str, 
                             local: str, prioridade: str = "normal"):
        """Create a new incident"""
        try:
            # Validate priority
            valid_priorities = ["baixa", "normal", "alta", "critica"]
            if prioridade.lower() not in valid_priorities:
                await interaction.response.send_message(
                    f"❌ Prioridade inválida. Use: {', '.join(valid_priorities)}",
                    ephemeral=True
                )
                return
            
            # Generate incident ID
            incident_id = f"OC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # Create incident
            await self.db.create_incident(
                incident_id, titulo, descricao, local, 
                interaction.user.id, prioridade.lower()
            )
            
            priority_emoji = {
                "baixa": "🟢",
                "normal": "🟡",
                "alta": "🟠",
                "critica": "🔴"
            }
            
            embed = discord.Embed(
                title=f"{priority_emoji.get(prioridade.lower(), '🟡')} Nova Ocorrência",
                description=titulo,
                color=discord.Color.gold()
            )
            embed.add_field(name="ID", value=incident_id, inline=True)
            embed.add_field(name="Prioridade", value=prioridade.upper(), inline=True)
            embed.add_field(name="Local", value=local, inline=True)
            embed.add_field(name="Descrição", value=descricao, inline=False)
            embed.add_field(name="Reportado por", value=interaction.user.mention, inline=True)
            embed.add_field(name="Data/Hora", value=datetime.now().strftime('%d/%m/%Y %H:%M:%S'), inline=True)
            embed.set_footer(text="GCM-BOT • Sistema de Ocorrências")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Incident created: {incident_id} by {interaction.user.name}")
        
        except Exception as e:
            logger.error(f"Create incident error: {e}")
            await interaction.response.send_message(f"❌ Erro ao criar ocorrência: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="ver_ocorrencia", description="Visualiza detalhes de uma ocorrência")
    async def view_incident(self, interaction: discord.Interaction, id_ocorrencia: str):
        """View incident details"""
        try:
            incident = await self.db.get_incident(id_ocorrencia.upper())
            
            if not incident:
                await interaction.response.send_message(f"❌ Ocorrência {id_ocorrencia} não encontrada!", ephemeral=True)
                return
            
            priority_emoji = {
                "baixa": "🟢",
                "normal": "🟡",
                "alta": "🟠",
                "critica": "🔴"
            }
            
            status_emoji = {
                "open": "🔴",
                "in_progress": "🟡",
                "closed": "🟢"
            }
            
            embed = discord.Embed(
                title=f"{priority_emoji.get(incident['priority'], '🟡')} {incident['title']}",
                description=incident['description'],
                color=discord.Color.gold()
            )
            embed.add_field(name="ID", value=incident['incident_id'], inline=True)
            embed.add_field(name=f"{status_emoji.get(incident['status'], '🟡')} Status", 
                          value=incident['status'].replace('_', ' ').upper(), inline=True)
            embed.add_field(name="Prioridade", value=incident['priority'].upper(), inline=True)
            embed.add_field(name="Local", value=incident['location'], inline=False)
            embed.add_field(name="Reportado por", value=f"<@{incident['reported_by']}>", inline=True)
            if incident['assigned_to']:
                embed.add_field(name="Atribuído a", value=f"<@{incident['assigned_to']}>", inline=True)
            embed.add_field(name="Criada em", value=incident['created_at'], inline=False)
            
            # Get updates
            updates = await self.db.get_incident_updates(incident['incident_id'])
            if updates:
                updates_text = ""
                for update in updates:
                    updates_text += f"<@{update['user_id']}> - {update['message']}\n"
                embed.add_field(name="Atualizações", value=updates_text, inline=False)
            
            embed.set_footer(text="GCM-BOT • Sistema de Ocorrências")
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            logger.error(f"View incident error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="atribuir_ocorrencia", description="Atribui uma ocorrência a um guarda")
    async def assign_incident(self, interaction: discord.Interaction, id_ocorrencia: str, guarda: discord.User):
        """Assign incident to officer"""
        try:
            incident = await self.db.get_incident(id_ocorrencia.upper())
            
            if not incident:
                await interaction.response.send_message(f"❌ Ocorrência {id_ocorrencia} não encontrada!", ephemeral=True)
                return
            
            # Check permissions
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Apenas administradores podem atribuir ocorrências", ephemeral=True)
                return
            
            await self.db.assign_incident(incident['incident_id'], guarda.id)
            
            embed = discord.Embed(
                title="✅ Ocorrência Atribuída",
                color=discord.Color.green()
            )
            embed.add_field(name="ID", value=incident['incident_id'], inline=True)
            embed.add_field(name="Título", value=incident['title'], inline=False)
            embed.add_field(name="Atribuído a", value=guarda.mention, inline=True)
            embed.set_footer(text="GCM-BOT • Sistema de Ocorrências")
            
            await interaction.response.send_message(embed=embed)
            
            # Notify assigned officer
            try:
                dm_embed = discord.Embed(
                    title="📢 Nova Ocorrência Atribuída",
                    description=f"Você foi atribuído à ocorrência: {incident['title']}",
                    color=discord.Color.orange()
                )
                dm_embed.add_field(name="ID", value=incident['incident_id'], inline=False)
                dm_embed.add_field(name="Local", value=incident['location'], inline=False)
                dm_embed.add_field(name="Descrição", value=incident['description'], inline=False)
                await guarda.send(embed=dm_embed)
            except:
                pass
            
            logger.info(f"Incident assigned: {incident['incident_id']} to {guarda.name}")
        
        except Exception as e:
            logger.error(f"Assign incident error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="atualizar_ocorrencia", description="Adiciona uma atualização à ocorrência")
    async def update_incident(self, interaction: discord.Interaction, id_ocorrencia: str, atualizacao: str):
        """Add update to incident"""
        try:
            incident = await self.db.get_incident(id_ocorrencia.upper())
            
            if not incident:
                await interaction.response.send_message(f"❌ Ocorrência {id_ocorrencia} não encontrada!", ephemeral=True)
                return
            
            await self.db.add_incident_update(incident['incident_id'], interaction.user.id, atualizacao)
            
            embed = discord.Embed(
                title="✅ Atualização Registrada",
                description=atualizacao,
                color=discord.Color.green()
            )
            embed.add_field(name="ID Ocorrência", value=incident['incident_id'], inline=True)
            embed.add_field(name="Atualizado por", value=interaction.user.mention, inline=True)
            embed.set_footer(text="GCM-BOT • Sistema de Ocorrências")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Incident updated: {incident['incident_id']}")
        
        except Exception as e:
            logger.error(f"Update incident error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="fechar_ocorrencia", description="Marca uma ocorrência como fechada")
    async def close_incident(self, interaction: discord.Interaction, id_ocorrencia: str):
        """Close incident"""
        try:
            incident = await self.db.get_incident(id_ocorrencia.upper())
            
            if not incident:
                await interaction.response.send_message(f"❌ Ocorrência {id_ocorrencia} não encontrada!", ephemeral=True)
                return
            
            # Check if user is assigned or admin
            if incident['assigned_to'] != interaction.user.id and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Apenas o responsável ou admin podem fechar", ephemeral=True)
                return
            
            await self.db.update_incident_status(incident['incident_id'], 'closed')
            
            embed = discord.Embed(
                title="✅ Ocorrência Fechada",
                color=discord.Color.green()
            )
            embed.add_field(name="ID", value=incident['incident_id'], inline=True)
            embed.add_field(name="Título", value=incident['title'], inline=False)
            embed.add_field(name="Fechada em", value=datetime.now().strftime('%d/%m/%Y %H:%M:%S'), inline=True)
            embed.set_footer(text="GCM-BOT • Sistema de Ocorrências")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Incident closed: {incident['incident_id']}")
        
        except Exception as e:
            logger.error(f"Close incident error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="ocorrencias_abertas", description="Lista todas as ocorrências abertas")
    async def list_open_incidents(self, interaction: discord.Interaction):
        """List open incidents"""
        try:
            incidents = await self.db.list_open_incidents()
            
            if not incidents:
                await interaction.response.send_message("📋 Nenhuma ocorrência aberta", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="🚨 Ocorrências Abertas",
                color=discord.Color.red()
            )
            
            for incident in incidents:
                priority_emoji = {
                    "baixa": "🟢",
                    "normal": "🟡",
                    "alta": "🟠",
                    "critica": "🔴"
                }
                
                embed.add_field(
                    name=f"{priority_emoji.get(incident['priority'], '🟡')} {incident['incident_id']}",
                    value=f"**{incident['title']}**\nLocal: {incident['location']}\nStatus: {incident['status']}",
                    inline=False
                )
            
            embed.set_footer(text=f"Total: {len(incidents)} ocorrências abertas | GCM-BOT")
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            logger.error(f"List open incidents error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
