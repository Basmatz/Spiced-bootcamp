def people(*siblings, **parents):
    for sibling in siblings:
        print(f"Siblingname: {sibling}")
    for parent in parents.values():
        print(f"Parent name: {parent}")

people("Lena", "Moritz", "Ulla", "Tina", mother="Elisabeth", father="Knut")


import pandas as pd

variable = pd.Series(range(10))

variable = variable.apply(lambda x : x**2)

print(variable)