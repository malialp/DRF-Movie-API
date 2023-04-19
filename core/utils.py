import random, string

def random_id(l):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(l)])

