import unittest
from catalog.engine.rules import Platform,Package,compare
class CompatibilityTests(unittest.TestCase):
    def test_exact(self):
        r=compare(Package('Symbian','9.1','armv5','sis'),Platform('Symbian','9.1','armv5'))
        self.assertEqual(r.level,'native'); self.assertEqual(r.score,100)
    def test_os_mismatch(self):
        r=compare(Package('DOS','3.x','x86','exe'),Platform('Windows','95','x86'))
        self.assertEqual(r.level,'unsupported')
    def test_arch_mismatch(self):
        r=compare(Package('Linux','6','arm64','deb'),Platform('Linux','6','x86_64'))
        self.assertEqual(r.level,'unsupported')
if __name__=='__main__': unittest.main()
