import pprint
import sys
from scipy.stats import t
from numpy import average, std

dungeons = {}
runs = []

import json
with open('affixes.json', 'r') as infile:
    affixes = json.load(infile)

with open('dungeons.json', 'r') as infile:
    dungeons = json.load(infile)

with open('runs.json', 'r') as infile:
    runs = json.load(infile)

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


def spec_count(dungeon=""):
    global runs, specs, spec_score, tanks, healers, melee, ranged
    for s in specs:
        spec_score[s] = 0
        for r in runs:
            if s in r:
                if dungeon:
                    if dungeon not in r[0]:
                        continue
                spec_score[s] += r.count(s)

    for display in [tanks, healers, melee, ranged]:
        for k, v in sorted(spec_score.items(), key=lambda x: x[1], reverse=True):
            if k in display:
                print str(v) + "  " + k
        print

def spec_scores(dungeon=""):
    global runs, specs, tanks, healers, melee, ranged
    spec_scores = {}
    spec_ci = {}
    analysis = []
    for s in specs:
        spec_scores[s] = []
        for r in runs:
            if s in r:
                if dungeon:
                    if dungeon not in r[0]:
                        continue
                spec_scores[s] += [r[1]]

        data = spec_scores[s]
        mean = average(data)
        n = len(data)
        stddev = std(data, ddof=0)
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


from math import sqrt

def _confidence(n, wins):
    if n == 0:
        return 0

    z = 1.6 
    phat = float(wins) / n
    return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def wilson(n, wins):
    if n == 0:
        return 0
    else:
        return _confidence(n, wins)

def sorted_effectiveness(sc):
    pairs = []
    for k, v in sc.iteritems():
        pairs += [[k, wilson(v[1], v[0])]]
    for k, v in sorted(pairs, key=lambda x: x[1], reverse=True):
        print "%.2f  " % v + k

        
def spec_analysis():
    global runs, specs, spec_score
    spec_correlation = {}
    for s in specs:
        spec_correlation[s] = {}
        for r in runs:
            if s not in r:
                continue
            current_run = copy.copy(r[2:])
            current_run.remove(s)
            for ss in current_run:
                if ss not in spec_correlation[s]:
                    spec_correlation[s][ss] = [0, 0]
                spec_correlation[s][ss][1] += 1
                spec_correlation[s][ss][0] += r[1]
        print s, "is best paired with..."
        sorted_effectiveness(spec_correlation[s])
        print

def dungeon_analysis():
    global runs, specs, spec_score
    
    dungeons_pretty = []
    for k, v in dungeons.iteritems():
        if k not in dungeons_pretty:
            dungeons_pretty += [k]

    dung_correlation = {}
    for s in dungeons_pretty:
        print s, "is most often run by..."
        spec_count(dungeon=s)
        print

print
print "Dungeon Scores:", affixes["us"]
print
print "    mean  dungeon"
dungeon_averages()
print
print

#print "Spec Counts"
#spec_count()
#print

print "Spec Scores:", affixes["us"]
print

print "     lcb   spec                       mean    n"
spec_scores()
print
sys.exit()

print "Spec Pairings"
print
spec_analysis()

print "Specs for each Dungeon"
print
dungeon_analysis()

