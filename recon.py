baseline = ('Java', "-inst=NOINST")

configs = [
    ('RR', ''),
    ('FR.FW.RACY', "-tool=BBF"),
    ('FR.FW.NONRACY', "-tool=BB  -readMissesOnly -writeMissesOnly"),
    ('FR.NOFW.NONRACY', "-tool=BB  -readMissesOnly"),
    ('NOFR.NOFW.NONRACY', "-tool=BB")
]

all_configs = [baseline] + configs

nthreads = 8

# Each entry is of the form ('name and args', 'jvm args', 'rr args')
benchmarks = [
    ('avrora', '-noverify', ''),
    # without -noverify: dacapo's validation of the output fails, but
    # the program itself doesn't crash.

    # BROKEN ('batik', '', ''),
    # InvocationTargetException from ClassFormatError: Invalid method
    # Code length 614880 in class file
    # org/apache/batik/xml/XMLCharacters
    #
    # -noverify turns this into a JVM segfault.

    # BROKEN ('eclipse', '-noverify', ''),
    # Even with -inst=NOINST, non-instrumentation failure:
    # Initialize workspace ...................Error creating workspace!
    # Java Model Exception: Java Model Status [Cannot nest
    # 'sampa/home/bpw/rr/RoadRunner/classes/rr/simple' inside library
    # 'sampa/home/bpw/rr/RoadRunner/classes']
    #
    # Later, we get a NullPointerException.
    #
    # With instrumentation and without -noverify
    # java.lang.VerifyError: (class:
    # org/eclipse/osgi/framework/internal/core/FrameworkProperties,
    # method: __$rr_inUse__$rr__Sync_ signature: ()Z) Illegal type in
    # constant pool
    #
    # With -noverify this turns into (regardless of -nojoin)
    #
    # java.lang.IllegalStateException: Unable to acquire application
    # service. Ensure that the org.eclipse.core.runtime bundle is
    # resolved and started (see config.ini).
    #
    # But it does not crash RR.

    # BROKEN ('h2', '', ''),
    # Even with -inst=NOINST (and regardless of -noverify, -multiLoader)
    # java.lang.NoSuchMethodException:
    # org.dacapo.h2.TPCC.make(org.dacapo.parser.Config, java.io.File,
    # java.lang.Boolean, java.lang.Boolean)

    # BROKEN ('jython', '', '') ,
    # many warnings about failing  to load classes, find methods
    #
    # java.lang.ClassFormatError: org/python/antlr/PythonParser

    ('luindex', '-noverify', ''),
    # without -noverify
    #    
    # java.lang.VerifyError: (class:
    # org/apache/lucene/store/IndexInput, method:
    # __$rr___$rr_length__$rr__Original___$rr__with_ThreadState_
    # signature: (Lrr/state/ShadowThread;)J) Stack size too large

    ('lusearch', '-noverify', ''),
    # without -noverify
    #    
    # java.lang.VerifyError: (class:
    # org/apache/lucene/store/IndexInput, method:
    # __$rr___$rr_length__$rr__Original___$rr__with_ThreadState_
    # signature: (Lrr/state/ShadowThread;)J) Stack size too large

    ('pmd', '-noverify', ''),
    # without -noverify
    #
    # java.lang.VerifyError: (class:
    # org/apache/xerces/impl/XMLEntityManager, method:
    # __$rr_getUserDir__$rr__Sync_ signature:
    # ()Lorg/apache/xerces/util/URI;) Illegal type in constant pool
    
    # BROKEN ('sunflow', '', ''),
    # without -noverify
    #
    # ClassFormatError: Invalid method Code length 94073 in class file
    # org/sunflow/core/tesselatable/Teapot
    #
    # JVM segfault with -noverify

    ('tomcat', '', '-multiLoader -shadowThread=-.* -maxTid=64'),
    # without -multiLoader
    ### PANIC Bad update cast: from: class
    # org.apache.juli.logging.LogFactory [0x56D73C7A (class
    # org.apache.catalina.loader.StandardClassLoader) -> 0x1F7182C1
    # (class sun.misc.Launcher$AppClassLoader) -> 0x553F5D07 (class
    # sun.misc.Launcher$ExtClassLoader) -> <System>] to class
    # __$rr_org_apache_juli_logging_LogFactory__$rr__Update_logConfig
    # [0x2FB3F8F6 (class org.dacapo.harness.DacapoClassLoader) ->
    # 0x1F7182C1 (class sun.misc.Launcher$AppClassLoader) ->
    # 0x553F5D07 (class sun.misc.Launcher$ExtClassLoader) ->
    # <System>].  
    ### Fix by alpha-renaming one of the classes to be unique.


    # BROKEN ('tradebeans', '', '-multiLoader -shadowThread=-.*'),
    # ExceptionInInitializerError ... caused by
    # java.lang.RuntimeException: Could not create jaxb contexts for
    # plugin types
    # java.lang.NoClassDefFoundError: Could not initialize class
    # org.apache.geronimo.system.configuration.AttributesXmlUtil

    # BROKEN ('tradesoap', '', ''),
    # Same as tradebeans

    ('xalan', '-noverify', '')
    # without -noverify: java.lang.VerifyError: (class:
    # org/apache/xerces/impl/XMLEntityManager, method:
    # __$rr_getUserDir__$rr__Sync_ signature:
    # ()Lorg/apache/xerces/util/URI;) Illegal type in constant pool
]

