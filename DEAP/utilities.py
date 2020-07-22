
import time
import os
import subprocess
from params import eaParams

# from params import eaParams

class utilities():
	
	params = eaParams()
	
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
		logString += str("%.2f" % best.fitness.values[0])+", "
		logString += "\""+str(best)+"\", "
		
		logString += "\""
		
		for node in sorted(self.params.nodes):
			if (self.params.nodes[node]):
				logString += node+", "
		logString += "\""
		
		with open('../best-log.csv', 'a') as f:
			# print >> f, logHeaders
			print >> f, logString


	def playbackBest(self, population):
		
		# run a simulation with visualisation using the best chromosome
		
		best = self.getBest(population)
		
		with open('../best.txt', 'w') as f:
			print >> f, self.params.sqrtRobots	
			print >> f, best		
			
		os.rename('../log.txt', '../logs/log-'+str(time.time())[0:10]+'.txt')
		
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

