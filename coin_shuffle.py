def generate_keypair():
    random_gen = Random.new().read
    return RSA.generate(1024, random_gen)