import pygame
import random

pygame.init()

fps = 75
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))


class Planet:
    def __init__(self, name, x, y, velocity, radius, mass, color, being_placed):
        self.name = name
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.being_placed = being_placed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def gravity(self, planets):
        if self.being_placed == False:
            G = 6.67408 * 10 ** -2
            for planet in planets:
                if planet != self:
                    distance = ((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2) ** 0.5
                    self.velocity.x += G * (planet.x - self.x) * planet.mass / self.mass / distance ** 2
                    self.velocity.y += G * (planet.y - self.y) * planet.mass / self.mass / distance ** 2

mass = 5.0

planets = []

running = True

while running:
    clock.tick(fps)
    print(clock.get_fps())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            planets.append(Planet("Planet", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pygame.math.Vector2(0, 0), 10, mass, (0, 25, 255), True))
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            planets[-1].velocity = pygame.math.Vector2((planets[-1].x - pygame.mouse.get_pos()[0]) / 50, (planets[-1].y - pygame.mouse.get_pos()[1]) / 50)
            planets[-1].being_placed = False


    screen.fill((0, 0, 0))

    for planet in planets:
        planet.gravity(planets)
        planet.move()
        planet.draw(screen)
        

    pygame.display.update()
