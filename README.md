# Python Chord Progression Network
Network transition chord progression generator

## DESCRIPTION

This class generates network transition chord progressions. The transitions are given by a `net` of scale positions, and the chord "flavors" are defined by a `chord_map` of types.

The chord types are as follows:

```
'' (i.e. an empty string) means a major chord.
'm' signifies a minor chord.
'7' is a seventh chord and 'M7' is a major 7th chord.
'dim' is a diminished chord and 'aug' is augmented.
'9', '11', and '13' are extended 7th chords.
'M9', 'M11', and 'M13' are extended major-7th chords.
'm9', 'm11', and 'm13' are extended minor-7th chords.
```

For the `major` scale (`ionian` mode), this `chord_map` is `['', 'm', 'm', '', '', 'm', 'dim']`. The `dorian` mode is `['m', 'm', '', '', 'm', 'dim', '']`. A `chromatic` scale is all minors. This can be set in the constructor, or seen by printing it after `Generator` construction.

The `tonic` attribute means that if the first chord of the progression is being generated, then for `0` choose a random successor, as defined by the `net`. For `1`, return the first chord in the scale. For any other value, choose a random value of the entire scale.

## SYNOPSIS
```python
from chord_progression_network import Generator

g = Generator( # defaults
    max=8,
    scale_note='C',
    scale_name='major',
    octave=4,
    net={
        1: [1, 2, 3, 4, 5, 6],
        2: [3, 4, 5],
        3: [1, 2, 4, 6],
        4: [1, 3, 5, 6],
        5: [1, 4, 6],
        6: [1, 2, 4, 5],
        7: [],
    },
    chord_map=[ '', 'm', 'm', '', '', 'm', 'dim' ],
    tonic=1,
    resolve=1,
    substitute=False,
    flat=False,
    phrase=None,
    chords=None,
    verbose=False,
)
phrase = g.generate()
```