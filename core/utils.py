import random, string

def random_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(11)])

