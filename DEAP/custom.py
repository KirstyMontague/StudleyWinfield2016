
import random
import time

from deap import gp
from deap import tools

from params import eaParams
from utilities import utilities
from primitives import Primitive
from primitives import Decorator
from primitives import Action
from primitives import Condition
from primitives import Ephemeral

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
		
		self.utils.logFirst()
		self.utils.logFitness(self.utils.getBest(population))
		
		# begin evolution
		self.eaLoop(logbook, population, toolbox, ngen, stats, halloffame=halloffame)

		# get the best individual at the end of the evolutionary run
		best = self.utils.getBest(population)
		
		# log chromosome and test performance in different environments
		self.utils.unseenSeeds(best)
		self.utils.logChromosome(best)
		
		# save and run simulation
		self.utils.saveOutput()
		self.utils.playbackBest(best)
		
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
			
			# print the best chromosome
			best = self.utils.getBest(population)
			self.utils.logFitness(best)
			print self.utils.printTree(best)


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
					# term = random.choice(pset.terminals[type_])
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
					# prim = random.choice(pset.primitives[type_])
					prim = random.choice(pset.primitives[type_] + pset.decorators[type_])
				except IndexError:
					primitiveAvailable = False
						 
				if primitiveAvailable:
					expr.append(prim)
					for arg in reversed(prim.args):
						stack.append((depth + 1, arg))
				else:
					try:
						# term = random.choice(pset.terminals[type_])
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

	def mutGenerate(self, pset, node):
		
		expr = [(node)]
		stack = []
		
		if node.arity > 0:
			for arg in reversed(node.args):
				stack.append((arg))
		
		while len(stack) != 0:
			type_ = stack.pop()
			try:
				term = random.choice(pset.terminals[type_])
			except IndexError:
				_, _, traceback = gp.sys.exc_info()
				raise IndexError, "The gp.generate function tried to add " \
										"a terminal of type '%s', but there is " \
										"none available." % (type_,), traceback
			
			if gp.isclass(term):
				term = term()
			
			expr.append(term)
			
		return expr

	def mutNodeReplacement(self, individual, pset):
		
		if len(individual) < 2:
			return individual,
		
		# choose existing node at random
		index = random.randrange(0, len(individual))
		node = individual[index]
		type_ = node.ret
		
		# make sure we have a real node and not an ephemeral constant
		count = 0
		while count < 20 and node not in pset.primitives[type_]+ pset.decorators[type_] + pset.conditions[type_] + pset.actions[type_]:
			count += 1
			index = random.randrange(0, len(individual))
			node = individual[index]
			type_ = node.ret
		
		if node not in pset.primitives[type_] + pset.decorators[type_] + pset.conditions[type_] + pset.actions[type_]:
			return individual,
		
		# choose a replacement node at random
		newlist = []
		if node in pset.primitives[node.ret] + pset.decorators[node.ret]:
			newList = pset.primitives[node.ret] + pset.decorators[node.ret]
		else:
			newList = pset.conditions[node.ret] + pset.actions[node.ret]
		prims = [p for p in newList if p.children == node.children]
		prim = random.choice(prims)
		
		# replace the selected node with one of the new type
		expr = [(prim)]
		if prim.arity > 0:
			for arg in prim.args:
				if arg not in prim.children:
					# this argument is a constant so generate a new one
					term = random.choice(pset.terminals[arg])
					if gp.isclass(term):
						term = term()
					expr.append(term)
				else:
					# this agument is a child node so keep it intact
					nodeSlice = individual.searchSubtree(index + len(expr))
					expr = expr + individual[nodeSlice]
			
			# replace node and subtree with new expression
			nodeSlice = individual.searchSubtree(index)
			exprSlice = slice(0, len(expr))
			individual[nodeSlice] = expr[exprSlice]
		else:
			# replace node with new primitive
			nodeSlice = individual.searchSubtree(index)
			primSlice = slice(0, 1)
			individual[nodeSlice] = [(prim)][primSlice]
		
		return individual,

	def mutShrinkToChild(self, individual, pset):

		if len(individual) < 3 or individual.height <= 1:
			return individual,

		iprims = []
		for i, node in enumerate(individual[1:], 1):
			if (node in pset.primitives[node.ret] + pset.decorators[node.ret]) and node.ret in node.args:
				iprims.append((i, node))

		if len(iprims) != 0:
			index, prim = random.choice(iprims)
			arg_idx = random.choice([i for i, type_ in enumerate(prim.args) if type_ == prim.ret])
			rindex = index + 1
			for _ in range(arg_idx + 1):
				rslice = individual.searchSubtree(rindex)
				subtree = individual[rslice]
				rindex += len(subtree)

			slice_ = individual.searchSubtree(index)
			individual[slice_] = subtree

		return individual,

	def mutShrinkToTerminal(self, individual, pset):

		if len(individual) < 3 or individual.height <= 1:
			return individual,

		iprims = []
		for i, node in enumerate(individual[1:], 1):
			if (node in pset.primitives[node.ret] + pset.decorators[node.ret]) and node.ret in node.args:
				iprims.append((i, node))

		if len(iprims) != 0:
			primIndex, prim = random.choice(iprims)
			primSlice = individual.searchSubtree(primIndex)

			iterms = []
			for i, node in enumerate(individual[primSlice], 1):
				if node in pset.actions[prim.ret] + pset.conditions[prim.ret]:
					iterms.append((i, node))

			termIndex, term = random.choice(iterms)
			termIndex += primIndex
			termSlice = individual.searchSubtree(termIndex - 1)
			subtree = individual[termSlice]

			primSlice = individual.searchSubtree(primIndex)
			individual[primSlice] = subtree

		return individual,

	def cxOnePoint(self, ind1, ind2):

		if len(ind1) < 2 or len(ind2) < 2:
			return ind1, ind2

		type_ = ind1.root.ret
		
		selection1 = [i for i, node in enumerate(ind1[1:], 1) if node.ret == type_]
		selection2 = [i for i, node in enumerate(ind2[1:], 1) if node.ret == type_]
		
		if len(selection1) == 0 or len(selection2) == 0:
			return ind1, ind2
		
		index1 = random.choice(selection1)
		index2 = random.choice(selection2)

		slice1 = ind1.searchSubtree(index1)
		slice2 = ind2.searchSubtree(index2)
		ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

		return ind1, ind2




	def mutEphemeral(self, individual, pset):

		ephemerals_idx = [index
								for index, node in enumerate(individual)
								if isinstance(node, Ephemeral)]

		if len(ephemerals_idx) > 0:
			ephemerals_idx = (random.choice(ephemerals_idx),)
			for i in ephemerals_idx:
				if type(individual[i]) in pset.bbReadIndexes or type(individual[i]) in pset.bbWriteIndexes:
					individual[i] = type(individual[i])()
				elif type(individual[i]) in pset.repetitions:
					print "=========================== reps ==========================="
					print individual
					
					magnitude = 0
					if random.random() < .33: magnitude = 2
					else: magnitude = 1
					
					direction = 0;
					if random.random() < .5: direction = -1
					else: direction = 1
					
					newValue = individual[i].value + (magnitude * direction)
					if newValue > 9: newValue = 9
					elif newValue < 1: newValue = 1
					
					print newValue
					individual[i].value = newValue
					print individual
					print ""
				else:
					print "=========================== constant ==========================="
					print individual
					print individual[i].value
					newValue = self.utils.gaussian(individual[i].value, .05)
					print newValue
					individual[i].value = newValue
					print individual
					print ""
		
		return individual,

	def mutUniformInner(self, individual, expr, pset):
		
		type_ = individual.root.ret
		
		if random.random() < 0.9:
			psets = pset.decorators[type_] + pset.primitives[type_]
		else:
			psets = pset.actions[type_] + pset.conditions[type_]
		
		nodeSet = [i for i, node in enumerate(individual[1:], 1) if node in psets]
		
		if (len(nodeSet) > 0): index = random.choice(nodeSet)
		else: index = random.choice([i for i, node in enumerate(individual[1:], 1) if node.ret == type_])
		
		print individual
		print index
		print individual[index].name
		
		slice_ = individual.searchSubtree(index)
		type_ = individual[index].ret
		individual[slice_] = expr(pset=pset, type_=type_)
		
		print individual
		print ""
		
		return individual,

	def mutNodeReplacementInner(self, individual, pset):
		
		if len(individual) < 2:
			return individual,
		
		# choose existing node at random
		type_ = individual.root.ret
		
		if random.random() < 0.9:
			psets = pset.decorators[type_] + pset.primitives[type_]
		else:
			psets = pset.actions[type_] + pset.conditions[type_]
		
		nodeSet = [i for i, node in enumerate(individual[1:], 1) if node in psets]
		
		if (len(nodeSet) > 0): index = random.choice(nodeSet)
		else: index = random.choice([i for i, node in enumerate(individual[1:], 1) if node.ret == type_])
		
		node = individual[index]
		
		print individual
		print index
		print individual[index].name
		
		# make sure we have a real node and not an ephemeral constant
		count = 0
		while count < 20 and node not in pset.primitives[type_]+ pset.decorators[type_] + pset.conditions[type_] + pset.actions[type_]:
			count += 1
			index = random.randrange(0, len(individual))
			node = individual[index]
			type_ = node.ret
		
		if node not in pset.primitives[type_] + pset.decorators[type_] + pset.conditions[type_] + pset.actions[type_]:
			return individual,
		
		# choose a replacement node at random
		newlist = []
		if node in pset.primitives[node.ret] + pset.decorators[node.ret]:
			newList = pset.primitives[node.ret] + pset.decorators[node.ret]
		else:
			newList = pset.conditions[node.ret] + pset.actions[node.ret]
		prims = [p for p in newList if p.children == node.children]
		prim = random.choice(prims)
		
		# replace the selected node with one of the new type
		expr = [(prim)]
		if prim.arity > 0:
			for arg in prim.args:
				if arg not in prim.children:
					# this argument is a constant so generate a new one
					term = random.choice(pset.terminals[arg])
					if gp.isclass(term):
						term = term()
					expr.append(term)
				else:
					# this agument is a child node so keep it intact
					nodeSlice = individual.searchSubtree(index + len(expr))
					expr = expr + individual[nodeSlice]
			
			# replace node and subtree with new expression
			nodeSlice = individual.searchSubtree(index)
			exprSlice = slice(0, len(expr))
			individual[nodeSlice] = expr[exprSlice]
		else:
			# replace node with new primitive
			nodeSlice = individual.searchSubtree(index)
			primSlice = slice(0, 1)
			individual[nodeSlice] = [(prim)][primSlice]
		
		print individual
		print ""
		
		return individual,

	def cxOnePointInner(self, ind1, ind2, pset):

		if len(ind1) < 2 or len(ind2) < 2:
			return ind1, ind2

		print self.utils.printTree(ind1)
		print self.utils.printTree(ind2)
		type_ = ind1.root.ret
		
		if random.random() < 0.9:
			psets = pset.decorators[type_] + pset.primitives[type_]
		else:
			psets = pset.actions[type_] + pset.conditions[type_]
			
		set1 = [i for i, node in enumerate(ind1[1:], 1) if node in psets]
		set2 = [i for i, node in enumerate(ind2[1:], 1) if node in psets]
		
		print set1
		print set2
		
		if (len(set1) > 0): index1 = random.choice(set1)
		else: index1 = random.choice([i for i, node in enumerate(ind1[1:], 1) if node.ret == type_])
		
		if (len(set2) > 0): index2 = random.choice(set2)
		else: index2 = random.choice([i for i, node in enumerate(ind2[1:], 1) if node.ret == type_])

		print ind1[index1].name
		print ind2[index2].name
		
		slice1 = ind1.searchSubtree(index1)
		slice2 = ind2.searchSubtree(index2)
		ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

		print self.utils.printTree(ind1)
		print self.utils.printTree(ind2)
		print ""
		
		return ind1, ind2



