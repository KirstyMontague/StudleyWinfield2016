
import random


class eaParams():
	
	deapSeed = 1;
	sqrtRobots = 3;
	iterations = 2;
	populationSize = 10;
	tournamentSize = 3;
	eliteSize = 3;
	generations = 2;
	maxFood = 8;

	crossoverProbability = 0.8;
	mutSRProbability = 0.05; 		# mutUniform
	mutSSProbability = 0.1;  		# mutShrink
	mutNRProbability = 0.5;  		# mutNodeReplacement
	mutECRProbability = 0.5; 		# mutEphemeral
	
	genSleep = 10
	evalSleep = 5
	
	nodes = {}
	
	def __init__(self):
		self.genSleep = self.populationSize / 2
		self.evalSleep = (self.sqrtRobots * self.sqrtRobots * self.iterations) / 9
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

		if (self.nodes['successd']): pset.addPrimitive(robot.successd, [str],  str)
		if (self.nodes['failured']): pset.addPrimitive(robot.failured, [str],  str)

		if (self.nodes['repeat']):
			pset.addPrimitive(robot.repeat, [repetitionsConstant, str],  str)
			pset.addEphemeralConstant("repetitions", lambda: random.randint(1,9), repetitionsConstant)

		if (self.nodes['ifltvar']): pset.addPrimitive(robot.ifltvar, [bbReadIndex, bbReadIndex], str)
		if (self.nodes['ifltcon']): pset.addPrimitive(robot.ifltcon, [bbReadIndex, float], str)
		if (self.nodes['ifgevar']): pset.addPrimitive(robot.ifgevar, [bbReadIndex, bbReadIndex], str)
		if (self.nodes['ifgecon']): pset.addPrimitive(robot.ifgecon, [bbReadIndex, float], str)

		if (self.nodes['ifltvar'] or self.nodes['ifltcon'] or self.nodes['ifgevar'] or self.nodes['ifgecon']):
			pset.addEphemeralConstant("bbReadIndex", lambda: random.randint(1,9), bbReadIndex)

		if (self.nodes['mf']): pset.addTerminal(robot.mf, str)
		if (self.nodes['ml']): pset.addTerminal(robot.ml, str)
		if (self.nodes['mr']): pset.addTerminal(robot.mr, str)

		if (self.nodes['successl']): pset.addTerminal(robot.successl, str)
		if (self.nodes['failurel']): pset.addTerminal(robot.failurel, str)

		if (self.nodes['set']):
			pset.addPrimitive(robot.set, [bbWriteIndex, float],  str)
			pset.addEphemeralConstant("bbWriteIndex", lambda: random.randint(1,2), bbWriteIndex)

		if (self.nodes['set'] or self.nodes['ifltcon'] or self.nodes['ifgecon']):
			pset.addEphemeralConstant("bbConstant", lambda: random.uniform(-1, 1), float)


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
