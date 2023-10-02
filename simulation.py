import pygame
import random
import brain
import math
import time

class simulation:
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    firsttime = True
    # Display settings
    WIDTH, HEIGHT = 600, 600

    def __init__(self, Brain):
        """Initialize the simulation with a Brain instance."""
        self.Brain = Brain
        self.iteration = 0
        self.total_fired_neurons = set()

    def initially(self):
        """Initialize the positions and colors of brain areas."""
        i = 0
        n = int(round(math.sqrt(self.Brain.num_brain_areas)))
        width_per_area = self.WIDTH // n
        height_per_area = self.HEIGHT // n
        for area in self.Brain.brain_areas:
            area.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            area.position_x_upper = int((i % n) * width_per_area)
            area.position_x_lower = int((((i) % n + 1)) * width_per_area) - 1
            area.position_y_upper = int((i // n) * height_per_area)
            area.position_y_lower = int(((i // n) + 1) * height_per_area) - 1
            i += 1

    def run_simulation(self):

        """Run the simulation, visualizing the brain areas, neurons, and their connections."""
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Brain Simulation")

        running = True
        screen.fill(self.WHITE)

        font = pygame.font.SysFont('arial', 18)

        # Initialize the positions of neurons within their respective brain areas
        for area in self.Brain.brain_areas:
            for neuron in area.neurons:
                neuron.x_pos = random.randint(area.position_x_upper, area.position_x_lower)
                neuron.y_pos = random.randint(area.position_y_upper, area.position_y_lower)
                pygame.draw.circle(screen, area.color, (neuron.x_pos, neuron.y_pos), 2)  # Made the dots a bit bigger


        start_time = time.time()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(self.WHITE)

            if(self.firsttime):
                for area in self.Brain.brain_areas:
                    for neuron in area.neurons:
                        for connection in neuron.connections:
                            thickness = min(15, max(1, int(connection.weight * 2.1)))  # Scale thickness with weight
                            pygame.draw.line(screen, (
                            min(255, int(connection.weight * 40)), 230 - min(230, int(connection.weight * 50)),
                            200 - min(200, int(connection.weight * 20))),
                                             (neuron.x_pos, neuron.y_pos),
                                             (connection.neuronB.x_pos, connection.neuronB.y_pos), thickness)

            # Draw neurons and represent their firing state with color and size
            for area in self.Brain.brain_areas:
                for neuron in area.neurons:
                    color = self.RED if neuron.firing else area.color
                    radius = 5 if neuron.firing else 2  # Made the dots a bit bigger
                    pygame.draw.circle(screen, color, (neuron.x_pos, neuron.y_pos), radius)
                    pygame.draw.circle(screen, self.BLACK, (neuron.x_pos, neuron.y_pos), radius, 1)  # Added shadow

            # Draw updated connections on top
            for area in self.Brain.brain_areas:
                for neuron in area.neurons:
                    if neuron.firing:
                        for connection in neuron.connections:
                            thickness = min(15, max(1, int(connection.weight * 2.1)))  # Scale thickness with weight
                            pygame.draw.line(screen, (min(255, int(connection.weight * 40)), 255 - min(255, int(connection.weight * 50)),
                            255 - min(255, int(connection.weight * 20))),
                            (neuron.x_pos, neuron.y_pos),
                            (connection.neuronB.x_pos, connection.neuronB.y_pos), thickness)

            # Display dynamic information
            elapsed_time = time.time() - start_time
            info_texts = [
                f'Iteration: {self.iteration}',
                f'Total Activated Neurons: {len(self.total_fired_neurons)}',
                f'Number of Brain Areas: {len(self.Brain.brain_areas)}',
                f'Number of Neurons: {len(self.Brain.brain_areas) * self.Brain.neurons_per_area}',
                f'Assemblie Size: {Brain.assemblie_size}',
                f'Elapsed Time: {elapsed_time:.2f} seconds',
                f'Plasticity: {Brain.plasticity}'
            ]
            y_pos = 10
            info_box_height = len(info_texts) * 20 + 20  # Calculate the height of the info box
            pygame.draw.rect(screen, self.WHITE, (5, 5, 250, info_box_height))  # Filled white rectangle
            pygame.draw.rect(screen, self.BLACK, (5, 5, 250, info_box_height), 2)  # Black border
            for info_text in info_texts:
                rendered_text = font.render(info_text, True, self.BLACK)
                screen.blit(rendered_text, (10, y_pos))
                y_pos += 20

            pygame.display.flip()
            #feel free to change the timesteps
            pygame.time.wait(200)  # Delay for visualization

            # Fire the assemblies and update the state of neurons and connections
            #Brain.fire_whole_brain()
            area.assemblie_fire()
            for neuron in area.neurons:
                if neuron.firing:
                    self.total_fired_neurons.add(neuron)

            self.iteration += 1

        pygame.quit()


# Initialize Simulation
# Feel free to change the values for different observations
pygame.init()
Brain = brain.Brain(seed=52,
                    num_brain_areas=(1 * 1),
                    neurons_per_area=60,
                    vertice_probability=0.05,
                    assemblie_size=6,
                    plasticity=0.3,
                    area_vertice_probability=0.3
                    )
sim = simulation(Brain)
sim.initially()
sim.run_simulation()
