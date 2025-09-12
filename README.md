# Python Chord Progression Network
Network transition chord progression generator

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