import random
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Patch



def overlap(vec1, vec2):
    """
    A function that takes two lists, vec1 and vec2,
    as its parameters and returns a float representing the proportion
    of elements that are equal at the corresponding indices in the two lists.
    :param vec1: binary vector.
    :param vec2: binary vector.
    :return: float
    """
    count = 0
    for i in range(len(vec1)):
        if (vec1[i] == vec2[i]):
            count += 1
    return count / len(vec1)

def generate_overlapping_vectors(n, a):
    """
    Generates two binary vectors of length n that overlap in a fraction a of their entries.
    :param n: int, Length of the binary vectors.
    :param a: float, Fraction of overlapping entries, should be between 0 and 1.
    :return: tuple, Two binary vectors as lists.
    """
    if a < 0 or a > 1:
        raise ValueError("Overlap fraction 'a' must be between 0 and 1")

    overlap_count = math.floor(int(n * a))  # Calculate the number of overlapping 1s

    vector1 = [random.choice([0, 1]) for _ in range(n)]
    vector2 = vector1.copy()

    entries = set()

    while(len(entries)<(n-overlap_count)):
        entries.add(random.choice(range(0,n)))

    for i in entries:
        vector2[i]=1-vector1[i]


    return [vector1, vector2]


def top_k_indices(input_list, k):
    """
    Returns the indices of the k highest values in the input list.

    :param input_list: list of numbers
    :param k: int, number of top indices to return
    :return: list of indices corresponding to the k highest values in input_list
    """
    if k > len(input_list) or k < 0:
        raise ValueError("k should be between 0 and the length of the input list")

    # Enumerate the input_list to get (index, value) pairs, then sort by value in descending order
    sorted_indices = sorted(range(len(input_list)), key=lambda i: input_list[i], reverse=True)

    # Return the first k indices from the sorted list of indices
    return sorted_indices[:k]


def random_projection(n,k,alpha,sparcity):
    """
    Perform a random projection and calculate the overlap and expected overlap of the resulting graphs.
    Parameters:
    n (int): neurons called Kenyon cells
    k (int): kinds of olfactory receptors
    alpha (float): The fraction of entries where the vectors overlap.
    Returns:
    list: A list containing the input parameters n, k, alpha, the expected overlap, and the actual overlap.
    """
    sparcity=1-sparcity
    vec = generate_overlapping_vectors(50,alpha)
    vec1=vec[0]
    vec2=vec[1]

    #make a graph with configurable sparsity
    bipartite_graph = [[random.choice([0 for _ in range(int(math.floor(sparcity*10)))]+[1 for _ in range(10 - int(math.floor(sparcity*10)))]) for _ in range(n)]for _ in range(50)]
    result_graph1 = [0 for _ in range(n)]
    result_graph2 = [0 for _ in range(n)]

    for i in range(n):
        for j in range(50):
            result_graph1[i]+=vec1[j]*bipartite_graph[j][i]
            result_graph2[i]+=vec2[j]*bipartite_graph[j][i]

    overlapp = len(set(top_k_indices(result_graph1,k)).intersection(set(top_k_indices(result_graph2,k))))/k

    temp = (1-alpha)/(1+alpha)
    expected = (k/n)**temp

    return [n,k,alpha,expected, overlapp]

def make_plot():
    """Makes the Plot"""
    n = 2000
    k = 100
    sparsity = 0.01
    alpha_list = []
    expected_overlap = []
    overlapp = []

    #gather the data for the plot
    for alpha in range(11):
        print(alpha)
        kk =[]
        aa =[]
        ee =[]
        oo =[]
        it=3
        # Calculate the average of three independent trials
        for i in range(it):
            random.seed(i)
            vec = random_projection(n, k, alpha * 0.1, sparsity)
            kk.append(vec[1])
            aa.append(vec[2])
            ee.append(vec[3])
            oo.append(vec[4])
        alpha_list.append(sum(aa)/it)
        expected_overlap.append(sum(ee)/it)
        overlapp.append(sum(oo)/it)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Assuming alpha_list is a list of x values, and expected_overlap and overlapp are y values
    ax.plot(alpha_list, expected_overlap, color='g', label='Theoretical Bound', alpha=0.5)
    ax.plot(alpha_list, overlapp, color='b', label='Empirical Observation', alpha=0.5)

    ax.set_xlabel('alpha')  # Adjust the label as per your requirement
    ax.set_ylabel('Overlap')

    # Display the legend
    ax.legend()

    plt.title('n=' + str(n)+' k='+ str(k)+ ' sparcity='+ str(sparsity))
    plt.show()


make_plot()