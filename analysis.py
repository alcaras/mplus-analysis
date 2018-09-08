import pprint
import sys
from scipy.stats import t
from numpy import average, std
from math import sqrt

dungeons = {}
runs = []

import json
with open('affixes.json', 'r') as infile:
    affixes = json.load(infile)

with open('dungeons.json', 'r') as infile:
    dungeons = json.load(infile)

with open('runs.json', 'r') as infile:
    runs = json.load(infile)

dungeons_pretty = []
for k, v in dungeons.iteritems():
    if k not in dungeons_pretty:
        dungeons_pretty += [k]
    
## import complete
               
def dungeon_averages():
    dungeon_averages = ((float(sum(scores)) / len(scores), s) for s, scores in dungeons.items())

    for average, dungeon in sorted(dungeon_averages, reverse=True):
        print str("%.2f" % average).rjust(8) + "  " + dungeon

specs = [u'Frost Mage', u'Balance Druid', u'Restoration Druid', u'Vengeance Demon Hunter', u'Windwalker Monk', u'Destruction Warlock', u'Holy Paladin', u'Arms Warrior', u'Brewmaster Monk', u'Retribution Paladin', u'Discipline Priest', u'Outlaw Rogue', u'Restoration Shaman', u'Blood Death Knight', u'Havoc Demon Hunter', u'Guardian Druid', u'Subtlety Rogue', u'Beast Mastery Hunter', u'Mistweaver Monk', u'Protection Paladin', u'Affliction Warlock', u'Enhancement Shaman', u'Shadow Priest', u'Survival Hunter', u'Assassination Rogue', u'Frost Death Knight', u'Elemental Shaman', u'Fury Warrior', u'Holy Priest', u'Arcane Mage', u'Unholy Death Knight', u'Feral Druid', u'Protection Warrior', u'Demonology Warlock', u'Marksmanship Hunter', u'Fire Mage']

tanks =  [u'Vengeance Demon Hunter',
          u'Brewmaster Monk',
          u'Blood Death Knight',
          u'Guardian Druid',
          u'Protection Paladin',
          u'Protection Warrior']

healers = [u'Restoration Druid',
           u'Holy Paladin',
           u'Discipline Priest',
           u'Restoration Shaman',
           u'Mistweaver Monk',
           u'Holy Priest',]

melee = [u'Windwalker Monk',
         u'Arms Warrior',
         u'Retribution Paladin',
         u'Outlaw Rogue',
         u'Havoc Demon Hunter',
         u'Subtlety Rogue',
         u'Enhancement Shaman',
         u'Survival Hunter',
         u'Assassination Rogue',
         u'Frost Death Knight',
         u'Fury Warrior',
         u'Unholy Death Knight',
         u'Feral Druid',]

ranged = [u'Frost Mage',
          u'Balance Druid',
          u'Destruction Warlock',
          u'Beast Mastery Hunter',
          u'Affliction Warlock',
          u'Shadow Priest',
          u'Elemental Shaman',
          u'Arcane Mage',
          u'Demonology Warlock',
          u'Marksmanship Hunter',
          u'Fire Mage']

import copy
import pprint

spec_score = {}

def spec_scores(dungeon="", spec=""):
    global runs, specs, tanks, healers, melee, ranged
    spec_scores = {}
    spec_ci = {}
    analysis = []
    for s in specs:
        spec_scores[s] = []
        for r in runs:
            cr = copy.copy(r)
            if spec:
                if spec not in cr:
                    continue
                else:
                    cr.remove(spec) # to prevent pairing with self, remove first instance
            if s in cr:
                if dungeon:
                    if dungeon not in cr[0]:
                        continue
                spec_scores[s] += [cr[1]]


        data = spec_scores[s]
        n = len(data)
        if n <= 2:
            continue
        mean = average(data)
        stddev = std(data, ddof=1)
        t_bounds = t.interval(0.95, len(data) - 1)
        ci = [mean + critval * stddev / sqrt(len(data)) for critval in t_bounds]
        spec_ci[s] = ci
        analysis += [[s, mean, stddev, n, ci]]

    for display in [tanks, healers, melee, ranged]:
        for k in sorted(analysis, key=lambda x: x[4][0], reverse=True):
            if k[0] in display:
                print str("%.2f" % k[4][0]).rjust(8) + "  ",
                print str(k[0]).ljust(22),
                print str("%.2f" % k[1]).rjust(8),
                print str("%d" % k[3]).rjust(4)
        print

def dungeon_analysis():
    global runs, specs, dungeons_pretty

    for s in dungeons_pretty:
        print s, "Spec Scores:", affixes["us"]
        spec_scores(dungeon=s)
        print

def pairing_analysis():
    global runs, specs, dungeons_pretty, tanks, healers, melee, ranged

    for display in [tanks, healers, melee, ranged]:
        for s in display:
            print s, "Pairing Scores:", affixes["us"]
            spec_scores(spec=s)
            print
        print

print
print "Dungeon Scores:", affixes["us"]
print
print "    mean  dungeon"
dungeon_averages()
print
print

print "Spec Scores:", affixes["us"]
print

print "     lcb   spec                       mean    n"
spec_scores()
print


print "Per Dungeon Spec Scores:", affixes["us"]
print
dungeon_analysis()
print

print "Per Spec Pairing Scores:", affixes["us"]
print
pairing_analysis()
print
