#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function

from optparse import OptionParser
import re
import socket
import subprocess
import sys
import time
import urllib

parser = OptionParser(description="""
this is the duenndns tool to update dynamic dns records
""")

parser.add_option("--key",
                    dest    = "key",
                    action  = "store",
                    help    = "key.",
                    default = None
)

parser.add_option("--nameserver",
                    dest    = "nameserver",
                    action  = "store",
                    help    = "nameserver.",
                    default = None
)

parser.add_option("--zone",
                    dest    = "zone",
                    action  = "store",
                    help    = "zone.",
                    default = None
)

parser.add_option("--client",
                    dest    = "client",
                    action  = "store",
                    help    = "client.",
                    default = None
)

parser.add_option("--ip",
                    dest    = "ip",
                    action  = "store",
                    help    = "ip. skip this option to trigger autodiscovery.",
                    default = None
)

parser.add_option("--ttl",
                    dest    = "ttl",
                    action  = "store",
                    help    = "ttl.",
                    default = "60"
)

parser.add_option("--check",
                    dest    = "check",
                    action  = "store_true",
                    help    = "check only via dig, do not update.",
                    default = False
)

parser.add_option("--verbose",
                    dest    = "verbose",
                    action  = "store_true",
                    help    = "be verbose.",
                    default = False
)

# parse the args
(options, args) = parser.parse_args()

def shell(cmd, stdin="", checkexe=True):
    if checkexe:
        try:
            subprocess.check_output(['which', cmd[0]])
        except subprocess.CalledProcessError:
            fatal_error('%s missing, not executable or not in PATH.' % cmd[0])

    cmdstring = " ".join(cmd)
    log("running: %s\ninput:%s" % (cmdstring, stdin), level=1)
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(input=stdin)
        out = "%s%s" % (stdout, stderr)
        rc = p.returncode
    except Exception as e:
        fatal_error("shell was unhappy", exception=e)
        out = "shell was unhappy: %s" % (cmdstring)
        rc = "exception"
    return(out, rc)

def log(string, level=0):
    # level is the verbosity-level needed to display this message
    if level == 0 or options.verbose:
        print(string)

def fatal_error(text, exit_status=-1, exception=None):
    if exception is not None:
        log(repr(exception))
    log('fatal error: %s' % (text))
    exit(exit_status)


def get_external_ip():
    try:
        url = "http://icanhazip.com/"
        ip = urllib.urlopen(url).read()

        matchObj = re.match( r'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})', ip)
        if matchObj:
            return matchObj.group()
    except Exception as e:
        fatal_error('autodiscovery failed', exception=e)

if options.key is None:
    fatal_error('key is None')

if options.nameserver is None:
    fatal_error('nameserver is None')

if options.zone is None:
    fatal_error('zone is None')

if options.client is None:
    fatal_error('client is None')

if options.ip is None:
    log('ip is None, starting autodiscovery')
    options.ip = get_external_ip()
    log("autodiscovery found %s" % (options.ip))

if options.ttl is None:
    fatal_error('ttl is None')

command = [
    "nsupdate",
    "-k",
    options.key
]

script = """
answer
server %(nameserver)s
zone %(zone)s.
ttl %(ttl)s
update delete %(client)s.%(zone)s. A
update add %(client)s.%(zone)s. A %(ip)s
send
quit
""" % {
    'nameserver'    : options.nameserver,
    'zone'          : options.zone,
    'client'        : options.client,
    'ip'            : options.ip,
    'ttl'           : options.ttl
}

if not options.check:
    ip = socket.gethostbyname( '%(client)s.%(zone)s' % {
            'client'    : options.client,
            'zone'      : options.zone
        }
    )

    log("ip is %s" % (ip))

    if options.ip == ip:
        log("doing nothing")
        sys.exit(0)
    else:
        out, rc = shell(command, stdin=script)

        if out:
            log(out)
        log("nsupdate status was %s" % rc)

"""
CHECK IF THE UPDATE WAS SUCCESSUL
"""

# http://stackoverflow.com/a/5849861/2536029
class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        log('[%s]: %s' % (
            self.name if self.name else '',
            time.time() - self.tstart)
        )

with Timer("wait for dns"):
    done = False
    frequency = 10
    maxloops = 12
    numloops = 0
    
    while not done:
        ip = socket.gethostbyname( '%(client)s.%(zone)s' % {
                'client'    : options.client,
                'zone'      : options.zone
            }
        )

        log("dns now tells: %s" % (ip))

        if ip == options.ip:
            done = True
        else:
            numloops += 1
            if numloops > maxloops:
                done = True
                log("giving up")
            else:
                log("still trying", level=1)
                time.sleep(frequency)
