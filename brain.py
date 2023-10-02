import math
import random
import logging
import time

logging.basicConfig(level=logging.INFO)


class Brain:
    def __init__(self, seed, num_brain_areas, neurons_per_area, vertice_probability, plasticity, assemblie_size,area_vertice_probability):
        """
        Initialize the Brain model with given parameters.

        :param seed: Seed for random number generator.
        :param num_brain_areas: Number of brain areas in the model.
        :param neurons_per_area: Number of neurons in each brain area.
        :param vertice_probability: Probability of creating connections between neurons and brain areas.
        :param plasticity: The plasticity factor affecting the connection weights.
        :param assemblie_size: Size of the neuron assemblies.
        :param area_vertice_probability: Probability that two areas are neighbouring and therefore connected

        """
        random.seed(seed)
        self.seed = seed
        self.num_brain_areas = num_brain_areas
        self.neurons_per_area = neurons_per_area
        self.vertice_probability = vertice_probability
        self.plasticity = plasticity
        self.assemblie_size = assemblie_size
        self.brain_areas = set()
        self.area_vertice_probability=area_vertice_probability

        self._create_brain_areas()
        self._create_area_connections()
        self._create_neuronal_connections()

    def _create_brain_areas(self):
        """Create brain areas based on the specified number of brain areas."""
        for i in range(self.num_brain_areas):
            self.brain_areas.add(
                BrainArea(i, self.vertice_probability, self.plasticity, self.neurons_per_area, self.assemblie_size))
        logging.info("Brain areas created.")

    def _create_area_connections(self):
        """Create connections between neighbouring brain areas."""
        for area_a in self.brain_areas:
            for area_b in self.brain_areas:
                if area_a != area_b and random.random() < self.area_vertice_probability:
                    area_a.neighbouring_areas.add(area_b)
        logging.info("Connections between brain areas created.")

    def _create_neuronal_connections(self):
        """Create neuronal connections between neurons in neighbouring areas."""
        for area in self.brain_areas:
            for neighbour_area in area.neighbouring_areas:
                for neuron_a in area.neurons:
                    for neuron_b in neighbour_area.neurons:
                        if random.random() < self.vertice_probability:
                            weight = 1 + random.random() * 0.5
                            connection = Connection(neuron_a, neuron_b, weight, self.plasticity)
                            area.connections.add(connection)
                            neuron_a.connections.add(connection)
        logging.info("Neuronal connections created.")

    def reset(self):

        # Reset the firing states and incoming fire count of all neurons in every brain area

        for area in self.brain_areas: # Iterate over all brain areas
            area.fired_neurons= set()
            for neuron in area.neurons: # Iterate over all neurons in the current brain area
                neuron.firing = False  # Reset the firing state of the neuron
                neuron.firing_prev = False  # Reset the previous firing state of the neuron
                neuron.incoming_fire = 0  # Reset the incoming fire count of the neuron

        # Reset the weights of all connections of all neurons in every brain area to their initial weights

        for area in self.brain_areas:  # Iterate over all brain areas
            for neuron in area.neurons:  # Iterate over all neurons in the current brain area
                for connection in neuron.connections:  # Iterate over all connections of the current neuron
                    connection.weight = connection.initial_weight  # Reset the weight of the connection to its initial weight

    def fire_brain_repeatedly(self, iterations):
        """
        Fires the whole brain repeatedly every second and logs the statistics.

        :param iterations: Number of times to fire the whole brain.
        """
        for _ in range(iterations):
            self.fire_whole_brain()
            self.log_brain_stats()
            time.sleep(1)  # Pause for one second between iterations

    def fire_whole_brain(self):
        """Simulate the firing of neurons in the whole brain."""
        all_k_caps = [area.make_k_cap(self.assemblie_size) for area in self.brain_areas]

        # Update the firing and firing_prev flags for each neuron in each area
        for area in self.brain_areas:
            area.reset_neurons_firing_state()

        # Fire all neurons in k_caps and update the connections' weights
        for k_cap in all_k_caps:
            for neuron in k_cap:
                neuron.fire()

        for area in self.brain_areas:
            area.update_connections_weight()

        # Fade the connections that have not been succsessful in firing neurons
        self.fade_connections()

        logging.info("Whole brain fired.")

    def log_brain_stats(self):
        """Logs the statistics of the brain, including the percentage of fired neurons in each area."""
        for area in self.brain_areas:
            total_neurons = len(area.neurons)
            fired_neurons = len(area.fired_neurons)
            fired_percentage = (fired_neurons / total_neurons) * 100
            logging.info(
                f"Brain Area {area.ID}: {fired_percentage:.2f}% neurons fired. Total Neurons: {total_neurons}, Fired Neurons: {fired_neurons}")

    def fade_connections(self):
        """fades the connections that have been activated but did not lead
        to the succsessful firing of the connected neuron"""
        for area in self.brain_areas:
            for neuron in area.neurons:
                for connection in neuron.connections:
                    if connection.neuronA.firing_prev and not connection.neuronB.firing:
                        connection.weight= math.max(1,connection.weight/(1+self.plasticity))

        pass


