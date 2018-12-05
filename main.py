import random
from BinaryGene import BinaryGene
from Rules import Rules
from Data import Data
from copy import deepcopy
import csv


# Performs one point crossover with random point selection
# def crossover(population, size, chromo_len, rulebase, data, cond_len):
#     for i in range(size):
#         crossover = random.random()
#         if i % 2 is 1 and crossover > 0.6:
#             crossover_pt = random.randint(0, chromo_len - 1)
#             population[i].set_fitness(0)
#             population[i - 1].set_fitness(0)
#             for j in range(chromo_len):
#                 if j >= crossover_pt:
#                     parent_one = population[i - 1].get_gene()[j]
#                     parent_two = population[i].get_gene()[j]
#                     population[i - 1].update_gene(j, parent_two)
#                     population[i].update_gene(j, parent_one)
#             #fitness_function(population[i - 1], cond_len, rulebase, data)
#             #fitness_function(population[i], cond_len, rulebase, data)
#     return population


# Performs mutation with random probability for each gene bit flip
def mutation(population, size, chromo_len, rulebase, data, cond_len):
   # print("B_M " + str(population[0].get_gene()))
    for i in range(size):
        population[i].set_fitness(0)
        for j in range(1, chromo_len + 1):
            mutate = random.random()
            if mutate < 0.01:
                if j % 15 is 0:
                    if population[i].get_gene()[j - 1] is 1:
                        population[i].update_gene(j - 1, 0)
                    else:
                        population[i].update_gene(j - 1, 1)
                else:
                    rand_num = random.uniform(-0.01, 0.01)
                    new_gene = rand_num + population[i].get_gene()[j]
                    if new_gene > 1:
                        population[i].update_gene(j - 1, 1)
                    elif new_gene < 0:
                        population[i].update_gene(j - 1, 1)
                    else:
                        population[i].update_gene(j - 1, new_gene)
    #print("A_M " + str(population[0].get_gene()))
    for i in range(size):
        fitness_function(population[i], cond_len, rulebase, data)
    return population


# Fitness function to determine fitness of current candidate
def fitness_function(gene, cond_len, rule_base, data):
    fitness = 0
    k = 0
    for i in range(10):
        for j in range(cond_len * 2):
            rule_base[i].update_cond(j, gene.get_gene()[k])
            k = k + 1
        rule_base[i].out = gene.get_gene()[k]
        k = k + 1
    #print("R " + str(rule_base[0].get_cond()) + str(rule_base[0].get_out()))
    for d in range(len(data)):
        for r in range(len(rule_base)):
            if match_range(data[d].get_var(), rule_base[r].get_cond(), cond_len) == True:
                #print("true")
                if data[d].get_classification() == rule_base[r].get_out():
                    fitness = fitness + 1
                    #print(fitness)
                break
    #print(fitness)
    gene.set_fitness(fitness)


def match_range(d, r, r_len):
    k = 0
    for i in range(len(d)):
        if d[k] < (r[i] * 2) or d[k] > (r[i] * 2) + 1:
            return False
            #break
        k = k + 1
    return True


def match(d, r):
    for i in range(len(d)):
        if d[i] is not r[i] and r[i] is not 2:
            return False
            break
    return True


# Tournament selection to determine new offspring for new generation pool
def tournament_selection(population, size):
    offspring = []
    for i in range(size):
        parent_one = random.randrange(0, size)
        parent_two = random.randrange(0, size)
        if population[parent_one].get_fitness() > population[parent_two].get_fitness():
            p1 = deepcopy(population[parent_one])
            offspring.append(p1)
        else:
            p2 = deepcopy(population[parent_two])
            offspring.append(p2)
        population[i] = offspring[i]

    return population


# initialises the chromosomes for the start pool for first generation
def __init__chromosomes(size, len, cond_len):
    k = 0
    population = [BinaryGene() for i in range(size)]
    for i in range(size):
        population[i].set_fitness(0)
        for j in range(len):
            #population[i].set_gene(random.randint(0, 1))
            if k is (cond_len * 2):
                population[i].set_gene(random.choice([0,1]))
                k = 0
            else:
                population[i].set_gene(random.uniform(0, 1))
                k = k + 1
            #if population[i].get_gene()[j] is 1:
            #    population[i].set_fitness(population[i].get_fitness() + 1)
        #print(population[i].get_gene())
        #exit()
    return population


