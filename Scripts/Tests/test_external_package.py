import OpenLxApp as lx

try:
    import numpy as np
except ImportError:
    lx.installPythonPackage('numpy')
    import numpy as np
    
a = np.array( [20,30,40,50] )
print (type(a))
b = np.arange( 4 )
print (b)  