class BrainArea:
    def __init__(self, ID, vertice_probability, plasticity, neurons_per_area, assemblie_size):
        """
        Initialize a BrainArea with given parameters.

        :param ID: Identifier for the brain area.
        :param vertice_probability: Probability of creating connections between neurons.
        :param plasticity: The plasticity factor affecting the connection weights.
        :param neurons_per_area: Number of neurons in the brain area.
        :param assemblie_size: Size of the neuron assemblies.
        """
        self.ID = ID
        self.vertice_probability = vertice_probability
        self.plasticity = plasticity
        self.neurons_per_area = neurons_per_area
        self.neurons = {Neuron(self.ID, i) for i in range(self.neurons_per_area)}
        self.neighbouring_areas = set()
        self.connections = set()
        self.assemblie_size = assemblie_size
        self._create_internal_connections()

        # Set to keep track of neurons that have fired
        self.fired_neurons = set()

    def _create_internal_connections(self):
        """Create connections between neurons within the brain area."""
        for neuron_a in self.neurons:
            for neuron_b in self.neurons:
                if random.random() < self.vertice_probability and not(neuron_b==neuron_a):
                    weight = 1 + random.random()*0.5
                    connection = Connection(neuron_a, neuron_b, weight, self.plasticity)
                    self.connections.add(connection)
                    neuron_a.connections.add(connection)
        logging.info(f"Internal connections in brain area {self.ID} created.")

    def assemblie_fire(self):
        """
        This method simulates the firing of a neuron assembly within the brain area.

        1. It first creates a k-cap assembly of neurons based on their incoming fire.
        2. Then, it resets the firing state of all neurons in the brain area.
        3. After that, it fires all neurons in the k-cap assembly.
        4. Finally, it updates the weight of all connections in the brain area based on the firing state of connected neurons.

        :return: k_cap: list of Neuron objects representing the neurons in the k-cap assembly that have been fired.
        """

        # Create a k-cap assembly of neurons based on their incoming fire
        k_cap = self.make_k_cap(self.assemblie_size)

        # Reset the firing state and incoming fire of all neurons in the brain area
        for neuron in self.neurons:
            if neuron.firing_prev:
                neuron.firing_prev = False
            if neuron.firing:
                neuron.firing = False
                neuron.firing_prev = True
            neuron.incoming_fire = 0

        # Fire all neurons in the k-cap assembly
        for neuron in k_cap:
            neuron.fire()

        # Update the weight of all connections in the brain area
        for neuron in self.neurons:
            for connection in neuron.connections:
                connection.update_weight()

        # Return the k-cap assembly of neurons that have been fired
        return k_cap

    def assemblie_fire_custom(self, list):
        """
        This method simulates the firing of an assembly of neurons and updates the state
        and synaptic weights of the neurons in the assembly.

        Parameters:
        list (List[Neuron]): A list of Neuron objects representing the neurons in the assembly
                             that are to be fired.

        Returns:
        List[Neuron]: Returns the list of Neuron objects that were fired.

        Note:
        - The Neuron object should have attributes: firing, firing_prev, incoming_fire, and connections.
        - The Connection object, part of Neuron's connections, should have a method update_weight to update its weight.
        """

        # Reset the firing states of all neurons in the assembly
        for neuron in self.neurons:
            if neuron.firing_prev:
                neuron.firing_prev = False  # Reset the previous firing state
            if neuron.firing:
                neuron.firing = False  # Reset the current firing state
                neuron.firing_prev = True  # Set the previous firing state as True since the neuron was firing
            neuron.incoming_fire = 0  # Reset the incoming fire count

        # Fire the neurons in the provided list
        for neuron in list:
            neuron.fire()  # The fire method should handle the logic of a neuron firing

        # Update the synaptic weights of the connections of all neurons in the assembly
        for neuron in self.neurons:
            for connection in neuron.connections:
                connection.update_weight()  # Update the weight of each connection

        # Return the list of neurons that were fired
        return list

    def make_k_cap(self, assemblie_size):
        """Create a k-cap assembly of neurons based on their incoming fire."""
        sorted_neurons = sorted(self.neurons, key=lambda neuron: neuron.incoming_fire, reverse=True)
        return sorted_neurons[:assemblie_size]

    def reset_neurons_firing_state(self):
        """Reset the firing state of all neurons in the brain area."""
        for neuron in self.neurons:
            neuron.reset_firing_state()

    def update_connections_weight(self):
        """Update the weight of all connections in the brain area."""
        for connection in self.connections:
            connection.update_weight()
            if connection.neuronA.firing_prev:
                self.fired_neurons.add(connection.neuronA)
            if connection.neuronB.firing:
                self.fired_neurons.add(connection.neuronB)


