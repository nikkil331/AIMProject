import unittest
import subprocess
import shlex

class StaticSyncBlockTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        getTool = shlex.split("./getToolFromEclipse")
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

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT1")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT1.java line 9']['depths'], [0]);

    def test_sameLock_diffPC1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT2")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT2")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 9']['depths'], [0]);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['neither'],10)
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT2.java line 11']['depths'], []);

    def test_sameLock_diffPC2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT3")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT3")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 9']['depths'], [0]);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['neither'],0)
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT3.java line 10']['depths'], [0]);

    def test_diffLockPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT4")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT4")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 9']['depths'], [0]);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['write'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['neither'],0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT4.java line 10']['depths'], [0]);

    def test_diffLock_samePC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT5")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT5")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['total'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['read'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT5.java line 7']['depths'], [0]);

    def test_recurseive_reentrant(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT6")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT6")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['total'], 11);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['neither'], 1);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT6.java line 5']['depths'], [0]);

    def test_parallel_sameLockPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT7")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT7")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT7.java line 14']['depths'], [0]);

    def test_parallel_sameLock_diffPC1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT8")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT8")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 14']['depths'], [0]);


        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['neither'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT8.java line 16']['depths'], []);

    def test_parallel_sameLock_diffPC2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT9")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT9")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 14']['depths'], [0]);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT9.java line 15']['depths'], [0]);

    def test_parallel_diffLock_diffPC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT10")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT10")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['read'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 14']['depths'], [0]);

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['total'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['read'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['write'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT10.java line 15']['depths'], [0]);

    def test_parallel_diffLock_samePC(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT11")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT11")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['total'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['read'], 20);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT11.java line 11']['depths'], [0]);

    def test_parallel_recursive_reentrant(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT12")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT12")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['total'], 110);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['read'], 100);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['neither'], 10);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT12.java line 11']['depths'], [0]);

    def test_syncOn_class(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t StaticSyncBlockTests.StaticSBT13")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder StaticSyncBlockTests.StaticSBT13")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT13.java line 6']['total'], 1);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT13.java line 6']['read'], 1);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT13.java line 6']['write'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT13.java line 6']['neither'], 0);
        self.assertEqual(resultList['StaticSyncBlockTests.StaticSBT13.java line 6']['depths'], [0]);


    def test_read_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest2")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest2")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest2.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest2.java line 6']['depths'], [0]);

    def test_neither(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest3")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest3")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest3.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['neither'], 1);
        self.assertEqual(resultList['SyncBlockTest3.java line 6']['depths'], []);

    def test_writefield_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest4")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest4")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest4.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest4.java line 7']['depths'], [0]);

    def test_rfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest5")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest5")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest5.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 7']['depths'], [0]);
        
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 10']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest5.java line 13']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['neither'], 1);
        self.assertEqual(resultList['SyncBlockTest5.java line 13']['depths'], []);

    def test_three_thread_read(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest7")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest7")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest7.java line 11']['total'], 3);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['read'], 3);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest7.java line 11']['depths'], [0]);
        
    def test_three_thread_writefield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest8")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest8")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest8.java line 12']['total'], 3);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['read'], 3);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest8.java line 12']['depths'], [0]);

    def test_two_nested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest9")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest9")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest9.java line 15']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 15']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest9.java line 17']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest9.java line 17']['depths'], [0]);

    def test_mulithreaded(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest10")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest10")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest10.java line 6']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 6']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest10.java line 9']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 9']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest10.java line 12']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['neither'], 10);
        self.assertEqual(resultList['SyncBlockTest10.java line 12']['depths'], []);

    def test_mulithreaded_nested1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest12")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest12")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest12.java line 25']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 25']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest12.java line 27']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 27']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest12.java line 29']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['neither'], 10);
        self.assertEqual(resultList['SyncBlockTest12.java line 29']['depths'], []);

    def test_mulithreaded_nested2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest13")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -maxTid=120 -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest13")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest13.java line 23']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 23']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest13.java line 25']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 25']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest13.java line 28']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['neither'], 100);
        self.assertEqual(resultList['SyncBlockTest13.java line 28']['depths'], []);

    def test_Integer_fields(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest14")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest14")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest14.java line 3']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 3']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest14.java line 6']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 6']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest14.java line 9']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['neither'], 10);
        self.assertEqual(resultList['SyncBlockTest14.java line 9']['depths'], []);

    def test_multithreaded_arrayfields(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest15")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -maxTid=55 -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest15")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest15.java line 7']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 7']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest15.java line 9']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 9']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest15.java line 14']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['read'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 14']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest15.java line 15']['total'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['write'], 50);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest15.java line 15']['depths'], [0]);

    def test_mulithreaded_nestedarray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest16")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -maxTid=30 -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest16")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest16.java line 16']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 16']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest16.java line 22']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 22']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest16.java line 30']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['neither'],250);
        self.assertEqual(resultList['SyncBlockTest16.java line 30']['depths'], []);

        self.assertEqual(resultList['SyncBlockTest16.java line 17']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['read'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 17']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest16.java line 23']['total'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['write'], 250);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest16.java line 23']['depths'], [0]);

    def test_mulithreaded_objectfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest17")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest17")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest17.java line 8']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 8']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest17.java line 9']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 9']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest17.java line 14']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['neither'],0);
        self.assertEqual(resultList['SyncBlockTest17.java line 14']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest17.java line 15']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest17.java line 15']['depths'], [0]);

    def test_syncOnWritten_field(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest18")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest18")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest18.java line 7']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest18.java line 7']['depths'], [0]);

    def test_syncOnWritten_object(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest19")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest19")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest19.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest19.java line 5']['depths'], [0]);

    def test_volatile_rwn(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest20")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest20")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest20.java line 8']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 8']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest20.java line 12']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 12']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest20.java line 15']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['neither'], 10);
        self.assertEqual(resultList['SyncBlockTest20.java line 15']['depths'], []);

    def test_get_set(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest21")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest21")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest21.java line 15']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 15']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest21.java line 18']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest21.java line 18']['depths'], [1]);

    def tetst_syncOnWritten_array(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest22")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest22")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest22.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest22.java line 5']['depths'], [0]);

    def test_syncOn_private(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest23")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest23")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest23.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest23.java line 5']['depths'], [0]);
    
    def test_multithreaded_syncOnField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest24")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -maxTid=25 -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest24")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest24.java line 8']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['read'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 8']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest24.java line 13']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['write'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 13']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest24.java line 17']['total'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['neither'], 20);
        self.assertEqual(resultList['SyncBlockTest24.java line 17']['depths'], []);        

    def test_mulithreaded_syncOnArray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest25")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest25")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest25.java line 8']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['read'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 8']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest25.java line 14']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['write'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 14']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest25.java line 19']['total'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['neither'], 10);
        self.assertEqual(resultList['SyncBlockTest25.java line 19']['depths'], []);

    def test_methodCalls(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest26")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest26")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest26.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 6']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest26.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest26.java line 10']['depths'], [0]);

    def test_syncOn_static(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest27")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder -noOrder SyncBlockTest27")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest27.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest27.java line 5']['depths'], [0]);

    def test_write_staticField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest28")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\"  -tool=tools.syncBlockStats.SyncBlocksStats -noOrder -noOrder SyncBlockTest28")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest28.java line 4']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 4']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest28.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 5']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest28.java line 9']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 9']['depths'], [0]);

        self.assertEqual(resultList['SyncBlockTest28.java line 10']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest28.java line 10']['depths'], [0]);

    def test_sync_this(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest31")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest31")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest31.java line 4']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest31.java line 4']['depths'], [0]);

    def test_serial_triplyNested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest33")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest33")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest33.java line 16']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 16']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest33.java line 18']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['read'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 18']['depths'], [1]);

        self.assertEqual(resultList['SyncBlockTest33.java line 21']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['neither'], 100);
        self.assertEqual(resultList['SyncBlockTest33.java line 21']['depths'], []);

    def test_multithreaded_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest34")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -maxTid=110 -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest34")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest34.java line 15']['total'], 100);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['write'], 100);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest34.java line 15']['depths'], [1]);

    def test_simpleArray_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest35")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest35")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest35.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest35.java line 5']['depths'], [0]);

    def test_simpleArray_read(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest36")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest36")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest36.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest36.java line 5']['depths'], [0]);
    
    def test_simple_final(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest38")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest38")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest38.java line 4']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest38.java line 4']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest38.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest38.java line 4']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest38.java line 4']['depths'], [0]);
    
    def test_methodCall_syncedClass(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest39")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest39")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest39.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest39.java line 5']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest39.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest39.java line 5']['neither'], 1);
        self.assertEqual(resultList['SyncBlockTest39.java line 5']['depths'], []);

    def test_oneMethodCall(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest41")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest41")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest41.java line 5']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest41.java line 5']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest41.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest41.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest41.java line 5']['depths'], [1]);

