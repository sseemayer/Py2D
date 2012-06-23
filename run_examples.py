#!/usr/bin/env python2

from py2d.examples.Main import ExampleRunner
from optparse import OptionParser

import os.path, pkgutil
import py2d.examples
import inspect
import py2d.examples.Main

def list_examples(startpath):

	pkgs = [name for _,name,_ in pkgutil.iter_modules([startpath])]

	for pkg in pkgs:
		importpath = startpath.replace("/",".") + pkg
		package = __import__(importpath, globals(), locals(), [importpath], -1)

		for name, obj in inspect.getmembers(package):
			if inspect.isclass(obj):
				if issubclass(obj, py2d.examples.Main.Example):
					desc = obj.__doc__
					if desc:
						desc = desc.split("\n")[0]
					print "%s.%s:\t%s" % (pkg, name, desc)

def example_from_string(self, example_name):
	import inspect


	package_name, class_name = example_name.rsplit('.', 1)
	package = __import__(package_name, globals(), locals(), [class_name], -1)
	
	cls = next((c[1] for c in inspect.getmembers(package, inspect.isclass) if c[0] == class_name))

	return cls(self)



if __name__ == "__main__":

	op = OptionParser()
	op.add_option("-e", "--example", dest="example", help="Start with example EXAMPLE", metavar="EXAMPLE")
	(opt, args) = op.parse_args()


	if opt.example:

		er = ExampleRunner()
		er.example = er.example_from_string(opt.example)
		er.main_loop()

	else:
		print "Please specify an example with the -e option!\nValid options:\n"
		list_examples("py2d/examples/")
