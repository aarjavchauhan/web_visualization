import os
import sys

folder = sys.argv[1]
script = sys.argv[2]

for root, dirs, files in os.walk(folder):
    for filename in files:
        data_file = "{}/{}".format(root,filename)
        os.system("python3 {} {}".format(script,data_file))
