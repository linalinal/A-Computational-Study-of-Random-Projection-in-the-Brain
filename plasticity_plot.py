import brain
import random
import matplotlib.pyplot as plt

# Configurable Constants
n = 10000 # The number of neurons per brain area
k = 100 # the assemblie size or group of neurons in the model

Seed =1

# the different plasticity parameters
parameters =[0,0.001,0.003,0.007,0.015,0.031,0.063,0.127,0.255,0.511]
for i in range(len(parameters)):
    Brain = brain.Brain(seed=Seed,
                             num_brain_areas=1,
                             neurons_per_area=n,
                             vertice_probability=0.01,
                             assemblie_size=k,
                             area_vertice_probability=1,
                             plasticity=parameters[i])

    brain_areas = Brain.brain_areas
    Area = random.choice(list(brain_areas))

    #create the stimulus
    Stimulus = []
    for ii in range(k):
        while True:
            neuron = random.choice(list(Area.neurons))
            if neuron not in Stimulus:
                Stimulus.append(neuron)
                break
    Area.assemblie_fire_custom(Stimulus)

    #support is the set of all the neurons that have fired due to the stimulus
    suport = set()
    plot =[]
    plot.append(len(suport))

    for iii in range(100):
        for a in Brain.brain_areas:
            k_cap = a.make_k_cap(k)
            Area.assemblie_fire_custom(list(set(Stimulus).union(set(k_cap))))
        suport.update(k_cap)
        plot.append(len(suport))


    plt.xlabel('#iterations')
    plt.ylabel('total support')
    plt.plot(range(101), plot, '-', label=str(parameters[i]))

plt.legend()
plt.show()
