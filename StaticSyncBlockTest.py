import unittest
import subprocess
import shlex

class StaticSyncBlockTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        getTool = shlex.split("bash getToolFromEclipse SyncBlocksStats")
        p = subprocess.Popen(getTool)
        p.wait();

        return

    def parseOutput(self, out):
        grep = shlex.split("grep result")
        find = subprocess.Popen(grep, stdin=out, stdout=subprocess.PIPE)
        output = find.stdout.read()

        result = {};
        exec output
        return result

    def test_sameLockPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT1")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT1")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['neither'], 0);

    def test_sameLock_diffPC1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT2")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT2")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['neither'], 0);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['neither'],10)

    def test_sameLock_diffPC2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT3")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT3")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['neither'], 0);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['neither'],0)

    def test_diffLockPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT4")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT4")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['neither'], 0);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['write'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['neither'],0)

    def test_diffLock_samePC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT5")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT5")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['total'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['read'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['neither'], 0);

    def test_recurseive_reentrant(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT6")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT6")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['total'], 11);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['neither'], 1);

    def test_parallel_sameLockPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT7")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT7")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['neither'], 0);

    def test_parallel_sameLock_diffPC1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT8")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT8")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['neither'], 0);
        
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['neither'], 10);

    def test_parallel_sameLock_diffPC2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT9")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT9")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['neither'], 0);
        
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['neither'], 0);
        
    def test_parallel_diffLock_diffPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT10")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT10")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['neither'], 0);
        
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['write'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['neither'], 0);
        
    def test_parallel_diffLock_samePC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT11")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT11")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['total'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['read'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['neither'], 0);
        
    def test_parallel_recursive_reentrant(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT12")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats StaticSyncBlockTests.StaticSBT12")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['total'], 110);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['read'], 100);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['neither'], 10);
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(StaticSyncBlockTest)
unittest.TextTestRunner(verbosity=2).run(suite)

