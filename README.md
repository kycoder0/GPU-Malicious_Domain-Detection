# Malicious Domain Detection with GPU computation

## Purpose
 &nbsp;&nbsp;&nbsp;&nbsp; This project was created in attempts to implement a system that autonomously works to effeciently and effectivley mark malicious domains as malicious and malignant ones as malignant. To do this, I have studied CUDA, specifically using Python's PyCuda wrapper, to implement the algorithm.

## Installation
### Prerequisites:
* A [CUDA Compatible GPU](https://developer.nvidia.com/cuda-gpus "CUDA compatible GPU")
* Latest installation of [Python3](https://www.python.org/downloads/ ""). Built and tested on Python 3.8.1
* Up to date [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx "Drivers")
* MySQL
* XAMPP web server or the like

Python Library Prerequisites:
* numpy
* pycuda
* mysqldb
* pandas
* threading
* psutil

Guide: <br>
* Install the CUDA Toolkit [here](https://developer.nvidia.com/cuda-toolkit ""). Different GPUs will require different versions of CUDA to run optimally. (Depending on GPU architecture)

* Before continuing to the next step I would reccomend downloading the [sample.py](https://github.com/TrevorRice39/malicious-domain-detection/blob/master/CUDA/sample.py "") from this repo. Run this and if there is no output or there are errors, there is a problem with your CUDA or PyCUDA installation.

* (This section will be completed for you when the installer is complete) Next you will need to create a MySQL database on your local computer/server. You need to name the database domains (can be customizable in the future) and use root with no password to log in. You need to create only one table.

| Static IP        | Domains           | Timestamp  |
| ------------- |:-------------:| -----:|
| 00.1.0100   | 123domain123.com | 2020-06-12T16:26:19+00:00 |

* Clone this repo onto your computer <br>
```
git clone https://github.com/TrevorRice39/malicious-domain-detection.git
``` 
* Ensure that your server is running with a valid database, and you can run 
    ```
    python3 main.py
    ```
    And the program should start.

## <span style="color:maroon">Eastern Kentucky Univeristy</span>
### Author: Trevor Rice