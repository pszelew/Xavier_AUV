import random

"""
Creating port and write it to ports.txt file
"""

port = random.randrange(8900, 9000, 1)
print(port)
with open('ports.txt', 'w') as f:
    f.write(str(port))

