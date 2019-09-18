import string
import random
import pandas
import os
directoryPath = os.path.dirname(os.path.realpath(__file__))
directoryPath = directoryPath[ :directoryPath.rfind('/')]
directoryPath = directoryPath[ :directoryPath.rfind('/')] + '/Data/random.csv'
if os.path.exists(directoryPath):
    os.remove(directoryPath)
class Generator:
    @staticmethod
    def generate(num_domains):
        level_one_domains = ['.com', '.net', '.io', '.blog', '.dev', '.eco', '.info']

        domains = list()
        for i in range(num_domains):
            domain = (''.join(random.choices(string.ascii_lowercase, k=(random.randint(0, 20) + 7)))) + (level_one_domains[random.randint(0, len(level_one_domains)-1)])
            domains.append(domain)
        df = pandas.DataFrame(data={"domain": domains})
        df.to_csv(directoryPath, index=False)
