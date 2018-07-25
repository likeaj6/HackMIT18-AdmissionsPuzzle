{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 482,
   "metadata": {},
   "outputs": [],
   "source": [
    "exp_num_dists = 10\n",
    "imbalance = 150*(10**10)\n",
    "eff_gap = -0.105\n",
    "n = 10\n",
    "D = 20"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 483,
   "metadata": {},
   "outputs": [],
   "source": [
    "import math\n",
    "def get_neighbors(dist_coord):\n",
    "    x, y = dist_coord\n",
    "    return (x-1)*n + y, (x+1)*n + y, (x*n)+y+1, x*n +(y-1)\n",
    "def get_coordinates(block, n):\n",
    "    return (math.floor(block/n), block%n)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 484,
   "metadata": {},
   "outputs": [],
   "source": [
    "# setup/import data\n",
    "import json\n",
    "from pprint import pprint\n",
    "with open('p6/voters.json') as data_file:\n",
    "    data_item = json.load(data_file)\n",
    "    \n",
    "voters_a = data_item['voters_by_block']['party_A']\n",
    "voters_b = data_item['voters_by_block']['party_B']\n",
    "blocks_pop = [a + b for a, b in zip(voters_a, voters_b)]\n",
    "\n",
    "blocks = {}\n",
    "blocks_assigned = {}\n",
    "for i in range(n):\n",
    "    blocks[i] = {}\n",
    "    blocks_assigned[i] = {}\n",
    "for i in range(100):\n",
    "    block = voters_a[i], voters_b[i]\n",
    "    x, y = get_coordinates(i, n)\n",
    "    blocks[x][y] = block\n",
    "    blocks_assigned[x][y] = False\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 485,
   "metadata": {},
   "outputs": [],
   "source": [
    "# dists will be an array of labels i.e 10, or the block at (1, 0)\n",
    "def get_block_vote_split(block):\n",
    "    x, y = get_coordinates(block, n)\n",
    "    a, b = blocks[x][y]\n",
    "    return a, b\n",
    "def get_block_pop(block):\n",
    "    a, b = get_block_vote_split(block)\n",
    "    return a + b\n",
    "def get_dist_vote_split(dist):\n",
    "    blocks_split = [get_block_vote_split(block) for block in dist]\n",
    "    a = sum([block[0] for block in blocks_split])\n",
    "    b = sum([block[1] for block in blocks_split])\n",
    "    return a, b\n",
    "def dist_population(dist): \n",
    "    a, b = get_dist_vote_split(dist)\n",
    "    return a + b\n",
    "def mean_dist_pop(dists):\n",
    "    mean = sum([dist_population(dist) for dist_num, dist in dists.items()])/len(dists)\n",
    "    return mean\n",
    "def dist_pop_imbalance(dists):\n",
    "    mean = mean_dist_pop(dists)\n",
    "    imbalance = sum([(dist_population(dist) - mean)**2 for dist_num, dist in dists.items()])\n",
    "    return imbalance\n",
    "def expected_eff_gap(dists, total_pop):\n",
    "    #First, compute the number of wasted votes for both parties.\n",
    "    #Then take the subtract the number of wasted votes for party B \n",
    "    #from the number of wasted votes for party A and divide that number by total population. \n",
    "    #A largely negative value is associated with gerrymandering in favor of party A.\n",
    "    wasted_dists = [calc_wasted_votes(dist) for dist_num, dist in dists.items()]\n",
    "    wasted_A = sum([a for (a, b) in wasted_dists])\n",
    "    wasted_B = sum([b for (a, b) in wasted_dists])\n",
    "    return (wasted_A - wasted_B)/total_pop\n",
    "def calc_wasted_votes(dist):\n",
    "    # a won\n",
    "    a, b = get_dist_vote_split(dist)\n",
    "    if (exp_prob_winning_dist(a, b) > 0.5):\n",
    "        return (a - (a+b))/2, b\n",
    "    # b won\n",
    "    else:\n",
    "        return a, (b - (a+b))/2\n",
    "    return\n",
    "def exp_prob_winning_dist(pop_A, pop_B):\n",
    "    # E[X] = n*p\n",
    "    # P[A winning] = E[X] + E[Y]/X + Y\n",
    "    return (.60*pop_A + .40*pop_B)/(pop_A + pop_B)\n",
    "\n",
    "def exp_num_districts(dists):\n",
    "    dists_splits = [get_dist_vote_split(dist) for dist_num, dist in dists.items()]\n",
    "    return sum([exp_prob_winning_dist(a, b) for (a, b) in dists_splits])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 486,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "8741\n"
     ]
    }
   ],
   "source": [
    "total_pop = sum(voters_a + voters_b)\n",
    "print(voters_a[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 487,
   "metadata": {},
   "outputs": [],
   "source": [
    "districts_left = 20"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 488,
   "metadata": {},
   "outputs": [],
   "source": [
    "import random\n",
    "from itertools import combinations\n",
    "\n",
    "# check if adding block to dist will result in a valid dist\n",
    "def is_valid_dist(dist, block):\n",
    "    if len(dist) == 0: \n",
    "        return True\n",
    "    valid_neighbor = False\n",
    "    block_coord = get_coordinates(block, n)\n",
    "    neighbors = get_neighbors(block_coord)\n",
    "    # if the block has a neighbor in dist, then it's reachable\n",
    "    block_neighbor_valid = [neighbor in dist for neighbor in neighbors]\n",
    "    return (True in block_neighbor_valid)\n",
    "\n",
    "def is_valid_configuration(dists):\n",
    "    total_blocks = 0\n",
    "    for i in range(D):\n",
    "        if len(dists[i] == 0):\n",
    "            return False\n",
    "        total_blocks += len(dists[i])\n",
    "    return (total_blocks == n**2)\n",
    "\n",
    "def best_neighbors(dists):\n",
    "#     possibleSwaps = list(combinations(list(dists), 2))\n",
    "#     allNeighbors = []\n",
    "#     for swap in possibleSwaps:\n",
    "#         allNeighbors.append(tour.move_city(tour.index(swap[0]),tour.index(swap[1])))\n",
    "    # TODO: implement if needed\n",
    "    return allNeighbors\n",
    "def change_random_block(dists):\n",
    "    tried_dists = []\n",
    "    randDistStart = random.randint(0, len(dists)-1)\n",
    "    while len(dists[randDistStart]) <= 1:\n",
    "        randDistStart = random.randint(0, len(dists)-1)\n",
    "    randBlock = random.choice(dists[randDistStart])\n",
    "    randDistTo = random.randint(0, len(dists)-1)\n",
    "    coords = get_coordinates(randBlock, n)\n",
    "    while randDistTo == randDistStart and not is_valid_dist(dists[randDistTo], randBlock):\n",
    "        randDistTo = random.randint(0, len(dists)-1)\n",
    "        if randDistTo not in tried_dists:\n",
    "            tried_dists.append(randDistTo)\n",
    "        if len(tried_dists) == len(dists):\n",
    "            randBlock = random.choice(dists[randDistStart])\n",
    "            tried_dists = []\n",
    "    dists[randDistStart].remove(randBlock)\n",
    "    dists[randDistTo].append(randBlock)\n",
    "    return dists\n",
    "        \n",
    "    return tour.move_city(randStart, randTo), self.cost(tour.move_city(randStart, randTo))\n",
    "def assign_blocks_to_district(blocks):\n",
    "    districts = {}\n",
    "    blocks_assigned = {}\n",
    "    has_empty_dist = True in [len(v)== 0 for k,v in districts.items()]\n",
    "    for i in range(D):\n",
    "        districts[i] = []\n",
    "    for i in range(n):\n",
    "        blocks_assigned[i] = {}\n",
    "        for j in range(n):\n",
    "            blocks_assigned[i][j] = False\n",
    "    for i in range(100):\n",
    "        x, y = get_coordinates(i, n)\n",
    "        while not blocks_assigned[x][y]:\n",
    "            a, b = get_block_vote_split(i)\n",
    "            # randomly assign as long as its valid\n",
    "            if has_empty_dist:\n",
    "                for k,v in districts.items():\n",
    "                    if len(v) == 0:\n",
    "                        blocks_assigned[x][y] = True\n",
    "                        districts[k].append(i)\n",
    "            else:\n",
    "                randDistNum = random.randint(0, D-1)\n",
    "                dist = districts[randDistNum]\n",
    "                if is_valid_dist(dist, i):\n",
    "                    blocks_assigned[x][y] = True\n",
    "                    dist.append(i)\n",
    "    return districts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "dists = assign_blocks_to_district(blocks)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(dists)\n",
    "# print(exp_num_districts(dists))\n",
    "# print(dist_pop_imbalance(dists))\n",
    "# print(expected_eff_gap(dists, total_pop))\n",
    "# print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)\n",
    "# print(dist_pop_imbalance(dists))\n",
    "# print(expected_eff_gap(dists, total_pop))\n",
    "current_best_imbalance = 10000000000000000\n",
    "while current_best_imbalance > imbalance:\n",
    "    original_dists = dict(dists)\n",
    "    new_dists = change_random_block(dists)\n",
    "    new_imbalance = dist_pop_imbalance(new_dists)\n",
    "    if new_imbalance <= current_best_imbalance:\n",
    "        current_best_imbalance = new_imbalance\n",
    "        print('imbalance', current_best_imbalance)\n",
    "        dists = new_dists\n",
    "    else: \n",
    "        dists = original_dists\n",
    "print(\"DONE WITH IMBALANCE\")\n",
    "current_best_exp = 0\n",
    "while exp_num_districts(dists) < exp_num_dists:\n",
    "    original_dists = dict(dists)\n",
    "    new_dists = change_random_block(dists)\n",
    "    new_exp_num = exp_num_districts(new_dists)\n",
    "    if (current_best_exp <= new_exp_num and dist_pop_imbalance(new_dists) <= imbalance):\n",
    "        current_best_exp = new_exp_num\n",
    "        print('num districts', new_exp_num)\n",
    "        dists = new_dists\n",
    "    else: \n",
    "        dists = original_dists\n",
    "print(\"DONE WITH DISTRICTS\")\n",
    "current_best_gap = 1.0\n",
    "while expected_eff_gap(dists, total_pop) < eff_gap:\n",
    "    original_dists = dict(dists)\n",
    "    new_dists = change_random_block(dists)\n",
    "    new_gap = expected_eff_gap(new_dists)\n",
    "    if (current_best_gap <= new_gap and exp_num_districts(new_dists) >= 10 and dist_pop_imbalance(new_dists) <= imbalance):\n",
    "        current_best_gap = new_gap\n",
    "        print('eff gap', current_best_gap)\n",
    "        dists = new_dists\n",
    "    else: \n",
    "        dists = original_dists\n",
    "print(\"DONE WITH GAP\")\n",
    "print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 412,
   "metadata": {},
   "outputs": [],
   "source": [
    "# key is dist, value is true if we've tried it\n",
    "combination_tried = {}\n",
    "# dists is an array of length D, of tuples (num_party_A, num_party_B) in district i\n",
    "dists = []\n",
    "# win condition\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 513,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "True False True\n"
     ]
    }
   ],
   "source": [
    "print(exp_num_districts(dists) >= exp_num_dists, dist_pop_imbalance(dists) <= imbalance, expected_eff_gap(dists, total_pop) >= eff_gap)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 519,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "7857742112766.95\n",
      "1500000000000\n"
     ]
    }
   ],
   "source": [
    "print(dist_pop_imbalance(dists))\n",
    "print(imbalance)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 515,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "10.002898155019142\n"
     ]
    }
   ],
   "source": [
    "print(exp_num_districts(dists))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 518,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0.26826444716245207\n"
     ]
    }
   ],
   "source": [
    "print(expected_eff_gap(dists, total_pop))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "while current_best_imbalance > imbalance:\n",
    "    original_dists = dict(dists)\n",
    "    new_dists = change_random_block(dists)\n",
    "    new_imbalance = dist_pop_imbalance(new_dists)\n",
    "    if new_imbalance <= current_best_imbalance:\n",
    "        current_best_imbalance = new_imbalance\n",
    "        print('imbalance', current_best_imbalance)\n",
    "        dists = new_dists\n",
    "    else: \n",
    "        dists = original_dists\n",
    "print(\"DONE WITH IMBALANCE\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
