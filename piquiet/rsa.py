from math import gcd
import json


def gcdExtended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcdExtended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return g, x, y


def coprime(a, b):
    return gcd(a, b) == 1


def get_prime(lower, upper):
    for num in range(lower, upper + 1):
        # all prime numbers are greater than 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                return num


def generate_rsa_key():
    e = 433
    i = 0.1
    while True:
        p = get_prime(int(i * e), int((i + 0.1) * e))
        q = get_prime(int((3 * i) * e), int((3 * i + 0.1) * e))
        if coprime(e, q) and coprime(e, q):
            break
        i += 0.05
    N = q * p
    phi = (q - 1) * (p - 1)
    g, d, k = gcdExtended(e, phi)
    if d < 0:
        d = k
    d = {"key": int(d)}
    with open('private.key', 'w') as f:
        json.dump(d, f)
    d = {"N": int(N),
         "e": int(e)}
    with open('public.key', 'w') as f:
        json.dump(d, f)


def encrypt(m):
    data = []
    for t in m:
        with open('public.key', 'r') as f:
            public = json.load(f)
        b = t.encode()
        i = int.from_bytes(b, "big")
        data.append(int((i ** public['e']) % public['N']))
    return data


def decrypt(i):
    with open('private.key', 'r') as f:
        private = json.load(f)
    with open('public.key', 'r') as f:
        public = json.load(f)
    s = ""
    for j in i:
        j = int((j ** private['key']) % public['N'])
        b = int.to_bytes(j, 32, "big")
        t = b.decode("utf-8")
        s += t
    return s


if __name__ == "__main__":
    generate_rsa_key()
    message = "hello world"
    enc = encrypt(message)
    text = decrypt(enc)
    print(f"{message} >> {enc} >> {text}")
