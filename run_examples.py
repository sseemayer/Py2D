#!/usr/bin/env python2

import examples
from optparse import OptionParser

if __name__ == "__main__":

	op = OptionParser()
	op.add_option("-e", "--example", dest="example", help="Start with example EXAMPLE", metavar="EXAMPLE")
	(opt, args) = op.parse_args()


	if opt.example:

		er = examples.ExampleRunner()
		er.example = er.example_from_string(opt.example)
		er.main_loop()

	else:
		print("Please specify an example with the -e option!\nValid options:\n")

		for example in examples.Example.__subclasses__():
			mod = example.__module__.replace("examples.", "")
			print("{0}.{1}\t- {2}".format(mod, example.__name__, example.__doc__.split("\n")[0]))
