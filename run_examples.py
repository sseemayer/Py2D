#!/usr/bin/env python2

from py2d.examples.Main import ExampleRunner
from optparse import OptionParser

if __name__ == "__main__":

	op = OptionParser()
	op.add_option("-e", "--example", dest="example", default="Logo.Logo", help="Start with example EXAMPLE", metavar="EXAMPLE")
	(opt, args) = op.parse_args()

	er = ExampleRunner()
	er.example = er.example_from_string(opt.example)
	er.main_loop()
