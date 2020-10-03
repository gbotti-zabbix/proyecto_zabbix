
# from datetime import datetime

# now = datetime.now()

# for x in range(0,100):
#     while x >= 80:
#         print
# current_time = now.strftime("%H:%M:%S")
# print(type(current_time))

import subprocess
proc = subprocess.Popen(["ping", "192.168.1.1"], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
(out, err) = proc.communicate()
print (out)