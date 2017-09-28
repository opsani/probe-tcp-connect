'''
Copyright (c) 2017, Opsani
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

License template: http://opensource.org/licenses/BSD-2-Clause
                  (as accessed on June 2, 2015)

probe.py - class definitions and utility functions for skopos probes
'''
from __future__ import print_function
import time

# === user error exceptions

class UserError(Exception):
    pass

class UserValidationError(Exception):
    pass

# === misc helpers

def extract_ip(inst):
    '''
    Extract the instance IP address (inst must be a dict containing the Skopos
    inst{} structure for a single instance).  Return the IP address as a string.
    Raise UserError exception if there is no IP address for the instance.
    '''
    ip = inst.get('ipaddr')
    if not ip:  # none or empty
        raise UserError('failed to extract instance IP address: got "{}"'.format(ip))
    return ip

def dbg_log(*args):
    with open('/tmp/skopos-probe.log', 'a') as f:
        f.write(' '.join([str(x) for x in args] + [ '\n', ]))

def wait_retry_op(timeout, op):
    '''
    Call a passed function op:  return on success, re-try on UserError, fail on
    UserValidationError or timeout.
    '''
    timeout = int(timeout)    # make sure it is an integer so we can compare
    start = time.time()
    while True:
        tstamp = time.time()  # measure before we start but compare after
        exc = None
        try:
            op()
        except UserError as e:
            exc = e
            pass
        except UserValidationError as e:
            raise  # raise at once, no retry
        else:
            return # success

        # fail on timeout:  we've tried at least once after the timeout period
        if tstamp >= start + timeout:
            raise exc if exc else UserError('timed out waiting for success response')

        # delay next request (avoid busy loop)
        time.sleep(1)

def parse_intlist(lst):
    '''
    Return set of integers parsed from a comma-separated string or list of strings.
    Examples:
    - lst: "200,404,201"
    - lst: ["200", "404", "201"]
    '''
    items = lst if isinstance(lst, list) else lst.split(',')
    ret = set()
    for v in items:
        ret.add(int(v))
    return ret
