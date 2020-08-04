
import random
import time

from deap import gp
from deap import tools

from params import eaParams
from utilities import utilities

class customGP():
	
	params = eaParams()
	utils = utilities()	
	
	def __init(self):
		random.seed(self.params.deapSeed)

	def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):
		
		chosen = []
		for i in xrange(k):
			aspirants = tools.selRandom(individuals, tournsize)
			best = self.utils.getBest(aspirants)
			chosen.append(best)
		return chosen


	def varAnd(self, population, toolbox):
		
		# apply crossover and mutation
		
		offspring = [toolbox.clone(ind) for ind in population]
			
		# crossover
		for i in range(1, len(offspring), 2):
			if random.random() < self.params.crossoverProbability:
				offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
																			 offspring[i])
				del offspring[i - 1].fitness.values, offspring[i].fitness.values

		# mutation - subtree replacement
		for i in range(len(offspring)):
			if random.random() < self.params.mutSRProbability:
				offspring[i], = toolbox.mutSubtreeReplace(offspring[i])
				del offspring[i].fitness.values

		# mutation - subtree shrink
		for i in range(len(offspring)):
			if random.random() < self.params.mutSSProbability:
				offspring[i], = toolbox.mutSubtreeShrink(offspring[i])
				del offspring[i].fitness.values

		# mutation - node replacement
		for i in range(len(offspring)):
			if random.random() < self.params.mutNRProbability:
				offspring[i], = toolbox.mutNodeReplace(offspring[i])
				del offspring[i].fitness.values

		# mutation - ephemeral constant replacement
		for i in range(len(offspring)):
			if random.random() < self.params.mutECRProbability:
				offspring[i], = toolbox.mutConstantReplace(offspring[i])
				del offspring[i].fitness.values
				
		return offspring


	def eaInit(self, population, toolbox, ngen, stats=None, halloffame=None, verbose=__debug__):

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
			print >> f, str(time.time())[0:10]
			for ind in population:
				print >> f, str("%.2f" % ind.fitness.values[0]) + " " + str(ind)
			print >> f, "-----------------------------------------------------------------------------------"
		
		# begin evolution
		self.eaLoop(logbook, population, toolbox, ngen, stats, halloffame=halloffame)

		# run a simulation with visualisation enabled using the best chromosome
		self.utils.playbackBest(toolbox.select(population, len(population)))
		return population, logbook


	def eaLoop(self, logbook, population, toolbox, ngen, stats=None, halloffame=None, verbose=__debug__):

		# evolutionary loop copied largely from algorithms.eaSimple

		for gen in range(1, ngen + 1):

			# pause to free up CPU
			time.sleep(self.params.genSleep)
		
			# create the next generation
			elites = tools.selBest(population, self.params.eliteSize)		
			offspring = toolbox.select(population, len(population)-self.params.eliteSize)
			
			# Vary the pool of individuals
			offspring = self.varAnd(offspring, toolbox)
			
			# assign to a new population
			newPop = elites + offspring

			# Evaluate the individuals with an invalid fitness
			invalid_ind = [ind for ind in newPop if not ind.fitness.valid]
			fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
			for ind, fit in zip(invalid_ind, fitnesses):
				ind.fitness.values = fit
				
			# print each fitness score and chromosome
			for ind in newPop:
				print str("%.2f" % ind.fitness.values[0]) + " " + self.utils.printTree(ind)

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
					print >> f, str("%.2f" % ind.fitness.values[0]) + " " + self.utils.printTree(ind)
				print >> f, str(gen) + " -----------------------------------------------------------------------------------"
				
			# print the best chromosome
			best = self.utils.getBest(toolbox.select(population, len(population)))
			print self.utils.printTree(best)
			
			# every tenth generation save parameters and best chromosome to file
			if (gen % 10 == 0):
				self.utils.saveBest(gen, toolbox.select(population, len(population)))

		# save parameters and best chromosome to file if we haven't already
		if (gen % 10 != 0):
			self.utils.saveBest(gen, toolbox.select(population, len(population)))


	def genFull(self, pset, min_, max_, type_=None):
		
		# copied verbatim from deap gp module
		
		def condition(height, depth):
			return depth == height
		return self.generate(pset, min_, max_, condition, type_)


	def generate(self, pset, min_, max_, condition, type_=None):
		
		if type_ is None:
			type_ = pset.ret
		expr = []
		height = random.randint(min_, max_)
		stack = [(0, type_)]
		time.sleep(0.2)
		while len(stack) != 0:
			depth, type_ = stack.pop()
			if condition(height, depth):
				try:
					term = random.choice(pset.terminals[type_] + pset.conditions[type_] + pset.actions[type_])
				except IndexError:
					_, _, traceback = gp.sys.exc_info()
					raise IndexError, "The gp.generate function tried to add " \
											"a terminal of type '%s', but there is " \
											"none available." % (type_,), traceback
				
				if gp.isclass(term):
					term = term()
				
				if term.arity > 0:
					for arg in reversed(term.args):
						stack.append((depth + 1, arg))
				
				expr.append(term)
			else:
				primitiveAvailable = True
				try:
					prim = random.choice(pset.primitives[type_])
				except IndexError:
					primitiveAvailable = False
						 
				if primitiveAvailable:
					expr.append(prim)
					for arg in reversed(prim.args):
						stack.append((depth + 1, arg))
				else:
					try:
						term = random.choice(pset.terminals[type_] + pset.conditions[type_] + pset.actions[type_])
					except IndexError:
						_, _, traceback = gp.sys.exc_info()
						raise IndexError, "The gp.generate function tried to add " \
												"a terminal of type '%s', but there is " \
												"none available." % (type_,), traceback
					
					if gp.isclass(term):
						term = term()
					
					if term.arity > 0:
						for arg in reversed(term.args):
							stack.append((depth + 1, arg))
					
					expr.append(term)

		return expr

	def mutNodeReplacement(self, individual, pset):

		if len(individual) < 2:
			return individual
		
		# choose existing node at random
		index = random.randrange(1, len(individual))
		node = individual[index]
		type_ = node.ret
		
		# make sure we have a real node and not an ephemeral constant
		count = 0
		while count < 20 and node not in pset.conditions[type_] + pset.actions[type_]:
			count += 1
			index = random.randrange(1, len(individual))
			node = individual[index]
			type_ = node.ret
		
		if node not in pset.conditions[type_] + pset.actions[type_]:
			return
		
		# choose a replacement node at random
		prims = [p for p in pset.primitives[node.ret] + pset.conditions[node.ret] + pset.actions[node.ret] if p.children == node.children]
		prim = random.choice(prims)
		
		print "----"
		print self.utils.printTree(individual)
		print node.name + " to " + prim.name
		
		expr = [(prim)]
		if prim.arity > 0:
			for arg in prim.args:
				term = random.choice(pset.terminals[arg])
				if gp.isclass(term):
					term = term()
				expr.append(term)
		
		nodeSlice = individual.searchSubtree(index)
		individual[nodeSlice] = expr
		
		print self.utils.printTree(individual)
		print "---------"

		return individual,


