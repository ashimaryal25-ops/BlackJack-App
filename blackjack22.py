import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
FPS = 60

canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Game")

font = pygame.font.SysFont(None, 24)  # Initializing font as default system font
clock = pygame.time.Clock()

# ---------------- Card Class ----------------
class Card:
    def __init__(self, number):
        self.fileName = f"assets/Cards/card{number}.png"  # Path to card image
        self.rank = number // 10
        self.suit = number % 10
        self.image = pygame.image.load(self.fileName).convert_alpha()  # Load card image
        self.points = 10 if self.rank >= 10 else self.rank             # Points value for the card, 10 for face cards

    def draw(self, x, y):
        canvas.blit(self.image, (x, y))  # Draw card image at (x, y)

    def getPoints(self):
        return self.points

# ---------------- Deck Class ----------------
class Deck:
    def __init__(self):
        self.cards = []
        for rank in range(1, 14):
            for suit in range(1, 5):
                self.cards.append(Card(rank * 10 + suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            self.__init__()
        return self.cards.pop()

    def draw(self, y):
        x = 50
        for card in self.cards:
            card.draw(x, y)
            x += 10


# ---------------- Player Class ----------------
class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.active = True
        self.last_card = None

    def collectCard(self, card):
        self.last_card = card
        self.points += card.getPoints()   # Update player points when collecting a card

    def stopPlaying(self):
        self.active = False          

    def isActive(self):
        return self.active

    def getPoints(self):
        return self.points

    def draw(self, x, y):
        if self.last_card:
            self.last_card.draw(x, y)
        color = (0, 200, 0) if self.active else (200, 0, 0)       # Green if active, red if not
        text = font.render(f"{self.name}: {self.points}", True, color)    # Renders player name and points
        canvas.blit(text, (x, y + 120))


# ---------------- Button Class----------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.is_pressed = False
        self.press_time = 0
        self.press_duration = 100

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # if left mouse button is clicked within button area
            self.is_pressed = True
            self.press_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.is_pressed:
            if pygame.time.get_ticks() - self.press_time > self.press_duration:
                self.is_pressed = False

    def draw(self):
        color = (255, 255, 0) if self.is_pressed else (200, 200, 200)
        pygame.draw.rect(canvas, color, self.rect)                  # Draws button background
        pygame.draw.rect(canvas, (0, 0, 0), self.rect, 2)           # Draws button border
        text_surf = font.render(self.text, True, (0, 0, 0))        
        canvas.blit(text_surf, (self.rect.x + 15, self.rect.y + 15)) # Draws button text


# ---------------- Casino Class ----------------
class Casino:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.deck.shuffle()
        self.current_player_index = 0

        self.buttons = {
            "hit": Button(50, 500, 100, 40, "Hit"),          #defining button instances as dictionary entries
            "stand": Button(200, 500, 100, 40, "Stand")
        }

    def add_player(self, player):
        self.players.append(player)

    def has_active_players(self):
        return any(player.isActive() for player in self.players)       

    def draw_players(self):
        spacing = WIDTH // len(self.players)
        x = spacing // 2
        y = 50
        for player in self.players:
            player.draw(x, y)
            x += spacing

    def next_player(self):
        if not self.has_active_players():
            return
        self.current_player_index = (self.current_player_index + 1) % len(self.players)  # Moves to next player
        if  self.has_active_players():
            while not self.players[self.current_player_index].isActive():               # Skips inactive players
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def playGame(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                player = self.players[self.current_player_index]

                if player.isActive():
                    if self.buttons["hit"].handle_event(event):          # Handle Hit button click
                        card = self.deck.deal()
                        player.collectCard(card)
                        if player.getPoints() >= 21:                # Check for bust
                            player.stopPlaying()
                        self.next_player()    

                    elif self.buttons["stand"].handle_event(event):          # Handle Stand button click
                        player.stopPlaying()
                        self.next_player()
                        
            
                for button in self.buttons.values():                     # Update button states
                    button.update()

            canvas.fill((0, 128, 0))
            self.deck.draw(HEIGHT // 2)
            self.draw_players()

            for button in self.buttons.values():                    # Draws buttons
                button.draw()

            if not self.has_active_players():                       # If no active players, display Game Over
                text = font.render("Game Over!", True, (255, 0, 0))
                canvas.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 - 40))

            pygame.display.flip()
            clock.tick(FPS)


casino = Casino()
casino.add_player(Player("Michael"))
casino.add_player(Player("Sarah"))
casino.add_player(Player("Charlie"))
casino.add_player(Player("David"))
casino.playGame()
