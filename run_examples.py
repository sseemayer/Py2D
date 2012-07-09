#!/usr/bin/env python2

from py2d.examples.Main import ExampleRunner
from optparse import OptionParser

import os.path, pkgutil
import py2d.examples
import inspect
import py2d.examples.Main

def list_examples(startpath):

	pkgs = [name for _,name,_ in pkgutil.iter_modules([startpath])]

	examples = []
	for pkg in pkgs:
		importpath = startpath.replace("/",".") + pkg
		package = __import__(importpath, globals(), locals(), [importpath], -1)

		format_doc = lambda d: d.split("\n")[0] if d else ""

		examples.extend((("%s.%s" % (pkg, name), format_doc(obj.__doc__)) for name, obj in inspect.getmembers(package) \
		                               if inspect.isclass(obj) \
					       and issubclass(obj, py2d.examples.Main.Example) \
					       and name != "Example"))

	return examples


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
		print "\n".join( "%s:\t%s" % (a,b) for a,b in list_examples("py2d/examples/"))
