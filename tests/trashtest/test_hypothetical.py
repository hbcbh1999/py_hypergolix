'''
LICENSING
-------------------------------------------------

hypergolix: A python Golix client.
    Copyright (C) 2016 Muterra, Inc.
    
    Contributors
    ------------
    Nick Badger
        badg@muterra.io | badg@nickbadger.com | nickbadger.com

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the
    Free Software Foundation, Inc.,
    51 Franklin Street,
    Fifth Floor,
    Boston, MA  02110-1301 USA

------------------------------------------------------

'''

import logging
import unittest


# Testing imports
from hypergolix.hypothetical import API
from hypergolix.hypothetical import public_api
from hypergolix.hypothetical import fixture_api


# ###############################################
# "Paragon of adequacy" test fixtures
# ###############################################
        
        
# These are not the droids you are looking for...


# ###############################################
# Testing
# ###############################################
        
        
class APITest(unittest.TestCase):
    ''' Test general API creation and operation.
    '''
    
    def setUp(self):
        ''' Set up the test by declaring a new class with it.
        '''
        class Fixtured(metaclass=API):
            def __init__(self):
                self.counter = 0
            
            @public_api
            def incr(self):
                self.counter += 1
                
            @incr.fixture
            def incr(self):
                self.counter += 2
                
            @public_api
            def decr(self):
                self.counter -= 1
                
            @fixture_api
            def reset(self):
                self.counter = 0
        
        self.apied = Fixtured
    
    def test_public(self):
        ''' Test the public API.
        '''
        public = self.apied()
        public.incr()
        self.assertEqual(public.counter, 1)
        public.incr()
        self.assertEqual(public.counter, 2)
        public.decr()
        self.assertEqual(public.counter, 1)
        
        with self.assertRaises(AttributeError):
            public.reset()
        
    def test_fixture(self):
        ''' Test the fixture API.
        '''
        fixture = self.apied.__fixture__()
        fixture.incr()
        self.assertEqual(fixture.counter, 2)
        fixture.incr()
        self.assertEqual(fixture.counter, 4)
        fixture.decr()
        self.assertEqual(fixture.counter, 3)
        fixture.reset()
        self.assertEqual(fixture.counter, 0)


# ###############################################
# Running directly
# ###############################################


if __name__ == "__main__":
    from hypergolix import logutils
    logutils.autoconfig(loglevel='debug')
    
    unittest.main()
    
    # from hypergolix.utils import TraceLogger
    # with TraceLogger(interval=10):
    #     unittest.main()
