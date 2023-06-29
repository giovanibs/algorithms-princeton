import big_o
from union_find.QuickUnion import QuickUnion

# cases to evaluate
tinyUF = '../tests/tinyUF.txt'
mediumUF = '../tests/mediumUF.txt'
largeUF = '../tests/largeUF.txt'

# setup
def uf_generator(source_file):
    for line in open(source_file):
        if len(line.split()) == 1:
            yield int(line.split()[0])
        
        elem1, elem2 = line.split()
        yield int(elem1), int(elem2)
        
generator = uf_generator(tinyUF)
n = next(generator)
print(f'{n=}')
uf = QuickUnion(n) # 1st line is the constructor argument 
 
best, others = big_o.big_o(QuickUnion.union, uf_generator, n_repeats=100)
print(best)