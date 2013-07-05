import unittest
import subprocess
import shlex

class SyncBlockTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        getTool = shlex.split("bash getToolFromEclipse SyncBlocksStats")
        p = subprocess.Popen(getTool)
        p.wait(); 

        return 

    def parseOutput(self, out):
        grep = shlex.split("grep result\ =\ {")
        find = subprocess.Popen(grep, stdin=out, stdout=subprocess.PIPE)
        output = find.stdout.readline() + find.stdout.readline() + find.stdout.readline() + find.stdout.readline()
        
        result = {};
        exec output
        return result

    def test_read_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest1")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest1")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)
       
        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 1)
        self.assertEqual(resultList["read"], 1)
        self.assertEqual(resultList["write"], 0)
        self.assertEqual(resultList["neither"], 0)
        return 
    
    def test_read_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest2")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest2")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 1)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_neither(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest3")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest3")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 1)

    def test_writefield_only(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest4")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest4")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 1)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)
        
    def test_wrfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest5")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest5")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 3)
        self.assertEquals(resultList["read"], 2)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 1)
        
    def test_no_blocks(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest6")
        p = subprocess.Popen(getTestClass);
        p.wait();

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest6")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 0)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_three_thread_read(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest7")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest7")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 3)
        self.assertEquals(resultList["read"], 3)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_three_thread_writefield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest8")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest8")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 3)
        self.assertEquals(resultList["read"], 3)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_two_nested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest9")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest9")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)
        
        self.assertEqual(resultList["total"], 2)
        self.assertEquals(resultList["read"], 1)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)

    def test_multithreaded(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest10")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest10")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 30)
        self.assertEquals(resultList["read"], 20)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 10)

    #def test_100threads_write(self):
    #   getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest11")
    #   p = subprocess.Popen(getTestClass);
    #   p.wait()

    #   runRR = shlex.split("rrrun -maxTid=150 -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-.*SyncBlocksStats.*\" -classes=\"-ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest11")
    #   runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

    #   resultList = self.parseOutput(runner.stdout)

    #   self.assertEqual(resultList["total"], 100)
    #   self.assertEquals(resultList["read"], 0)
    #   self.assertEquals(resultList["write"], 100)
    #   self.assertEquals(resultList["neither"], 0)
    
    def test_multithreaded_nested1(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest12")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest12")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 30)
        self.assertEquals(resultList["read"], 20)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 10)
    
    def test_multithreaded_nested2(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest13")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=150 -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-.*SyncBlocksStats.*\" -classes=\"-ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest13")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 300)
        self.assertEquals(resultList["read"], 100)
        self.assertEquals(resultList["write"], 100)
        self.assertEquals(resultList["neither"], 100)

    def test_Integer_fields(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest14")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest14")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 30)
        self.assertEquals(resultList["read"], 20)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 10)
    
    def test_multithreaded_arrayfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest15")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=60 -array=COARSE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-.*SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest15")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 200)
        self.assertEquals(resultList["read"], 150)
        self.assertEquals(resultList["write"], 50)
        self.assertEquals(resultList["neither"], 0)

    def test_multithreaded_nestedarray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest16")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=60 -array=COARSE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-.*SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest16")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1250)
        self.assertEquals(resultList["read"], 750)
        self.assertEquals(resultList["write"], 250)
        self.assertEquals(resultList["neither"], 250)

    def test_multithreaded_objectfield(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest17")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=60 -array=COARSE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-.*SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest17")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 400)
        self.assertEquals(resultList["read"], 300)
        self.assertEquals(resultList["write"], 100)
        self.assertEquals(resultList["neither"], 0)
    
    def test_syncOnWritten_field(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest18")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest18")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)
    
    def test_syncOnWritten_object(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest19")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -field=FINE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest19")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)

    def test_volatile_rwn(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest20")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -field=FINE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest20")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 30)
        self.assertEquals(resultList["read"], 20)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 10)

    def test_get_set(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest21")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -field=FINE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest21")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 2)
        self.assertEquals(resultList["read"], 2)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_syncOnWritten_array(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest22")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -field=FINE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest22")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)

    def test_syncOn_private(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest23")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -field=FINE -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest23")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)
    
    def test_multithreaded_syncOnField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest24")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=30 -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest24")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 60)
        self.assertEquals(resultList["read"], 20)
        self.assertEquals(resultList["write"], 20)
        self.assertEquals(resultList["neither"], 20)

    def test_multithreaded_syncOnArray(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest25")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest25")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 30)
        self.assertEquals(resultList["read"], 10)
        self.assertEquals(resultList["write"], 10)
        self.assertEquals(resultList["neither"], 10)

    def test_methodCalls(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest26")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest26")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 2)
        self.assertEquals(resultList["read"], 2)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_syncOn_static(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest27")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest27")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)

    def test_write_staticField(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest28")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest28")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 4)
        self.assertEquals(resultList["read"], 3)
        self.assertEquals(resultList["write"], 1)
        self.assertEquals(resultList["neither"], 0)
    #    
    #def test_syncOn_write_local(self):
    #   getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest29")
    #   p = subprocess.Popen(getTestClass);
    #   p.wait()

    #   runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest29")
    #   runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

    #   resultList = self.parseOutput(runner.stdout)

    #   self.assertEqual(resultList["total"], 1)
    #   self.assertEquals(resultList["read"], 0)
    #   self.assertEquals(resultList["write"], 1)
    #   self.assertEquals(resultList["neither"], 0)
        
    #def test_local_access(self):
    #   getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest30")
    #   p = subprocess.Popen(getTestClass);
    #   p.wait()

    #   runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest30")
    #   runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

    #   resultList = self.parseOutput(runner.stdout)

    #   self.assertEqual(resultList["total"], 1)
    #   self.assertEquals(resultList["read"], 0)
    #   self.assertEquals(resultList["write"], 1)
    #   self.assertEquals(resultList["neither"], 0)
        
    def test_sync_this(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest31")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest31")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 1)
        self.assertEquals(resultList["read"], 1)
        self.assertEquals(resultList["write"], 0)
        self.assertEquals(resultList["neither"], 0)

    def test_serial_triplyNested(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest33")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest33")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 300)
        self.assertEquals(resultList["read"], 100)
        self.assertEquals(resultList["write"], 100)
        self.assertEquals(resultList["neither"], 100)
        
    def test_multithreaded_write(self):
        getTestClass = shlex.split("bash getTargetFromEclipse -t SyncBlockTest34")
        p = subprocess.Popen(getTestClass);
        p.wait()

        runRR = shlex.split("rrrun -maxTid=150 -classpath=\"./src/Targets\" -toolpath=\"./classes/tools/trials\" -classes=\"-SyncBlocksStats.*\" -classes=\"-.*ScriptEngine.*\" -tool=SyncBlocksStats SyncBlockTest34")
        runner = subprocess.Popen(runRR, stdout=subprocess.PIPE)

        resultList = self.parseOutput(runner.stdout)

        self.assertEqual(resultList["total"], 100)
        self.assertEquals(resultList["read"], 0)
        self.assertEquals(resultList["write"], 100)
        self.assertEquals(resultList["neither"], 0)








    
suite = unittest.TestLoader().loadTestsFromTestCase(SyncBlockTests)
unittest.TextTestRunner(verbosity=2).run(suite)
