import sys
import subprocess
import shlex

class BenchmarksSyncBlockStats():
    def __init__(self):
        return
 
    def run(self, args):
        getTool = shlex.split("./getToolFromEclipse SyncBlocksStats")
        p = subprocess.Popen(getTool);
        p.wait();

        if(len(args) < 2):
            print "Must give number of times to run"
            exit();

        numRuns = int(args[1]);

        benchmarks = {"avrora" : [], "batik" : [], "jython" : [], "lusearch" : [], "sunflow" : []}
    
        for program in benchmarks.keys():
            results = list();
            benchmarks[program] = results;
            print "Running " + program
            for i in range(numRuns):
                results.append(self.runBenchmark(program))
            print program + " completed."

        for program in benchmarks.keys():
            total = 0;
            read = 0;
            write = 0;
            neither = 0;
            for result in benchmarks[program]:
                total = total + result[0]
                read = read + result[1]
                write = write + result[2]
                neither = neither + result[3]

            totalavg = total/numRuns
            readavg = read/numRuns
            writeavg = write/numRuns
            neitheravg = neither/numRuns

            totaldev = self.getDeviation(totalavg, benchmarks[program], 0)
            readdev = self.getDeviation(readavg, bechnmarks[program], 1)
            writedev = self.getDeviation(writeavg, benchmarks[program], 2)
            neitherdev = self.getDeviation(neitheravg, benchmarks[program], 3)

            print program
            print "Average: Total = " + totalavg + " Read = " + readavg+ " Write = " + writeavg + " Neither = " + neitheravg
            print "StandardDeviation: Total = " + totladev + " Read = " + readdev + " Wrte = " + writedev + " Neither = " + neitherdev
            print ""


    def getDeviation(self, mean, results, index):
        sum = 0
        for result in results:
            sum = sum + math.pow((result[index] - mean), 2)
        return sum / len(results)       
           

    def runBenchmark(self, program):
        run = shlex.split("rrrun -toolpath=\"./classes/tools/trials\" -classpath=\"./DaCapo\" -classes=\"-.*TeeOutputStream.*\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats Harness " + program)
        runOutput = subprocess.Popen(run, stdout=subprocess.PIPE)
        runOutput.wait();

        parseOutput = subprocess.Popen(["grep", "result"], stdin=runOutput.stdout, stdout=subprocess.PIPE)
        parseOutput.wait();

        result = list()

        expression = parseOutput.stdout.readline() + parseOutput.stdout.readline() + parseOutput.stdout.readline() + parseOutput.stdout.readline()

        exec expression

        return result

this = BenchmarksSyncBlockStats()
this.run(sys.argv)
