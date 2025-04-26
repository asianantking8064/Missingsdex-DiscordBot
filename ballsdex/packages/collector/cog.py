import discord
from discord import app_commands
from discord.ext import commands

from ballsdex.core.models import (
    Ball,
    BallInstance,
    Player,
    Special,
)
from ballsdex.core.utils.transformers import BallEnabledTransform
from tortoise.exceptions import DoesNotExist

class Collector(commands.GroupCog, group_name="claim"):
    """
    Cog for claiming collector countryballs.
    """

    @app_commands.command()
    async def collector(self, interaction: discord.Interaction, countryball: BallEnabledTransform):
        """
        Claim a collector countryball.

        Parameters
        ----------
        countryball: Ball
            Ball to claim.
        """
        player, _ = await Player.get_or_create(discord_id=interaction.user.id)

        try:
            special = await Special.get(name="Collector")
        except DoesNotExist:
            await interaction.response.send_message(
                "No `Collector` special is registered on this bot.", ephemeral=True
            )
            return

        # Check if the player already has a collector instance for this ball
        already_claimed = await BallInstance.filter(
            ball=countryball, player=player, special=special
        ).exists()
        if already_claimed:
            await interaction.response.send_message(
                "You have already claimed this collector ball.", ephemeral=True
            )
            return

        # Fetch the player's ball instances for the given countryball
        player_balls = await BallInstance.filter(
            ball=countryball, player=player
        ).order_by("-catch_date")

        # Determine the required amount based on rarity
        rarity = countryball.rarity
        if rarity <= 0.7:
            required_amount = 15
        elif rarity <= 0.9:
            required_amount = 22
        elif rarity <= 38.0:
            required_amount = 35
        elif rarity <= 52.0:
            required_amount = 40
        elif rarity <= 58.0:
            required_amount = 50
        elif rarity <= 68.0:
            required_amount = 70
        elif rarity <= 70.0:
            required_amount = 85
        elif rarity <= 100.0:
            required_amount = 100
        elif rarity <= 120.0:
            required_amount = 120
        else:
            required_amount = 0

        # Check if the player has enough balls to claim the collector
        if len(player_balls) < required_amount:
            await interaction.response.send_message(
                f"You need **{required_amount}** {countryball.country} balls to claim this collector.\n"
                f"You currently have **{len(player_balls)}**.",
                ephemeral=True,
            )
            return

        # Create a new BallInstance for the collector
        collector_instance = await BallInstance.create(
            ball=countryball,
            player=player,
            health_bonus=0,
            attack_bonus=0,
            defense_bonus=0,
            special=special,
        )

        await interaction.response.send_message(
            f"Congratulations! You have claimed a collector {collector_instance.ball.country}!",
            ephemeral=True,
        )

    @app_commands.command()
    async def diamond(self, interaction: discord.Interaction, countryball: BallEnabledTransform):
        """
        Claim a diamond countryball.

        Parameters
        ----------
        countryball: Ball
            Ball to claim.
        """
        player, _ = await Player.get_or_create(discord_id=interaction.user.id)

        try:
            special = await Special.get(name="Diamond")
        except DoesNotExist:
            await interaction.response.send_message(
                "No `Diamond` special is registered on this bot.", ephemeral=True
            )
            return

        # Check if the player already has a diamond instance for this ball
        already_claimed = await BallInstance.filter(
            ball=countryball, player=player, special=special
        ).exists()
        if already_claimed:
            await interaction.response.send_message(
                "You have already claimed this diamond ball.", ephemeral=True
            )
            return

        # Check if the player has enough shiny instances of the ball
        required_shinies = 1  # Set the required number of shinies here
        shiny_count = await BallInstance.filter(
            ball=countryball, player=player, shiny=True
        ).count()

        if shiny_count < required_shinies:
            await interaction.response.send_message(
                f"You need **{required_shinies} shiny {countryball.country} balls** to claim this diamond ball.\n"
                f"You currently have **{shiny_count}**.",
                ephemeral=True,
            )
            return

        # Create a new BallInstance for the diamond
        diamond_instance = await BallInstance.create(
            ball=countryball,
            player=player,
            health_bonus=0,
            attack_bonus=0,
            defense_bonus=0,
            special=special,
        )

        await interaction.response.send_message(
            f"Congratulations! You have claimed a diamond {diamond_instance.ball.country}!",
            ephemeral=True,
        )