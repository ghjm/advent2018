import textx
import networkx

txmm = textx.metamodel_from_str("""
file:
    rules += rule
;
rule:
    'Step' prereq=/[A-Z]/ 'must be finished before step' step=/[A-Z]/ 'can begin.'
;
""")
txm = txmm.model_from_file("input7.txt")

G = networkx.DiGraph()
for rule in txm.rules:
    G.add_node(rule.step)
    G.add_node(rule.prereq)
    G.add_edge(rule.prereq, rule.step)

print ''.join(networkx.lexicographical_topological_sort(G))