# initilises the rule base list creating list size and rule size
def __init__rules(len, num_rule):
    rulebase = [Rules() for i in range(num_rule)]
    for i in range(num_rule):
        for j in range(len * 2):
            rulebase[i].set_cond(0)
    return rulebase


# initilises the data set by reading in text file and creating list of all data
def __init__data(file, len, data_len):
    k = 0
    data = [Data() for i in range(data_len)]
    file_name = open(file, 'r', newline='')
    next(file_name)
    next(file_name)
    for line in file_name:
        line = line.strip('\n')
        line = line.strip('\r')
        temp = ""
        j = 0
        for i in line:
            if(i is not " "):
                temp = temp + i
                if j is 63:
                    data[k].classification = int(temp)
                    temp = ""
            else:
                data[k].set_var(str(temp))
                temp = ""
            j = j + 1
        #print(str(data[k].get_var()) + " " + str(data[k].classification))
        k = k + 1
    return data


# calcualtes mean, max and sum of current population
def fitness(population, size):
    max = sum = 0
    for i in range(size):
        if population[i].get_fitness() > max:
            max = population[i].get_fitness()
        sum = sum + population[i].get_fitness()
    mean = sum / size
    print("MEAN: " + str(mean))
    print("MAX: " + str(max))
    #print("SUM: " + str(sum))
    return population, mean, max


# main program to run GA
def main():
    var = 400
    pop_size = var
    mean = []
    cond_len = 7
    data_len = 2000
    num_rule = 10
    chromosome_len = ((cond_len * 2) + 1) * num_rule
    generations = 500

    train = []
    test = []

    data_set = __init__data("data3.txt", cond_len, data_len).copy()
    population_obj = __init__chromosomes(pop_size, chromosome_len, cond_len).copy()
    rule_base = __init__rules(cond_len, num_rule).copy()

    for i in range(len(data_set)):
        if i % 2 is 0:
            test.append(data_set[i])
        else:
            train.append(data_set[i])

    print(len(train))
    print(len(test))


    best = 0


    for i in range(generations):

        print("GENERATION " + str(i + 1))
        population_obj = tournament_selection(population_obj, pop_size).copy()
        #print("T " + str(population_obj[0].get_gene()))
        #population_obj = crossover(population_obj, pop_size, chromosome_len, rule_base, train, cond_len).copy()
        #print("C " + str(population_obj[0].get_gene()))
        population_obj = mutation(population_obj, pop_size, chromosome_len, rule_base, train, cond_len).copy()
        #print("M " + str(population_obj[0].get_gene()))


        # Maintain best fitness gene for each generation
        for gene in population_obj:
            if gene.get_fitness() >= best:
                best = gene.get_fitness()
                temp_best = deepcopy(gene)
        worst = best
        for gene in population_obj:
            if gene.get_fitness() < worst:
                worst = gene.get_fitness()
        for j in range(len(population_obj)):
            if population_obj[j].get_fitness() is worst:
                population_obj[j] = deepcopy(temp_best)
                break

        population_obj, val, val_2 = fitness(population_obj, pop_size)

        for i in range(len(population_obj)):
            fitness_function(population_obj[i], cond_len, rule_base, test)



        mean.append(val)
        mean.append(val_2)
        print("-------------------")


        #print(population_obj[0].get_gene())

    with open('genetic_algorithm.csv', 'w', newline='') as new:
        writer = csv.writer(new)
        writer.writerow(["Generation", "Mean", "Best"])
        count = 0
        for i in range(generations * 2):
            if i % 2 is 1:
                count = count + 1
                temp = []
                temp.append(count)
                temp.append(mean[i - 1])
                temp.append(mean[i])
                writer.writerow(temp)


main()


# for j in range(len):
    #     if gene.get_gene()[j] is 1:
    #         fitness = fitness + 1
    # gene.set_fitness(fitness)


# for gene in population_obj:
        #     print("Gene: " + str(gene.get_gene()) + " " + str(gene.get_fitness()))
        #     text = "["
        #     text2 = "["
        #     for i in range(10):
        #         for j in range(5):
        #             text = text + str(rule_base[i].get_cond()[j]) + ", "
        #             text2 = text2 + str(dataset[i].get_var()[j]) + ", "
        #         text = text + str(rule_base[i].get_out()) + ", "
        #         text2 = text2 + str(dataset[i].get_classification()) + ", "


       # print("Rule: " + text + "]")
        #print("Data: " + text2 + "]")