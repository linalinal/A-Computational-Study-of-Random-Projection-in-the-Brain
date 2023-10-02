import brain
import random
import math
import matplotlib.pyplot as plt



def compute_expression(n, k, a):
    """
    Computes the theoretical expression provided by Theorem 3.

    :param n: Total number of neurons per area.
    :param k: Size of the assembly.
    :param a: Alpha, representing the fraction of overlapping nodes between two stimuli.
    :return: The computed theoretical overlap value.
    """
    term1 = math.pow(math.log(n/k), a/(1+a))
    term1=1/term1

    term2 = k/n
    term3 = (1-a)/(1+a)

    result = term1 * (term2 ** term3)
    return result

def run_once(n,k,alpha,seed):
    """
    Runs the model once for given parameters and computes the actual and expected overlap.

    :param n: Total number of neurons per area.
    :param k: Size of the assembly.
    :param alpha: Fraction of overlapping nodes between two stimuli.
    :param seed: Seed for random number generator.
    :return: A list containing the actual overlap and the expected overlap.
    """
    random.seed(seed)

    Brain = brain.Brain(seed=seed,
                        num_brain_areas=2,
                        neurons_per_area=n,
                        vertice_probability=0.05,
                        assemblie_size=k,
                        plasticity=0.3,
                        area_vertice_probability=1
                        )

    Area1 = random.choice(list(Brain.brain_areas))
    Area2 = random.choice(list(Brain.brain_areas))

    while (Area2 == Area1):
        Area2 = random.choice(list(Brain.brain_areas))

    stimulus1 = set()
    stimulus2 = set()

    while(len(list(stimulus1))<k):
        stimulus1.add(random.choice(list(Area1.neurons)))

    while(len(list(stimulus2))<alpha*k):
        stimulus2.add(random.choice(list(stimulus1)))

    while(len(list(stimulus2))<k):
        neuron = random.choice(list(Area1.neurons))
        if not neuron in stimulus1:
            stimulus2.add(neuron)

    Area1.assemblie_fire_custom(stimulus1)
    k_cap_stim_1 = Area2.make_k_cap(k)
    Brain.reset()

    Area1.assemblie_fire_custom(stimulus2)
    k_cap_stim_2 = Area2.make_k_cap(k)
    Brain.reset()

    set1 = set(k_cap_stim_2)
    set2 = set(k_cap_stim_1)
    overlap = len(set1.intersection(set2))/(len(set2))
    expected_overlap = compute_expression(n,k,alpha)
    return [overlap, expected_overlap]



def make_plot():
    """
    Generates and plots the theoretical bound and empirical overlap against varying alpha values.
    """
    alpha_values =[]
    expected_overlap =[]
    actual_overlap =[]

    aa=[]
    rr=[]
    ee=[]
    ac=[]

    for a in range(101):
        alpha = a*0.01

        rr = []
        ee = []
        ac = []

        it = 4

        #calculate the average of four independent trials
        for i in range(it):
            random.seed(it)
            run = run_once(2000, 100, alpha, a)
            ee.append(run[1])
            ac.append(run[0])

        alpha_values.append(alpha)
        expected_overlap.append(sum(ee)/it)
        actual_overlap.append(sum(ac)/it)
        print(a)

    # Create a figure and a set of subplots

    fig, ax = plt.subplots()

    # Plotting the first graph on the subplot
    ax.plot(alpha_values, expected_overlap, label='Expected Overlap')

    # Plotting the second graph on the same subplot
    ax.plot(alpha_values, actual_overlap, label='Empirical Overlap')

    # Setting title and labels
    ax.set_title('The expected and empirical overlap of the caps two stimuli\nthat overlap in a fraction alpha of their nodes')
    ax.set_xlabel('Alpha')
    ax.set_ylabel('Overlap of k_cap in downstream area')

    # Adding a legend to differentiate the two lines
    ax.legend()

    # Show the plot
    plt.show()

make_plot()







