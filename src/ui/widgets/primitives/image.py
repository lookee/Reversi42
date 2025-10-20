"""
Image Widget - Auto-resizing image component

Image widget with intelligent auto-scaling and multiple fit modes.

Design Pattern: Component
"""

from typing import Literal, Optional, Tuple

import pygame

from ui.widgets.base import Widget


class Image(Widget):
    """
    Image widget with auto-scaling.

    Features:
    - Multiple fit modes (contain, cover, fill, none)
    - Maintains aspect ratio (optional)
    - Auto-resizing to container
    - Supports center_in_parent

    Usage:
        # Auto-fit to 300x200 container
        img = Image("logo.png", width=300, height=200, fit="contain")

        # Fixed size, no scaling
        img = Image("icon.png", fit="none")

        # Fill container, crop if needed
        img = Image("background.png", width=800, height=600, fit="cover")
    """

    def __init__(
        self,
        image_path: str,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        fit: Literal["contain", "cover", "fill", "none"] = "contain",
        center_in_parent: bool = False,
    ):
        """
        Initialize image widget.

        Args:
            image_path: Path to image file
            x, y: Position
            width: Widget width (0 = original image width)
            height: Widget height (0 = original image height)
            fit: How to fit image in widget bounds
                - "contain": Scale to fit inside bounds, maintain aspect ratio
                - "cover": Scale to cover entire bounds, maintain aspect ratio (may crop)
                - "fill": Stretch to fill bounds exactly (may distort)
                - "none": No scaling, use original size
            center_in_parent: Auto-center in parent container
        """
        self.image_path = image_path
        self.fit = fit
        self.original_surface: Optional[pygame.Surface] = None
        self.scaled_surface: Optional[pygame.Surface] = None

        # Load image
        try:
            self.original_surface = pygame.image.load(image_path)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {image_path}: {e}")
            # Create placeholder surface
            self.original_surface = pygame.Surface((100, 100))
            self.original_surface.fill((200, 200, 200))  # Gray placeholder

        # Determine widget size
        img_width, img_height = self.original_surface.get_size()
        widget_width = width if width > 0 else img_width
        widget_height = height if height > 0 else img_height

        super().__init__(x, y, widget_width, widget_height, center_in_parent)

        # Scale image to fit
        self._scale_image()

    def _scale_image(self):
        """Scale image based on fit mode."""
        if not self.original_surface:
            return

        img_width, img_height = self.original_surface.get_size()
        target_width = self.rect.width
        target_height = self.rect.height

        if self.fit == "none":
            # No scaling
            self.scaled_surface = self.original_surface
            self.rect.width = img_width
            self.rect.height = img_height

        elif self.fit == "fill":
            # Stretch to fill (may distort)
            self.scaled_surface = pygame.transform.scale(
                self.original_surface, (target_width, target_height)
            )

        elif self.fit == "contain":
            # Scale to fit inside bounds, maintain aspect ratio
            img_aspect = img_width / img_height
            target_aspect = target_width / target_height

            if img_aspect > target_aspect:
                # Image is wider, fit to width
                new_width = target_width
                new_height = int(target_width / img_aspect)
            else:
                # Image is taller, fit to height
                new_height = target_height
                new_width = int(target_height * img_aspect)

            self.scaled_surface = pygame.transform.smoothscale(
                self.original_surface, (new_width, new_height)
            )

        elif self.fit == "cover":
            # Scale to cover entire bounds, maintain aspect ratio (may crop)
            img_aspect = img_width / img_height
            target_aspect = target_width / target_height

            if img_aspect > target_aspect:
                # Image is wider, fit to height
                new_height = target_height
                new_width = int(target_height * img_aspect)
            else:
                # Image is taller, fit to width
                new_width = target_width
                new_height = int(target_width / img_aspect)

            # Scale and crop
            scaled = pygame.transform.smoothscale(self.original_surface, (new_width, new_height))

            # Crop to target size (center crop)
            crop_x = (new_width - target_width) // 2
            crop_y = (new_height - target_height) // 2
            self.scaled_surface = scaled.subsurface(
                pygame.Rect(crop_x, crop_y, target_width, target_height)
            ).copy()

    def set_size(self, width: int, height: int):
        """Update size and rescale image."""
        super().set_size(width, height)
        self._scale_image()

    def render(self, surface: pygame.Surface):
        """Render image."""
        if not self.visible or not self.scaled_surface:
            return

        # Get absolute rect for rendering
        abs_rect = self.get_absolute_rect()

        # Center image in widget rect if smaller (for "contain" mode)
        if self.fit == "contain" and self.scaled_surface:
            img_width, img_height = self.scaled_surface.get_size()
            offset_x = (abs_rect.width - img_width) // 2
            offset_y = (abs_rect.height - img_height) // 2
            surface.blit(self.scaled_surface, (abs_rect.x + offset_x, abs_rect.y + offset_y))
        else:
            surface.blit(self.scaled_surface, abs_rect)

    def set_image(self, image_path: str):
        """
        Change the image.

        Args:
            image_path: Path to new image file
        """
        self.image_path = image_path
        try:
            self.original_surface = pygame.image.load(image_path)
            self._scale_image()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {image_path}: {e}")
