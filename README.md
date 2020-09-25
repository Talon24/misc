# misc
Collection of minor scripts or other things

## toggle_stream.py
Automate starting and stopping video streaming server and get the URL
that you need to send to the receiver.

## number_namer.py
Shows the name of a long number in a pronouncable way.
```
.\number_namer.py 123456789741258369 -l English-short
123 quintillion
456 quadrillion
789 trillion
741 billion
258 million
369
```

## actor_pairings.py
Ever wondered if there are voice actors that work together very often? find out with this script using imdb.
Works with direct imdb links or the name identifier in the url (ht&#8203;tps://ww&#8203;w.imdb.com/name/**nm0354937**/)


```
C:\Users\Talon\Documents\git\misc>actor_pairings.py https://www.imdb.com/name/nm0354937/ nm1035752 https://www.imdb.com/name/nm0768620/
--- Media in which Jennifer Hale and Mark Meer and Raphael Sbarge cooperated:
Mass Effect
Mass Effect 2
Mass Effect 3

C:\Users\Talon\Documents\git\misc>actor_pairings.py nm0768620 nm1035752 nm0354937
--- Media in which Raphael Sbarge and Mark Meer and Jennifer Hale cooperated:
Mass Effect
Mass Effect 2
Mass Effect 3

C:\Users\Talon\Documents\git\misc>actor_pairings.py nm0354937 nm1035752
--- Media in which Jennifer Hale and Mark Meer cooperated:
Baldur's Gate II - Der Thron des Bhaal
Baldur's Gate II: Schatten von Amn
Baldur's Gate: Siege of Dragonspear
Dragon Age: Inquisition
From the Mouths of Babes
Mass Effect
Mass Effect 2
Mass Effect 3
The Long Dark
```
