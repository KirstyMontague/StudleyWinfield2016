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


# EA parameters

deapSeed = 14
sqrtRobots = 3
iterations = 2
populationSize = 15
tournamentSize = 3
eliteSize = 3
generations = 50

crossoverProbability = 0.8
mutSRProbability = 0.05
mutSSProbability = 0.1
mutNRProbability = 0.5
mutECRProbability = 0.5


# these values are used to free up the CPU after each generation and evaluation

genSleep = populationSize / 2
evalSleep = (sqrtRobots * sqrtRobots * iterations) / 9
print genSleep
print evalSleep
print ""



def nodeSettings():
	pSettings['selm2'] = True
	pSettings['selm3'] = True
	pSettings['selm4'] = True
	pSettings['seqm2'] = True
	pSettings['seqm3'] = True
	pSettings['seqm4'] = True
	pSettings['probm2'] = True
	pSettings['probm3'] = True
	pSettings['probm4'] = True
	pSettings['repeat'] = True
	pSettings['successd'] = True
	pSettings['failured'] = True
	pSettings['ifltvar'] = True
	pSettings['ifltcon'] = True
	pSettings['ifgevar'] = True
	pSettings['ifgecon'] = True
	pSettings['mf'] = True
	pSettings['mr'] = True
	pSettings['ml'] = True
	# pSettings['set'] = True
	pSettings['successl'] = True
	pSettings['failurel'] = True


def addNodes():
	
	# add the nodes chosen in nodeSettings() and dependencies if they have any
	
	if (pSettings['ifltvar']): pset.addPrimitive(robot.ifltvar, [bbInput, bbInput], str)
	if (pSettings['ifltcon']): pset.addPrimitive(robot.ifltcon, [bbInput, constant], str)
	if (pSettings['ifgevar']): pset.addPrimitive(robot.ifgevar, [bbInput, bbInput], str)
	if (pSettings['ifgecon']): pset.addPrimitive(robot.ifgecon, [bbInput, constant], str)
			
	if (pSettings['ifltvar'] or pSettings['ifltcon'] or pSettings['ifgevar'] or pSettings['ifgecon']): 	
		pset.addPrimitive(robot.bb, [bbInput], bbInput)
		pset.addEphemeralConstant("index", lambda: random.randint(0,5), bbInput)
	
	if (pSettings['ifltcon'] or pSettings['ifgecon']):
		pset.addPrimitive(robot.rand, [constant], constant)
		pset.addEphemeralConstant("constant", lambda: random.randint(0,100), constant)

	if (pSettings['successl']): pset.addTerminal(robot.successl, str)
	if (pSettings['failurel']): pset.addTerminal(robot.failurel, str)

	if (pSettings['selm2']): pset.addPrimitive(robot.selm2, [str, str],  str)
	if (pSettings['seqm2']): pset.addPrimitive(robot.seqm2, [str, str],  str)
	if (pSettings['probm2']): pset.addPrimitive(robot.probm2, [str, str],  str)
	if (pSettings['selm3']): pset.addPrimitive(robot.selm3, [str, str, str],  str)
	if (pSettings['seqm3']): pset.addPrimitive(robot.seqm3, [str, str, str],  str)
	if (pSettings['probm3']): pset.addPrimitive(robot.probm3, [str, str, str],  str)
	if (pSettings['selm4']): pset.addPrimitive(robot.selm4, [str, str, str, str],  str)
	if (pSettings['seqm4']): pset.addPrimitive(robot.seqm4, [str, str, str, str],  str)
	if (pSettings['probm4']): pset.addPrimitive(robot.probm4, [str, str, str, str],  str)

	if (pSettings['repeat']):
		pset.addPrimitive(robot.repeat, [repetitions, str],  str)
		pset.addPrimitive(robot.repetitions, [repetitions], repetitions)
		pset.addEphemeralConstant("repetitions", lambda: random.randint(1,9), repetitions)

	if (pSettings['successd']): pset.addPrimitive(robot.successd, [str],  str)
	if (pSettings['failured']): pset.addPrimitive(robot.failured, [str],  str)

	if (pSettings['mf']): pset.addTerminal(robot.mf, str)
	if (pSettings['ml']): pset.addTerminal(robot.ml, str)
	if (pSettings['mr']): pset.addTerminal(robot.mr, str)


