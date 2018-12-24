import sys
import re
import copy

def read_data():
    r_army = re.compile('^(.+):$')
    r_group = re.compile('(\d+) units each with (\d+) hit points (\((.+)\))? ?with an attack that does (\d+) (.+) '+
                         'damage at initiative (\d+)')
    armies = list()
    army_name = None
    groups = dict()
    with open("input24.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            m = r_army.match(line)
            if m:
                if army_name is not None:
                    armies.append({'name': army_name, 'groups': groups})
                    groups = dict()
                army_name = m.groups()[0]
            m = r_group.match(line)
            if m:
                g = m.groups()
                new_group = {
                    'units': int(g[0]),
                    'hp': int(g[1]),
                    'attack_strength': int(g[4]),
                    'attack_type': g[5],
                    'initiative': int(g[6]),
                    'weak_to': list(),
                    'immune_to': list(),
                }
                if g[3] is not None:
                    wil = [s.strip() for s in g[3].split(';')]
                    for wi in wil:
                        wis = re.split('[, ]+', wi)
                        if wis[0] == 'weak':
                            for i in range(2, len(wis)):
                                new_group['weak_to'].append(wis[i])
                        elif wis[0] == 'immune':
                            for i in range(2, len(wis)):
                                new_group['immune_to'].append(wis[i])
                groups[len(groups)+1] = new_group
        armies.append({'name': army_name, 'groups': groups})
    return armies

def merge_dicts(d1, d2):
    d1c = d1.copy()
    d1c.update(d2)
    return d1c

def damage_done(attacker, defender, boost=0):
    damage = (attacker['attack_strength'] + boost) * attacker['units']
    attack_type = attacker['attack_type']
    if attack_type in defender['immune_to']:
        damage = 0
    if attack_type in defender['weak_to']:
        damage *= 2
    return damage

def effective_power(units, attack_stregth, boost, use_boost):
    if use_boost:
        adj_strength = attack_stregth + boost
    else:
        adj_strength = attack_stregth
    return units * adj_strength

def do_battle(armies, show=False, boost=0):
    if len(armies) != 2:
        print "Wrong number of armies"
        sys.exit(-1)

    boost_army = None
    for i in range(len(armies)):
        if armies[i]['name'] == 'Immune System':
            boost_army = i
    if boost_army is None:
        print "Could not find boost army"
        sys.exit(-1)

    my_armies = copy.deepcopy(armies)

    while True:
        if show:
            for i in range(len(my_armies)):
                print my_armies[i]['name'] + ':'
                for a in my_armies[i]['groups']:
                    units = my_armies[i]['groups'][a]['units']
                    if units > 0:
                        print 'Group', a, 'contains', units, 'units'

        # Target selection phase
        if show:
            print ""
        attackers = [merge_dicts({'army': army, 'uid': uid}, my_armies[army]['groups'][uid])
                     for army in [0, 1] for uid in my_armies[army]['groups']]
        attackers = sorted(attackers, key=lambda v: (0 - effective_power(v['units'], v['attack_strength'],
                                                                         boost, v['army'] == boost_army),
                                                     0 - v['initiative']))
        available_targets = [set([a['uid'] for a in attackers if a['army'] == army and a['units'] > 0])
                             for army in [0, 1]]
        if any([len(at) == 0 for at in available_targets]):
            break
        targets = dict()
        for attacker in attackers:
            if attacker['units'] == 0:
                continue
            enemy_army = 1 if attacker['army'] == 0 else 0
            if len(available_targets[enemy_army]) == 0:
                continue
            enemy_damage = {uid: merge_dicts({'damage_done': damage_done(attacker, my_armies[enemy_army]['groups'][uid],
                                                                         boost if enemy_army != boost_army else 0)},
                                             my_armies[enemy_army]['groups'][uid])
                            for uid in available_targets[enemy_army]}
            if show:
                for ed in enemy_damage:
                    print my_armies[attacker['army']]['name'], 'group', attacker['uid'], \
                                     'would deal defending group', ed, enemy_damage[ed]['damage_done'], 'damage'
            sorted_enemies = sorted(enemy_damage.keys(),
                                    key=lambda uid: (
                                        0 - enemy_damage[uid]['damage_done'],
                                        0 - effective_power(enemy_damage[uid]['units'],
                                                            enemy_damage[uid]['attack_strength'],
                                                            boost, enemy_army == boost_army),
                                        0 - enemy_damage[uid]['initiative'],
                                    ))
            if enemy_damage[sorted_enemies[0]]['damage_done'] > 0:
                targets[(attacker['army'], attacker['uid'])] = (enemy_army, sorted_enemies[0])
                available_targets[enemy_army] -= {sorted_enemies[0]}

        # Attack phase
        if show:
            print ""
        attackers = sorted(attackers, key=lambda v: (0 - v['initiative']))
        anything_happened = False
        for attacker_army, attacker_uid in [(a['army'], a['uid']) for a in attackers]:
            if (attacker_army, attacker_uid) in targets:
                attacker = my_armies[attacker_army]['groups'][attacker_uid]
                defender_army, defender_uid = targets[(attacker_army, attacker_uid)]
                defender = my_armies[defender_army]['groups'][defender_uid]
                damage = damage_done(attacker, defender, boost if boost_army == attacker_army else 0)
                units_lost = min(damage // defender['hp'], defender['units'])
                if units_lost > 0:
                    anything_happened = True
                if show:
                    print my_armies[attacker_army]['name'], 'group', attacker_uid, \
                        'attacks defending group', str(defender_uid)+',', 'killing', units_lost, 'units'
                my_armies[defender_army]['groups'][defender_uid]['units'] -= units_lost

        if not anything_happened:
            return 'Stalemate', 0

        if show:
            print '---------'

    if show:
        print 'Result:'
    muc = 0
    winner = None
    for i in [0, 1]:
        unit_count = sum([my_armies[i]['groups'][g]['units'] for g in my_armies[i]['groups']])
        if unit_count > muc:
            winner = my_armies[i]['name']
            muc = unit_count
        if show:
            print my_armies[i]['name'], 'has', unit_count, 'units remaining.'

    return winner, muc

def find_boost(armies, desired_winner='Immune System', show=False):
    lobound = None
    hibound = None
    lowest_winning_boost = None
    lwb_muc = None
    while True:
        if lobound is None and hibound is None:
            boost = 1000
        elif hibound is None:
            boost = lobound * 2
        elif lobound is None:
            boost = hibound / 2
        else:
            boost = lobound + (hibound-lobound)//2

        if show:
            print "Trying", boost
        winner, muc = do_battle(armies, boost=boost)
        if winner == desired_winner:
            hibound = boost
            if lowest_winning_boost is None or boost < lowest_winning_boost:
                lowest_winning_boost = boost
                lwb_muc = muc
        else:
            lobound = boost
        if show:
            print "   result:", winner, "won with", muc, "units remaining"
            print "   new lobound", lobound, "hibound", hibound

        if hibound is not None and lobound is not None and hibound - lobound <= 1:
            return lowest_winning_boost, desired_winner, lwb_muc

def main():
    armies = read_data()
    winner, muc = do_battle(armies)
    print 'Part A:', winner, 'wins with', muc, 'units remaining.'
    boost, winner, muc = find_boost(armies)
    print 'Part B:', boost, 'boost required for', winner, 'to win with', muc, 'remaining'

if __name__ == '__main__':
    main()
