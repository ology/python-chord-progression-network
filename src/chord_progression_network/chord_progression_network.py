import random
import re
import networkx as nx
import musical_scales

class Generator:
    def __init__(
        self,
        max=8,
        net=None,
        chord_map=None,
        scale_name='major',
        scale_note='C',
        octave=4,
        tonic=True,
        resolve=True,
        substitute=False,
        sub_cond=None,
        flat=False,
        verbose=False,
    ):
        self.max = max
        self.net = net if net is not None else {
            1: [1, 2, 3, 4, 5, 6],
            2: [3, 4, 5],
            3: [1, 2, 4, 6],
            4: [1, 3, 5, 6],
            5: [1, 4, 6],
            6: [1, 2, 4, 5],
            7: [],
        }
        self.scale_name = scale_name
        self.scale_note = scale_note
        self.octave = octave
        self.tonic = tonic
        self.resolve = resolve
        self.substitute = substitute
        self.sub_cond = sub_cond if sub_cond is not None else lambda: random.randint(0, 3) == 0
        self.flat = flat
        self.verbose = verbose
        self.chord_map = chord_map if chord_map is not None else self._build_chord_map()
        self.scale = self._build_scale()
        self.graph = self._build_graph()
        self.phrase = None
        self.chords = None

    def _build_chord_map(self):
        scale_maps = {
            'chromatic':  ['m'] * 12,
            'major':      ['', 'm', 'm', '', '', 'm', 'dim'],
            'ionian':     ['', 'm', 'm', '', '', 'm', 'dim'],
            'dorian':     ['m', 'm', '', '', 'm', 'dim', ''],
            'phrygian':   ['m', '', '', 'm', 'dim', '', 'm'],
            'lydian':     ['', '', 'm', 'dim', '', 'm', 'm'],
            'mixolydian': ['', 'm', 'dim', '', 'm', 'm', ''],
            'minor':      ['m', 'dim', '', 'm', 'm', '', ''],
            'aeolian':    ['m', 'dim', '', 'm', 'm', '', ''],
            'locrian':    ['dim', '', 'm', 'm', '', '', 'm'],
        }
        return scale_maps.get(self.scale_name)

    def _build_scale(self):
        # XXX this uses the patched musical_scales package
        s = musical_scales.scale(self.scale_note, starting_octave=5)
        if self.flat:
            flattened = [ self._equiv(note) for note in s ]
            s = flattened
        return s

    def _equiv(self, note):
        match = re.search(r"^([A-G][#b]+?)(\d)$", note)
        n = match.group(1)
        octave = match.group(2)
        equiv = {
            'C#':  'Db',
            'D#':  'Eb',
            'E#':  'F',
            'F#':  'Gb',
            'G#':  'Ab',
            'A#':  'Bb',
            'B#':  'C',
            'Cb':  'B',
            'Dbb': 'C',
            'Ebb': 'D',
            'Fb':  'E',
            'Gbb': 'F',
            'Abb': 'G',
            'Bbb': 'A',
        }
        return equiv.get(note) + octave if note in equiv else note + octave

    def _build_graph(self):
        g = nx.DiGraph()
        for posn, neighbors in self.net.items():
            for neighbor in neighbors:
                g.add_edge(posn, neighbor)
        return g

    def generate(self):
        if len(self.chord_map) != len(self.net):
            raise ValueError('chord_map length must equal number of net keys')

        progression = []
        v = None
        for n in range(1, self.max + 1):
            v = self._next_successor(n, v)
            progression.append(v)
        if self.verbose:
            print('Progression:', progression)

        chord_map = list(self.chord_map)
        if self.substitute:
            for i, chord in enumerate(chord_map):
                substitute = self.substitution(chord) if self.sub_cond() else chord
                if substitute == chord and i < len(progression) and self.sub_cond():
                    progression[i] = str(progression[i]) + 't'
                chord_map[i] = substitute
            if self.verbose:
                print('Chord map:', chord_map)

        phrase = [self._tt_sub(chord_map, n) for n in progression]
        self.phrase = phrase
        if self.verbose:
            print('Phrase:', self.phrase)

        chords = [self._chord_with_octave(chord, self.octave) for chord in phrase]
        if self.flat:
            chords = [[self._equiv(note) for note in chord] for chord in chords]
        self.chords = chords
        if self.verbose:
            print('Chords:', self.chords)
        return chords

    def _next_successor(self, n, v):
        v = v if v is not None else 1
        s = None
        if n == 1:
            if self.tonic == 0:
                s = self._random_successor(1)
            elif self.tonic == 1:
                s = 1
            else:
                s = self._full_keys()
        elif n == self.max:
            if self.resolve == 0:
                s = self._random_successor(v) or self._full_keys()
            elif self.resolve == 1:
                s = 1
            else:
                s = self._full_keys()
        else:
            s = self._random_successor(v)
        return s

    def _random_successor(self, v):
        successors = list(self.graph.successors(v))
        return random.choice(successors) if successors else None

    def _full_keys(self):
        keys = [k for k, v in self.net.items() if len(v) > 0]
        return random.choice(keys)

    def _tt_sub(self, chord_map, n):
        note = None
        if isinstance(n, str) and 't' in n:
            n = int(n.replace('t', ''))
            # Tritone substitution logic for chromatic scale
            chromatic = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
            idx = chromatic.index(self.scale[n - 1]) if self.scale[n - 1] in chromatic else 0
            note = chromatic[(idx + 6) % len(chromatic)]
            if self.verbose:
                print(f'Tritone: {self.scale[n - 1]} => {note}')
        else:
            note = self.scale[int(n) - 1]
        note += chord_map[int(n) - 1]
        return note

    def _chord_with_octave(self, chord, octave):
        # Placeholder: returns chord as a list with octave appended
        # Replace with actual chord note generation logic as needed
        return [f"{chord}{octave}"]

    def substitution(self, chord):
        substitute = chord
        if chord in ['', 'm']:
            roll = random.randint(0, 1)
            substitute = chord + 'M7' if roll == 0 else chord + '7'
        elif chord in ['dim', 'aug']:
            substitute = chord + '7'
        elif chord in ['-5', '-9']:
            substitute = f"7({chord})"
        elif chord == 'M7':
            roll = random.randint(0, 2)
            substitute = ['M9', 'M11', 'M13'][roll]
        elif chord == '7':
            roll = random.randint(0, 2)
            substitute = ['9', '11', '13'][roll]
        elif chord == 'm7':
            roll = random.randint(0, 2)
            substitute = ['m9', 'm11', 'm13'][roll]
        if self.verbose and substitute != chord:
            print(f'Substitute: "{chord}" => "{substitute}"')
        return substitute
