# mplus-analysis
analysis of mythic+ dungeon and class balance using the raider.io api

the goal of this is to look at comparative dungeon + class balance so far

sample output (as of 2018 sept 6):

```
Dungeon Scores: Fortified, Sanguine, Necrotic, Infested

    mean  dungeon
   79.28  Freehold
   78.74  Atal'dazar
   75.88  The Underrot
   73.65  Siege of Boralus
   72.33  Waycrest Manor
   70.64  Tol Dagor
   70.06  Kings' Rest
   68.44  Shrine of the Storm
   66.99  Temple of Sethraliss
   64.30  The MOTHERLODE!!


Spec Scores: Fortified, Sanguine, Necrotic, Infested

     lcb   spec                       mean    n
   71.64   Protection Paladin        73.98  119
   70.97   Brewmaster Monk           73.69   99
   70.53   Blood Death Knight        71.95  371
   69.17   Vengeance Demon Hunter    71.44  139
   64.77   Protection Warrior        68.84   33
   63.43   Guardian Druid            67.42   39

   72.27   Mistweaver Monk           74.93  102
   71.87   Restoration Shaman        75.71   46
   71.75   Discipline Priest         73.43  262
   70.46   Restoration Druid         72.61  153
   67.51   Holy Paladin              69.65  145
   63.39   Holy Priest               65.79   92

   72.23   Subtlety Rogue            74.30  146
   69.51   Havoc Demon Hunter        71.11  265
   69.43   Arms Warrior              71.70  152
   69.14   Outlaw Rogue              70.84  263
   68.63   Windwalker Monk           72.14   77
   68.50   Unholy Death Knight       73.83   29
   68.43   Assassination Rogue       72.86   43
   66.87   Retribution Paladin       69.44   95
   66.08   Frost Death Knight        72.73   19
   64.80   Enhancement Shaman        70.19   17
   63.52   Fury Warrior              69.86   17
   61.33   Survival Hunter           70.00   11
   46.36   Feral Druid               77.16    3

   74.27   Balance Druid             76.33  150
   71.34   Affliction Warlock        73.33  188
   71.07   Frost Mage                72.34  439
   69.57   Beast Mastery Hunter      71.19  259
   68.78   Destruction Warlock       73.36   40
   67.48   Shadow Priest             72.69   20
   66.52   Elemental Shaman          73.30   13
   65.04   Arcane Mage               68.84   37
   59.84   Demonology Warlock        65.04    8
   51.49   Marksmanship Hunter       61.29    6
     nan   Fire Mage                 60.99    1
```

methodology is looking at the top 20 dungeon runs for each dungeon, in each of four regions: us, eu, tw, kr -- the mean is simply the mean of all scores for a dungeon or a spec (each dungeon has an n of 80, but spec distribution varies widely)

'lcb' in the spec scores = "lower 95% confidence bound" -- i.e. given some specs don't have many people playing them at a high level, chose to sort by that instead of the mean
