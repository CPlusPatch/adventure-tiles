""" This file contains the UI class, which is responsible for rendering the UI """
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from variables import (
    RESOLUTION,
    UI_ZOOM,
    GameStates,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_GAP,
)
from tile import Tile
from pos import Pos

if TYPE_CHECKING:
    from game import Game
    from level import Level

HEART_100 = pygame.image.load("assets/ui/heart_100.png")
HEART_75 = pygame.image.load("assets/ui/heart_75.png")
HEART_50 = pygame.image.load("assets/ui/heart_50.png")
HEART_25 = pygame.image.load("assets/ui/heart_25.png")
HEART_0 = pygame.image.load("assets/ui/heart_0.png")


class UI:
    """The UI class, which is responsible for rendering the UI"""

    game: Game
    level: Level

    def __init__(self, game: Game, level: Level):
        self.game = game
        self.level = level
        self.surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)

    def render(self):
        """
        Renders the UI
        """
        self.surface.fill((0, 0, 0, 0))

        if self.game.state == GameStates.PLAYING:
            self.render_health()
        elif self.game.state == GameStates.MENU:
            self.render_menu()
        return self.surface

    def render_menu(self):
        """Renders the menu"""
        # Render dark overlay on top of game
        overlay = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.surface.blit(overlay, (0, 0))

        # Render menu box
        box_size = (300, 180)
        box_pos = (
            RESOLUTION[0] / 2 - box_size[0] / 2,
            RESOLUTION[1] / 2 - box_size[1] / 2,
        )

        # Brown and pixelated rounded corners box
        pygame.draw.rect(
            self.surface,
            (139, 69, 19),
            pygame.Rect(box_pos, box_size),
            border_radius=3,
        )

        # Render resume, save, quit and load button
        stack = VButtonStack(
            [
                UIButtonRenderer(
                    "Resume",
                    self.game.resume,
                    # gold
                    bgcolor=(255, 215, 0),
                    outlinecolor=(0, 0, 0),
                ),
                UIButtonRenderer(
                    "Save",
                    self.level.save,
                    bgcolor=(255, 215, 0),
                    outlinecolor=(0, 0, 0),
                ),
                UIButtonRenderer(
                    "Load",
                    self.level.load,
                    bgcolor=(255, 215, 0),
                    outlinecolor=(0, 0, 0),
                ),
                UIButtonRenderer(
                    "Quit",
                    self.game.quit,
                    bgcolor=(255, 215, 0),
                    outlinecolor=(0, 0, 0),
                ),
            ],
            Pos(box_pos[0] + box_size[0] / 2, box_pos[1] + box_size[1] / 2),
        )

        stack_surface = stack.render()
        self.surface.blit(
            stack_surface,
            (
                box_pos[0] + box_size[0] / 2 - stack_surface.get_width() / 2,
                box_pos[1] + box_size[1] / 2 - stack_surface.get_height() / 2,
            ),
        )

    def render_health(self):
        """
        Draws a red health bar with a pink outline in the top right
        """
        health = 10  # self.level.players["0"]["health"] - 10
        max_health = 20
        bar_width = 300
        bar_height = 30
        outline_width = 3

        # Draw health bar
        health_bar = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

        # Draw health, add pink outline after

        pygame.draw.rect(
            health_bar,
            (255, 192, 203),
            pygame.Rect(
                0,
                outline_width,
                bar_width - outline_width,
                bar_height - outline_width,
            ),
            border_radius=0,
        )
        pygame.draw.rect(
            health_bar,
            (255, 0, 0),
            pygame.Rect(
                0,
                outline_width,
                (health / max_health) * bar_width,
                bar_height - outline_width * 2,
            ),
            border_radius=3,
        )

        pygame.draw.rect(
            health_bar,
            (255, 192, 203),
            pygame.Rect(0, 0, bar_width, bar_height),
            width=outline_width,
            border_radius=3,
        )

        # Draw bar to top right of screen with margin

        margin = 10

        self.surface.blit(
            health_bar,
            (
                RESOLUTION[0] - bar_width - margin,
                margin,
            ),
        )


