
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(	name='py2d',
	version='0.1',
	description='Py2D library of 2D-game-related algorithms',
	url='http://www.github.com/sseemayer/py2d',

	author='Stefan Seemayer',
	author_email='mail@semicolonsoftware.de',

	packages=['py2d', 'py2d.Math'],
	cmdclass = {'build_ext': build_ext},
	ext_modules = [
		Extension("py2d.Bezier", ["py2d/Bezier.py"]),
		Extension("py2d.FOV", ["py2d/FOV.py"]),
		Extension("py2d.FOVConverter", ["py2d/FOVConverter.py"]),
		Extension("py2d.Navigation", ["py2d/Navigation.py"]),
		Extension("py2d.SVG", ["py2d/SVG.py"]),
		Extension("py2d.Math", ["py2d/Math/__init__.py"]),
		Extension("py2d.Math.Operations", ["py2d/Math/Operations.py"]),
		Extension("py2d.Math.Polygon", ["py2d/Math/Polygon.py"]),
		Extension("py2d.Math.Transform", ["py2d/Math/Transform.py"]),
		Extension("py2d.Math.Vector", ["py2d/Math/Vector.py"]),
	]
)