##doesn't notice access to this!
#    def test_readThis(self):
#        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest42")
#        p = subprocess.Popen(getTestClass);
#        p.wait()

#        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest42")
#        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

#        resultList = self.parseOutput(runner.stdout)

#        self.assertEqual(resultList['SyncBlockTest42.java line 6']['total'], 1);
#        self.assertEqual(resultList['SyncBlockTest42.java line 6']['read'], 1);
#        self.assertEqual(resultList['SyncBlockTest42.java line 6']['write'], 0);
#        self.assertEqual(resultList['SyncBlockTest42.java line 6']['neither'], 0);
#        self.assertEqual(resultList['SyncBlockTest42.java line 6']['depths'], [0]);
    
    def test_interfaceInheritance(self):
        getTestInterface = shlex.split("bash getTargetFromEclipse -t SyncBlockTestI");
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest44");
        p = subprocess.Popen(getTestInterface);
        p.wait()
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest44");
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest44.java line 8']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest44.java line 8']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest44.java line 8']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest44.java line 8']['neither'], 1);
        self.assertEqual(resultList['SyncBlockTest44.java line 8']['depths'], []);

    def test_heirarchy(self):
        getSuperClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest45")
        getFirstSubclass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest46")
        getSecondSubclass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest47")

        p = subprocess.Popen(getSuperClass);
        p.wait()
        p = subprocess.Popen(getFirstSubclass);
        p.wait()
        p = subprocess.Popen(getSecondSubclass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest47")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest46.java line 3']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest46.java line 3']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest46.java line 3']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest46.java line 3']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest46.java line 3']['depths'], [1]);
    
        self.assertEqual(resultList['SyncBlockTest46.java line 6']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest46.java line 6']['read'], 1);
        self.assertEqual(resultList['SyncBlockTest46.java line 6']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest46.java line 6']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest46.java line 6']['depths'], [1]);

    def test_recursive_reentrant_readLast(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest37")

        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest37")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest37.java line 5']['total'], 11);
        self.assertEqual(resultList['SyncBlockTest37.java line 5']['read'], 11);
        self.assertEqual(resultList['SyncBlockTest37.java line 5']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest37.java line 5']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest37.java line 5']['depths'], [0,1,2,3,4,5,6,7,8,9,10]);
    
    def test_mulitpleDepths(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest40")

        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun  -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest40")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest40.java line 3']['total'], 2);
        self.assertEqual(resultList['SyncBlockTest40.java line 3']['read'], 2);
        self.assertEqual(resultList['SyncBlockTest40.java line 3']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest40.java line 3']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest40.java line 3']['depths'], [0,1]);

    def test_rnw_diffDepths(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest43")

        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -array=FINE -classpath=\"src/Targets\" -toolpath=\"classes\" -classes=\"-tools.syncBlockStats.*\" -tool=tools.syncBlockStats.SyncBlocksStats -noOrder SyncBlockTest43")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList['SyncBlockTest43.java line 4']['total'], 2);
        self.assertEqual(resultList['SyncBlockTest43.java line 4']['read'], 2);
        self.assertEqual(resultList['SyncBlockTest43.java line 4']['write'], 0);
        self.assertEqual(resultList['SyncBlockTest43.java line 4']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest43.java line 4']['depths'], [1,2]);

        self.assertEqual(resultList['SyncBlockTest43.java line 18']['total'], 1);
        self.assertEqual(resultList['SyncBlockTest43.java line 18']['read'], 0);
        self.assertEqual(resultList['SyncBlockTest43.java line 18']['write'], 1);
        self.assertEqual(resultList['SyncBlockTest43.java line 18']['neither'], 0);
        self.assertEqual(resultList['SyncBlockTest43.java line 18']['depths'], [0]);

suite = unittest.TestLoader().loadTestsFromTestCase(StaticSyncBlockTest)
unittest.TextTestRunner(verbosity=2).run(suite)

