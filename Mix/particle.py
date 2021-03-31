import pygame, random

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255, 255, 255)
black = (0, 0, 0)

class Particle:
    def __init__(self):
        self.particles = []
    
    def emit(self, surface):
        self.remove_particle()
        if self.particles:
            for particle in self.particles:
                # direction
                particle[0][0] += particle[2][0]
                particle[0][1] += particle[2][1]
                # size
                particle[1] += 0.05
                particle[1] -= 0.1
                # gravity
                particle[2][1] += 0.05
                pygame.draw.circle(surface, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[1]))

    def add_particle(self, xy=None, rad=None, direct=None):
        if not xy:
            mouse_pos = pygame.mouse.get_pos()
            pos = [mouse_pos[0], mouse_pos[1]]
        else:
            pos = xy

        if rad:
            radius = random.randint(rad[0], rad[1])
        else:
            radius = random.randint(3, 7)

        if direct:
            direction = direct
        else:
            direction = [random.randint(0, 20) / 10 - 1, -2]

        color = random.choice([red, green, blue, white, black])

        # Make Particle
        particle = [pos, radius, direction, color]
        self.particles.append(particle)

    def remove_particle(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

    def handle_click(self, mouse):
        if mouse[0]:
            self.add_particle()