def getBest(population):	
	
	# get the best member of the population
	
	for individual in population:		
		
		thisFitness = individual.fitness.getValues()[0]
		currentBest = False
		
		if ('best' not in locals()):
			currentBest = True
		
		elif (thisFitness > bestFitness):
			currentBest = True
		
		elif (thisFitness == bestFitness and individual.height > 3 and individual.height < bestHeight):
			currentBest = True
			
		if (currentBest):
			best = individual
			bestFitness = thisFitness	
			bestHeight = individual.height
			
	return best
	
	
def saveBest(gen, population):
	
	# save the best member of the population to the log
	
	best = getBest(population)
	
	logHeaders = "Time,Seed,Robots,Iterations,Population Size,Tournament Size,Elites,Generations,Fitness,Chromosome,Nodes"
	logString = str(time.time())[0:-3]+", "
	logString += str(deapSeed)+", "
	logString += str(sqrtRobots)+", "
	logString += str(iterations)+", "
	logString += str(populationSize)+", "
	logString += str(tournamentSize)+", "
	logString += str(eliteSize)+", "
	logString += str(gen)+", "
	logString += str("%.2f" % best.fitness.values[0])+", "
	logString += "\""+str(best)+"\", "
	
	logString += "\""
	for node in sorted(pSettings):
		if (pSettings[node]):
			logString += node+", "
	logString += "\""
	
	with open('../best-log.csv', 'a') as f:
		# print >> f, logHeaders
		print >> f, logString


def playbackBest(population):
	
	# run a simulation with visualisation using the best chromosome
	
	best = getBest(population)
	
	with open('../best.txt', 'w') as f:
		print >> f, sqrtRobots	
		print >> f, best		
		
	os.rename('../log.txt', '../logs/log-'+str(time.time())[0:-3]+'.txt')
	
	subprocess.call(["/bin/bash", "playback", "", "./"])


def selTournament(individuals, k, tournsize, fit_attr="fitness"):
	
	chosen = []
	for i in xrange(k):
		aspirants = tools.selRandom(individuals, tournsize)
		best = getBest(aspirants)
		chosen.append(best)
	return chosen


def varAnd(population, toolbox):
	
	# apply crossover and mutation
	
	offspring = [toolbox.clone(ind) for ind in population]
		
	# crossover
	for i in range(1, len(offspring), 2):
		if random.random() < crossoverProbability:
			offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
																		 offspring[i])
			del offspring[i - 1].fitness.values, offspring[i].fitness.values

	# mutation - subtree replacement
	for i in range(len(offspring)):
		if random.random() < mutSRProbability:
			offspring[i], = toolbox.mutSubtreeReplace(offspring[i])
			del offspring[i].fitness.values

	# mutation - subtree shrink
	for i in range(len(offspring)):
		if random.random() < mutSSProbability:
			offspring[i], = toolbox.mutSubtreeShrink(offspring[i])
			del offspring[i].fitness.values

	# mutation - node replacement
	for i in range(len(offspring)):
		if random.random() < mutNRProbability:
			offspring[i], = toolbox.mutNodeReplace(offspring[i])
			del offspring[i].fitness.values

	# mutation - ephemeral constant replacement
	for i in range(len(offspring)):
		if random.random() < mutECRProbability:
			offspring[i], = toolbox.mutConstantReplace(offspring[i])
			del offspring[i].fitness.values
			
	return offspring


def eaInit(population, toolbox, ngen, stats=None, halloffame=None, verbose=__debug__):

	# preliminary steps before beginning evolutionary loop
	# copied largely from algorithms.eaSimple

	logbook = tools.Logbook()
	logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])
	logbook.chapters["fitness"].header = "min", "avg", "max"
	logbook.chapters["size"].header = "min", "avg", "max"

	# Evaluate the individuals with an invalid fitness
	invalid_ind = [ind for ind in population if not ind.fitness.valid]
	fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	for ind, fit in zip(invalid_ind, fitnesses):
		ind.fitness.values = fit

	if halloffame is not None:
		halloffame.update(population)

	for ind in population:
		print str("%.2f" % ind.fitness.values[0]) + " " + str(ind)
	
	record = stats.compile(population) if stats else {}
	logbook.record(gen=0, nevals=len(invalid_ind), **record)
	if verbose:
		print ""
		print logbook.stream
		print "-----------------------------------------------------------------------------------"
	
	# save each fitness score and chromosome to file
	with open('../log.txt', 'w') as f:
		print >> f, ""
		print >> f, str(time.time())[0:-3]
		for ind in population:
			print >> f, str("%.2f" % ind.fitness.values[0]) + " " + str(ind)
		print >> f, "-----------------------------------------------------------------------------------"
	
	# begin evolution
	eaLoop(logbook, population, toolbox, ngen, stats, halloffame=halloffame)

	# run a simulation with visualisation enabled using the best chromosome
	playbackBest(toolbox.select(population, len(population)))
	return population, logbook


