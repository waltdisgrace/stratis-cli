# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test 'list'.
"""

import time
import unittest

from stratis_cli._actions._stratisd_constants import StratisdErrorsGen

from stratis_cli._constants import TOP_OBJECT

from stratis_cli._dbus import Manager
from stratis_cli._dbus import get_object

from .._constants import _DEVICES

from .._misc import _device_list
from .._misc import Service


class ListTestCase(unittest.TestCase):
    """
    Test 'list'.
    """

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testList(self):
        """
        List should just succeed.
        """
        (result, rc, message) = Manager(self._proxy).ListPools()
        self.assertEqual(type(result), list)
        self.assertEqual(type(rc), int)
        self.assertEqual(type(message), str)

        self.assertEqual(result, [])
        self.assertEqual(rc, StratisdErrorsGen.get_object().STRATIS_OK)


class List2TestCase(unittest.TestCase):
    """
    Test 'list' with something actually to list.
    """
    _POOLNAME = 'deadpool'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        Manager(self._proxy).CreatePool(
           self._POOLNAME,
           [d.device_node for d in _device_list(_DEVICES, 1)],
           0
        )

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testList(self):
        """
        List should just succeed.
        """
        (result, rc, message) = Manager(self._proxy).ListPools()

        self.assertEqual(type(result), list)
        self.assertEqual(type(rc), int)
        self.assertEqual(type(message), str)

        self.assertEqual(len(result), 1)

        self.assertEqual(type(result[0]), str)
        self.assertEqual(rc, StratisdErrorsGen.get_object().STRATIS_OK)
