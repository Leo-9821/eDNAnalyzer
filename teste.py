d = {'a': {'b': 'c', 'd': 'e'}, 'f': {'g': 'h', 'i': 'j'}}


for letra, letra2 in d.items():
    for lol in letra2.values():
        print(lol)
