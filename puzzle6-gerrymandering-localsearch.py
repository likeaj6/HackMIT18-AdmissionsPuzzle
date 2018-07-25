exp_num_dists = 10
imbalance = 150*(10**10)
eff_gap = -0.105
n = 10
D = 20


# In[109]:


import math
import pandas as pd

def highlight_cells(x):
    df = x.copy()
    #set default color
    #df.loc[:,:] = 'background-color: papayawhip'
    df.loc[:,:] = ''
    #set particular cell colors
    df.iloc[0,0] = 'background-color: red'
    df.iloc[1,1] = 'background-color: orange'
    df.iloc[2,2] = 'background-color: yellow'
    df.iloc[3,3] = 'background-color: lightgreen'
    df.iloc[4,4] = 'background-color: cyan'
    df.iloc[5,5] = 'background-color: violet'
    return df

def visualize_districts(dists):
    dist_graph = []
    for k, v in dists.items():
        dist_graph.append(v)
    dist_matrix = []
    for i in range(n):
        dist_matrix.append([])
        for j in range(n):
            dist_matrix[i].append('@')
    for index, district in enumerate(dist_graph):
        for block in district:
            x, y = get_coordinates(block, n)
            dist_matrix[x][y] = index
    df = pd.DataFrame(dist_matrix, columns=list(range(n)))
    df.style.applymap(highlight_cells, axis = None)
    print(df)
def get_neighbors(dist_coord):
    x, y = dist_coord
#     return (x-1)*n + y, (x+1)*n + y, (x*n)+y+1, x*n + (y-1)
    return (x-1, y), (x+1, y), (x, y+1), (x,y-1)
def get_coordinates(block, n):
    return (math.floor(block/n), block%n)

# In[6]:


# setup/import data
import json
from pprint import pprint
with open('p6/voters.json') as data_file:
    data_item = json.load(data_file)

voters_a = data_item['voters_by_block']['party_A']
voters_b = data_item['voters_by_block']['party_B']
blocks_pop = [a + b for a, b in zip(voters_a, voters_b)]

blocks = {}
blocks_assigned = {}
for i in range(n):
    blocks[i] = {}
    blocks_assigned[i] = {}
for i in range(100):
    block = voters_a[i], voters_b[i]
    x, y = get_coordinates(i, n)
    blocks[x][y] = block
    blocks_assigned[x][y] = False



# In[70]:


# dists will be an array of labels i.e 10, or the block at (1, 0)
def get_block_vote_split(block):
    x, y = get_coordinates(block, n)
    a, b = blocks[x][y]
    return a, b
def get_block_pop(block):
    a, b = get_block_vote_split(block)
    return a + b
def get_dist_vote_split(dist):
    blocks_split = [get_block_vote_split(block) for block in dist]
    a = sum([block[0] for block in blocks_split])
    b = sum([block[1] for block in blocks_split])
    return a, b
def dist_population(dist):
    a, b = get_dist_vote_split(dist)
    return a + b
def mean_dist_pop(dists):
    mean = sum([dist_population(dist) for dist_num, dist in dists.items()])/len(dists)
    return mean
def dist_pop_imbalance(dists):
    mean = mean_dist_pop(dists)
    imbalance = sum([(dist_population(dist) - mean)**2 for dist_num, dist in dists.items()])
    return imbalance
def expected_eff_gap(dists, total_pop):
    #First, compute the number of wasted votes for both parties.
    #Then take the subtract the number of wasted votes for party B
    #from the number of wasted votes for party A and divide that number by total population.
    #A largely negative value is associated with gerrymandering in favor of party A.
    wasted_dists = [calc_wasted_votes(dist) for dist_num, dist in dists.items()]
    wasted_A = sum([a for (a, b) in wasted_dists])
    wasted_B = sum([b for (a, b) in wasted_dists])
    return (wasted_A - wasted_B)/total_pop
def calc_wasted_votes(dist):
    # a won
    a, b = get_dist_vote_split(dist)
    if (exp_prob_winning_dist(a, b) > 0.5):
        return (a - b- 1), b
    # b won
    else:
        return a, (b - a - 1)
def exp_prob_winning_dist(pop_A, pop_B):
    # E[X] = n*p
    # E[X] + E[Y]/X + Y
    return (.60*pop_A + .40*pop_B)/(pop_A + pop_B)

def exp_num_districts(dists):
    dists_splits = [get_dist_vote_split(dist) for dist_num, dist in dists.items()]
    return sum([exp_prob_winning_dist(a, b) for (a, b) in dists_splits])


# In[71]:


total_pop = sum(voters_a + voters_b)
print(voters_a[0])


# In[72]:


districts_left = 20


# In[92]:


import random
from itertools import combinations

# check if adding block to dist will result in a valid dist
def is_valid_dist(dist, block):
    if len(dist) == 0:
        return True
    block_coord = get_coordinates(block, n)
    neighbors = get_neighbors(block_coord)
#     print(neighbors)
    # if the block has a neighbor in dist, then it's reachable
    coords = [get_coordinates(b, n) for b in dist]
#     for c in coords:
#         for neigh in neighbors:
#             if neigh[0] == c[0] and neigh[1] == c[1]:
#                 return True
#     return False
    block_neighbor_valid = [neighbor in coords for neighbor in neighbors]
    return (True in block_neighbor_valid)

