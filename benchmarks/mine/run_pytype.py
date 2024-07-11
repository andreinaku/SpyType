import os
import time
import sys


binpath = os.path.join(sys.argv[1])
start_time = time.time()
to_run = f'{binpath} {sys.argv[2]}'
os.system(to_run)
end_time = time.time()
diff_time = end_time - start_time
print(f'{diff_time:4f}s')

