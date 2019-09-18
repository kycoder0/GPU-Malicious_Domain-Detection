# Malicious Domain Detection with GPU computation

## Purpose
 &nbsp;&nbsp;&nbsp;&nbsp; This project was created in attempts to implement a system that autonomously works to effeciently and effectivley mark malicious domains as malicious and malignant ones as malignant. To do this, I have studied CUDA, specifically using Python's PyCuda wrapper, to implement the algorithm. The project is still in its infancy and can still be improved greatly.

## Progress
 &nbsp;&nbsp;&nbsp;&nbsp; So far, I have a fully functional system that allows me or another user to upload data sets (malicious domains) into a local database and then run tests with single domains, or list of domains to discover if they are malicious or not. I have implemented speed tests that compare the computation times between the GPU and CPU and I have also put work into creating a GUI for the full system. The system currently works as expected, but needs work to allow users to enter data more easily than now. My next step in the project is to implement a web crawler using Scrapy, that allows me to to scrape data domains from websites that have known malicious domains. I would also like to create a more sophisticated string matching algorithm that can extract the second level domain instead of doing a full comparison in hopes of correctly identifying more domains.

## 

## <span style="color:maroon">Eastern Kentucky Univeristy</span>
### Author: Trevor Rice