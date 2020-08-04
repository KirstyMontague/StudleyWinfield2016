
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

class PrimitiveSetTyped(object):

	def __init__(self, name, in_types, ret_type, prefix="ARG"):
		self.terminals = gp.defaultdict(list)
		self.primitives = gp.defaultdict(list)
		self.arguments = []
		# setting "__builtins__" to None avoid the context
		# being polluted by builtins function when evaluating
		# GP expression.
		self.context = {"__builtins__": None}
		self.mapping = dict()
		self.terms_count = 0
		self.prims_count = 0

		self.name = name
		self.ret = ret_type
		self.ins = in_types
		for i, type_ in enumerate(in_types):
			arg_str = "{prefix}{index}".format(prefix=prefix, index=i)
			self.arguments.append(arg_str)
			term = Terminal(arg_str, True, type_)
			self._add(term)
			self.terms_count += 1

	def renameArguments(self, **kargs):
		for i, old_name in enumerate(self.arguments):
			if old_name in kargs:
				new_name = kargs[old_name]
				self.arguments[i] = new_name
				self.mapping[new_name] = self.mapping[old_name]
				self.mapping[new_name].value = new_name
				del self.mapping[old_name]

	def _add(self, prim):
		def addType(dict_, ret_type):
			if ret_type not in dict_:
				new_list = []
				for type_, list_ in dict_.items():
					if issubclass(type_, ret_type):
						for item in list_:
							if item not in new_list:
								new_list.append(item)
				dict_[ret_type] = new_list

		addType(self.primitives, prim.ret)
		addType(self.terminals, prim.ret)

		self.mapping[prim.name] = prim
		if isinstance(prim, Primitive):
			for type_ in prim.args:
				addType(self.primitives, type_)
				addType(self.terminals, type_)
			dict_ = self.primitives
		else:
			dict_ = self.terminals

		for type_ in dict_:
			if issubclass(prim.ret, type_):
				dict_[type_].append(prim)

	def addPrimitive(self, primitive, in_types, ret_type, name=None):
	 
		if name is None:
			name = primitive.__name__
		prim = Primitive(name, in_types, ret_type)

		assert name not in self.context or \
			self.context[name] is primitive, \
		"Primitives are required to have a unique name. " \
		"Consider using the argument 'name' to rename your " \
		"second '%s' primitive." % (name,)

		self._add(prim)
		self.context[prim.name] = primitive
		self.prims_count += 1

	def addTerminal(self, terminal, ret_type, name=None):

		symbolic = False
		if name is None and callable(terminal):
			name = terminal.__name__

		assert name not in self.context, \
			"Terminals are required to have a unique name. " \
			"Consider using the argument 'name' to rename your " \
			"second %s terminal." % (name,)

		if name is not None:
			self.context[name] = terminal
			terminal = name
			symbolic = True
		elif terminal in (True, False):
			# To support True and False terminals with Python 2.
			self.context[str(terminal)] = terminal

		prim = Terminal(terminal, symbolic, ret_type)
		self._add(prim)
		self.terms_count += 1

	def addEphemeralConstant(self, name, ephemeral, ret_type):
	 
		module_gp = globals()
		if name not in module_gp:
			class_ = type(name, (Ephemeral,), {'func': staticmethod(ephemeral),
														  'ret': ret_type})
			module_gp[name] = class_
		else:
			class_ = module_gp[name]
			if issubclass(class_, Ephemeral):
				if class_.func is not ephemeral:
					raise Exception("Ephemerals with different functions should "
									    "be named differently, even between psets.")
				elif class_.ret is not ret_type:
					raise Exception("Ephemerals with the same name and function "
										 "should have the same type, even between psets.")
			else:
				raise Exception("Ephemerals should be named differently "
								   "than classes defined in the gp module.")

		self._add(class_)
		self.terms_count += 1

	def addADF(self, adfset):
		prim = Primitive(adfset.name, adfset.ins, adfset.ret)
		self._add(prim)
		self.prims_count += 1

	@property
	def terminalRatio(self):
		return self.terms_count / float(self.terms_count + self.prims_count)



class Primitive(object):
	
	__slots__ = ('name', 'arity', 'args', 'ret', 'seq')

	def __init__(self, name, args, ret):
		self.name = name
		self.arity = len(args)
		self.args = args
		self.ret = ret
		args = ", ".join(map("{{{0}}}".format, range(self.arity)))
		self.seq = "{name}({args})".format(name=self.name, args=args)

	def format(self, *args):
		return self.seq.format(*args)

	def __eq__(self, other):
		if type(self) is type(other):
			return all(getattr(self, slot) == getattr(other, slot)
						  for slot in self.__slots__)
		else:
			return NotImplemented


class Terminal(object):
	
	__slots__ = ('name', 'value', 'ret', 'conv_fct')

	def __init__(self, terminal, symbolic, ret):
		self.ret = ret
		self.value = terminal
		self.name = str(terminal)
		self.conv_fct = str if symbolic else repr

	@property
	def arity(self):
		return 0

	def format(self):
		return self.conv_fct(self.value)

	def __eq__(self, other):
		if type(self) is type(other):
			return all(getattr(self, slot) == getattr(other, slot)
						  for slot in self.__slots__)
		else:
			return NotImplemented


class Ephemeral(Terminal):

	def __init__(self):
		Terminal.__init__(self, self.func(), symbolic=False, ret=self.ret)

	@staticmethod
	def func():
		raise NotImplementedError