class Neuron:
    def __init__(self, brain_area_ID, neuron_ID):
        """
        Initialize a Neuron with given parameters.

        :param brain_area_ID: Identifier for the brain area to which the neuron belongs.
        :param neuron_ID: Identifier for the neuron within the brain area.
        """
        self.brain_area_ID = brain_area_ID
        self.neuron_ID = neuron_ID
        self.connections = set()
        self.firing = False
        self.firing_prev = False
        self.incoming_fire = 0

    def fire(self):
        """Set the neuron to firing state and propagate the fire to connected neurons."""
        #print("FIRES"+str(self.neuron_ID))
        self.firing = True
        for connection in self.connections:
            #print("connected to "+ str(connection.neuronB.neuron_ID)+"with connectionweight"+str(connection.weight))
            connection.neuronB.incoming_fire += connection.weight

    def reset_firing_state(self):
        """Reset the firing and previous firing state of the neuron."""
        if self.firing_prev:
            self.firing_prev = False  # Reset the previous firing state
        if self.firing:
            self.firing = False  # Reset the current firing state
            self.firing_prev = True  # Set the previous firing state as True since the neuron was firing
        self.incoming_fire = 0  # Reset the incoming fire count


class Connection:
    def __init__(self, neuronA, neuronB, weight, plasticity):
        """
        Initialize a Connection with given parameters.

        :param neuronA: The starting neuron of the connection.
        :param neuronB: The ending neuron of the connection.
        :param weight: The weight of the connection.
        :param plasticity: The plasticity factor affecting the connection weight.
        """
        self.neuronA = neuronA
        self.neuronB = neuronB
        self.weight = weight
        self.initial_weight = weight
        self.plasticity = plasticity

    def update_weight(self):
        """Update the weight of the connection based on the firing state of connected neurons."""
        if self.neuronA.firing_prev and self.neuronB.firing:
            self.weight *= (1 + self.plasticity)