#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2010 Chris Lamb <lamby@debian.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive import Config

class TestConfigConstructor(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir)

class TestSimple(TestConfigConstructor):
    def testArch386(self):
        lb = Config(self.dir, architecture='i386')
        self.assertEqual(lb.bootstrap['LB_ARCHITECTURE'], 'i386')

    def testArchAmd64(self):
        lb = Config(self.dir, architecture='amd64')
        self.assertEqual(lb.bootstrap['LB_ARCHITECTURE'], 'amd64')

    def testNoOptions(self):
        lb = Config(self.dir)

    def testInvalid(self):
        self.assertRaises(TypeError, Config, self.dir, this_config_never_exists='value')

class TestOther(TestConfigConstructor):
    def testArchChangesKernelFlavour(self):
        lb_i386 = Config(self.dir, architecture='i386')
        self.setUp()
        lb_amd64 = Config(self.dir, architecture='amd64')
        self.assertNotEqual(lb_i386.chroot['LB_LINUX_FLAVOURS'],
            lb_amd64.chroot['LB_LINUX_FLAVOURS'])

    def testHyphenatedOption(self):
        lb = Config(self.dir, packages_lists='my-package-list')
        self.assertEqual(lb.chroot['LB_PACKAGES_LISTS'], ['my-package-list'])

    def testSpaceInValue(self):
        lb = Config(self.dir, packages_lists="hello there")
        self.assertEqual(lb.chroot['LB_PACKAGES_LISTS'], ['hello', 'there'])

    def testAllowPassingOptionsSecondTime(self):
        lb = Config(self.dir, packages_lists="one two")
        lb = Config(self.dir, packages_lists="three four")
        self.assertEqual(lb.chroot['LB_PACKAGES_LISTS'], ['three', 'four'])

if __name__ == "__main__":
    unittest.main()