class VButtonStack:
    """Vertical stack of buttons"""

    buttons: list[UIButtonRenderer]
    screen_position: Pos

    def __init__(self, buttons: list[UIButtonRenderer], screen_position: Pos):
        self.buttons = buttons
        self.screen_position = screen_position

    def render(self):
        """Renders the buttons"""
        surface = pygame.Surface(
            (BUTTON_WIDTH, (BUTTON_HEIGHT + BUTTON_GAP) * len(self.buttons)),
            pygame.SRCALPHA,
        )
        for i, button in enumerate(self.buttons):
            button_surface = button.render()
            surface.blit(
                button_surface,
                (
                    0,
                    i * (BUTTON_HEIGHT + BUTTON_GAP),
                ),
            )
        return surface

    def tick(self):
        """Called every frame, at 60 frames a second"""
        # Check if is being clicked
        # If so, call the onclick function
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = Pos(*pygame.mouse.get_pos())
            for i, button in enumerate(self.buttons):
                if (
                    mouse_pos.x > self.screen_position.x
                    and mouse_pos.x < self.screen_position.x + BUTTON_WIDTH
                    and mouse_pos.y
                    > self.screen_position.y + i * (BUTTON_HEIGHT + BUTTON_GAP)
                    and mouse_pos.y
                    < self.screen_position.y
                    + i * (BUTTON_HEIGHT + BUTTON_GAP)
                    + BUTTON_HEIGHT
                ):
                    button.on_click()


class UIButtonRenderer:
    """Renders a button"""

    text: str
    onclick: callable
    bgcolor: pygame.color.Color
    outlinecolor: pygame.color.Color
    is_hovered: bool

    def __init__(
        self,
        text: str,
        onclick: callable,
        bgcolor: pygame.color.Color = pygame.color.Color("black"),
        outlinecolor: pygame.color.Color = pygame.color.Color("white"),
    ):
        self.text = text
        self.onclick = onclick
        self.bgcolor = bgcolor
        self.outlinecolor = outlinecolor
        # TODO: Add hover effect
        self.is_hovered = False

    def render(self):
        """Returns a surface with the rendered button"""
        surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)

        # Draw rectangle with rounded corners and outline
        pygame.draw.rect(
            surface,
            self.bgcolor,
            pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
            border_radius=3,
        )

        pygame.draw.rect(
            surface,
            self.outlinecolor,
            pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
            width=2,
            border_radius=3,
        )

        # If button is hovered, render shine effect
        if self.is_hovered:
            shiny_surface = pygame.Surface(
                (BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA
            )

            pygame.draw.rect(
                shiny_surface,
                (255, 255, 255, 110),
                (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                border_radius=3,
            )

            surface.blit(
                shiny_surface,
                (0, 0),
            )

        text_renderer = FontRenderer(self.text)
        text_surface = text_renderer.render()

        surface.blit(
            text_surface,
            (
                BUTTON_WIDTH / 2 - text_surface.get_width() / 2,
                BUTTON_HEIGHT / 2 - text_surface.get_height() / 2,
            ),
        )

        return surface

    def on_hover(self, is_hovered):
        self.is_hovered = is_hovered

    def on_click(self):
        """Called when the button is clicked"""
        self.onclick()


class FontRenderer:
    """Renders font using the font sprites"""

    text: str

    def __init__(self, text: str):
        self.text = text

    def render(self):
        """Returns a surface with the rendered text"""
        allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKL\
            MNOPQRSTUVWXYZ0123456789$+%#&)(.!,_/) "

        text = self.text.lower()

        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)

        # Render each character of text with kerning -1 and UI_ZOOM applied onto the surface
        # Font is NOT monospace
        # Spaces are just 4-pixel spaces and not a character
        # Font height is 8

        x = 0
        y = 0

        for char in text:
            if char not in allowed_characters:
                continue
            if char == " ":
                x += 4 * UI_ZOOM
                continue
            char_surface = pygame.image.load(f"assets/font/font_{char}.png")
            surface.blit(char_surface, (x, y))
            x += char_surface.get_width() - 1

        x += 1

        # Crop surface to text
        surface = surface.subsurface(pygame.Rect(0, 0, x, 8))

        # Scale surface by UI_ZOOM
        surface = pygame.transform.scale(
            surface,
            (int(surface.get_width() * UI_ZOOM), int(surface.get_height() * UI_ZOOM)),
        )

        return surface
