'''
Scratchpad for test-based development.

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


import sys
import pathlib
import logging
import datetime


def autoconfig(tofile=True, logdirname='logs', loglevel='debug'):
    if tofile:
        fname = sys.argv[0]
        logdir = pathlib.Path(logdirname)

        if (not logdir.exists()) or (not logdir.is_dir()):
            logdir.mkdir()

        # Note that double slashes don't cause problems.
        prefix = logdirname + '/' + pathlib.Path(fname).stem
        ii = 0
        date = str(datetime.date.today())
        ext = '.pylog'
        while pathlib.Path(prefix + '_' + date + '_' + str(ii) + ext).exists():
            ii += 1
        logname = prefix + '_' + date + '_' + str(ii) + ext
        print('USING LOGFILE: ' + logname)

        # Make a log handler
        loghandler = logging.FileHandler(logname)
        loghandler.setFormatter(
            logging.Formatter(
                '%(threadName)-10.10s '
                '%(name)-17.17s  %(levelname)-5.5s  '
                '%(message)s'
            )
        )
        
        # Add to root logger
        logging.getLogger('').addHandler(loghandler)

    # Calculate the logging level
    loglevel = loglevel.lower()
    loglevel_enum = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'shouty': logging.ERROR,
        'extreme': logging.ERROR
    }
    try:
        log_setpoint = loglevel_enum[loglevel]
    except KeyError:
        log_setpoint = logging.WARNING
        
    # Silence the froth but keep the good stuff
    logging.getLogger('').setLevel(log_setpoint)
    
    if loglevel == 'shouty':
        logging.getLogger('asyncio').setLevel(logging.INFO)
        logging.getLogger('websockets').setLevel(logging.DEBUG)
        
    elif loglevel == 'extreme':
        logging.getLogger('asyncio').setLevel(logging.DEBUG)
        logging.getLogger('websockets').setLevel(logging.DEBUG)
        
    else:
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        logging.getLogger('websockets').setLevel(logging.WARNING)