def is_valid_configuration(dists):
#     print('CHECKING VALID CONFIG')
#     visualize_districts(dists)
#     print("-" * 40)
    temp_dists = copy.deepcopy(dists)
    total_blocks = 0
    valid = True
    for i in range(D):
        if len(temp_dists[str(i)]) == 0:
            print('got here')
            return False
        dist = temp_dists[str(i)]
        for j in range(len(dist)):
            block = dist[j]
            dist.remove(block)
            valid = is_valid_dist(dist, block)
            if is_valid_dist(dist, block) == False:
                return False
            else:
                dist.append(block)
        total_blocks += len(dist)
    return valid and (total_blocks == n**2)

# def best_neighbors(dists):
#     possibleSwaps = list(combinations(list(dists), 2))
#     allNeighbors = []
#     for swap in possibleSwaps:
#         allNeighbors.append(tour.move_city(tour.index(swap[0]),tour.index(swap[1])))
    # TODO: implement if needed
#     return allNeighbors

def assign_blocks_to_district(blocks):
    districts = {}
    blocks_assigned = {}
    has_empty_dist = True in [len(v)== 0 for k,v in districts.items()]
    for i in range(D):
        districts[str(i)] = []
    for i in range(n):
        blocks_assigned[i] = {}
        for j in range(n):
            blocks_assigned[i][j] = False
    for i in range(n*n):
        x, y = get_coordinates(i, n)
        while not blocks_assigned[x][y]:
            a, b = get_block_vote_split(i)
            # randomly assign as long as its valid
            if has_empty_dist:
                for k,v in districts.items():
                    if len(v) == 0:
                        blocks_assigned[x][y] = True
                        districts[str(k)].append(i)
            else:
                randDistNum = random.randint(0, D-1)
                dist = districts[str(randDistNum)]
                if is_valid_dist(dist, i):
                    blocks_assigned[x][y] = True
                    dist.append(i)
    return districts


# In[93]:


# visualize_districts(dists)
import copy
def change_random_block(temp_dists):
    # Not working properly???
#     original_dists = copy.deepcopy(dists)
#     visualize_districts(dists)
#     print("-" * 40)
    tried_dists = []
    randDistStart = random.randint(0, len(temp_dists)-1)
    while len(temp_dists[str(randDistStart)]) == 1:
        randDistStart = random.randint(0, len(temp_dists)-1)
    randBlock = random.choice(temp_dists[str(randDistStart)])
    randDistTo = random.randint(0, len(temp_dists)-1)
    while randDistStart == randDistTo:
        randDistTo = random.randint(0, len(temp_dists)-1)
    coords = get_coordinates(randBlock, n)
    valid = False
    while valid == False:
        if randDistTo in tried_dists == False:
            tried_dists.append(randDistTo)
        if len(tried_dists) == len(temp_dists):
            randBlock = random.choice(temp_dists[str(randDistStart)])
            tried_dists = []
        randDistTo = random.randint(0, len(temp_dists)-1)
        if is_valid_dist(temp_dists[str(randDistTo)], randBlock):
            temp_dists[str(randDistStart)].remove(randBlock)
            temp_dists[str(randDistTo)].append(randBlock)
            if is_valid_configuration(temp_dists) == False:
                temp_dists[str(randDistStart)].append(randBlock)
                temp_dists[str(randDistTo)].remove(randBlock)
            else:
                valid = True
    return temp_dists

# def cost(dists):
#     return ((exp_num_dists-exp_num_districts(dists))*10)**2 + ((dist_pop_imbalance(dists)-imbalance)/1000)**2 + ((expected_eff_gap(dists, total_pop))*100000000)

def get_best_block(temp_dists):
    randDistStart = random.randint(0, len(temp_dists)-1)
    while len(temp_dists[str(randDistStart)]) == 1:
        randDistStart = random.randint(0, len(temp_dists)-1)
    possible_districts = list(range(D))
    possible_districts.remove(randDistStart)
    valid_dists = {}
    while len(valid_dists) < 1:
        randBlock = random.choice(temp_dists[str(randDistStart)])
        for dist in possible_districts:
            temp = copy.deepcopy(temp_dists)
            if is_valid_dist(temp[str(dist)], randBlock):
                temp[str(dist)].append(randBlock)
                temp[str(randDistStart)].remove(randBlock)
                if is_valid_configuration(temp):
                    valid_dists[str(dist)] = cost(temp)
    configs = valid_dists.items()
    min_dist = min(configs, key= lambda t: t[1])
    temp_dists[str(min_dist[0])].append(randBlock)
    temp_dists[str(randDistStart)].remove(randBlock)
    return temp_dists


def cost(dists):
    return (expected_eff_gap(dists, total_pop))*100000000
dists = assign_blocks_to_district(blocks)
current_gap = expected_eff_gap(dists, total_pop)
while current_gap > 0:
    orig_dists = copy.deepcopy(dists)
    new_dists = change_random_block(dists)
    if is_valid_configuration(new_dists) == False:
        print("invalid configuration!!!")
    if expected_eff_gap(new_dists, total_pop) < current_gap:
        current_gap = expected_eff_gap(new_dists, total_pop)
        print(current_gap)
        dists = new_dists
    else:
        dists = orig_dists
visualize_districts(dists)
print("-" * 40)

visualize_districts(dists)
