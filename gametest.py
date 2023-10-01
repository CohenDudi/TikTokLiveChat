import asyncio
import io
from asyncio import AbstractEventLoop
from typing import List, Optional

import pygame
from PIL import Image, ImageDraw, ImageFilter

from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent , GiftEvent , ConnectEvent , LikeEvent , FollowEvent , ShareEvent
import random
import math
import pygame_textinput

#game2
import commons
import pygame
import vector
import entities

from vector import Vector
from ball import Ball, BallType

enemyList = []
gameOneEnemyList = [[[(0,0)]]*45]*90
ballsOpsList = []

giftNum = 5
likeNum = 20
followNum = 3
shareNum = 5
leaderBoard = []
gameTimeMin = 3
gameTimeMS = 0
gameSpeed = 0.025
gameType = ["Fight", "Peggle"]

class Comment:
    """
    Comment object for displaying to screen

    """

    def findEnemy(self):
        if self.gotAttacked == 1 and self.idleMod == 0:
            if self.CDAttacked > 0:
                if (self.xpos + (self.gotAttackedX / 20) * self.speed) > 390 or (self.xpos + (self.gotAttackedX / 20) * self.speed) < 10  :
                    self.gotAttackedX = self.gotAttackedX*-1
                self.xpos += ((self.gotAttackedX / 20) * self.speed)
                if (self.ypos + (self.gotAttackedY / 20) * self.speed) > 800 or (self.ypos + (self.gotAttackedY / 20) * self.speed) < 160 :
                    self.gotAttackedY = self.gotAttackedY*-1
                self.ypos += ((self.gotAttackedY / 20) * self.speed)
                self.CDAttacked -= 1
            else:
                self.gotAttacked = 0
                self.CDAttacked = 10
        else:
            self.xpos = self.xpos
            self.enemyDistance = 999999999
            dist = 999999999
            try:
                c = min([e for e in enemyList if e is not self], key=lambda e: pow(e.xpos-self.xpos, 2) + pow(e.ypos-self.ypos, 2))
            except:
                c = None
            if c is not None:
                dx, dy = c.xpos - self.xpos, c.ypos - self.ypos
                dist = math.hypot(dx, dy)
                if self.enemyDistance > dist > 64:
                    self.enemyDistance = dist
                    dx, dy = dx / dist, dy / dist  # Normalize.
                    self.xpos += dx * 2 * self.speed
                    self.ypos += dy * 2 * self.speed
                    # myradians = math.atan2(c.ypos - self.ypos, c.xpos - self.xpos)
                    myradians = math.atan2(self.ypos - c.ypos, self.xpos - c.xpos)
                    self.degreeAnemy = math.degrees(myradians)

                    self.distxt: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(self.enemyDistance), True, (20, 20, 30))
                else:
                    if dist <= 64 and dx != 0 and dy != 0:
                        if c.health > 0:
                            c.health -= self.attackPower
                            if c.health < 1:
                                self.health = self.Orghealth
                                self.score[0] += 1
                                leaderBoard.sort(key=lambda a: a[1], reverse=True)
                            self.gotAttacked = 1
                            self.gotAttackedX += -1 * dx
                            self.gotAttackedY += -1 * dy
                            c.gotAttackedX += dx
                            c.gotAttackedY += dy
                            c.distxt: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(c.enemyDistance), True, (20, 20, 30))
                            c.healthtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(c.health), True, (20, 20, 30))
                            c.gotAttacked = 1
                        else:
                            # enemyList.remove(c)
                            # print(enemyList)
                            del c



            """
            
            for c in enemyList:
                dx, dy = c.xpos - self.xpos, c.ypos - self.ypos
                dist = math.hypot(dx, dy)
                if self.enemyDistance > dist > 64:
                    self.enemyDistance = dist
                    dx, dy = dx / dist, dy / dist  # Normalize.
                    self.xpos += dx * 2 * self.speed
                    self.ypos += dy * 2 * self.speed
                    #myradians = math.atan2(c.ypos - self.ypos, c.xpos - self.xpos)
                    myradians = math.atan2(self.ypos - c.ypos ,self.xpos -  c.xpos )
                    self.degreeAnemy = math.degrees(myradians)

                    self.distxt: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(self.enemyDistance), True, (20, 20, 30))
                else:
                    if dist <= 64 and dx != 0 and dy != 0:
                        if c.health > 0 :
                            c.health -= self.attackPower
                            if c.health < 1:
                                self.health = self.Orghealth
                                self.score[0] += 1
                                leaderBoard.sort(key=lambda a: a[1], reverse=True)
                            self.gotAttacked = 1
                            self.gotAttackedX += -1*dx
                            self.gotAttackedY += -1*dy
                            c.gotAttackedX += dx
                            c.gotAttackedY += dy
                            c.distxt: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(c.enemyDistance), True, (20, 20, 30))
                            c.healthtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(c.health), True, (20, 20, 30))
                            c.gotAttacked = 1
                        else:
                            #enemyList.remove(c)
                            #print(enemyList)
                            del c
                """

    def addLikes(self, likes : int):
        self.totalLikes += likes
        #if likes >0:
             #print("likes " + self.author + " : " + str(likes) + " total: " +str(self.totalLikes))
        if self.totalLikes > likeNum and self.totalLikes > 0:
            print("like: " + self.author + " : " + str(likes) + " total: " + str(self.totalLikes))
            self.totalLikes -= math.floor((self.totalLikes / likeNum)) * likeNum
            random1 = random.randint(1, 3)
            # print(random1)
            if random1 == 1:
                self.health += 1
                self.Orghealth += 1
                print("like: "+self.author + " " + " health: +" + str(self.health) + "/" + str(self.Orghealth))
            if random1 == 2:
                self.attackPower += 1
                print("like: "+self.author + " attack: +" + str(self.attackPower))
            if random1 == 3:
                self.health = self.Orghealth
                print("like: "+self.author + " max health: "+ str(self.health) + "/" + str(self.Orghealth ))

    def addFollowBonus(self):
        self.health += followNum
        self.Orghealth += followNum
        self.attackPower += followNum
        print("Follower bonus: " + self.author)
        print("Follower bonus: " + self.author + " " + " health: +" + str(self.health) + "/" + str(self.Orghealth))
        print("Follower bonus: " + self.author + " attack: +" + str(self.attackPower))
        print("Follower bonus: " + self.author + " max health: " + str(self.health) + "/" + str(self.Orghealth))

    def addShareBonus(self):
        self.health += shareNum
        self.Orghealth += shareNum
        self.attackPower += shareNum
        print("Share bonus: " + self.author)
        print("Share bonus: " + self.author + " " + " health: +" + str(self.health) + "/" + str(self.Orghealth))
        print("Share bonus: " + self.author + " attack: +" + str(self.attackPower))
        print("Share bonus: " + self.author + " max health: " + str(self.health) + "/" + str(self.Orghealth))

    def __init__(self, author: str, text: str, image: bytes , gifts : int , giftImage : bytes):
        """
        Initialize comment object

        :param author: Author name
        :param text: Comment text
        :param image: Comment image (as bytes)

        """
        self.enemyDistance = 999999999
        self.author: str = author
        self.text: str = text
        self.speed = 3
        self.health = 5
        self.Orghealth = 5
        self.gotAttacked = 0
        self.CDAttacked = 10
        self.gotAttackedX = 0
        self.gotAttackedY = 0
        self.idleMod = 0
        self.idledirecx = 0
        self.idledirecy = 0
        self.degreeAnemy = 0
        self.giftCount = gifts
        self.giftIconCount = 0
        self.attackPower = 1
        self.totalLikes = 0
        self.score = [0]
        self.fullHealthTXT = str(self.health) + "/" + str(self.Orghealth)
        self.name: pygame.surface = pygame.font.SysFont("Arial", 20, bold=True).render(self.author, True, (0, 0, 0))
        self.comment: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(self.text, True, (20, 20, 30))
        self.distxt: pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(str(self.enemyDistance), True, (20, 20, 30))
        self.healthtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=False).render(self.fullHealthTXT, True, (20, 20, 30))
        self.attackhtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 20, bold=True).render(str(self.attackPower), True, (20, 20, 30))
        self.icon: Optional[pygame.image] = None
        self.giftImageicon: Optional[pygame.image] = None
        self.xpos = random.randint(100, 300)
        self.ypos = random.randint(160, 800)




        try:
            image = self.__mask_circle_transparent(Image.open(io.BytesIO(image)), 2)
            self.icon = pygame.transform.scale(pygame.image.frombuffer(image.tobytes(), image.size, image.mode), (64, 64))
            #print(f"{self.author} -> {self.text}")

            if giftImage != 0:
                giftImage = self.__mask_circle_transparent(Image.open(io.BytesIO(giftImage)), 2)
                self.giftImageicon = pygame.transform.scale(pygame.image.frombuffer(giftImage.tobytes(), giftImage.size, giftImage.mode), (64, 64))
            enemyList.append(self)
        except:
            pass

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

    def blit(self, screen: pygame.display, x: int, y: int) -> None:
        """
        Blit a comment to a surface

        :param screen: Screen to blit on
        :param x: X-position
        :param y: Y-Position

        """

        # If exists
        if self.icon:
            screen.blit(self.icon, (x, y))
            screen.blit(self.name, (x, y - 20))
            #screen.blit(self.healthtxt, (x - 70, y))
            ARed = pygame.draw.rect(screen, (124, 252, 0), (x , y+74 , 70, 15), 0)
            surf = pygame.Surface((ARed.w * 0, ARed.h * 0))
            screen.blit(surf, (x, y))
            AGreen = pygame.draw.rect(screen, (255, 0, 0), (x+4, y + 77, ((self.health*60)/self.Orghealth), 10), 0)
            surf2 = pygame.Surface((AGreen.w * 0 , AGreen.h *0 ))
            screen.blit(surf2, (x, y))
            swordImg = pygame.image.load("data/swordimg.PNG").convert_alpha()
            swordImg = pygame.transform.scale(swordImg, (72, 72))
            swordImg = pygame.transform.rotate(swordImg, self.degreeAnemy)
            if self.giftIconCount > 0:
                try:
                    self.giftImageicon.set_alpha(180 - ((self.giftIconCount - 10)*-10))
                    screen.blit(self.giftImageicon, (x, y))
                except:
                    pass
                self.giftIconCount -= 1
            screen.blit(swordImg, (x-36, y))

            self.fullHealthTXT = str(self.health) + "/" + str(self.Orghealth)
            self.healthtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 14, bold=True).render(self.fullHealthTXT, True, (20, 20, 30))
            screen.blit(self.healthtxt, (x+20, y + 75))

            fistAttack = pygame.image.load("data/fistAttack.PNG").convert_alpha()
            fistAttack = pygame.transform.scale(fistAttack, (32, 32))
            screen.blit(fistAttack, (x+40, y+30))
            self.attackhtxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 16, bold=True).render(str(self.attackPower), True, (20, 20, 30))
            screen.blit(self.attackhtxt, (x+51, y + 46))

            points = pygame.image.load("data/point.png").convert_alpha()
            points = pygame.transform.scale(points, (24, 24))
            screen.blit(points, (x+44 , y ))
            pointTxt = pygame.surface = pygame.font.SysFont("Segoe UI Emoji", 16, bold=True).render(str(self.score[0]), True, (20, 20, 30))
            screen.blit(pointTxt, (x+51, y+7))

        """
                if self.icon:
            screen.blit(self.icon, (x + 10, y - 5))
random.randint(100,800)
        
        screen.blit(self.name, (x + 60, y))
        screen.blit(self.comment, (x + self.name.get_width() + 70, y + self.comment.get_height() / 4))
        """



