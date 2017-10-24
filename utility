class CmdLine:
	'''
	Simple command line parser.
	This class parses command line given in form app.exe [option]...[option],
	where option is -opt_name [arg1]...[arg2].
	'''
	def __init__(self, argv):
		'''Parse command line and construct object.'''
		
		self.options = {}
		param = ""
		for i in range(0, len(argv)):
			argvi = argv[i]
			if argvi[0] == '-':
				param = argvi[1:]
				if param not in self.options :
					self.options[param] = []
			else:
				if len(param) == 0:
					continue
				self.options[param].append(argvi)
	
	#------------------------------------------------------------
	# Member functions
	#------------------------------------------------------------
	def getParam(self, param_name, is_mandatory):
		'''
		Get information about parameter.
		Throw object of class CmdLine::Exception if mandatory parameter is missing.
		param_name    - Name of parameter without '-'.
		is_mandatory  - Set to true for mandatory parameter.
		return
		-1 parameter is missing (for optional parameters) 
		0  parameter is a switch
		>0 number of values associated with given parameter
		'''
		
		if param_name in self.options:
			return len(self.options[param_name])
		else:
			if is_mandatory == 1:
				raise OmdExampleException("Mandatory parameter '" + str(param_name) + "' is missing")
			else:
				return -1
	
	def getValue(self, param_name, n = 0, default = None):
		'''
		Retrieve the n-th value of parameter.
		Throw object of class OmdExampleException if parameter or value is missing and
		default is None. If Default is passed then default value is returned.
		param_name - Name of parameter without '-'.
		 n          - Index in array of associated values started from 0. 
		 default    - This value will be returned if parameter or value is missing. 
		 return     - The n-th value of parameter.
		'''
		if param_name in self.options:
			v = self.options[param_name]
			if n >= 0 and n < len(v):
				return v[n]
		if default != None :
			return default
		else :
			raise OmdExampleException("Value for parameter '" + str(param_name) + "' is missing")
	
	def __str__(self):
		'''Output object to the standart output'''
		return self.options.__str__()
