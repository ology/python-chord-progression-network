import unittest
import sys
sys.path.append('./src')
from chord_progression_network.chord_progression_network import Generator

class TestChordProgression(unittest.TestCase):
    def test_defaults(self):
        g = Generator()
        self.assertEqual(g.max, 8)
        self.assertEqual(len(g.net), 7)
        self.assertEqual(len(g.chord_map), 7)
        self.assertEqual(g.scale_name, 'major')
        self.assertEqual(g.scale_note, 'C')
        self.assertEqual(len(g.scale), 8)
        self.assertEqual(g.octave, 4)
        self.assertEqual(g.tonic, 1)
        self.assertEqual(g.resolve, 1)
        self.assertEqual(g.substitute, False)
        self.assertEqual(g.flat, False)
        self.assertEqual(g.phrase, None)
        self.assertEqual(g.chords, None)
        self.assertEqual(len(g.graph.nodes), 6)
        self.assertEqual(len(g.graph.edges), 24)

    def test_scale_note(self):
        g = Generator(
            scale_note='Bb',
            # verbose=True
        )
        expect = ['A#4', 'D5', 'F5']
        p = g.generate()
        self.assertEqual(p[0], expect)
        self.assertEqual(p[-1], expect)
        g = Generator(
            scale_note='A',
            scale_name='minor',
            chord_map=['m', 'dim', '', 'm', 'm', '', ''],
            # verbose=True
        )
        expect = ['A4', 'C5', 'E5']
        p = g.generate()
        self.assertEqual(p[0], expect)
        self.assertEqual(p[-1], expect)

    def test_flattening(self):
        g = Generator(scale_note='Bb', flat=True)
        expect = ['Bb4', 'D5', 'F5']
        p = g.generate()
        self.assertEqual(p[0], expect)
        self.assertEqual(p[-1], expect)

    def test_substitution(self):
        g = Generator(scale_note='Bb')
        p = g.substitution('')
        self.assertTrue(p == '7' or p == 'M7')
        p = g.substitution('m')
        self.assertTrue(p == 'm7' or p == 'mM7')
        p = g.substitution('7')
        self.assertTrue(p == '9' or p == '11' or p == '13')
        # always substitute
        g = Generator(
            max=3,
            substitute=True,
            sub_cond=lambda: True
        )
        p = g.generate()
        for chord in p:
            self.assertTrue(len(chord) > 3)

    def test_net(self):
        g = Generator(
            max=7,
            net={ 1: [2], 2: [3], 3: [4], 4: [5], 5: [6], 6: [7], 7: [1] },
            resolve=False
        )
        expect = [
            ['C4', 'E4', 'G4'], ['D4', 'F4', 'A4'], ['E4', 'G4', 'B4'],
            ['F4', 'A4', 'C5'], ['G4', 'B4', 'D5'], ['A4', 'C5', 'E5'],
            ['B4', 'D5', 'F5'],
        ]
        p = g.generate()
        self.assertEqual(p, expect)

    def test_chord_map(self):
        g = Generator(chord_map=[''])
        with self.assertRaises(ValueError):
            g.generate()
        g = Generator(scale_name='chromatic')
        self.assertEqual(g.chord_map, ['m'] * 12)

if __name__ == '__main__':
    unittest.main()
