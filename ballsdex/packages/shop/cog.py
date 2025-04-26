import discord, asyncio
from discord import app_commands
from discord.ext import commands

from ballsdex.core.models import (
    Ball,
    BallInstance,
    Player,
    Special,
    PrivacyPolicy,
)
from ballsdex.core.utils.transformers import BallEnabledTransform
from tortoise.exceptions import DoesNotExist
from ballsdex.packages.balls.cog import inventory_privacy
from ballsdex.core.models import PrivacyPolicy
class Shop(commands.GroupCog, group_name="shop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Store the bot instance
        super().__init__()

    @app_commands.command()
    async def balance(self, interaction: discord.Interaction, user: discord.User | None = None):
        """
        Check your coin balance or another user's balance.
        """
        user_obj = user or interaction.user
        try:
            player = await Player.get(discord_id=user_obj.id)
        except DoesNotExist:
            if user_obj == interaction.user:
                await interaction.response.send_message(
                    "You don't have a balance yet.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"{user_obj.name} doesn't have a balance yet.", ephemeral=True
                )
            return

        # Check privacy settings if viewing another user's balance
        if user and user != interaction.user:
            if player.privacy_policy == PrivacyPolicy.DENY:
                await interaction.response.send_message(
                    "This user has set their balance to private.", ephemeral=False
                )
                return
            elif player.privacy_policy == PrivacyPolicy.SAME_SERVER:
                if not interaction.guild or interaction.guild.get_member(user_obj.id) is None:
                    await interaction.response.send_message(
                        "This user has set their balance to be visible only to members of the same server.",
                        ephemeral=False,
                    )
                    return

        embed = discord.Embed(
            title=f"{user_obj.name}'s Balance" if user else "Your Balance",
            description=f"Coins: **{player.coins}**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command()
    async def view(self, interaction: discord.Interaction):
        '''
        View the shop.
        '''
        class BuyModal(discord.ui.Modal, title="Buy Item"):
            item_id = discord.ui.TextInput(
                label="Enter the item ID you want to buy:",
                placeholder="e.g., 1",
                required=True,
            )

            def __init__(self, player):
                super().__init__()
                self.player = player

            async def on_submit(self, interaction: discord.Interaction):
                item_id = self.item_id.value.strip()

                if item_id == "1":  # Example for Basic Box
                    price = 100

                    if self.player.coins >= price:
                        self.player.coins -= price
                        await self.player.save()
                        await interaction.response.send_message(
                            f"You bought a `Basic Box` for `{price}` coins! Opening the box...",
                            ephemeral=True,
                        )
                    else:
                        await interaction.response.send_message(
                            "You don't have enough coins to buy this item.",
                            ephemeral=True,
                        )
                else:
                    await interaction.response.send_message(
                        "Invalid item ID. Please try again.",
                        ephemeral=True,
                    )

        class BuyButton(discord.ui.View):
            def __init__(self, player):
                super().__init__()
                self.player = player

            @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
            async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(BuyModal(self.player))

        player, _ = await Player.get_or_create(discord_id=interaction.user.id)

        embed = discord.Embed(
            title="Shop",
            description="Use buttons to navigate and perform actions.",
            color=discord.Color.gold()
        )
        embed.add_field(name="[1] Basic Box", value="3 Balls, everything excluding T1-T5 \nPrice: **500** Coins", inline=False)
        embed.add_field(name="[#] Item Name", value="Description\nPrice: **X** Coins", inline=False)
        await interaction.response.send_message(embed=embed, view=BuyButton(player))