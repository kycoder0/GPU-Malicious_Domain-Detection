import pandas as pd
import pycuda
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
import numpy as np
class Matcher:
    def __init__(self, readpath):
        """
        Constructor that sets up our data to search domains against it
        @params:
            readpath: the path to our local domain data
        """
        self.readpath = readpath
        fileName = self.readpath[self.readpath.rfind('/') + 1:]
        #print('Reading ' + fileName + '...')
        df = pd.read_csv(self.readpath, encoding = "ISO-8859-1", sep = ',', names = list(range(0,3)), dtype='unicode')

        df = df.drop([df.columns[0], df.columns[2]], axis = 'columns')
        self.data = df.values # numpy array
        #print(self.data)
        self.data = self.data.ravel() # transforms the dataframe into a single column
        #print(self.data)
        self.data = self.data.astype(numpy.str)
        #print(self.data)
        print(len(self.data))
        self.set_to_naive()
        self.algorithm = 'Naive'
        self.is_loaded = False
    def unload_gpu(self):
        data_changed = numpy.empty_like(self.data)
        cuda.memcpy_dtoh(data_changed, self.data_gpu)
        self.is_loaded = False

    def set_to_naive(self):
        self.mod = SourceModule("""
            #include <stdio.h>
          __global__ void kernel(char *data, char *word, char *flag, int *length)
          {
            if(flag[0] == 1) {
                return;
            }

            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);
            //printf("length:%d blockId:%d threadY:%d threadX:%d\\n", length[0], blockId, threadIdx.y, threadIdx.x);
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
        self.algorithm = 'Naive'
    def set_algorithm(self, name):
        if name == 'Levenshtein':
            self.set_to_kmp()
        else:
            self.set_to_naive()

    def load_gpu(self):
        self.data_gpu = cuda.mem_alloc(len(max(self.data, key=len)) * self.data.size * 8) # allocate memory
        #print(len(max(self.data, key=len)) * self.data.size * 8)
        cuda.memcpy_htod(self.data_gpu, self.data)
        # print('max len = ' + str(len(max(self.data, key=len))))
        self.max_length = len(max(self.data, key=len)) * 4
        
        self.func = self.mod.get_function("kernel")
        self.is_loaded = True
    def set_to_hamming(self):
        self.mod = SourceModule("""
            #include <stdio.h>
          __global__ void kernel(char *data, char *word, int *length, int *distances, int *word_len)
          {
            //dp[0][0] = 1;
            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int distances_idx = (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);
            int data_idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);

            //printf("%d\\n", distances[distances_idx]);
            //distances[distances_idx] = 0;
            int len;

            if (length[0] > word_len[0]) {
                len = word_len[0];
            }
            else {
                len = length[0];
            }

            int diff = 0;

            for (int i = 0; i < len; i++) {
                if (data[data_idx + 4 * i] != word[4*i]) {
                    diff += 1;
                }
            }

            distances[distances_idx] = diff;
        }
            """)
    
    def set_to_levenshtein(self):
        self.mod = SourceModule("""
            #include <stdio.h>
          __global__ void kernel(char *data, char *word, int *length, int *distances, int *word_len)
          {
            //dp[0][0] = 1;
            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int distances_idx = (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);
            int data_idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);

            //printf("%d\\n", distances[distances_idx]);
            //distances[distances_idx] = 0;

            int dp [300][300];
           // int len = length[0];
           int len = length[0]/4;
           //printf("%d %d", len, word_len[0]);
            for (int i = 0; i <= len; i++) {
                for (int j = 0; j <= word_len[0]; j++) {
                    dp[i][j] = 0;
                }
            }

            for (int i = 0; i <= len; i++) {
                dp[i][0] = i;
            }

            for (int j = 0; j <= word_len[0]; j++) {
                dp[0][j] = j;
            }

            int val1 = 0;
            int val2 = 0;
            int val3 = 0;
            
            for (int i = 1; i <= len; i++) {
                for (int j = 1; j <= word_len[0]; j++) {
                    //printf("%c", data[data_idx + (i - 1)*4]);
                    if (data[data_idx + (j - 1)*4] == word[(i-1)*4]) {
                        val1 = dp[i - 1][j] + 1;
                        val2 = dp[i - 1][j - 1];
                        val3 = dp[i][j - 1] + 1;
                        if (val1 < val2) {
                            if (val1 < val3) {
                                dp[i][j] = val1;
                            }
                            else {
                                dp[i][j] = val3;
                            }
                        }
                        else {
                            if (val2 < val3) {
                                dp[i][j] = val2;
                            }
                            else {
                                dp[i][j] = val3;
                            }
                        }
                    }
                    else {
                        val1 = dp[i - 1][j] + 1;
                        val2 = dp[i - 1][j - 1] + 1;
                        val3 = dp[i][j - 1] + 1;
                        if (val1 < val2) {
                            if (val1 < val3) {
                                dp[i][j] = val1;
                            }
                            else {
                                dp[i][j] = val3;
                            }
                        }
                        else {
                            if (val2 < val3) {
                                dp[i][j] = val2;
                            }
                            else {
                                dp[i][j] = val3;
                            }
                        }
                    }
                }
                //printf("\\n");
            }
            
            distances[distances_idx] = dp[len][word_len[0]];
            //free(dp);
            //printf("%d", distances[distances_idx]);
            //dp = NULL;
          }
          """)
#self.func(self.data_gpu, word_gpu, length_gpu, word_len_gpu, flag_gpu
    def set_to_kmp(self):
        self.mod = SourceModule("""
            #include <stdio.h>

            
          __global__ void kernel(char *data, char *word, int *length, int *word_len, char *flag)
          {
            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int distances_idx = (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);
            int data_idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);

            int M = *word_len;
            int N = 0;

            while (data[N * 4 + data_idx] != '\\0') {
                N++;
            }
            //printf("%d\\n", N);
            int lps[300];
            // computing lps array
            int len = 0;
            lps[0] = 0;

            int i = 1;

            while (i < M) {
                if (word[i*4] == word[len]) {
                    len++;
                    lps[i] = len;
                    i++;
                }
                else {
                    if (len != 0) {
                        len = lps[len - 1];
                    }
                    else // if (len == 0) 
                    {
                        lps[i] = 0;
                        i++;
                    }
                }
            }
            // kmp algorithm
            i = 0;
            int j = 0;

            while (i < N) {

                if (word[j*4] == data[i * 4 + data_idx]) {
                    j++;
                    i++;
                }

                if (j == M) {
                    
                    flag[0] = 1;
                    j = lps[j - 1];
                }
                else if (i < N && word[j*4] != data[i * 4 + data_idx]) {
                    // Do not match lps[0..lps[j-1]] characters, 
                    // they will match anyway 
                    if (j != 0)
                        j = lps[j - 1];
                    else
                        i = i + 1;
                }
            }
            
        }
            """)
#self.data_gpu, word_gpu, length_gpu, word_len_gpu, flag_gpu
    def set_to_rabin_karp(self):
        self.mod = SourceModule("""
            #include <stdio.h>
            #define d 256
          __global__ void kernel(char *data, char *word, int *length, int *word_len, char *flag)
          {
            //dp[0][0] = 1;
            int blockId = blockIdx.y * gridDim.x + blockIdx.x;
            int distances_idx = (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);
            int data_idx = length[0] * (blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x);

            int M = *word_len;
            int N = 0;

            while (data[N * 4 + data_idx] != '\\0') {
                N++;
            }

            int i, j;
            int p = 0;
            int t = 0;
            int h = 1;
            int q = 101;
            
            for (i = 0; i < M - 1; i++)
                h = (h * d) % q;
            
            for (i = 0; i < M; i++) {
                p = (d * p + word[i * 4]) % q;
                t = (256 * t + data[i * 4 + data_idx]) % q;
            }


            for (i = 0; i <= N - M; i++) {
                if (p == t) {
                    for (j = 0; j < M; j++) {
                        if (data[(i+j)*4 + data_idx] != word[j * 4])
                            break;
                    }

                    if (j == M)
                        flag[0] = 1;
                }
                if (i < N - M) {
                    t = (d * (t - data[i * 4 + data_idx] * h) + data[(i+M)*4]) % q;

                    if (t < 0)
                        t = (t + q);
                }
            }

        }
            """)
    def get_levenshtein_distance(self, word):
        distances = [0 for x in range(len(self.data))]
        # dp = [[0 for x in range(self.max_length//4)] for i in range(self.max_length//4)]
        #print(dp)
         # initializing our variables
        word_len = len(word)
        word = numpy.asarray(word)
        flag = numpy.asarray(0)
        length = numpy.int32(self.max_length)
        distances = numpy.asarray(distances)
        word_len =  numpy.int32(word_len)
       # dp = numpy.asarray(dp)

        # allocating memory for our variables on the GPU
        word_gpu = cuda.mem_alloc(self.max_length * 8)
        #flag_gpu = cuda.mem_alloc(32)
        length_gpu = cuda.mem_alloc(length.nbytes)
        distances_gpu = cuda.mem_alloc(len(self.data) * 32)
        word_len_gpu = cuda.mem_alloc(word_len.nbytes)
        #dp_gpu = cuda.mem_alloc(((self.max_length//4)**2) * 128)

        # putting the variables into the GPU memory we allocated
        cuda.memcpy_htod(word_gpu, word)
        #cuda.memcpy_htod(flag_gpu, flag)
        cuda.memcpy_htod(length_gpu, length)
        cuda.memcpy_htod(distances_gpu, distances)
        cuda.memcpy_htod(word_len_gpu, word_len)
        #cuda.memcpy_htod(dp_gpu, dp)
        # calculating the number of blocks we need for our data
        grid_size = int((self.data.size/1024)**(0.5))

        self.set_to_levenshtein()
        self.func = self.mod.get_function("kernel")
        # calling our kernel
        self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (grid_size + 1, grid_size + 1, 1), block=(32, 32,1))
        #self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (1, 1, 1), block=(1, 1 ,1))
        # cleaning the variables from our GPU, since we didn't clean up the
        # database data, it is still stored on the GPU, ready for a new search
        word_changed = numpy.empty_like(word)
        #flag_changed = numpy.empty_like(flag)
        length_changed = numpy.empty_like(length)
        distances_changed = numpy.empty_like(distances)
        word_len_changed = numpy.empty_like(word_len)
        #dp_changed = numpy.empty_like(dp)

        cuda.memcpy_dtoh(word_changed, word_gpu)
        #cuda.memcpy_dtoh(flag_changed, flag_gpu)
        cuda.memcpy_dtoh(length_changed, length_gpu)
        cuda.memcpy_dtoh(distances_changed, distances_gpu)
        cuda.memcpy_dtoh(word_len_changed, word_gpu)
        #cuda.memcpy_dtoh(dp_changed, dp_gpu)

        highest_match = self.get_match_levenshtein(distances_changed)
        return highest_match # return if the flag has been changed to 1
    
    def get_match_levenshtein(self, distances):
        print(distances)
        min_pos = min(range(len(distances)), key=distances.__getitem__)
        return self.data[min_pos]

    def get_hamming_distance(self, word):
        distances = [0 for x in range(len(self.data))]
        # dp = [[0 for x in range(self.max_length//4)] for i in range(self.max_length//4)]
        #print(dp)
         # initializing our variables
        word_len = len(word)
        word = numpy.asarray(word)
        flag = numpy.asarray(0)
        length = numpy.int32(self.max_length)
        distances = numpy.asarray(distances)
        word_len =  numpy.int32(word_len)
       # dp = numpy.asarray(dp)

        # allocating memory for our variables on the GPU
        word_gpu = cuda.mem_alloc(self.max_length * 8)
        #flag_gpu = cuda.mem_alloc(32)
        length_gpu = cuda.mem_alloc(length.nbytes)
        distances_gpu = cuda.mem_alloc(len(self.data) * 32)
        word_len_gpu = cuda.mem_alloc(word_len.nbytes)
        #dp_gpu = cuda.mem_alloc(((self.max_length//4)**2) * 128)

        # putting the variables into the GPU memory we allocated
        cuda.memcpy_htod(word_gpu, word)
        #cuda.memcpy_htod(flag_gpu, flag)
        cuda.memcpy_htod(length_gpu, length)
        cuda.memcpy_htod(distances_gpu, distances)
        cuda.memcpy_htod(word_len_gpu, word_len)
        #cuda.memcpy_htod(dp_gpu, dp)
        # calculating the number of blocks we need for our data
        grid_size = int((self.data.size/1024)**(0.5))

        self.set_to_hamming()
        self.func = self.mod.get_function("kernel")
        # calling our kernel
        self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (grid_size + 1, grid_size + 1, 1), block=(32, 32,1))
        #self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (1, 1, 1), block=(1, 1 ,1))
        # cleaning the variables from our GPU, since we didn't clean up the
        # database data, it is still stored on the GPU, ready for a new search
        word_changed = numpy.empty_like(word)
        #flag_changed = numpy.empty_like(flag)
        length_changed = numpy.empty_like(length)
        distances_changed = numpy.empty_like(distances)
        word_len_changed = numpy.empty_like(word_len)
        #dp_changed = numpy.empty_like(dp)

        cuda.memcpy_dtoh(word_changed, word_gpu)
        #cuda.memcpy_dtoh(flag_changed, flag_gpu)
        cuda.memcpy_dtoh(length_changed, length_gpu)
        cuda.memcpy_dtoh(distances_changed, distances_gpu)
        cuda.memcpy_dtoh(word_len_changed, word_gpu)
        #cuda.memcpy_dtoh(dp_changed, dp_gpu)

        highest_match = self.get_match_levenshtein(distances_changed)
        return highest_match # return if the flag has been changed to 1
    def is_malicious_naive_gpu(self, word):
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

    def is_malicious_naive_cpu(self, word):
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

    def is_malicious_naive(self, word, hardware):

        if hardware == 'GPU':
            return self.is_malicious_naive_gpu(word)
        else:
            return self.is_malicious_naive_cpu(word)


    def is_malicious_kmp_gpu(self, word):
        #distances = [0 for x in range(len(self.data))]
        # dp = [[0 for x in range(self.max_length//4)] for i in range(self.max_length//4)]
        #print(dp)
         # initializing our variables
        word_len = len(word)
        word = numpy.asarray(word)
        flag = numpy.asarray(0)
        length = numpy.int32(self.max_length)
        #distances = numpy.asarray(distances)
        word_len =  numpy.int32(word_len)
       # dp = numpy.asarray(dp)

        # allocating memory for our variables on the GPU
        word_gpu = cuda.mem_alloc(self.max_length * 8)
        flag_gpu = cuda.mem_alloc(32)
        length_gpu = cuda.mem_alloc(length.nbytes)
        #distances_gpu = cuda.mem_alloc(len(self.data) * 32)
        word_len_gpu = cuda.mem_alloc(word_len.nbytes)
        #dp_gpu = cuda.mem_alloc(((self.max_length//4)**2) * 128)

        # putting the variables into the GPU memory we allocated
        cuda.memcpy_htod(word_gpu, word)
        cuda.memcpy_htod(flag_gpu, flag)
        cuda.memcpy_htod(length_gpu, length)
        #cuda.memcpy_htod(distances_gpu, distances)
        cuda.memcpy_htod(word_len_gpu, word_len)
        #cuda.memcpy_htod(dp_gpu, dp)
        # calculating the number of blocks we need for our data
        grid_size = int((self.data.size/1024)**(0.5))

        self.set_to_kmp()
        self.func = self.mod.get_function("kernel")
        # calling our kernel
        self.func(self.data_gpu, word_gpu, length_gpu, word_len_gpu, flag_gpu, grid = (grid_size + 1, grid_size + 1, 1), block=(32, 32,1))
        #self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (1, 1, 1), block=(1, 1 ,1))
        # cleaning the variables from our GPU, since we didn't clean up the
        # database data, it is still stored on the GPU, ready for a new search
        word_changed = numpy.empty_like(word)
        flag_changed = numpy.empty_like(flag)
        length_changed = numpy.empty_like(length)
       # distances_changed = numpy.empty_like(distances)
        word_len_changed = numpy.empty_like(word_len)
        #dp_changed = numpy.empty_like(dp)

        cuda.memcpy_dtoh(word_changed, word_gpu)
        cuda.memcpy_dtoh(flag_changed, flag_gpu)
        cuda.memcpy_dtoh(length_changed, length_gpu)
        #cuda.memcpy_dtoh(distances_changed, distances_gpu)
        cuda.memcpy_dtoh(word_len_changed, word_gpu)
        #cuda.memcpy_dtoh(dp_changed, dp_gpu)
        return flag_changed

    def is_malicious_rabin_karp_gpu(self, word):
        #distances = [0 for x in range(len(self.data))]
        # dp = [[0 for x in range(self.max_length//4)] for i in range(self.max_length//4)]
        #print(dp)
         # initializing our variables
        word_len = len(word)
        word = numpy.asarray(word)
        flag = numpy.asarray(0)
        length = numpy.int32(self.max_length)
        #distances = numpy.asarray(distances)
        word_len =  numpy.int32(word_len)
       # dp = numpy.asarray(dp)

        # allocating memory for our variables on the GPU
        word_gpu = cuda.mem_alloc(self.max_length * 8)
        flag_gpu = cuda.mem_alloc(32)
        length_gpu = cuda.mem_alloc(length.nbytes)
        #distances_gpu = cuda.mem_alloc(len(self.data) * 32)
        word_len_gpu = cuda.mem_alloc(word_len.nbytes)
        #dp_gpu = cuda.mem_alloc(((self.max_length//4)**2) * 128)

        # putting the variables into the GPU memory we allocated
        cuda.memcpy_htod(word_gpu, word)
        cuda.memcpy_htod(flag_gpu, flag)
        cuda.memcpy_htod(length_gpu, length)
        #cuda.memcpy_htod(distances_gpu, distances)
        cuda.memcpy_htod(word_len_gpu, word_len)
        #cuda.memcpy_htod(dp_gpu, dp)
        # calculating the number of blocks we need for our data
        grid_size = int((self.data.size/1024)**(0.5))

        self.set_to_rabin_karp()
        self.func = self.mod.get_function("kernel")
        # calling our kernel
        self.func(self.data_gpu, word_gpu, length_gpu, word_len_gpu, flag_gpu, grid = (grid_size + 1, grid_size + 1, 1), block=(32, 32,1))
        #self.func(self.data_gpu, word_gpu, length_gpu, distances_gpu, word_len_gpu, grid = (1, 1, 1), block=(1, 1 ,1))
        # cleaning the variables from our GPU, since we didn't clean up the
        # database data, it is still stored on the GPU, ready for a new search
        word_changed = numpy.empty_like(word)
        flag_changed = numpy.empty_like(flag)
        length_changed = numpy.empty_like(length)
       # distances_changed = numpy.empty_like(distances)
        word_len_changed = numpy.empty_like(word_len)
        #dp_changed = numpy.empty_like(dp)

        cuda.memcpy_dtoh(word_changed, word_gpu)
        cuda.memcpy_dtoh(flag_changed, flag_gpu)
        cuda.memcpy_dtoh(length_changed, length_gpu)
        #cuda.memcpy_dtoh(distances_changed, distances_gpu)
        cuda.memcpy_dtoh(word_len_changed, word_gpu)
        #cuda.memcpy_dtoh(dp_changed, dp_gpu)
        return flag_changed
    def is_malicious_kmp_cpu(self, word):
        pass

    def is_malicious_kmp(self, word, hardware):
        if hardware == 'GPU':
            return self.is_malicious_kmp_gpu(word)
        else:
            return self.is_malicious_kmp_cpu(word)
    def is_malicious(self, domains, hardware, algorithm):
        """
        This function sets up our temporary variables and calls our kernel that
        resides on our GPU threads to check if our domain is malicious or not
        @params:
            word: the domain to be searched for
        """

        malicious_domains = list()
        times = list()
        cuda.Context.set_limit(cuda.limit.STACK_SIZE, 0)
        if hardware == 'GPU':
            if algorithm == 'Levenshtein':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.get_levenshtein_distance(domain))
                    cuda.Context.set_limit(cuda.limit.STACK_SIZE, 0)
                    end = time.time()
                    times.append(end-start)
            elif algorithm == 'Hamming':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.get_hamming_distance(domain))
                    end = time.time()
                    times.append(end-start)
            elif algorithm == 'KMP':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.is_malicious_kmp_gpu(domain))
                    end = time.time()
                    times.append(end-start)
            elif algorithm == 'Rabin-Karp':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.is_malicious_rabin_karp_gpu(domain))
                    end = time.time()
                    times.append(end-start)
            else:
                self.set_to_naive()
                self.func = self.mod.get_function("kernel")
                print(domains)
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.is_malicious_naive_gpu(domain))
                    end = time.time()
                    times.append(end-start)
        else:
            if algorithm == 'Levenshtein':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.get_levenshtein_distance_cpu(domain))
                    end = time.time()
                    times.append(end-start)
            elif algorithm == 'Hamming':
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.get_hamming_distance_cpu(domain))
                    end = time.time()
                    times.append(end-start)
            else:
                for domain in domains:
                    start = time.time()
                    malicious_domains.append(self.cpu_run(domain))
                    end = time.time()
                    times.append(end-start)
        for i in range(1, len(times)):
            times[i] = times[i] + times[i-1]
        print(malicious_domains)
        print(times)
        cuda.Context.set_limit(cuda.limit.STACK_SIZE, 0)
        return malicious_domains, times
    def levenshteinlist(self, dom1, domlist):
        length = len(domlist)
        distlist = [] 
        for i in range(length):
            distlist.append(self.levenshtein(dom1, domlist[i]))
        return distlist
    def levenshtein(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                )
        return matrix[size_x - 1, size_y - 1]
    def get_levenshtein_distance_cpu(self, domain):
        distances_changed = self.levenshteinlist(domain, self.data)
        return self.get_match_levenshtein(distances_changed)

    def get_hamming_distance_helper(self, domain1, domain2):
        smallest_len = min(len(domain1), len(domain2))

        count = 0
        for i in range(smallest_len):
            if domain1[i] != domain2[i]:
                count = count + 1
        return count
    def get_hamming_distance_cpu(self, domain):

        dist_list = []
        for do in self.data:
            dist_list.append(self.get_hamming_distance_helper(domain, do))
        return self.get_match_levenshtein(dist_list)
        
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
        domains = samples
        matched = 0
        for domain in domains:
            if (self.is_malicious_naive_cpu(domain)):
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





def main():
    domains = ['easter', 'con', 'fhoewahyf9aw48yf9y32498py9f8023hy']

    matcher = Matcher('C:\\Users\\trevo\\Documents\\malicious-domain-detection\\localdata.csv')

    matcher.load_gpu()


    #matcher.load_gpu()
    matcher.is_malicious(domains, 'GPU', 'Rabin-Karp')
if __name__ == '__main__':
    main()