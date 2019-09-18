import time
import numpy as np
from pycuda import driver, compiler, gpuarray, tools
import math
from sys import getsizeof

import pycuda.autoinit

kernel_code1 = """
__global__ void test1(char** d_wordList) {
      (d_wordList[blockIdx.x][threadIdx.x])++;
}
    """

kernel_code2 = """
__global__ void test2(char* d_wordList, size_t *offsets) {
    (d_wordList[offsets[blockIdx.x] + threadIdx.x])++;
}
    """




mod = compiler.SourceModule(kernel_code1)
ker_test1 = mod.get_function("test1")



wordList = ['asd','bsd','csd']

d_words = []

for word in wordList:
    d_words.append(gpuarray.to_gpu(np.array(word, dtype=str)))

d_wordList = gpuarray.to_gpu(np.array([word.ptr for word in d_words], dtype=np.uintp))

ker_test1(d_wordList, block=(3,1,1), grid=(3,1,1))

for word in d_words:
  result = word.get()
  print (result)

mod2 = compiler.SourceModule(kernel_code2)
ker_test2 = mod2.get_function("test2")
wordlist2 = np.array(['asdbsdcsd'], dtype=str)
d_words2 = gpuarray.to_gpu(np.array(['asdbsdcsd'], dtype=str))
offsets = gpuarray.to_gpu(np.array([0,3,6,9], dtype=np.uint64))
ker_test2(d_words2, offsets, block=(3,1,1), grid=(3,1,1))
h_words2 = d_words2.get()
print (h_words2)
