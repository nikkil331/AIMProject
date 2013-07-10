#!/usr/bin/env python

import os
import sys
import time
import recon
from optparse import OptionParser
import subprocess

scripts_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

parser = OptionParser()
parser.add_option("-p","--pretend", dest="pretend", action="store_true", default=False,
                  help="Just print what would be run.")
parser.add_option("-e","--email", dest="email", action="store_true", default=False,
                  help="Email $USER when done.")
parser.add_option("-r", "--reps", dest="reps", type="int", default=1,
                      help="Number of reps per config.")
parser.add_option("-w","--warmup", dest="warmup", type="int", default=0,
                      help="Number of times to run each config before recording.")
# parser.add_option("-m", "--max-threads", dest="maxthreads", type="int", default=2,
#                   help="Max number of threads. Every power of 2 that is > 0 and < this will be tried.")
# parser.add_option("-t", "--num-threads", dest="threads", type="int", default=8,
#                   help="Number of threads.")

os.chdir(scripts_dir)

## Compile timer callback
classpath = scripts_dir + ':' + scripts_dir + '/dacapo-9.12-bach.jar'
print "Classpath = " + classpath
try:
    subprocess.check_call(['javac', '-cp', classpath, 'TimerCallback.java'])
except subprocess.CalledProcessError:
    print "TimerCallback.java does not compile. :-("
    sys.exit(1)

stamp = str(int(time.time()))
logsdir = os.path.abspath("results-" + stamp)
os.makedirs(logsdir)
logfile = os.path.abspath(logsdir + "/log.py")
progressfile = os.path.abspath(logsdir + '/progress.txt')

os.chdir(logsdir)

(opts,args) = parser.parse_args(sys.argv)



run = 0

log = []

class NextConfigException(Exception):
    def __init__(self):
        pass
class NextBenchmarkException(Exception):
    def __init__(self):
        pass
    
def interrupt():
    while True:
        try:
            print "Paused.  r  Continue at next {r}epetition of current config of current benchmark. [default]"
            print "         c  Continue at next {c}onfig of current benchmark."
            print "         b  Continue at next {b}enchmark."
            print "         q  {Q}uit the run script after flushing the log."
            i = raw_input("> ")
            if i == 'r' or i == 'R':
                return
            elif i == 'c' or i == 'C':
                raise NextConfigException
            elif i == 'b' or i == 'B':
                raise NextBenchmarkException
            elif i == 'q' or i == 'Q':
                break
        except KeyboardInterrupt:
            pass
    raise KeyboardInterrupt

def do(run, cmd, key="run"):
    print "[" + key + " " + str(run) + "] " + cmd
    if not opts.pretend:
        try:
            subprocess.check_call(cmd.split(' '))
            return True
        except subprocess.CalledProcessError:
            return False

def flush(log,path):
    f = open(path, 'w')
    f.write(repr(log))
    f.close()

def progress(msg,path):
    f = open(path, 'a')
    f.write(msg + '\n')
    f.close()

os.environ['JVM_ARGS'] = os.getenv('JVM_ARGS') + ' -cp ' + classpath

def setJvmArgs(args):
    jvmArgString = os.getenv('JVM_ARGS') + ' ' + jvmArgs
    os.putenv('JVM_ARGS', jvmArgString)
    print 'JVM_ARGS=' + jvmArgString

rr = ' '.join(['rrrun',
               '-noxml',
               '-quiet',
               '-classpath=' + classpath,
               '-array=FINE',
               '-classes=-Harness',
               '-classes=-org.dacapo.harness.*',
               '-classes=-org.dacapo.parser.*',
               '-classes=-TimerCallback',
               ''])

nthreads = recon.nthreads
# run tests
for name,jvmArgs,rrArgs in recon.benchmarks:
    try:
        cls = rrArgs + " Harness --callback TimerCallback --scratch-directory " + scripts_dir + '/scratch ' + name
        for key,config in recon.all_configs:
            try:
                print("Config: " + repr((name, key)))
                print("Warmup runs (" + str(opts.warmup) + "):")
                for i in range(opts.warmup):
                    do(run, rr + ' ' + config + " " + cls, key="warmup")
                print("Recording runs (" + str(opts.reps) + "):")
                for i in range(opts.reps):
                    try:
                        run += 1
                        fn_key = str(run) + "-" + name
                        cmd = rr + " -logs=" + logsdir +" -xml="  + fn_key + ".xml"  + '  ' + config
#                        os.putenv('BBGRAPHFILE', logsdir + '/' + fn_key + '.graph')
                        cmd +=  " " + cls
                        setJvmArgs(jvmArgs)
                        if do(run, cmd):
                            perffile = logsdir + '/' + name + '.perfdata'
                            perf = 'None'
                            if os.path.exists(perffile):
                                f = open(perffile)
                                perf = f.read()
                                f.close()
                            progress(time.asctime() + "    run " + str(run) + "    " + name + '    ' + key + '    ' + perf, progressfile)
                            log.append((stamp, run, key, name, nthreads, cmd))
                            os.system('mv ' + perffile + ' ' + logsdir + '/' + fn_key + '.perfdata');
                        else:
                            progress(time.asctime() + "    run " + str(run) + "    " + name + '    ' + key + "    CRASHED", progressfile)
                            os.system('rm -f ' + logsdir + '/' + name + '.perfdata');
                    except KeyboardInterrupt:
                        progress(time.asctime() + "    run " + str(run) + "    " + name + '    ' + key + "    INTERRUPTED", progressfile)
                        os.system('rm -f ' + logsdir + '/' + name + '.perfdata');
                        interrupt()
            except NextConfigException:
                pass
            finally:
                flush(log,logfile)
    except NextBenchmarkException:
        pass
print
print "Results in " + logsdir
progress(time.asctime() + "    Done",progressfile)

f = open(progressfile)
print f.read()
f.close()

if opts.email:
    os.system("echo " + logsdir + " | mail -s dacapo " + os.getenv("USER", "bpw"))
