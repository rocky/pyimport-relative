A relative import of a module for older versions of Python (i.e. pre 2.6) or where you want this feature and need it to be compatible with older versions of Python. In contrast to Python's relative imports and Python 2.7 and 3.x's import\_lib, you might not have to always import upper levels.

As per import() sans "from lists" which is used here, we always
return the top-level import name even when a compound import
(e.g. a.b.c) is given.

Sorry, we don't do "from lists".

# Synopsis #

```
  from import_relative import import_relative, get_srcdir

  Mbase_proc = import_relative('base_proc', '.', 'pydbgr')
  Mbytecode  = import_relative('bytecode', '..lib', 'pydbgr')

  srcdir = get_srcdir() # like os.path.dirname(__file__)
```
