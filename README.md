# Chord Progression Network
Network transition chord progression generator

## DESCRIPTION

This class generates network transition chord progressions. The transitions are given by a `net` of scale positions, and the chord "flavors" are defined by a `chord_map` of types. The chords that are returned are either named chords or lists of three or more named notes with octaves.

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

The `tonic` attribute means that if the first chord of the progression is being generated, then for `0` choose a random successor of the first chord, as defined by the `net` attribute. For `1`, return the first chord in the scale. For any other value, choose a random value of the entire scale.

The `resolve` attribute means that if the last progression chord is being generated, then for `0` choose a random successor. As for the `tonic`, for `1`, return the first chord in the scale, and for any other value, choose a random value of the entire scale. In all other cases (i.e. the middle chords of the progression), choose a random successor.

By default, all chords and notes with accidentals are returned as sharps. If you want flats, set the `flat` attribute to `True` in the constructor.

If the `substitute` attribute is set to `True`, then the progression chords are subject to extended, "jazz" chord, including tritone substitution. For now, for this work-in-progress advanced option, please see the `substitution()` method in the source...

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
    flat=False,
    chord_phrase=False,
    substitute=False,
    verbose=False,
)
phrase = g.generate()
```

## MUSICAL EXAMPLE
```python
from music21 import chord, stream
from chord_progression_network import Generator

g = Generator(verbose=True)
phrase = g.generate()

s = stream.Score()
p = stream.Part()

for notes in phrase:
    p.append(chord.Chord(notes, type='whole'))

s.append(p)

s.show()
```