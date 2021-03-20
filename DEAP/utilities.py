
import time
import os
import math
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
		
		runningFitness = 0
		robots = {}
		seed = 0
		for i in self.params.arenaParams:
			
			# get maximum food available with the current gap between the nest and food
			maxFood = self.calculateMaxFood(i)
			
			for j in range(self.params.iterations):
				
				# write seed to file
				seed += 1
				with open('../seed.txt', 'w') as f:
					print >> f, seed
					print >> f, i

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
				
				# divide to get average for this iteration, normalise and add to running total
				thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
				thisFitness /= maxFood
				runningFitness += thisFitness
				
				# increment counter and pause to free up CPU
				time.sleep(self.params.trialSleep)
		
		# divide to get average per seed
		fitness = runningFitness / self.params.iterations

		# divide to get average per arena configuration and apply derating factor
		fitness = fitness / len(self.params.arenaParams)
		beforeDerated = fitness
		fitness *= self.deratingFactor(individual)

		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		return (fitness, )

	def evaluateSeeds(self, individual):
		
		# save number of robots and chromosome to file
		with open('../chromosome.txt', 'w') as f:
			print >> f, self.params.sqrtRobots
			print >> f, individual
		
		runningFitness = 0
		robots = {}
		seed = 10
		for i in self.params.arenaParams:
			
			# get maximum food available with the current gap between the nest and food
			maxFood = self.calculateMaxFood(i)
			
			for j in range(self.params.iterations):
				
				# write seed to file
				seed += 1
				with open('../seed.txt', 'w') as f:
					print >> f, seed
					print >> f, i

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
				
				# divide to get average for this iteration, normalise and add to running total
				thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
				
				thisFitness /= maxFood
				
				self.output += str("%.4f" % thisFitness)+","
				
				runningFitness += thisFitness
				
				# increment counter and pause to free up CPU
				time.sleep(self.params.trialSleep)
		
		# divide to get average per seed
		fitness = runningFitness / self.params.iterations

		# divide to get average per arena configuration and apply derating factor
		fitness = fitness / len(self.params.arenaParams)
		beforeDerated = fitness
		fitness *= self.deratingFactor(individual)

		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		return (fitness, )

	def calculateMaxFood(self, gap):
		
		turn180 = self.params.turn180
		forwards1m = self.params.forwards1m
		totalSteps = self.params.totalSteps
		
		journey = forwards1m * gap + 1
		firstTrip = journey * 2 + turn180
		otherTrips = journey * 2 + turn180 * 2
		
		return math.floor((totalSteps - firstTrip) / otherTrips) + 1

	def getBest(self, population):	
		
		# get the best member of the population
		
		for individual in population:		
			
			thisFitness = individual.fitness.getValues()[0]
			currentBest = False
			
			if ('best' not in locals()):
				currentBest = True
			
			elif (thisFitness > bestFitness):
				currentBest = True
			
			elif (thisFitness == bestFitness and bestHeight > 3 and individual.height < bestHeight):
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
		self.output += str("%.4f" % best.fitness.values[0])+","

	def unseenCases(self, best):
		self.output += ","
		self.params.iterations = self.params.unseenIterations
		for param in self.params.unseenParams:
			self.params.arenaParams = [param, param]
			fitness = self.evaluateRobot(best)
			self.output += str("%.4f" % fitness)+","
			print fitness
			time.sleep(self.params.evalSleep)
		
		self.output += ","
		
	def unseenSeeds(self, best):
		self.output += ","
		self.params.iterations = self.params.unseenIterations
		fitness = self.evaluateSeeds(best)
		self.output += ","+str("%.4f" % fitness)+",,"
		print fitness

	def logChromosome(self, best):
		# save the best member of the population to the log
		self.output += "\""+self.printTree(best)+"\", "
	
	def saveOutput(self):
		logHeaders = "Time,Seed,Robots,Population Size,Tournament Size,Elites,Iterations,Arena Params,Unseen Iterations,Unseen Params,Nodes,"
		logHeaders += "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,"
		logHeaders += "argos seeds:,11,12,13,14,15,16,17,18,19,20,,Average Unseen,,Chromosome"
		
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


