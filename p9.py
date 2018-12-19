import LinkedList

def elfgame(players, max_marble):
    circ = LinkedList.LinkedList([0])
    cur = circ.head
    scores = dict()
    for p in range(1, players+1):
        scores[p] = 0
    for m in range(1, max_marble+1):
        player = ((m-1) % players) + 1
        if m % 23 == 0:
            ptr = circ.backward_circular(cur, 7)
            cur = ptr.next
            scores[player] += m + ptr.data
            circ.remove(ptr)
        else:
            ptr = circ.forward_circular(cur, 1)
            cur = circ.add(m, ptr)
    return scores

for p, m in [(9, 25), (10,1618), (13,7999), (17,1104), (21,6111), (30,5807), (468,71010), (468,7101000)]:
    eg = elfgame(p, m)
    best = max(eg,key=eg.get)
    print p, m, best, eg[best]