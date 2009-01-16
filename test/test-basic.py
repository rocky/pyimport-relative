#!/usr/bin/env python
'Unit test for import_relative'
import inspect, os, sys, unittest
top_builddir = os.path.join(os.path.dirname(__file__), '..')
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, top_builddir)
from import_relative import *

def true(): return true

class TestImportRelative(unittest.TestCase):

    def test_basic(self):
        """Basic sanity testing."""
        test_basic = import_relative('test-basic')
        self.assertTrue(inspect.ismodule(test_basic),
                        'import_relative should return a module type')

        filename = os.path.join(get_srcdir(), 'test-basic.py')
        self.assertEqual(os.path.sep, filename[0],
                         'get_srcdir should return an absolute path name')

        check_fn = test_basic.__file__
        if (check_fn.endswith(".pyc") or check_fn.endswith(".pyo")):
            check_fn = check_fn[:-1]
            pass

        self.assertEqual(filename, check_fn,
                         'import_relative should set __file__ correctly')

        self.assertEqual('test-basic', test_basic.__name__,
                         'import_relative should set __name__ correctly')

        self.assertTrue(test_basic.true(),
                        'should be able to use fns inside returned module')

        self.assertTrue(sys.modules.has_key('test-basic'))

        ir = import_relative('import_relative', os.pardir)
        os2 = ir.import_relative('os2.path')
        self.assertTrue('test.os2.path', os2.path.me)

        ir = import_relative('import_relative', '..')
        os2 = ir.import_relative('os2.path')
        self.assertTrue('test.os2.path', os2.path.me)

        return

    pass

if __name__ == '__main__':
    unittest.main()
