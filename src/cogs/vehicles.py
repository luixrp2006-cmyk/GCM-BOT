import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class VehiclesCog(commands.Cog):
    """Vehicle management commands"""
    
    def __init__(self, bot: commands.Bot, db):
        self.bot = bot
        self.db = db
    
    @app_commands.command(name="adicionar_viatura", description="Adiciona uma nova viatura")
    async def add_vehicle(self, interaction: discord.Interaction, placa: str, modelo: str, notas: str = None):
        """Add a new vehicle"""
        try:
            # Check permissions (admin only)
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Apenas administradores podem adicionar viaturas", ephemeral=True)
                return
            
            await self.db.add_vehicle(placa, modelo, notas)
            
            embed = discord.Embed(
                title="✅ Viatura Adicionada",
                color=discord.Color.green()
            )
            embed.add_field(name="Placa", value=placa.upper(), inline=True)
            embed.add_field(name="Modelo", value=modelo, inline=True)
            if notas:
                embed.add_field(name="Notas", value=notas, inline=False)
            embed.set_footer(text="GCM-BOT • Gestão de Viaturas")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Vehicle added: {placa} - {modelo}")
        
        except Exception as e:
            logger.error(f"Add vehicle error: {e}")
            if "UNIQUE constraint failed" in str(e):
                await interaction.response.send_message(f"❌ A placa {placa} já existe!", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="pegar_viatura", description="Atribui uma viatura a você")
    async def assign_vehicle(self, interaction: discord.Interaction, placa: str):
        """Assign vehicle to officer"""
        try:
            placa = placa.upper()
            
            # Check if vehicle exists
            vehicle = await self.db.get_vehicle(placa)
            if not vehicle:
                await interaction.response.send_message(f"❌ Viatura {placa} não encontrada!", ephemeral=True)
                return
            
            # Check if already assigned
            if vehicle['status'] == 'in_use':
                await interaction.response.send_message(
                    f"❌ A viatura {placa} já está em uso por outro guarda!",
                    ephemeral=True
                )
                return
            
            # Assign vehicle
            await self.db.assign_vehicle(placa, interaction.user.id)
            
            embed = discord.Embed(
                title="✅ Viatura Atribuída",
                color=discord.Color.green()
            )
            embed.add_field(name="Placa", value=placa, inline=True)
            embed.add_field(name="Modelo", value=vehicle['model'], inline=True)
            embed.add_field(name="Status", value="Em uso", inline=True)
            embed.set_footer(text="GCM-BOT • Gestão de Viaturas")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Vehicle assigned: {placa} to {interaction.user.name}")
        
        except Exception as e:
            logger.error(f"Assign vehicle error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="devolver_viatura", description="Devolve uma viatura")
    async def return_vehicle(self, interaction: discord.Interaction, placa: str):
        """Return vehicle"""
        try:
            placa = placa.upper()
            
            # Check if vehicle exists
            vehicle = await self.db.get_vehicle(placa)
            if not vehicle:
                await interaction.response.send_message(f"❌ Viatura {placa} não encontrada!", ephemeral=True)
                return
            
            # Check if assigned to user
            if vehicle['assigned_to'] != interaction.user.id:
                await interaction.response.send_message(
                    "❌ Esta viatura não está atribuída a você!",
                    ephemeral=True
                )
                return
            
            # Return vehicle
            await self.db.return_vehicle(placa)
            
            embed = discord.Embed(
                title="✅ Viatura Devolvida",
                color=discord.Color.green()
            )
            embed.add_field(name="Placa", value=placa, inline=True)
            embed.add_field(name="Modelo", value=vehicle['model'], inline=True)
            embed.add_field(name="Status", value="Disponível", inline=True)
            embed.set_footer(text="GCM-BOT • Gestão de Viaturas")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"Vehicle returned: {placa}")
        
        except Exception as e:
            logger.error(f"Return vehicle error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="listar_viaturas", description="Lista todas as viaturas")
    async def list_vehicles(self, interaction: discord.Interaction):
        """List all vehicles"""
        try:
            vehicles = await self.db.list_vehicles()
            
            if not vehicles:
                await interaction.response.send_message("📋 Nenhuma viatura cadastrada", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="📋 Frota de Viaturas",
                color=discord.Color.blue()
            )
            
            for vehicle in vehicles:
                status_emoji = "🟢" if vehicle['status'] == 'available' else "🔴"
                assigned = f"<@{vehicle['assigned_to']}>" if vehicle['assigned_to'] else "Ninguém"
                
                embed.add_field(
                    name=f"{status_emoji} {vehicle['plate']}",
                    value=f"Modelo: {vehicle['model']}\nAtribuída a: {assigned}",
                    inline=True
                )
            
            embed.set_footer(text=f"Total: {len(vehicles)} viaturas | GCM-BOT")
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            logger.error(f"List vehicles error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="info_viatura", description="Visualiza informações de uma viatura")
    async def vehicle_info(self, interaction: discord.Interaction, placa: str):
        """Get vehicle info"""
        try:
            vehicle = await self.db.get_vehicle(placa.upper())
            
            if not vehicle:
                await interaction.response.send_message(f"❌ Viatura {placa} não encontrada!", ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"🚗 {vehicle['plate']}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Modelo", value=vehicle['model'], inline=True)
            embed.add_field(name="Status", value=vehicle['status'], inline=True)
            embed.add_field(name="Atribuída a", value=f"<@{vehicle['assigned_to']}>" if vehicle['assigned_to'] else "Disponível", inline=False)
            if vehicle['notes']:
                embed.add_field(name="Notas", value=vehicle['notes'], inline=False)
            embed.add_field(name="Criada em", value=vehicle['created_at'], inline=False)
            embed.set_footer(text="GCM-BOT • Gestão de Viaturas")
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            logger.error(f"Vehicle info error: {e}")
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