def eaLoop(logbook, population, toolbox, ngen, stats=None, halloffame=None, verbose=__debug__):

	# evolutionary loop copied largely from algorithms.eaSimple

	for gen in range(1, ngen + 1):

		# pause to free up CPU
		time.sleep(genSleep)
	
		# create the next generation
		elites = tools.selBest(population, eliteSize)		
		offspring = toolbox.select(population, len(population)-eliteSize)
		
		# Vary the pool of individuals
		offspring = varAnd(offspring, toolbox)
		
		# assign to a new population
		newPop = elites + offspring

		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in newPop if not ind.fitness.valid]
		fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit
			
		# print each fitness score and chromosome
		for ind in newPop:
			print str("%.2f" % ind.fitness.values[0]) + " " + str(ind)

		# Update the hall of fame with the generated individuals
		if halloffame is not None:
			halloffame.update(newPop)

		# Replace the current population by the offspring
		population[:] = newPop

		# Append the current generation statistics to the logbook
		record = stats.compile(population) if stats else {}
		logbook.record(gen=gen, nevals=len(invalid_ind), **record)
		if verbose:
			print "-----------------------------------------------------------------------------------"
			print logbook.stream
			print "-----------------------------------------------------------------------------------"
		
			
		# save each fitness score and chromosome to file
		with open('../log.txt', 'a') as f:
			for ind in newPop:
				print >> f, str("%.2f" % ind.fitness.values[0]) + " " + str(ind)
			print >> f, str(gen) + " -----------------------------------------------------------------------------------"
			
		# print the best chromosome
		best = getBest(toolbox.select(population, len(population)))
		print best
		
		# every tenth generation save parameters and best chromosome to file
		if (gen % 10 == 0):
			saveBest(gen, toolbox.select(population, len(population)))

	# save parameters and best chromosome to file if we haven't already
	if (gen % 10 != 0):
		saveBest(gen, toolbox.select(population, len(population)))


def evaluateRobot(individual):
	
	# save number of robots and chromosome to file
	with open('../chromosome.txt', 'w') as f:
		print >> f, sqrtRobots	
		print >> f, individual
	
	seed = 0	
	runningFitness = 0
	robots = {}
	for i in range(iterations):
		
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
		thisFitness /= sqrtRobots * sqrtRobots
		runningFitness += thisFitness
	
	# divide to get average per iteration
	fitness = runningFitness / iterations
	
	# pause to free up CPU
	time.sleep(evalSleep)
	
	return (fitness, )


class robotObject(object):

	def seqm2(one, two): print ""
	def selm2(one, two): print ""
	def probm2(one, two): print ""
	def seqm3(one, two): print ""
	def selm3(one, two): print ""
	def probm3(one, two): print ""
	def seqm4(one, two): print ""
	def selm4(one, two): print ""
	def probm4(one, two): print ""
	def mf(): print ""
	def ml(): print ""
	def mr(): print ""
	def ifltvar(): print ""
	def ifltcon(): print ""
	def ifgevar(): print ""
	def ifgecon(): print ""
	def successl(): print ""
	def failurel(): print ""
	def repeat(): print ""
	def successd(): print ""
	def failured(): print ""
	def bb(): print ""
	def rand(): print ""
	def repetitions(): print ""

class bbInput(): x = 1	
class constant(): x = 1
class repetitions(): x = 1


robot = robotObject()
pset = gp.PrimitiveSetTyped("MAIN", [], str)
pSettings = {}

nodeSettings()
addNodes()

creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=4)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


toolbox.register("evaluate", evaluateRobot)
toolbox.register("select", selTournament, tournsize=tournamentSize)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.register("mutSubtreeShrink", gp.mutShrink)
toolbox.register("mutNodeReplace", gp.mutNodeReplacement, pset=pset)
toolbox.register("mutConstantReplace", gp.mutEphemeral, mode="one")





def main():
	random.seed(deapSeed)

	pop = toolbox.population(n=populationSize)
	hof = tools.HallOfFame(1)
	
	stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values[0])
	stats_size = tools.Statistics(key=lambda depth: depth.height)
	mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	mstats.register("avg", numpy.mean)
	mstats.register("std", numpy.std)
	mstats.register("min", numpy.min)
	mstats.register("max", numpy.max)

	eaInit(pop, toolbox, generations, mstats, halloffame=hof)
    
	return pop, hof, mstats

if __name__ == "__main__":
	main()
