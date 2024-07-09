import random
import string


def assign_1_prim(c):
    a, b = c
    aux = a >> b
    return aux

# Generate values for each type
bool_val = random.choice([True, False])
int_val = random.randint(-100, 100)
float_val = random.uniform(-100.0, 100.0)
complex_val = complex(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))
range_val = range(random.randint(0, 10))
str_val = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Generate bytes and bytearray
bytes_val = bytes([random.getrandbits(8) for _ in range(10)])
bytearray_val = bytearray([random.getrandbits(8) for _ in range(10)])
memoryview_val = memoryview(bytearray_val)
none_val = None

# Store all values in a list for easy reference
values = [int_val, int_val]

# Filter out unhashable types for sets and frozensets
hashable_values = [int_val, int_val]

# Create container types
set_val = set(hashable_values)
frozenset_val = frozenset(hashable_values)
list_val = list(values)
tuple_val = tuple(values)


for c in list_val:
    aux = assign_1_prim(c)

print(aux)
