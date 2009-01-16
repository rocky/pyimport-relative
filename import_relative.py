import imp, os, re, sys
def get_srcdir(level=1):
    ''' Get directory of caller as an absolute file name. `level' is
    the number of frames to look back.  So for import file which is
    really doing work on behalf of *its* caller, we go back 2.

    NB: f_code.co_filenames and thus this code kind of broken for
    zip'ed eggs circa Jan 2009
    '''
    caller = sys._getframe(level)
    filename = caller.f_code.co_filename
    return os.path.normcase(os.path.dirname(os.path.abspath(filename)))

re_dots = re.compile(r'^\.+$')

def import_relative(import_name, path=None):
    '''Import `import_name' using `path' as the location to start
    looking for it.  If `path' is not given, we'll look starting in
    the directory where the import_relative was issued. As per
    __import__() which this uses, we alway return the top-level import
    name even when a compound import (e.g. a.b.c) is given.  Sorry, we
    don't do "from lists", global or local variables here.

    TODO: add a package/namespace parameter for which to add the name under.
    '''

    # Turn path into an absolute file name.
    if path is None:
        srcdir = get_srcdir(2)
    elif os.path.sep == path[0]:
        srcdir = path
    else:
        # Check for ., .., ...
        if re_dots.match(path):
            d = os.path.pardir
            for i in range(len(path)-2):
                d = os.path.join(d, os.path.pardir)
                pass
            path = d
            pass
        srcdir = os.path.abspath(os.path.join(get_srcdir(2), path))
        pass

    import_modules = import_name.split('.')
    top_module = import_modules[0]
    last_module =  import_modules[-1]
    top_file_prefix = os.path.join(srcdir, top_module)
  
    mod = sys.modules.get(top_module)
    if not mod or not mod.__file__.startswith(top_file_prefix):

        # If any of the following calls raises an exception,
        # there's a problem we can't handle -- let the caller handle it.
        
        fp, pathname, description = imp.find_module(top_module, [srcdir])
        
        module_save = None
        if sys.modules.get(top_module):
            # Temporarily nuke module so we will have to find it anew using
            # our hacked sys.path.
            fn = sys.modules[top_module].__file__
            if not fn.startswith(os.path.join(srcdir, top_module)):
                module_save = sys.modules[top_module]
                del sys.modules[top_module]
                pass
            pass
        try:
            mod = imp.load_module(top_module, fp, pathname, description)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
                pass
            if module_save:
                sys.modules[top_module] = module_save
                pass
            pass
        pass

    # find_module module doesn't seem to work for compounds,
    # e.g. imp.find_module('a.b', '/path/to/a').  Maybe when I
    # understand 'knee' from:
    # http://docs.python.org/library/imputil.html better. (It seems
    # to be a translation into Python of its C code).
    # 
    # Until then, So we'll use this hacky method which doesn't deal
    # with "from .. import .. as .." renaming which would need to look
    # at __name__.
    
    prefix = top_module
    prev   = mod
    del import_modules[0]
    for mod_name in import_modules:
        prefix += '.' + mod_name
        module_save = None
        if sys.modules.get(prefix):
            # Temporarily nuke module so we will have to find it anew using
            # our hacked sys.path.
            fn = sys.modules[prefix].__file__
            if not fn.startswith(os.path.join(srcdir, top_module)):
                module_save = sys.modules[prefix]
                del sys.modules[prefix]
                pass
            pass
        try:
            next_mod = __import__(name = prefix,
                                  fromlist=['__bogus__'])
        except:
            break
        finally:
            if module_save:
                sys.modules[prefix] = module_save
                pass
            pass
        
        if hasattr(next_mod, '__path__'):
            np = next_mod.__path__
            np[0], np[-1] = np[-1], np[0]
            pass
        setattr(prev, mod_name, next_mod)
        prev = next_mod
        pass

    return mod

# Demo it
if __name__=='__main__':
    import_relative = import_relative('import_relative')
    print import_relative
    print import_relative.__name__
    print import_relative.__file__
    # The 2nd time around, we should have info cached.
    # Can you say Major Major?
    import_relative2 = import_relative.import_relative('import_relative',
                                                       os.curdir)
    
    # Originally done with os.path, But nosetest seems to run this.
    os2 = import_relative.import_relative('os2.path', 'test')
    print os2
    print os2.path
    print os2.path.__name__
    print os2.path.__file__
    print os2.path.me
    # Warning. I've destroyed the real os.
    pass
