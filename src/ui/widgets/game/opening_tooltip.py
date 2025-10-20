"""OpeningTooltip - Opening book information widget"""

import pygame

from ui.widgets.primitives import Label, Panel


class OpeningTooltip(Panel):
    def __init__(self):
        super().__init__(width=300, height=100)
        self.title_label = Label("", font_size=20)
        self.info_label = Label("", font_size=16)
        self.add(self.title_label)
        self.add(self.info_label)

    def set_opening_info(self, opening_name: str, advantage: str = ""):
        if opening_name:
            self.title_label.set_text(f"Opening: {opening_name}")
            self.info_label.set_text(f"Advantage: {advantage}" if advantage else "")
            self.show()
        else:
            self.hide()
