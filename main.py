import random
from BinaryGene import BinaryGene
from Rules import Rules
from Data import Data
from copy import deepcopy
import csv


# Performs one point crossover with random point selection
def crossover(population, size, len, rulebase, data, cond_len):
    print("Crossover")
    for i in range(size):
        crossover = random.random()
        if i % 2 is 1 and crossover > 0.6:
            crossover_pt = random.randint(0, len - 1)
            population[i].set_fitness(0)
            population[i - 1].set_fitness(0)
            for j in range(len):
                if j >= crossover_pt:
                    parent_one = population[i - 1].get_gene()[j]
                    parent_two = population[i].get_gene()[j]
                    population[i - 1].update_gene(j, parent_two)
                    population[i].update_gene(j, parent_one)
            fitness_function(population[i - 1], cond_len, rulebase, data)
            fitness_function(population[i], cond_len, rulebase, data)
    return population


# Performs mutation with random probability for each gene bit flip
def mutation(population, size, len, rulebase, data, cond_len):
    print("Mutation")
    for i in range(size):
        population[i].set_fitness(0)
        k = 0
        for j in range(len):
            mutate = random.random()
            if mutate < 0.01:
                if k is cond_len:
                    if population[i].get_gene()[j] is 1:
                        population[i].update_gene(j, 0)
                    else:
                        population[i].update_gene(j, 1)
                else:
                    if population[i].get_gene()[j] is 1:
                        population[i].update_gene(j, random.choice([0, 2]))
                    else:
                        population[i].update_gene(j, random.choice([1, 2]))
            if k is cond_len:
                k = 0
            else:
                k = k + 1
    for i in range(size):
        fitness_function(population[i], cond_len, rulebase, data)
    return population, rulebase


# Fitness function to determine fitness of current candidate
def fitness_function(gene, len, rule_base, data):
    fitness = 0
    k = 0
    for i in range(10):
        for j in range(len):
            rule_base[i].update_cond(j, gene.get_gene()[k])
            k = k + 1
        rule_base[i].out = gene.get_gene()[k]
        k = k + 1
    for d in data:
        for r in rule_base:
            if match(d.get_var(), r.get_cond()) is True:
                if d.get_classification() == r.get_out():
                    fitness = fitness + 1
                    break
    gene.set_fitness(fitness)


def match(d, r):
    for i in range(len(d)):
        if d[i] is not r[i] and r[i] is not 2:
            return False
            break
    return True


# Tournament selection to determine new offspring for new generation pool
def tournament_selection(population, size):
    print("Tournament Selection")
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
            if k is cond_len:
                population[i].set_gene(random.randint(0, 1))
                k = 0
            else:
                population[i].set_gene(random.randint(0, 2))
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
        for j in range(len):
            rulebase[i].set_cond(0)
    return rulebase


# initilises the data set by reading in text file and creating list of all data
def __init__data(file, len, data_len):
    k = 0
    data = [Data() for i in range(data_len)]
    file_name = open(file, 'r', newline='')
    next(file_name)
    for line in file_name:
        line = line.strip('\n')
        j = 0
        for i in line:
            if j < len:
                data[k].set_var(i)
            j = j + 1
        data[k].classification = line[len + 1]
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
    print("SUM: " + str(sum))
    return population, mean, max


# main program to run GA
def main():
    var = 50
    pop_size = var
    generations = 50
    mean = []
    cond_len = 7
    data_len = 64
    num_rule = 10
    chromosome_len = (cond_len + 1) * num_rule
    print(chromosome_len)

    data_set = __init__data("data2.txt", cond_len, data_len)
    population_obj = __init__chromosomes(pop_size, chromosome_len, cond_len).copy()
    rule_base = __init__rules(cond_len, num_rule).copy()

    best = 0

    for i in range(generations):

        print("GENERATION " + str(i + 1))
        population_obj = tournament_selection(population_obj, pop_size)
        population_obj = crossover(population_obj, pop_size, chromosome_len, rule_base, data_set, cond_len)
        population_obj, rule_base = mutation(population_obj, pop_size, chromosome_len, rule_base, data_set, cond_len)


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

        mean.append(val)
        mean.append(val_2)
        print("-------------------")

    for gene in population_obj:
        if gene.get_fitness() == val_2:
            print(gene.get_gene())

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