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
  Mbase = import_relative('base', '.', 'trepan) # Adds trepan.io.base
  # The following adds trepan.lib.bytecode
  Mbytecode = import_relative('bytecode', '..lib', 'trepan) 

  class MyClass(Mio.InputBase): # Use name from Mio
     ...

  # like os.path.realpath(os.path.dirname(__file__))
  srcdir = get_srcdir() 

No import path searching is done. If the imports are not there, we fail. 

Rationale
=========

In my development, each module (which is a file in Python) can be run standalone. When called as a main program, it runs demo code. Each module is responsible for importing those other modules it needs. 

I have not been able to get relative imports to work nor have I been able to use *importlib* either in Python 2 or 3. They seem to error out because they can't find upper levels or something like that.

Bugs
====

Sorry, we don't do "from lists".

Various packing systems like pip and loaders may not work with this.
This code is fragile. 

I keep wanting to believe that there is already a way to develop out of the source code tree (not a copy of it as distutils is wont to do), not fiddle with search paths, and have demo code in modules so they can be run equally well as a main program and embedded as a module in the entire system. 

Until then, I have this.

