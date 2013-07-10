#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function


from optparse import OptionParser
import subprocess

parser = OptionParser(description="""
this is the duenndns tool to update dynamic dns records
""".strip())

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
                    help    = "ip.",
                    default = None
)

parser.add_option("--ttl",
                    dest    = "ttl",
                    action  = "store",
                    help    = "ttl.",
                    default = "60"
)

# parse the args
(options, args) = parser.parse_args()

def shell(cmd, stdin="", checkexe=True):
    if checkexe:
        try:
            subprocess.check_output(['which', cmd[0]])
        except subprocess.CalledProcessError:
            fatalError('%s missing, not executable or not in PATH.' % cmd[0])

    cmdstring = " ".join(cmd)
    print("running: %s\ninput:%s" % (cmdstring, stdin))
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

def fatal_error(text, exit_status=-1, exception=None):
    if exception is not None:
        print(repr(exception))
    print('fatal error: %s' % (text))
    exit(exit_status)

if options.key is None:
	fatal_error('key is None')

if options.nameserver is None:
	fatal_error('nameserver is None')

if options.zone is None:
	fatal_error('zone is None')

if options.client is None:
	fatal_error('client is None')

if options.ip is None:
	fatal_error('ip is None')

if options.ttl is None:
	fatal_error('ttl is None')

command = [
	"nsupdate",
	"-k",
	options.key
]

# command = ["cat"]


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
	'nameserver'	: options.nameserver,
	'zone'			: options.zone,
	'client'		: options.client,
	'ip'			: options.ip,
	'ttl'			: options.ttl
}

out, rc = shell(command, stdin=script)

print(out)

print("status was %s" % rc)

control = [
	'dig',
	'%(client)s.%(zone)s' % {
		'client'	: options.client,
		'zone'		: options.zone
	},
	'A'
]

out, rc = shell(control)

print(out)	