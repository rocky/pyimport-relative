# -*- coding: utf-8 -*-
"""
Introduction
============


More akin to *require_relative* of Ruby than Python's *import_relative* .

When you have a large package that contains nested submodules this allows the nested submodules to refer to one another without having to pull in or know much about or explicitly import entire top-level tree.

Synopsis
========

::

  from import_relative import import_relative, get_srcdir
  # Below "trepan" is my top-level namespace
  # 'io' is the directory this file is in.
  Mbase = import_relative('base', '.', 'trepan') # Adds trepan.io.base
  # The following adds trepan.lib.bytecode
  Mbytecode = import_relative('bytecode', '..lib', 'trepan')

  class MyClass(Mbase.InputBase): # Use name from Mbase
     ...

  # NOTE; if your module name is "io" import like this:
  Mio = import_relative('trepan.io', '..')
  # rather than
  Mio = import_relative('io', '..trepan')

  # like os.path.realpath(os.path.dirname(__file__))
  srcdir = get_srcdir()
  srcdir = get_srcdir(1) # same as above
  srcdir = get_srcdir(2) # my caller's os.path.realpath(os.path.dirname(__file__)

No import path searching is done. If the imports are not there, we fail.

Rationale
=========

In my development, each module (which is a file in Python) can be run standalone. When called as a main program, it runs demo code. Each module is responsible for importing those other modules it needs.

I have not been able to get relative imports to work. For example I get among the error messages:

::
    ValueError: Attempted relative import in non-package

or using python's `-m` switch:

::
   Import by filename is not supported.

Nor have I been able to use *importlib* either in Python 2 or 3. They seem to error out because they can't find upper-level modules or something like that.

Bugs
====

Sorry, we don't do "from lists".

When importing a simple name like "io" or "format" which might be around elsewhere you should add enough of the parent namespace to make the package unique.

That is instead of

::
    Mio = import_relative('io', '.')

or

::
    Mio = import_relative('io', '..trepan')

use:

::
    Mio = import_relative('trepan.io', '..')

Here is another example I ran into. Instead of:

::
    Mformat = import_relative('format', '..lib', 'pydbgr')

use:

::
    Mformat = import_relative('lib.format', '...pydbgr')

Various packing systems like pip and loaders may not work with this.
This code is fragile. Down the line I'll probably redo to integrate with Python 3's [http://docs.python.org/3/library/importlib.html importlib] better.


I keep wanting to believe that there is already a way to develop out of the source code tree (not a copy of it as distutils is wont to do), not fiddle with search paths, and have demo code in modules so they can be run equally well as a main program and embedded as a module in the entire system.

Until then, I have this.

See `Pydbgr <https://code.google.com/p/pydbgr/>` or `Python3-trepan <https://code.google.com/p/python3-trepan/>` for large projects that use this.
"""
__docformat__ = 'restructuredtext'
__all__ = ['import_relative']
