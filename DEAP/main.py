import copy
import random
import subprocess
import time
import os

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from params import eaParams
from custom import customGP
from utilities import utilities
from primitives import PrimitiveSetTyped



# EA parameters

params = eaParams()
customGP = customGP()
utilities = utilities()

def evaluateRobot(individual):
	
	# save number of robots and chromosome to file
	with open('../chromosome.txt', 'w') as f:
		print >> f, params.sqrtRobots	
		print >> f, individual
	
	seed = 0	
	runningFitness = 0
	robots = {}
	for i in range(params.iterations):
		
		# write seed to file
		seed = seed + 1
		with open('../seed.txt', 'w') as f:
			print >> f, seed
		
		# run argos
		subprocess.call(["/bin/bash", "evaluate", "", "./"])
		
		# result from file	
		f = open("../result.txt", "r")
		
		# check each line for values that need saved
		for line in f:
			first = line[0:4]		
			if (first == "food"):
				line = line[5:]
				robotId = int(float(line[0:line.find(' ')]))
				line = line[line.find(' ')+1:-1]
				robots[robotId] = line
		
		# measure food collected by each robot and add to cumulative total
		thisFitness = 0.0;
		for r in robots:
			thisFitness += float(robots[r])
		
		# divide to get average for this iteration and add to running total
		thisFitness /= params.sqrtRobots * params.sqrtRobots
		runningFitness += thisFitness
	
	# divide to get average per iteration and normalise
	fitness = runningFitness / params.iterations
	fitness = fitness / params.maxFood
	
	# apply derating factor to large trees	
	fitness *= utilities.deratingFactor(individual)
	
	# pause to free up CPU
	time.sleep(params.evalSleep)
	
	return (fitness, )




toolbox = base.Toolbox()

experiment = "bt"

if experiment == "original":

	pset = gp.PrimitiveSetTyped("MAIN", [], str)
	params.addNodes(pset)

	creator.create("Fitness", base.Fitness, weights=(1.0,))
	creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

	toolbox.register("expr_init", customGP.genFull, pset=pset, min_=1, max_=4)

	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluateRobot)
	toolbox.register("select", customGP.selTournament, tournsize=params.tournamentSize)

	toolbox.register("mate", gp.cxOnePoint)
	toolbox.register("expr_mut", customGP.genFull, min_=0, max_=2)
	toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
	toolbox.register("mutSubtreeShrink", gp.mutShrink)
	toolbox.register("mutNodeReplace", gp.mutNodeReplacement, pset=pset)
	toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")

if experiment == "bt":

	pset = PrimitiveSetTyped("MAIN", [], str)
	params.addNodes(pset)

	creator.create("Fitness", base.Fitness, weights=(1.0,))
	creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

	toolbox.register("expr_init", customGP.genFull, pset=pset, min_=1, max_=4)

	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluateRobot)
	toolbox.register("select", customGP.selTournament, tournsize=params.tournamentSize)

	toolbox.register("mate", customGP.cxOnePoint)
	toolbox.register("expr_mut", customGP.genFull, min_=0, max_=2)
	toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
	toolbox.register("mutSubtreeShrink", customGP.mutShrinkToChild, pset=pset)
	toolbox.register("mutNodeReplace", customGP.mutNodeReplacement, pset=pset)
	toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")

if experiment == "weighted":
	
	# toolbox.register("mate", customGP.cxOnePointInner, pset=pset)
	# toolbox.register("expr_mut", customGP.genFull, min_=0, max_=2)
	# toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
	# toolbox.register("mutSubtreeShrink", customGP.mutShrinkToChild, pset=pset)
	# toolbox.register("mutNodeReplace", customGP.mutNodeReplacement, pset=pset)
	# toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")
	
	# toolbox.register("mate", customGP.cxOnePoint)
	# toolbox.register("expr_mut", customGP.genFull, min_=0, max_=2)
	# toolbox.register("mutSubtreeReplace", customGP.mutUniformInner, expr=toolbox.expr_mut, pset=pset)
	# toolbox.register("mutSubtreeShrink", customGP.mutShrinkToChild, pset=pset)
	# toolbox.register("mutNodeReplace", customGP.mutNodeReplacementInner, pset=pset)
	# toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")
	
	toolbox.register("mate", customGP.cxOnePointInner, pset=pset)
	toolbox.register("expr_mut", customGP.genFull, min_=0, max_=2)
	toolbox.register("mutSubtreeReplace", customGP.mutUniformInner, expr=toolbox.expr_mut, pset=pset)
	toolbox.register("mutSubtreeShrink", customGP.mutShrinkToChild, pset=pset)
	toolbox.register("mutNodeReplace", customGP.mutNodeReplacementInner, pset=pset)
	toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")
	





def main():
	random.seed(params.deapSeed)

	pop = toolbox.population(n=params.populationSize)
	hof = tools.HallOfFame(1)
	
	stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values[0])
	stats_size = tools.Statistics(key=lambda depth: depth.height)
	mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	mstats.register("avg", numpy.mean)
	mstats.register("std", numpy.std)
	mstats.register("min", numpy.min)
	mstats.register("max", numpy.max)

	customGP.eaInit(pop, toolbox, params.generations, mstats, halloffame=hof)
    
	return pop, hof, mstats

if __name__ == "__main__":
	main()
