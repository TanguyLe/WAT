import string
import random

# A new hash is created every time the server is restarted
HASH_SECRET = ""
for i in range(1, 30):
    HASH_SECRET += random.choice(string.ascii_letters)

HASH_ALGORITHM = "HS256"
