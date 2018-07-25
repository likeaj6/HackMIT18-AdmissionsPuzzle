
# coding: utf-8

exp_num_dists = 10
imbalance = 150*(10**10)
eff_gap = -0.105
n = 10
D = 20

import math
def get_neighbors(dist_coord):
    x, y = dist_coord
    return (x-1)*n + y, (x+1)*n + y, (x*n)+y+1, x*n +(y-1)
def get_coordinates(block, n):
    return (math.floor(block/n), block%n)


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
        return (a - (a+b))/2, b
    # b won
    else:
        return a, (b - (a+b))/2
    return
def exp_prob_winning_dist(pop_A, pop_B):
    # E[X] = n*p
    # P[A winning] = E[X] + E[Y]/X + Y
    return (.60*pop_A + .40*pop_B)/(pop_A + pop_B)

def exp_num_districts(dists):
    dists_splits = [get_dist_vote_split(dist) for dist_num, dist in dists.items()]
    return sum([exp_prob_winning_dist(a, b) for (a, b) in dists_splits])


# In[486]:


total_pop = sum(voters_a + voters_b)
print(voters_a[0])


# In[487]:


districts_left = 20

import random
from itertools import combinations

# check if adding block to dist will result in a valid dist
def is_valid_dist(dist, block):
    if len(dist) == 0:
        return True
    valid_neighbor = False
    block_coord = get_coordinates(block, n)
    neighbors = get_neighbors(block_coord)
    # if the block has a neighbor in dist, then it's reachable
    block_neighbor_valid = [neighbor in dist for neighbor in neighbors]
    return (True in block_neighbor_valid)

def is_valid_configuration(dists):
    total_blocks = 0
    for i in range(D):
        if len(dists[i] == 0):
            return False
        total_blocks += len(dists[i])
    return (total_blocks == n**2)

# def best_neighbors(dists):
#     possibleSwaps = list(combinations(list(dists), 2))
#     allNeighbors = []
#     for swap in possibleSwaps:
# #         allNeighbors.append(tour.move_city(tour.index(swap[0]),tour.index(swap[1])))
#     # TODO: implement if needed
#     return allNeighbors
def change_random_block(dists):
    tried_dists = []
    randDistStart = random.randint(0, len(dists)-1)
    # we don't want to move a block if the district only has one block
    while len(dists[randDistStart]) <= 1:
        randDistStart = random.randint(0, len(dists)-1)
    randBlock = random.choice(dists[randDistStart])
    randDistTo = random.randint(0, len(dists)-1)
    coords = get_coordinates(randBlock, n)
    while randDistTo == randDistStart and not is_valid_dist(dists[randDistTo], randBlock):
        randDistTo = random.randint(0, len(dists)-1)
        if randDistTo not in tried_dists:
            tried_dists.append(randDistTo)
        if len(tried_dists) == len(dists):
            randBlock = random.choice(dists[randDistStart])
            tried_dists = []
    dists[randDistStart].remove(randBlock)
    dists[randDistTo].append(randBlock)
    return dists

def assign_blocks_to_district(blocks):
    districts = {}
    blocks_assigned = {}
    has_empty_dist = True in [len(v)== 0 for k,v in districts.items()]
    for i in range(D):
        districts[i] = []
    for i in range(n):
        blocks_assigned[i] = {}
        for j in range(n):
            blocks_assigned[i][j] = False
    for i in range(100):
        x, y = get_coordinates(i, n)
        while not blocks_assigned[x][y]:
            a, b = get_block_vote_split(i)
            # randomly assign as long as its valid
            if has_empty_dist:
                for k,v in districts.items():
                    if len(v) == 0:
                        blocks_assigned[x][y] = True
                        districts[k].append(i)
            else:
                randDistNum = random.randint(0, D-1)
                dist = districts[randDistNum]
                if is_valid_dist(dist, i):
                    blocks_assigned[x][y] = True
                    dist.append(i)
    return districts

dists = assign_blocks_to_district(blocks)

