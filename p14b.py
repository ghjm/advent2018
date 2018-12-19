def find_recipe(target):
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    search = [int(c) for c in target]
    while True:
        mix = str(recipes[elf1] + recipes[elf2])
        recipes.extend([int(c) for c in mix])
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
        if len(recipes) >= len(search):
            if recipes[-len(search):] == search:
                return len(recipes)-len(search)
            if recipes[-len(search)-1:-1] == search:
                return len(recipes)-len(search)-1

print find_recipe('51589')  # 9
print find_recipe('01245')  # 5
print find_recipe('92510')  # 18
print find_recipe('59414')  # 2018
print find_recipe('286051')
