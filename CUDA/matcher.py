import pandas as pd
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import sys
import numpy
import math
import time
import random
import os
#import resource
import psutil
class Matcher:
    def __init__(self, readpath):
        """
        Constructor that sets up our data to search domains against it
        @params:
            readpath: the path to our local domain data
        """
        self.readpath = readpath
        fileName = self.readpath[self.readpath.rfind('/') + 1:]
        print('Reading ' + fileName + '...')
        df = pd.read_csv(self.readpath, encoding = "ISO-8859-1", sep = ',', names = list(range(0,3)), dtype='unicode')

        df = df.drop([df.columns[0], df.columns[2]], axis = 'columns')
        self.data = df.values # numpy array
        self.data = self.data.ravel() # transforms the dataframe into a single column
        self.data = self.data.astype(numpy.str)
    def unload_gpu(self):
        data_changed = numpy.empty_like(self.data)
        cuda.memcpy_dtoh(data_changed, self.data_gpu)

    def load_gpu(self):

        print(self.data)
        print(len(self.data))
        self.data_gpu = cuda.mem_alloc(len(max(self.data, key=len)) * self.data.size * 8) # allocate memory
        cuda.memcpy_htod(self.data_gpu, self.data)
        self.max_length = len(max(self.data, key=len)) * 4
        self.mod = SourceModule("""
            #include <stdio.h>
          __global__ void kernel(char *data, char *word, char *flag, int *length)
          {
            if(flag[0] == 1) {
                return;
            }
            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);

            int tempFlag = 1;
            for (int i = idx; i < length[0] + idx; i += 4) {
                if (data[i] != word[i-idx]) {
                    tempFlag = 0;
                    break;
                }
            }
            if(tempFlag == 1) {
                flag[0] = 1;
            }

          }

          """)
        self.func = self.mod.get_function("kernel")

    def is_malicious(self, word):
        """
        This function sets up our temporary variables and calls our kernel that
        resides on our GPU threads to check if our domain is malicious or not
        @params:
            word: the domain to be searched for
        """
        # initializing our variables
        word = numpy.asarray(word)
        flag = numpy.asarray(0)
        length = numpy.int32(self.max_length)

        # allocating memory for our variables on the GPU
        word_gpu = cuda.mem_alloc(self.max_length * 8)
        flag_gpu = cuda.mem_alloc(32)
        length_gpu = cuda.mem_alloc(length.nbytes)

        # putting the variables into the GPU memory we allocated
        cuda.memcpy_htod(word_gpu, word)
        cuda.memcpy_htod(flag_gpu, flag)
        cuda.memcpy_htod(length_gpu, length)

        # calculating the number of blocks we need for our data
        grid_size = int((self.data.size/1024)**(0.5))

        # calling our kernel
        self.func(self.data_gpu, word_gpu, flag_gpu, length_gpu, grid = (grid_size + 1, grid_size + 1, 1), block=(32, 32,1))

        # cleaning the variables from our GPU, since we didn't clean up the
        # database data, it is still stored on the GPU, ready for a new search
        word_changed = numpy.empty_like(word)
        flag_changed = numpy.empty_like(flag)
        length_changed = numpy.empty_like(length)
        cuda.memcpy_dtoh(word_changed, word_gpu)
        cuda.memcpy_dtoh(flag_changed, flag_gpu)
        cuda.memcpy_dtoh(length_changed, length_gpu)
        return flag_changed # return if the flag has been changed to 1

    def is_malicious_cpu(self, word):
        """
        Simple Python function that essentially does the same thing as our GPU
        algorithm, however, uses the CPU instead
        @params:
            word: The domain that will be labeled as malicious or not
        """
        found = False
        for x in self.data:
            if (found):
                continue
            if x == word:
                found = True
        return found

    def time_diff(self, num_samples):
        """
        Function to compare the average computation times of each algorithm
        @params:
            num_samples: the number of domains you'd like to search for
        """
        sum = 0
        for i in range(num_samples):
            x = self.data[random.randint(0, len(self.data))]
            cpu_start = time.time()
            self.is_malicious_cpu(x)
            cpu_total = time.time() - cpu_start

            gpu_start = time.time()
            self.is_malicious(x)
            gpu_total = time.time() - gpu_start

            diff = cpu_total - gpu_total
            sum += diff
        total_diff = sum/num_samples
        print("The GPU is on average, " + str(round(total_diff, 3)) + " seconds faster than the CPU")


    def gpu_run(self, samples):
        domains = samples.values
        matched = 0
        for domain in domains:
            print(domain[0])
            if (self.is_malicious(domain[0])):
                print(domain[0] + ' malicious')
                matched += 1
        return matched

    def gpu_speed_test(self, samples):
        start = time.time()
        matched = self.gpu_run(samples)
        end = time.time() - start

        return (matched, end)

    def gpu_memory_test():
        pass


    def cpu_run(self, samples):
        domains = samples.values
        matched = 0
        for domain in domains:
            print(domain[0])
            if (self.is_malicious_cpu(domain[0])):
                print(domain[0] + ' malicious')
                matched += 1
        return matched

    def cpu_speed_test(self, samples):
        start = time.time()
        matched = self.cpu_run(samples)
        end = time.time() - start

        return (matched, end)

    def cpu_memory_test(self, samples):
        #start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss)
        matched = self.cpu_run(samples)
        #end_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_mem
        print(process.memory_info().rss)
        #print("end = " + str(end_mem))
