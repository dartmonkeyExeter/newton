import pygame
import random
from copy import deepcopy

pygame.init()

fps = 75
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Newton's Law of Universal Gravitation Simulator")

color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255,255,0), (0,255,255), (255,0,255), (255,255,255)]
mass = 5
color = (255, 255, 255)
size = 10

class Grid:
    def __init__(self):
        self.init_vertices = []
        self.vertices = []
        self.color = (25, 25, 25)
        for i in range(0, 801, 40):
            for j in range(0, 801, 40):
                self.vertices.append([i, j])
                self.init_vertices.append([i, j])

    def draw(self, screen):
        for vertex in self.vertices:
            pygame.draw.circle(screen, self.color, vertex, 2)
        for i in range(21):
            for j in range(21 - 1):
                point1 = self.vertices[i + (j * 21)]
                point2 = self.vertices[i + ((j + 1) * 21)]
                pygame.draw.line(screen, self.color, point1, point2, 1)
        for i in range(21 - 1):
            for j in range(21):
                point1 = self.vertices[i + 1 + (j * 21)]
                point2 = self.vertices[i + (j * 21)]
                pygame.draw.line(screen, self.color, point1, point2, 1)
        
        

    def distort(self, planets):
    # vertices attempt to move back to the original position slowly
        for vertex in self.vertices:
            vertex[0] += (self.init_vertices[self.vertices.index(vertex)][0] - vertex[0]) / 50
            vertex[1] += (self.init_vertices[self.vertices.index(vertex)][1] - vertex[1]) / 50

        for vertex in self.vertices:
            for planet in planets:
                distance = ((vertex[0] - planet.x) ** 2 + (vertex[1] - planet.y) ** 2) ** 0.5
                distance_from_original_pos = ((vertex[0] - self.init_vertices[self.vertices.index(vertex)][0]) ** 2 + (vertex[1] - self.init_vertices[self.vertices.index(vertex)][1]) ** 2) ** 0.5
                if distance <= 10 * planet.mass and distance_from_original_pos <= 10 * planet.mass:
                    # Calculate the force of attraction
                    force = 0.5 * planet.mass  # Adjust the constant as needed

                    # Limit the distance to prevent excessive attraction
                    min_distance = 20.0
                    if distance < min_distance:
                        distance = min_distance

                    # Update vertex coordinates based on the force
                    vertex[0] -= (force * (vertex[0] - planet.x)) / (distance ** 2)
                    vertex[1] -= (force * (vertex[1] - planet.y)) / (distance ** 2)

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
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 1)
    
    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def gravity(self, planets):
        if self.being_placed == False:
            G = 6.67408 * 10 ** -2
            for planet in planets:
                distance = ((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2) ** 0.5
                if planet != self and planet.being_placed == False and self.being_placed == False and self.mass >= planet.mass:
                    self.velocity.x += G * (planet.x - self.x) * self.mass / planet.mass / distance ** 2
                    self.velocity.y += G * (planet.y - self.y) * self.mass / planet.mass / distance ** 2
                elif planet != self and planet.being_placed == False and self.being_placed == False and self.mass < planet.mass:
                    self.velocity.x += G * (planet.x - self.x) * self.mass * planet.mass / distance ** 2
                    self.velocity.y += G * (planet.y - self.y) * self.mass * planet.mass / distance ** 2

    def init_trajectory(self, planets):
        G = 6.67408 * 10 ** -2
        parts_to_draw = 250

        line_positions = []

        temp_x = self.x
        temp_y = self.y

        temp_velocity = pygame.math.Vector2((self.x - pygame.mouse.get_pos()[0]) / 50, (self.y - pygame.mouse.get_pos()[1]) / 50)

        for i in range(parts_to_draw):
            for planet in planets:
                distance = ((temp_x - planet.x) ** 2 + (temp_y - planet.y) ** 2) ** 0.5
                if planet != self and planet.being_placed == False and self.being_placed == True and self.mass >= planet.mass:
                    temp_velocity.x += G * (planet.x - temp_x) * (self.mass / planet.mass) / distance ** 2
                    temp_velocity.y += G * (planet.y - temp_y) * (self.mass / planet.mass) / distance ** 2
                elif planet != self and planet.being_placed == False and self.being_placed == True and self.mass < planet.mass:
                    temp_velocity.x += G * (planet.x - temp_x) * (self.mass * planet.mass) / distance ** 2
                    temp_velocity.y += G * (planet.y - temp_y) * (self.mass * planet.mass) / distance ** 2

            temp_x += temp_velocity.x
            temp_y += temp_velocity.y

            line_positions.append(pygame.math.Vector2(temp_x, temp_y))

        for i in range(len(line_positions) - 1):
            point1 = (line_positions[i].x, line_positions[i].y)
            point2 = (line_positions[i + 1].x, line_positions[i + 1].y)
            pygame.draw.line(screen, (255, 255, 255), point1, point2, 1)

    def update_trajectory(self, planets):
        G = 6.67408 * 10 ** -2
        parts_to_draw = 50

        line_positions = []

        temp_x = self.x
        temp_y = self.y

        temp_velocity = self.velocity

        for i in range(parts_to_draw):
            for planet in planets:
                distance = ((temp_x - planet.x) ** 2 + (temp_y - planet.y) ** 2) ** 0.5
                if planet != self and planet.being_placed == False and self.being_placed == True and self.mass >= planet.mass:
                    temp_velocity.x += G * (planet.x - temp_x) * self.mass / planet.mass / distance ** 2
                    temp_velocity.y += G * (planet.y - temp_y) * self.mass / planet.mass / distance ** 2
                elif planet != self and planet.being_placed == False and self.being_placed == True and self.mass < planet.mass:
                    temp_velocity.x += G * (planet.x - temp_x) * self.mass * planet.mass / distance ** 2
                    temp_velocity.y += G * (planet.y - temp_y) * self.mass * planet.mass / distance ** 2

            temp_x += temp_velocity.x
            temp_y += temp_velocity.y

            line_positions.append(pygame.math.Vector2(temp_x, temp_y))

        for i in range(len(line_positions) - 1):
            point1 = (line_positions[i].x, line_positions[i].y)
            point2 = (line_positions[i + 1].x, line_positions[i + 1].y)
            pygame.draw.line(screen, (255, 255, 255), point1, point2, 1)

    def collision(self, planets):
        for planet in planets:
            if planet != self:
                distance = ((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2) ** 0.5
                if distance <= self.radius + planet.radius:
                    planets.remove(planet)
                    self.radius = self.radius + planet.radius
                    self.mass = self.mass + planet.mass
                    self.color = color_list[(color_list.index(self.color) + color_list.index(planet.color)) % len(color_list)]
                    self.velocity = pygame.math.Vector2((self.velocity.x * self.mass + planet.velocity.x * planet.mass) / self.mass, (self.velocity.y * self.mass + planet.velocity.y * planet.mass) / self.mass)
                    break

class Button:
    def __init__(self, name, x, y, color, font_size, button_size, var):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.button_size = button_size
        self.var = var
        
    def draw(self, screen):
        pygame.draw.rect(screen, color, (self.x, self.y, self.button_size, self.button_size / 2))
        font = pygame.font.SysFont("Arial", self.font_size)
        text = font.render(f"{self.name}: {self.var}", True, (0, 0, 0))
        screen.blit(text, (self.x, self.y))
    

new_grid = Grid()
planets = []

UI_buttons = [Button("Mass", 5, 5, (255, 255, 255), 8, 40, mass), 
              Button("Color", 55, 5, color, 8, 40, color), 
              Button("Size", 105, 5, (255, 255, 255), 8, 40, size)]

running = True

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            planets.append(Planet("Planet", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pygame.math.Vector2(0, 0), size, mass, color, True))
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            planets[-1].velocity = pygame.math.Vector2((planets[-1].x - pygame.mouse.get_pos()[0]) / 50, (planets[-1].y - pygame.mouse.get_pos()[1]) / 50)
            planets[-1].being_placed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            cur_mouse_pos = pygame.mouse.get_pos()
            for planet in planets:
                if planet.x - planet.radius <= cur_mouse_pos[0] <= planet.x + planet.radius and planet.y - planet.radius <= cur_mouse_pos[1] <= planet.y + planet.radius:
                    planets.remove(planet)
                    break
        if event.type == pygame.MOUSEWHEEL and event.y == 1:
            # based on position of buttons, if mouse is over the button, change the mass, color, or size of the planet
            cur_mouse_pos = pygame.mouse.get_pos()

            if 5 <= cur_mouse_pos[0] <= 45 and 5 <= cur_mouse_pos[1] <= 25:
                mass += 1
                UI_buttons[0].var = mass
            elif 55 <= cur_mouse_pos[0] <= 95 and 5 <= cur_mouse_pos[1] <= 25:
                color = color_list[(color_list.index(color) + 1) % len(color_list)]
                UI_buttons[1].var = color
            elif 105 <= cur_mouse_pos[0] <= 145 and 5 <= cur_mouse_pos[1] <= 25:
                size += 1
                UI_buttons[2].var = size
        if event.type == pygame.MOUSEWHEEL and event.y == -1:
            # based on position of buttons, if mouse is over the button, change the mass, color, or size of the planet
            cur_mouse_pos = pygame.mouse.get_pos()

            if 5 <= cur_mouse_pos[0] <= 45 and 5 <= cur_mouse_pos[1] <= 25:
                mass -= 1
                UI_buttons[0].var = mass
            elif 55 <= cur_mouse_pos[0] <= 95 and 5 <= cur_mouse_pos[1] <= 25:
                color = color_list[(color_list.index(color) - 1) % len(color_list)]
                UI_buttons[1].var = color
            elif 105 <= cur_mouse_pos[0] <= 145 and 5 <= cur_mouse_pos[1] <= 25:
                size -= 1
                UI_buttons[2].var = size

    screen.fill((0, 0, 0))
    
    new_grid.distort(planets)
    new_grid.draw(screen)
    

    for planet in planets:
        if planet.being_placed == True:
            planet.init_trajectory(planets)

    for planet in planets:
        if planet.being_placed == False:
            planet.update_trajectory(planets)
        planet.gravity(planets)
        planet.move()
        planet.collision(planets)
        planet.draw(screen)
    
    for button in UI_buttons:
        button.draw(screen)

    pygame.display.update()
