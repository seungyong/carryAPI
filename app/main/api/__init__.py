from app import app, api

# API File
from .champion import champion_bp, champion_ns
from .item import item_bp, item_ns
from .spell import spell_bp, spell_ns
from .game import game_bp, game_ns
from .player import player_bp, player_ns
from .rune import rune_bp, rune_ns

# Blueprint Register
app.register_blueprint(champion_bp, name='champion_bp', url_prefix='/champions')
app.register_blueprint(item_bp, name='item_bp', url_prefix='/items')
app.register_blueprint(spell_bp, name='spell_bp', url_prefix='/spells')
app.register_blueprint(game_bp, name='game_bp', url_prefix='/games')
app.register_blueprint(player_bp, name='player_bp', url_prefix='/players')
app.register_blueprint(rune_bp, name='rune_bp', url_prefix='/runes')

# Namespace Register
api.add_namespace(champion_ns)
api.add_namespace(item_ns)
api.add_namespace(spell_ns)
api.add_namespace(game_ns)
api.add_namespace(player_ns)
api.add_namespace(rune_ns)
