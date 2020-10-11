
import random


class eaParams():
	
	deapSeed = 5
	sqrtRobots = 3
	populationSize = 25
	tournamentSize = 3
	eliteSize = 3
	generations = 50

	crossoverProbability = .8
	mutSRProbability = 0.05 		# mutUniform
	mutSSProbability = 0.1  		# mutShrink
	mutNRProbability = 0.5  		# mutNodeReplacement
	mutECRProbability = 0.5 		# mutEphemeral

	# evaluation parameters for evolving and testing
	iterations = 2
	arenaParams = [.3, .9]
	unseenIterations = 2
	unseenParams = [.3, .4, .5, .6, .7, .8, .9, 1.0]

	# timesteps required to turn and move, and total timesteps available
	turn180 = 72
	forwards1m = 160
	totalSteps = 2400

	genSleep = 10
	evalSleep = 5
	trialSleep = 0
	
	nodes = {}
	
	def __init__(self):
		self.genSleep = self.populationSize / 2
		self.evalSleep = (self.sqrtRobots * self.sqrtRobots * self.iterations) / 9
		self.trialSleep = .5
		print self.genSleep
		print self.evalSleep
		self.nodes = {
			"selm2" : True,
			"selm3" : True,
			"selm4" : True,
			"seqm2" : True,
			"seqm3" : True,
			"seqm4" : True,
			"probm2" : True,
			"probm3" : True,
			"probm4" : True,
			"repeat" : True,
			"successd" : True,
			"failured" : True,
			"ifltvar" : True,
			"ifltcon" : True,
			"ifgevar" : True,
			"ifgecon" : True,
			"mf" : True,
			"mr" : True,
			"ml" : True,
			"set" : True,
			"successl" : True,
			"failurel" : True
		}

	def addNodes(self, pset):
		
		robot = robotObject()

		if (self.nodes['selm2']): pset.addPrimitive(robot.selm2, [str, str],  str)
		if (self.nodes['seqm2']): pset.addPrimitive(robot.seqm2, [str, str],  str)
		if (self.nodes['probm2']): pset.addPrimitive(robot.probm2, [str, str],  str)
		if (self.nodes['selm3']): pset.addPrimitive(robot.selm3, [str, str, str],  str)
		if (self.nodes['seqm3']): pset.addPrimitive(robot.seqm3, [str, str, str],  str)
		if (self.nodes['probm3']): pset.addPrimitive(robot.probm3, [str, str, str],  str)
		if (self.nodes['selm4']): pset.addPrimitive(robot.selm4, [str, str, str, str],  str)
		if (self.nodes['seqm4']): pset.addPrimitive(robot.seqm4, [str, str, str, str],  str)
		if (self.nodes['probm4']): pset.addPrimitive(robot.probm4, [str, str, str, str],  str)

		if (self.nodes['successd']): pset.addDecorator(robot.successd, [], [str],  str)
		if (self.nodes['failured']): pset.addDecorator(robot.failured, [], [str],  str)
		if (self.nodes['repeat']): pset.addDecorator(robot.repeat, [repetitionsConstant], [str],  str)

		if (self.nodes['ifltvar']): pset.addCondition(robot.ifltvar, [bbReadIndex, bbReadIndex], str)
		if (self.nodes['ifltcon']): pset.addCondition(robot.ifltcon, [bbReadIndex, float], str)
		if (self.nodes['ifgevar']): pset.addCondition(robot.ifgevar, [bbReadIndex, bbReadIndex], str)
		if (self.nodes['ifgecon']): pset.addCondition(robot.ifgecon, [bbReadIndex, float], str)

		if (self.nodes['mf']): pset.addAction(robot.mf, [], str)
		if (self.nodes['ml']): pset.addAction(robot.ml, [], str)
		if (self.nodes['mr']): pset.addAction(robot.mr, [], str)
		if (self.nodes['successl']): pset.addAction(robot.successl, [], str)
		if (self.nodes['failurel']): pset.addAction(robot.failurel, [], str)
		if (self.nodes['set']): pset.addAction(robot.set, [bbWriteIndex, float], str)

		pset.addEphemeralConstant("bbWriteIndex", lambda: random.randint(1,2), bbWriteIndex)
		pset.addEphemeralConstant("bbReadIndex", lambda: random.randint(1,9), bbReadIndex)
		pset.addEphemeralConstant("bbConstant", lambda: random.uniform(-1, 1), float)
		pset.addEphemeralConstant("repetitions", lambda: random.randint(1,9), repetitionsConstant)

class robotObject(object):

	def action(): print ""
	def seqm2(one, two): print ""
	def selm2(one, two): print ""
	def probm2(one, two): print ""
	def seqm3(one, two): print ""
	def selm3(one, two): print ""
	def probm3(one, two): print ""
	def seqm4(one, two): print ""
	def selm4(one, two): print ""
	def probm4(one, two): print ""
	def set(): print ""
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

class bbReadIndex(): x = 1
class bbWriteIndex(): x = 1
class bbConstant(): x = 1
class repetitionsConstant(): x = 1
