recipes = [3, 7]
elf1 = 0
elf2 = 1

req_exp = 286051
while len(recipes) <= req_exp + 10:
    mix = str(recipes[elf1] + recipes[elf2])
    recipes.extend([int(c) for c in mix])
    elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
    elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
print ''.join([str(n) for n in recipes[req_exp:req_exp+10]])
