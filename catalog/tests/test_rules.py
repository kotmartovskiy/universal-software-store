import unittest
from catalog.engine.rules import Package, Platform, compare

class CompatibilityTests(unittest.TestCase):
    def test_exact_native(self):
        r = compare(Package("Symbian","9.1","armv5","sis"), Platform("Symbian","9.1","armv5"))
        self.assertEqual((r.level,r.score), ("native",95))

    def test_os_mismatch(self):
        r = compare(Package("DOS","3.3","x86","exe"), Platform("Windows","98","x86"))
        self.assertEqual(r.level, "unsupported")

    def test_arch_mismatch(self):
        r = compare(Package("Linux","6.1","aarch64","deb"), Platform("Linux","6.1","x86_64"))
        self.assertEqual(r.level, "unsupported")

    def test_os_range(self):
        r = compare(Package("Windows","9","x86_64","exe", min_os_version="7", max_os_version="11"), Platform("Windows","10","x86_64"))
        self.assertIn(r.level, ("native", "partial"))
        self.assertIn("supported range", r.reason)

    def test_ram_requirement(self):
        r = compare(Package("DOS","3.3","x86","exe", min_ram_mb=640), Platform("DOS","3.3","x86", memory_mb=256))
        self.assertEqual(r.level, "unsupported")

    def test_arm_conditional(self):
        r = compare(Package("Linux","2.6","armv5","deb"), Platform("Linux","2.6","armv7"))
        self.assertEqual(r.level, "partial")
        self.assertIn("conditionally", r.reason)

    def test_compatibility_layer(self):
        r = compare(Package("Windows","98","x86","exe", compatibility_layer="Wine"), Platform("Linux","6.1","x86_64"))
        self.assertEqual(r.level, "assisted")
        self.assertIn("Wine", r.reason)

if __name__ == "__main__":
    unittest.main()
