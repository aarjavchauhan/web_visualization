import os
import sys

folder = sys.argv[1]

for root, dirs, files in os.walk(folder):
    for filename in files:
        data_file = "{}/{}".format(root,filename)
        os.system("python3 links.py {}".format(data_file))
