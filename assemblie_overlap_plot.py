import brain
import random
import math
import matplotlib.pyplot as plt

# Constants
# feel free to change n and k
n = 2000 # The number of neurons per brain area, possibly related to the size of the modeled brain area
k = 100 # Possibly related to the assemblie size or group of neurons in the model

# Lists to store overlap values for different simulations
x=[] # To store stimulus overlap values
y=[] # To store projection overlap values
z=[] # To store assemblie overlap values

# Looping over a range of overlap stimulus values to simulate different scenarios
for ii in range(10,70):

    zz=[] # Temporary list to store assemblie overlap values for each iteration
    yy=[] # Temporary list to store projection overlap values for each iteration
    aa=50 # Number of iterations for each overlap stimulus value, to average out the randomness in the model
    for a in range(aa):

        overlap_stimulus = ii * 0.01 # Calculating overlap stimulus value
        Seed = a # Setting seed value for random number generation to ensure reproducibility
        random.seed(Seed)

        # Creating a Brain object with specified parameters
        # feel free to change tha brain parameters
        Brain = brain.Brain(seed=Seed,
                                 num_brain_areas=2,
                                 neurons_per_area=n,
                                 vertice_probability=0.003,
                                 assemblie_size=k,
                                 area_vertice_probability=1,
                                 plasticity=0.1)

        brain_areas = Brain.brain_areas
        Area1 = random.choice(list(brain_areas))

        while (True):
            Area2 = random.choice(list(brain_areas))
            if(not(Area1 == Area2)):
                break

        Stimulus1 = []
        Stimulus2 = []

        #make Stimulus1
        for i in range(k):
            while True:
                neuron = random.choice(list(Area1.neurons))
                if neuron not in Stimulus1:
                    Stimulus1.append(neuron)
                    break

        #make Stimulus2 with the desired overlap
        for i in range(math.floor(k*overlap_stimulus)):
            while True:
                neuron = random.choice(Stimulus1)
                if neuron not in Stimulus2:
                    Stimulus2.append(neuron)
                    break

        for i in range(k-math.floor(k*overlap_stimulus)):
            while True:
                neuron = random.choice(list(Area1.neurons))
                if neuron not in Stimulus1 and neuron not in Stimulus2:
                    Stimulus2.append(neuron)
                    break

        #make the projection of Stimulus1
        Area1.assemblie_fire_custom(Stimulus1)
        k_caps1 = Area2.make_k_cap(k)
        k_caps11 = Area1.make_k_cap(k)


        Brain.reset()

        #make the projection of Stimulus2
        Area1.assemblie_fire_custom(Stimulus2)
        k_caps2 =[]
        k_caps2 = Area2.make_k_cap(k)
        k_caps22 = Area1.make_k_cap(k)


        Brain.reset()

        #append the overlap of the projection to the temporary list
        yy.append(len(set(k_caps1).intersection(set(k_caps2)))/len( k_caps1))

        #temporary parameters
        sett = set()
        l0=0
        lenn=1
        count=0
        p1=[]
        q1=[]

        # Create the assemblies for Stimulus1 for both brain Areas and I see the assemblies as completed if
        # over the turn of 8 iteration there hasn't been any new time winner
        while(l0 < lenn and count < 8):
            l0 = len(sett)
            Area1.assemblie_fire_custom(Stimulus1)
            p1 = Area1.assemblie_fire()
            q1 = Area2.assemblie_fire()

            for i in p1:
                sett.add(i)
            for i in q1:
                sett.add(i)
            lenn = len(sett)
            if(l0 == lenn):
                count+=1

        Brain.reset()

        #temporary Parameters
        sett = set()
        l0 = 0
        lenn = 1
        count=0
        p2 = []
        q2 = []

        # Create the assemblies for Stimulus2 for both brain Areas and I see the assemblies as completed if
        # over the turn of 8 iteration there hasn't been any new time winner
        while (l0 < lenn and count < 8):
            l0 = len(sett)
            Area1.assemblie_fire_custom(Stimulus2)
            p2 = Area1.assemblie_fire()
            q2 = Area2.assemblie_fire()
            for i in p2:
                sett.add(i)
            for i in q2:
                sett.add(i)
            lenn = len(sett)
            if (l0 == lenn):
                count += 1

        #append the overlap of the assemblies to the temporary list
        zz.append(len(set(p1).intersection(set(p2)))/((len( p1)+len(p2))/2))

        #reset the weights of the connections and the incoming fires of the neurons
        Brain.reset()

    x.append(overlap_stimulus)

    #compute the average of the iterations
    z.append(sum(zz)/aa)
    y.append(sum(yy)/aa)


plt.xlabel('Stimulus Overlap')
plt.ylabel('Projection Overlap')


# Theoretical and Conjectured Bound Functions
# These functions  relate to the theoretical and conjectured bounds discussed in the paper, providing a way to compare the model outputs with the expected bounds
def theoretical_bound(x):
    temp = (1-x)/(1+x)
    temp = (k/n)**temp
    temp2 = x/(1+x)
    temp2 = math.log(n/k)**temp2
    return temp/temp2

def conjectured_bound(x):
    temp = (1-x)/(1+x)
    temp = (k/n)**temp
    return temp

# Compute y-values for the function over a range of x-values
theoretical_values = [theoretical_bound(i) for i in x]
conjectured_values = [conjectured_bound(i) for i in x]

# Plot the function
plt.plot(x, z, '-', label='assemblie overlap')
plt.plot(x, y,'-', label='projection overlap')
plt.plot(x, conjectured_values, '-', label='conjectured bound')
plt.plot(x, theoretical_values, '-', label='theoretical bound')
plt.legend()
plt.show()