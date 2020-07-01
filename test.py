import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

print(cuda.mem_get_info())

cuda.DeviceAllocation.free(0)