def cost(dists):
    return ((exp_num_dists-exp_num_districts(dists))*100000)**2 + ((dist_pop_imbalance(dists)-imbalance))**2 + ((expected_eff_gap(dists, total_pop))*100000000000000)

# print(exp_num_districts(dists))
# print(dist_pop_imbalance(dists))
# print(expected_eff_gap(dists, total_pop))
# print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)
# print(dist_pop_imbalance(dists))
# print(expected_eff_gap(dists, total_pop))
current_best_exp = 0
while current_best_exp < 9.9:
    original_dists = dict(dists)
    new_dists = change_random_block(dists)
    new_exp_num = exp_num_districts(new_dists)
    if (current_best_exp <= new_exp_num):
        current_best_exp = new_exp_num
        print('num districts', new_exp_num)
        dists = new_dists
    else:
        dists = original_dists
print(exp_num_districts(dists), dist_pop_imbalance(dists))

print("DONE WITH DISTRICTS")
current_cost = 100000000000000001000000000000000010000000000000000
while exp_num_districts(dists) < 9.9 or dist_pop_imbalance(dists) > imbalance or expected_eff_gap(dists, total_pop) < eff_gap:
    original_dists = dict(dists)
    new_dists = change_random_block(dists)
    new_cost = cost(new_dists)
    if exp_num_districts(new_dists) >= 9.9 and new_cost <= current_cost:
        current_cost = new_cost
        print('cost', new_cost)
        print('num districts', exp_num_districts(new_dists))
        print('imbalance', dist_pop_imbalance(new_dists))
        print('eff gap', expected_eff_gap(new_dists, total_pop))
        dists = new_dists
    else:
        dists = original_dists
print("DONZOOOO")
print(dists)

#
# current_best_imbalance = 10000000000000000
# while current_best_imbalance > imbalance:
#     original_dists = dict(dists)
#     new_dists = change_random_block(dists)
#     new_imbalance = dist_pop_imbalance(new_dists)
#     if new_imbalance <= current_best_imbalance:
#         current_best_imbalance = new_imbalance
#         print('imbalance', current_best_imbalance)
#         dists = new_dists
#     else:
#         dists = original_dists
# print("DONE WITH IMBALANCE")
# current_best_exp = 0
# while current_best_exp < exp_num_dists:
#     original_dists = dict(dists)
#     new_dists = change_random_block(dists)
#     new_exp_num = exp_num_districts(new_dists)
#     if ((dist_pop_imbalance(new_dists) <= imbalance) and (current_best_exp <= new_exp_num)):
#         current_best_exp = new_exp_num
#         print('num districts', new_exp_num)
#         dists = new_dists
#     else:
#         dists = original_dists
# print(exp_num_districts(dists), dist_pop_imbalance(dists))
#
# print("DONE WITH DISTRICTS")
# current_best_gap = -1
# while current_best_gap < eff_gap:
#     original_dists = dict(dists)
#     new_dists = change_random_block(dists)
#     new_gap = expected_eff_gap(new_dists)
#     if ((exp_num_districts(new_dists) >= 10) and (dist_pop_imbalance(new_dists) <= imbalance) and (current_best_gap <= new_gap)):
#         current_best_gap = new_gap
#         print('eff gap', current_best_gap)
#         dists = new_dists
#     else:
#         dists = original_dists
# print("DONE WITH GAP")
# print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)

# key is dist, value is true if we've tried it
combination_tried = {}
# dists is an array of length D, of tuples (num_party_A, num_party_B) in district i
dists = []
# win condition

# print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)
#
# print(dist_pop_imbalance(dists))
# print(imbalance)
#
# print(exp_num_districts(dists))
#
# print(expected_eff_gap(dists, total_pop))
#
#
# # In[ ]:
#
#
# while current_best_imbalance > imbalance:
#     original_dists = dict(dists)
#     new_dists = change_random_block(dists)
#     new_imbalance = dist_pop_imbalance(new_dists)
#     if new_imbalance <= current_best_imbalance:
#         current_best_imbalance = new_imbalance
#         print('imbalance', current_best_imbalance)
#         dists = new_dists
#     else:
#         dists = original_dists
# print("DONE WITH IMBALANCE")
