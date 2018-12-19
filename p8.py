data = list()

with open('input8.txt', 'r') as f:
    for line in f:
        data.extend([int(tok) for tok in line.split()])

cur = 0

def get_next():
    global cur
    n = data[cur]
    cur += 1
    return n

def read_node():
    num_children = get_next()
    num_metadata = get_next()
    children = list()
    for i in range(num_children):
        children.append(read_node())
    metadata = list()
    for i in range(num_metadata):
        metadata.append(get_next())
    return { 'children': children, 'metadata': metadata }

roots = list()
while cur < len(data):
    roots.append(read_node())

def sum_metadata(node):
    s = sum(node['metadata'])
    for c in node['children']:
        s += sum_metadata(c)
    return s

total_metadata = sum([sum_metadata(root) for root in roots])
print total_metadata

def value_of_node(node):
    children = node['children']
    metadata = node['metadata']
    if len(children) == 0:
        return sum(metadata)
    s = 0
    for c in metadata:
        if c == 0:
            continue
        c -= 1
        if c >= len(children):
            continue
        s += value_of_node(children[c])
    return s

total_value = sum([value_of_node(root) for root in roots])
print total_value
