"""ScorePanel - Score display widget"""

import pygame

from ui.widgets.base import HBox
from ui.widgets.primitives import Label


class ScorePanel(HBox):
    def __init__(self, black_name="Black", white_name="White"):
        super().__init__(spacing=20)
        self.black_label = Label(f"{black_name}: 2", font_size=24)
        self.white_label = Label(f"{white_name}: 2", font_size=24)
        self.add(self.black_label)
        self.add(self.white_label)

    def update_scores(self, black_count: int, white_count: int):
        self.black_label.set_text(f"Black: {black_count}")
        self.white_label.set_text(f"White: {white_count}")
