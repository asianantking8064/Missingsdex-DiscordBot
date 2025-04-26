# adjusts every rarity, if you were using 1.0, 2.0, 3.0 etc, to the way they way should be 

from collections import defaultdict
from ballsdex.core.models import Ball

balls = await Ball.all().order_by("rarity")
total_rarity = sum(ball.rarity for ball in balls)

for ball in balls:
    new = ball.rarity / total_rarity
    await Ball.filter(id=ball.id).update(rarity=new)

# A cool box command i made that, well, lets you open a box that gives you 3 balls with a special card

@app_commands.command()
  @app_commands.checks.cooldown(1, 5400, key=lambda i: i.user.id)
  async def box(self, interaction: discord.Interaction):
        """
        Open a box!
        """
        UserID = str(interaction.user.id)
        player, created = await Player.get_or_create(discord_id=UserID)

        cob1 = await CountryBall.get_random()
        instance1 = await BallInstance.create(
                ball=cob1.model,
                player=player,
                shiny=random.randint(1, what_you_want) == 1,
                attack_bonus=random.randint(-20, 20),
                health_bonus=random.randint(-20, 20),
                special= await Special.get(pk=int(what_you_want)),
            )

        cob2 = await CountryBall.get_random()
        instance2 = await BallInstance.create(
            ball=cob2.model,
            player=player,
            shiny=random.randint(1, what_you_want) == 1,
            attack_bonus=random.randint(-20, 20),
            health_bonus=random.randint(-20, 20),
            special= await Special.get(pk=int(what_you_want)),
        )

        cob3 = await CountryBall.get_random()
        instance3 = await BallInstance.create(
            ball=cob3.model,
            player=player,
            shiny=random.randint(1, what_you_want) == 1,
            attack_bonus=random.randint(-20, 20),
            health_bonus=random.randint(-20, 20),
            special= await Special.get(pk=int(what_you_want)),
        )

        emoji1 = self.bot.get_emoji(instance1.countryball.emoji_id)
        emoji2 = self.bot.get_emoji(instance2.countryball.emoji_id)
        emoji3 = self.bot.get_emoji(instance3.countryball.emoji_id)

        embed = discord.Embed(title=f"<@{UserID}> has opened a **Ballsdex Box**!", description="", color=discord.Colour.blue())
        embed.add_field(name=f"x1 {emoji1} {cob1.name}", value=f"``💖{instance1.attack_bonus}`` ``⚔️{instance1.health_bonus}`` ``✨{instance1.shiny}``")
        embed.add_field(name=f"x1 {emoji2} {cob2.name}", value=f"``💖{instance2.attack_bonus}`` ``⚔️{instance2.health_bonus}`` ``✨{instance2.shiny}``")
        embed.add_field(name=f"x1 {emoji3} {cob3.name}", value=f"``💖{instance3.attack_bonus}`` ``⚔️{instance3.health_bonus}`` ``✨{instance3.shiny}``")
        embed.set_thumbnail(url="") # Set the thumbnail as an image url, if you dont want one delete the line 
        embed.set_footer(text="Open your next box in 1.5 hours from this message.")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=False
        )
        return

# I made a new button for if you want people to have name hints, you can add more hints if you want they’re pretty easy to do I was too lazy to make a hint limit 

@button(style=discord.ButtonStyle.secondary, label="Gimme a hint!")
    async def hint_button(self, interaction: discord.Interaction["BallsDexBot"], button: Button):

        if self.ball.caught:
            await interaction.response.send_message("No hint for you! I was caught already!", ephemeral=True)
        else: 
            hints = [
            f"This balls name stars with the letter **{self.ball.name[0]}**...",
            f"This balls name ends with the letter **{self.ball.name[-1]}**...",
            f"This balls name has **{len(self.ball.name)}** letters inside of it...",
            ]
            hint = random.choice(hints)
            await interaction.response.send_message(hint, ephemeral=True)