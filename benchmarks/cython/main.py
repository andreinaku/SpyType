import bigproduct
import bigproduct2
import bigproduct3
import time


optim_times = []
for j in range(1000):
    start = time.time()
    for i in range(1000):
        bigproduct.bigproduct([6,2,4,6,2,3], 3)
    optim_time = time.time() - start
    optim_times.append(optim_time)
optim_mean = sum(optim_times) / len(optim_times)
print(f"optim = {optim_mean}")

slow_times = []
for j in range(1000):
    start = time.time()
    for i in range(1000):
        bigproduct2.bigproduct([6,2,4,6,2,3], 3)
    slow_time = time.time() - start
    slow_times.append(slow_time)
slow_mean = sum(slow_times) / len(slow_times)
print(f"slow = {slow_mean}")

orig_times = []
for j in range(1000):
    start = time.time()
    for i in range(1000):
        bigproduct2.bigproduct([6,2,4,6,2,3], 3)
    orig_time = time.time() - start
    orig_times.append(orig_time)
orig_mean = sum(orig_times) / len(orig_times)
print(f"orig = {orig_mean}")

print(f"{orig_mean / optim_mean} times faster than CPython (original)")
print(f"Running time with undeclared types: {slow_mean * 1000:.6f}ms")
print(f"Running time with declared types: {optim_mean * 1000:.6f}ms")
print(f"Performance increase: {slow_mean / optim_mean:.2f}x")
