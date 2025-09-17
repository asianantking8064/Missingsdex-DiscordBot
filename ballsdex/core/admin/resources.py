"""
FastAPI Admin resources registration.

This module must define and register admin resources for your models.
It was previously replaced with Discord bot code, which prevented the
admin panel from registering resources and led to 404s like /admin/ball/list
and links resolving to /admin/None.
"""

from fastapi_admin.app import app
from fastapi_admin.resources import Model

from ballsdex.core.models import Ball, BallInstance, GuildConfig, Player, Special


@app.register
class BallResource(Model):
    label = "Balls"
    model = Ball


@app.register
class BallInstanceResource(Model):
    label = "Ball Instances"
    model = BallInstance


@app.register
class PlayerResource(Model):
    label = "Players"
    model = Player


@app.register
class SpecialResource(Model):
    label = "Special Events"
    model = Special


@app.register
class GuildConfigResource(Model):
    label = "Guild Configs"
    model = GuildConfig
