import random as rnd

bin_set = ['0', '1']
base: int = len(bin_set)


def generate_tuple(size):
    return tuple(rnd.randint(0, 1) for _ in range(size))

variables: int = 4

AZ: int = (65, 91 + variables)
alfabeto = [chr(i) for i in range(*AZ)]

CANALM: dict[str: tuple[int]] = {
    clave: generate_tuple(base**(variables+1)) for clave in alfabeto[:variables]
}