class DisplayCase:
    """
    DisplayCase class for managing pygame

    """

    def __init__(self, loop: AbstractEventLoop, height: int = 900, width: int = 450):
        """
        Initialize a display case

        :param loop: asyncio event loop
        :param height: Screen height
        :param width: Screen width

        """
        print("case")
        self.height: int = height
        self.width: int = width

        self.loop: AbstractEventLoop = loop
        self.screen: pygame.display = pygame.display.set_mode((width, height))
        self._running: bool = True
        self.screen: pygame.display = pygame.display.set_mode((self.width, self.height))
        self.queue: List[CommentEvent] = list()
        self.active: List[Comment] = list()
        self.queue2: List[GiftEvent] = list()
        self.queue3: List[LikeEvent] = list()
        self.queue4: List[FollowEvent] = list()
        self.queue5: List[ShareEvent] = list()
        self.gameTime = 0
        self.gameMod = 1



    async def start(self):
        """
        Start the loop
        :return: None

        """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("TikTok LIVE")


        ballsOpsList.append(Ball(Vector(112.5,700),self.screen,ball_type = BallType.OPS))
        ballsOpsList.append(Ball(Vector(225,700),self.screen,ball_type = BallType.OPS))
        ballsOpsList.append(Ball(Vector(337,700),self.screen,ball_type = BallType.OPS))

        ballsOpsList.append(Ball(Vector(150,500),self.screen,ball_type = BallType.OPS))
        ballsOpsList.append(Ball(Vector(300,500),self.screen,ball_type = BallType.OPS))

        ballsOpsList.append(Ball(Vector(225,300),self.screen,ball_type = BallType.OPS))

        self._running = True
        await self.__screen_loop()

    def stop(self):
        """
        Stop the loop
        :return: None

        """

        self._running = False
        pygame.quit()

    async def __pop_queue(self):
        leaderBoard.sort(key=lambda a: a[1], reverse=True)
        if self.gameMod == 1:
            if len(self.queue) > 0:
                event = self.queue.pop(0)
                self.addUsers(event.user.unique_id,event.comment,(await event.user.avatar.download()),0 , 0 , 0 , 0 , 0)

            if len(self.queue2) > 0:
                gifts = self.queue2.pop(0)
                self.addUsers(gifts.user.unique_id, " ", (await gifts.user.avatar.download()), gifts.gift.info.diamond_count, (await gifts.gift.info.image.download()), 0, 0, 0)

            if len(self.queue3) > 0:
                likes = self.queue3.pop(0)
                self.addUsers(likes.user.unique_id," ",(await likes.user.avatar.download()),0 , 0 , likes.likes , 0 , 0)

            if len(self.queue4) > 0:
                follow = self.queue4.pop(0)
                print("follow: " + follow.user.unique_id)
                self.addUsers(follow.user.unique_id," ",(await follow.user.avatar.download()),0 , 0 , 0 , 1 , 0)

            if len(self.queue5) > 0:
                share = self.queue5.pop(0)
                print("share: " + share.user.unique_id)
                self.addUsers(share.user.unique_id," ",(await share.user.avatar.download()),0 , 0 , 0 , 0 , 1)

        if self.gameMod == 2:
            if len(self.queue) > 0:
                event = self.queue.pop(0)
                #self.addUsers(event.user.unique_id,event.comment,(await event.user.avatar.download()),0 , 0 , 0 , 0 , 0)
                #entities.balls.append(Ball(Vector(random.randint(10, 440), 250), self.screen, vector.random_vector() * 300, image = await event.user.avatar.download(), radius = 32 , name = event.user.unique_id)  )
                self.addBall(event.user.unique_id , await event.user.avatar.download(),0,0,0,0)


            if len(self.queue2) > 0:
                gifts = self.queue2.pop(0)
                self.addUsers(gifts.user.unique_id, " ", (await gifts.user.avatar.download()), gifts.gift.info.diamond_count, (await gifts.gift.info.image.download()), 0, 0, 0)

            if len(self.queue3) > 0:
                likes = self.queue3.pop(0)
                self.addUsers(likes.user.unique_id," ",(await likes.user.avatar.download()),0 , 0 , likes.likes , 0 , 0)

            if len(self.queue4) > 0:
                follow = self.queue4.pop(0)
                print("follow: " + follow.user.unique_id)
                self.addUsers(follow.user.unique_id," ",(await follow.user.avatar.download()),0 , 0 , 0 , 1 , 0)

            if len(self.queue5) > 0:
                share = self.queue5.pop(0)
                print("share: " + share.user.unique_id)
                self.addUsers(share.user.unique_id," ",(await share.user.avatar.download()),0 , 0 , 0 , 0 , 1)




        """
        comment = Comment(
            author=event.user.unique_id,
            text=event.comment,
            image=(await event.user.avatar.download())
        )
        """
        #print(event.raw_data)

        #self.active.insert(0, comment)
        #print("Comment Received:", self.active)



    def addBonus(self, c : Comment):
        if c.giftCount % giftNum == 0 and c.giftCount != 0:
            random1 = random.randint(1,3)
            print("gift: " + c.author + " : " + str(c.giftCount))
            #print(random1)
            if random1 == 1:
                c.health += 1
                c.Orghealth += 1
                print("gift: "+c.author + " " + " health: +"+ str(c.health) + "/" + str(c.Orghealth))
            if random1 == 2:
                c.attackPower += 1
                print("gift: "+c.author + " attack: +" + str(c.attackPower))
            if random1 ==3:
                c.health = c.Orghealth
                print("gift: "+c.author + " max health: "+ str(c.health) + "/" + str(c.Orghealth ))

    def addBall(self, a : str , image : bytes ,giftNumber : int , likes : int , follow : int , share : int ):
        for item in entities.balls:
            if item.author == a:
                #item.giftCount += giftNumber
                #item.Orghealth += giftNumber
                #item.health += giftNumber
                #self.addBonus(item)
                #item.addLikes(likes)
                #if giftImage != 0:
                #    item.giftIconCount = 10
                #if follow == 1:
                #    item.addFollowBonus()
                #if share == 1:
                #    item.addShareBonus()
                return

        ball = Ball(
            Vector(random.randint(10, 440), 250),
            self.screen,
            vector.random_vector() * 300,
            image= image,
            radius=32,
            name=a)



        #comment.addLikes(likes)
        #comment.health += giftNumber
        #comment.Orghealth += giftNumber
        #if follow == 1:
        #    comment.addFollowBonus()
        #if share == 1:
        #    comment.addShareBonus()

        #self.addBonus(comment)
        #if giftImage != 0:
            #print(giftImage)
        #    comment.giftIconCount = 10
        #self.active.insert(0, comment)
        entities.balls.append(ball)
        for x in range (0,len(leaderBoard)):
            if leaderBoard[x][0] == ball.author:
                ball.score[0] = leaderBoard[x][1][0]
                leaderBoard[x] = (ball.author, ball.score)
                return
        leaderBoard.append((ball.author, ball.score))



    def addUsers(self, a : str , t : str , image : bytes , giftNumber : int,giftImage : bytes , likes : int , follow : int , share : int):
        for item in self.active:
            if item.author == a:
                item.giftCount += giftNumber
                item.Orghealth += giftNumber
                item.health += giftNumber
                self.addBonus(item)
                item.addLikes(likes)
                if giftImage != 0:
                    item.giftIconCount = 10
                if follow == 1:
                    item.addFollowBonus()
                if share == 1:
                    item.addShareBonus()
                return

        comment = Comment(
            a,
            t,
            image,
            giftNumber,
            giftImage
        )
        comment.addLikes(likes)
        #comment.health += giftNumber
        #comment.Orghealth += giftNumber
        if follow == 1:
            comment.addFollowBonus()
        if share == 1:
            comment.addShareBonus()

        self.addBonus(comment)
        if giftImage != 0:
            #print(giftImage)
            comment.giftIconCount = 10
        self.active.insert(0, comment)

        for x in range (0,len(leaderBoard)):
            if leaderBoard[x][0] == comment.author:
                comment.score[0] = leaderBoard[x][1][0]
                leaderBoard[x] = (comment.author, comment.score)
                return
        #for l in leaderBoard:
        #    if l[0] == comment.author:
        #        comment.score[0] = l[1][0]
        #        leaderBoard[] = (l[0], comment.score)
        #        return
        leaderBoard.append((comment.author, comment.score))

    async def __screen_loop(self):
        """
        Main loop for screen
        :return: None

        """

        while self._running:
            #(len(entities.balls))
            # Clear screen
            #if self.gameMod == 2:
            #    self.cleanQue()
            self.screen.fill((180, 180, 180))
            if self.gameMod == 1:
                bg = pygame.image.load("data/bg.png")
                rules = pygame.image.load("data/rules.png")
            if self.gameMod == 2:
                bg = pygame.image.load("data/bgGame2.jpg")
                rules = pygame.image.load("data/rulesGame2.png")
            bg = pygame.transform.scale(bg, (450, 900))

            rules = pygame.transform.scale(rules, (450, 140))
            self.screen.blit(bg, (0, 0))
            self.screen.blit(rules, (0, 0))
            headLindLeader: pygame.surface = pygame.font.SysFont("Arial", 20, bold=True).render("LeaderBoard:", True, (0, 0, 0))
            self.screen.blit(headLindLeader, (255, 55))
            if len(leaderBoard) > 0:
                leader1: pygame.surface = pygame.font.SysFont("Arial", 18, bold=True).render(leaderBoard[0][0] + " " + str(leaderBoard[0][1][0]), True, (0, 0, 0))
                self.screen.blit(leader1, (255, 75))
            if len(leaderBoard) > 1:
                leader2: pygame.surface = pygame.font.SysFont("Arial", 18, bold=True).render(leaderBoard[1][0] + " " + str(leaderBoard[1][1][0]), True, (0, 0, 0))
                self.screen.blit(leader2, (255, 95))
            if len(leaderBoard) > 2:
                leader3: pygame.surface = pygame.font.SysFont("Arial", 18, bold=True).render(leaderBoard[2][0] + " " + str(leaderBoard[2][1][0]), True, (0, 0, 0))
                self.screen.blit(leader3, (255, 115))


            """
            seconds = round(self.gameTime * gameSpeed)
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            """
            seconds = (pygame.time.get_ticks() - self.gameTime) / 1000
            seconds = gameTimeMin*60 - seconds
            seconds = round(seconds)
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            if self.gameMod == 2:
                #if round(seconds) % 2 == 0:
                    #entities.balls.append(Ball(Vector(random.randint(10, 440), 250), self.screen, vector.random_vector() * 300))
                self.game2()




            time = "%02d:%02d" % (minutes, seconds)

            timeBox = pygame.draw.rect(self.screen, (0, 162, 232), (172, 150, 80, 40), 0)
            surf = pygame.Surface((timeBox.w * 0 , timeBox.h *0 ))
            self.screen.blit(surf, (170, 140))


            time: pygame.surface = pygame.font.SysFont("Arial", 30, bold=True).render(time, True, (0, 0, 0))
            self.screen.blit(time, (180, 150))
            #print(str(minutes) + ":" + str(seconds.))
            # Get events
            events: List[pygame.event] = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()
                    return

            # Enumerate through & display data
            if self.gameMod == 1:
                for idx, comment in enumerate(self.active):
                    y: int = int(self.height - (15 + ((idx + 1) * 40)))
                    if y > 0:
                        #comment.blit(self.screen, 20, y)
                        comment.findEnemy()
                        comment.blit(self.screen, comment.xpos, comment.ypos)



            # Pop from the queue
            if len(self.queue) > 0 or len(self.queue2) > 0 or len(self.queue3) > 0 or len(self.queue4) > 0 or len(self.queue5) > 0:
                self.loop.create_task(self.__pop_queue())

            # Cap active at 50 items
            #self.active = self.active[:50]
            for c in self.active:
                if c.health < 1:
                    self.active.remove(c)
                    enemyList.remove(c)
            #self.gameTime -= 1



            #print(self.gameTime)

            pygame.display.update()
            if gameTimeMin * 60 - ((pygame.time.get_ticks() - self.gameTime) / 1000) < 1:
                if len(gameType) == self.gameMod:
                    self.gameMod = 1
                else:
                    self.gameMod += 1
                self.cleanQue()
                print(self.gameMod)
                self.gameTime = pygame.time.get_ticks()



            await asyncio.sleep(gameSpeed)

    def cleanQue(self):
        self.queue.clear()
        self.queue2.clear()
        self.queue3.clear()
        self.queue4.clear()
        self.queue5.clear()
        self.active.clear()
        enemyList.clear()
        entities.balls.clear()
        leaderBoard.clear()

    # game2
    def update(self):
        entities.update_balls()
        entities.update_ops(ballsOpsList)

    def draw(self):
        #ball_default = pygame.image.load("data/ball.png.png")
        entities.draw_balls()
        for e in ballsOpsList:
            e.draw()

    def game2(self):
        self.update()
        self.draw()



