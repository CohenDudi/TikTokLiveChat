import random

import commons
import entities
import vector
import pygame
import math

from vector import Vector
from enum import Enum
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFilter
import io
from typing import List, Optional





ball_default = pygame.image.load("data/ball.png")
class BallType(Enum):
    DEFAULT = 0
    OPS = 1


class Ball:
    def __init__(self, position: Vector, screen: pygame.display, velocity: Vector = Vector(0, 0), radius: float = 8,
                 ball_type: BallType = BallType.DEFAULT, image: bytes = None , name : str = None):
        self.screen = screen
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0
        self.author = name
        self.name: pygame.surface = pygame.font.SysFont("Arial", 20, bold=True).render(self.author, True, (0, 0, 0))
        self.ball_type = BallType(ball_type)
        self.score = [0]
        self.icon: Optional[pygame.image] = None

        self.image = image
        if self.image is None:
            self.icon = ball_default
        else:
            try:
                self.image = self.__mask_circle_transparent(Image.open(io.BytesIO(self.image)), 2)
                self.icon = pygame.transform.scale(pygame.image.frombuffer(self.image.tobytes(), self.image.size, self.image.mode), (64, 64))
            except:
                print(self.author)
                pass

        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True

    def update(self):
        if self.ball_type == BallType.DEFAULT:
            self.velocity.y += commons.delta_time * commons.gravity
            self.position += self.velocity * commons.delta_time
            self.check_screen_collisions()

    def draw(self):
        top_left_position = self.position - self.radius
        if self.name != None and self.icon != None:
            self.screen.blit(self.icon, top_left_position.make_int_tuple())
            self.screen.blit(self.name, (top_left_position.x, top_left_position.y - 20))
            if self.ball_type == BallType.DEFAULT:
                points = pygame.image.load("data/point.png").convert_alpha()
                points = pygame.transform.scale(points, (64, 24))
                self.screen.blit(points, (top_left_position.x , top_left_position.y+60))

                pointTxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 16, bold=True).render(str(self.score[0]), True, (20, 20, 30))
                self.screen.blit(pointTxt, (top_left_position.x+15, top_left_position.y+68))


    def check_screen_collisions(self):
        if self.position.x < self.radius or self.position.x > commons.screen_w - self.radius:
            self.velocity.x = -self.velocity.x
        if self.position.y < self.radius:
            self.velocity.y = -self.velocity.y
        elif self.position.y > commons.screen_h + self.radius:
            self.alive = False
            top_left_position = self.position - self.radius
            if top_left_position.x < 90 or top_left_position.x > 360:
                self.score[0] += 500
            if 90 <= top_left_position.x < 180 or 270 < top_left_position.x <= 360:
                self.score[0] += 1000
            if 180 <= top_left_position.x <= 270:
                self.score[0] += 2000

    def check_opst_collisions(self , balls):
        for b in balls:
            dx, dy = b.position.x - self.position.x,  b.position.y - self.position.y
            dist = math.hypot(dx, dy)
            if dist < b.radius*2:
                self.velocity.x = -self.velocity.x
                self.velocity.y = -self.velocity.y

    @staticmethod
    def __mask_circle_transparent(original: Image, blur_radius: int, offset: int = 0) -> Image:
        """
        Crop a profile picture into a circle

        :param original: Original profile picture
        :param blur_radius: Blur radius
        :param offset: Offset
        :return: New image

        """

        offset += blur_radius * 2
        mask = Image.new("L", original.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, original.size[0] - offset, original.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = original.copy()
        result.putalpha(mask)

        return result
