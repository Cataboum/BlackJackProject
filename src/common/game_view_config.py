from dataclasses import dataclass, field
from typing import Optional, List

from marshmallow import fields, Schema, post_load

from src.common.constants import CONFIG_GAME_VIEW


@dataclass
class Dimensions:
    width: Optional[int] = field(default=None)
    height: Optional[int] = field(default=None)


class DimensionsSchema(Schema):
    width = fields.Integer(default=None)
    height = fields.Integer(default=None)

    @post_load
    def make(self, data):
        return Dimensions(**data)


@dataclass
class Coordinates:
    x: Optional[int] = field(default=None)
    y: Optional[int] = field(default=None)


class CoordinatesSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()

    @post_load
    def make(self, data):
        return Coordinates(**data)


@dataclass
class AreaDefinition(Coordinates, Dimensions):
    color: Optional[List[int]] = field(default=None)
    pass


class AreaDefinitionSchema(CoordinatesSchema, DimensionsSchema):
    color = fields.List(fields.Integer())
    @post_load()
    def make(self, data):
        return AreaDefinition(**data)


@dataclass
class CardArea:
    dealer: AreaDefinition
    player: AreaDefinition
    extra_card_offset: Coordinates


class CardAreaSchema(Schema):
    dealer = fields.Nested(AreaDefinitionSchema())
    player = fields.Nested(AreaDefinitionSchema())
    extra_card_offset = fields.Nested(CoordinatesSchema())

    @post_load
    def make(self, data):
        return CardArea(**data)


@dataclass
class GameView:
    card_areas: CardArea
    window: AreaDefinitionSchema
    cards: Dimensions
    game_buttons: AreaDefinitionSchema


class GameViewSchema(Schema):
    card_areas = fields.Nested(CardAreaSchema())
    window = fields.Nested(AreaDefinitionSchema())
    cards = fields.Nested(DimensionsSchema())
    game_buttons = fields.Nested(AreaDefinitionSchema())

    @post_load
    def make(self, data) -> GameView:
        return GameView(**data)


game_view_schema = GameViewSchema()
game_view: GameView
game_view_config, game_view_config_errors = game_view_schema.load(
    CONFIG_GAME_VIEW
)
# TODO: Add tests for loading