def streamBox():
    pygame.init()
    textinput = pygame_textinput.TextInputVisualizer()

    screen = pygame.display.set_mode((1000, 200))
    clock = pygame.time.Clock()

    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()

        # Feed it with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        screen.blit(textinput.surface, (10, 10))

        for event in events:
            if event.type == pygame.QUIT:
                return textinput

        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':
    """
    This example requires the following ADDITIONAL packages to run:
    => Pillow, Pygame

    """
    print("start")
    #stream = streamBox()
    #steamName = "@"+str(stream.value)
    loop: AbstractEventLoop = asyncio.get_event_loop()
    client: TikTokLiveClient = TikTokLiveClient("@chat_play_games", loop=loop)
    client.add_listener('comment', lambda event: display.queue.append(event))
    client.add_listener('gift', lambda event: display.queue2.append(event))
    client.add_listener('like', lambda event: display.queue3.append(event))
    client.add_listener('follow', lambda event: display.queue4.append(event))
    client.add_listener('share', lambda event: display.queue5.append(event))
    client.add_listener('connect', lambda event: print('Connected!'))
    display: DisplayCase = DisplayCase(loop)
    #display.gameTime = (gameTimeMin / gameSpeed) * 60
    display.gameTime = pygame.time.get_ticks()
    loop.create_task(client.start())
    loop.run_until_complete(display.start())


@client.on("gift")
async def on_gift(event: GiftEvent):
    """
    This is an example for the "gift" event to show you how to read gift data properly.

    Important Note:

    Gifts of type 1 can have streaks, so we need to check that the streak has ended
    If the gift type isn't 1, it can't repeat. Therefore, we can go straight to printing

    """

    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")


@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("comment")
async def on_comment(_: CommentEvent):
    print("comment")





