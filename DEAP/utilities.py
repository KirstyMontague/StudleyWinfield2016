
import time
import os
import subprocess
from params import eaParams

import numpy
from numpy import random

class utilities():
	
	params = eaParams()
	numpy.random.seed(0)
	output = ""
		
	def evaluateRobot(self, individual):
		
		# save number of robots and chromosome to file
		with open('../chromosome.txt', 'w') as f:
			print >> f, self.params.sqrtRobots
			print >> f, individual
		
		counter = 0
		runningFitness = 0
		robots = {}
		for i in range(self.params.iterations):
			
			# write seed to file
			with open('../seed.txt', 'w') as f:
				print >> f, counter + 1
				print >> f, self.params.arenaParams[counter]
			counter += 1
			
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
			thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
			runningFitness += thisFitness
			
			# pause to free up CPU
			time.sleep(self.params.trialSleep)
			
		# divide to get average per iteration and normalise
		fitness = runningFitness / self.params.iterations
		fitness = fitness / self.params.maxFood
		
		# apply derating factor to large trees
		fitness *= self.deratingFactor(individual)

		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		return (fitness, )


	def getBest(self, population):	
		
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


	def logFirst(self):
		
		# save parameters to the output
		
		self.output = str(time.time())[0:10]+", "
		self.output += str(self.params.deapSeed)+", "
		self.output += str(self.params.sqrtRobots)+", "
		self.output += str(self.params.populationSize)+", "
		self.output += str(self.params.tournamentSize)+", "
		self.output += str(self.params.eliteSize)+", "
		
		self.output += str(self.params.iterations)+", "

		for param in self.params.arenaParams:
			self.output += str(param)+" "
		self.output += ","
		
		self.output += str(self.params.unseenIterations)+", "

		for param in self.params.unseenParams:
			self.output += str(param)+" "
		self.output += ","
		
		self.output += "\""
		for node in sorted(self.params.nodes):
			if (self.params.nodes[node]):
				self.output += node+", "
		self.output += "\","

	def logFitness(self, best):
		# save the best fitness to the output
		self.output += str("%.4f" % best.fitness.values[0])+", "

	def unseenCases(self, best):
		self.params.iterations = self.params.unseenIterations
		for param in self.params.unseenParams:
			self.params.arenaParams = [param, param]
			fitness = self.evaluateRobot(best)
			self.output += str("%.4f" % fitness)+","
			print fitness
		
		self.output += ","

	def logChromosome(self, best):
		# save the best member of the population to the log
		self.output += "\""+self.printTree(best)+"\", "
	
	def saveOutput(self):
		logHeaders = "Time,Seed,Robots,Population Size,Tournament Size,Elites,Iterations,Arena Params,Unseen Iterations,Unseen Params,Nodes,"
		print self.output
		with open('../es.csv', 'a') as f:
			# print >> f, logHeaders
			print >> f, self.output


	def saveBest(self, gen, population):
		
		# save the best member of the population to the log
		
		best = self.getBest(population)
		
		logHeaders = "Time,Seed,Robots,Iterations,Population Size,Tournament Size,Elites,Generations,Fitness,Chromosome,Nodes"

		logString = str(time.time())[0:10]+", "
		logString += str(self.params.deapSeed)+", "
		logString += str(self.params.sqrtRobots)+", "
		logString += str(self.params.iterations)+", "
		logString += str(self.params.populationSize)+", "
		logString += str(self.params.tournamentSize)+", "
		logString += str(self.params.eliteSize)+", "
		logString += str(gen)+", "
		logString += str("%.4f" % best.fitness.values[0])+", "
		logString += "\""+self.printTree(best)+"\", "
		
		logString += "\""
		for node in sorted(self.params.nodes):
			if (self.params.nodes[node]):
				logString += node+", "
		logString += "\""
		
		with open('../log.csv', 'a') as f:
			# print >> f, logHeaders
			print >> f, logString

	def playbackBest(self, best):
		
		# run a simulation with visualisation using the best chromosome
		
		with open('../best.txt', 'w') as f:
			print >> f, self.params.sqrtRobots	
			print >> f, best		
			
		subprocess.call(["/bin/bash", "playback", "", "./"])

	def deratingFactor(self, individual):

		height = float(individual.height)
		length = float(len(individual))	
		
		rUsage = height / 30
		if (length / 140 > rUsage):
			rUsage = length / 140
		
		factor = 1
		if rUsage > .75:
			rUsage -= .75
			factor = 1 - (rUsage * 4)
			if factor < 0:
				factor = 0
		
		return factor

	def printTree(self, tree):
		
		string = ""
		stack = []
		for node in tree:
			stack.append((node, []))
			while len(stack[-1][1]) == stack[-1][0].arity:
				prim, args = stack.pop()
				string = prim.format(*args)
				if (string[1:4].find(".") >= 0): string = string[0:5]
				if len(stack) == 0:
					break  # If stack is empty, all nodes should have been seen
				stack[-1][1].append(string)

		return string

	def gaussian(self, num, stdDev):
		
		magnitude = num * num
		magnitude = magnitude**(.5)
		magnitude = magnitude/10
		x = random.normal(loc=num, scale=magnitude)
		print x
		if (x < -1): x = -1 + (x - -1)
		if (x > 1): x = 1 - (x - 1)
		
		return x


