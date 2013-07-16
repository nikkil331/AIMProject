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

    def test_read_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest2")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest2")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest2.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['neither'], 0);

    def test_neither(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest3")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest3")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest3.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['neither'], 1);
    
    def test_writefield_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest4")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest4")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest4.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['neither'], 0);
        
    def test_wrfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest5")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest5")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest5.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['neither'], 1);

    def test_three_thread_read(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest7")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest7")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest7.java line 11']['total'], 3);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['read'], 3);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['neither'], 0);
        
    def test_three_thread_writefield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest8")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest8")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest8.java line 12']['total'], 3);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['read'], 3);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['neither'], 0);
        
    def test_two_nested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest9")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest9")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest9.java line 15']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['neither'], 0);
        
    def test_mulithreaded(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest10")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest10")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest10.java line 6']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['neither'], 10);

    def test_mulithreaded_nested1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest12")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest12")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest12.java line 25']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['neither'], 10);
        
    def test_mulithreaded_nested2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest13")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=120 -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest13")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest13.java line 23']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['neither'], 100);
        
    def test_Integer_fields(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest14")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest14")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest14.java line 3']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['neither'], 10);
        
    def test_multithreaded_arrayfields(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest15")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -maxTid=55 -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest15")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest15.java line 7']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['write'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['neither'], 0);
        
    def test_mulithreaded_nestedarray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest16")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -maxTid=30 -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest16")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest16.java line 16']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['neither'],250);

        self.assertEqual(resultList['SyncBlockTest16.java line 17']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['write'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['neither'], 0);
        
    def test_mulithreaded_objectfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest17")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest17")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest17.java line 8']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['neither'],0);

        self.assertEqual(resultList['SyncBlockTest17.java line 15']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['neither'], 0);
        
    def test_syncOnWritten_field(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest18")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest18")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest18.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['neither'], 0);
        
    def test_syncOnWritten_object(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest19")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest19")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest19.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['neither'], 0);
        
    def test_volatile_rwn(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest20")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest20")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest20.java line 8']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['neither'], 10);
        
    def test_get_set(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest21")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest21")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest21.java line 15']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['neither'], 0);

    def tetst_syncOnWritten_array(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest22")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest22")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest22.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['neither'], 0);
        
    def test_syncOn_private(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest23")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest23")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest23.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['neither'], 0);
    
    def test_multithreaded_syncOnField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest24")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=25 -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest24")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest24.java line 8']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['read'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['write'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['neither'], 20);
        
    def test_mulithreaded_syncOnArray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest25")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest25")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest25.java line 8']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['write'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['neither'], 10);

    def test_methodCalls(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest26")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest26")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest26.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['neither'], 0);

    def test_syncOn_static(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest27")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest27")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest27.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['neither'], 0);
        
    def test_write_staticField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest28")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest28")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest28.java line 4']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['neither'], 0);

    def test_sync_this(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest31")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest31")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest31.java line 4']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['neither'], 0);
        
    def test_serial_triplyNested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest33")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest33")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest33.java line 16']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['neither'], 0);
        
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['neither'], 100);
    
    def test_multithreaded_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest34")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=110 -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest34")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest34.java line 15']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['neither'], 0);
        
    def test_simpleArray_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest35")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest35")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest35.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['neither'], 0);
        
    def test_simpleArray_read(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest36")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -tool=SyncBlocksStats SyncBlockTest36")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest36.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['neither'], 0);
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(StaticSyncBlockTest)
unittest.TextTestRunner(verbosity=2).run(suite)

