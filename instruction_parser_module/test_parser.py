from unittest import TestCase

from instruction_parser_module.parser import parse_line


class Test(TestCase):

    def test_instruction_complete(self):
        group, instruction = parse_line('#PAINT([0,1],color=#00FF00,text="foo bar baz",text_color=#0F0,group=foo-bar_baz)')
        self.assertEqual(group, 'foo-bar_baz')
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), '#00FF00')
        self.assertEqual(instruction.get_text(), 'foo bar baz')
        self.assertEqual(instruction.get_text_color(), '#0F0')

    def test_instruction_sans_couleur_sans_couleur_texte(self):
        group, instruction = parse_line('#PAINT([0,1],text="foo bar baz",group=foo-bar_baz)')
        self.assertEqual(group, 'foo-bar_baz')
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), None)
        self.assertEqual(instruction.get_text(), 'foo bar baz')
        self.assertEqual(instruction.get_text_color(), None)

    def test_instruction_sans_texte(self):
        group, instruction = parse_line('#PAINT([0,1],color=#00FF00,group=foo-bar_baz)')
        self.assertEqual(group, 'foo-bar_baz')
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), '#00FF00')
        self.assertEqual(instruction.get_text(), None)
        self.assertEqual(instruction.get_text_color(), None)

    def test_instruction_sans_group(self):
        group, instruction = parse_line('#PAINT([0,1],color=#00FF00,text="foo bar baz")')
        self.assertEqual(group, None)
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), '#00FF00')
        self.assertEqual(instruction.get_text(), 'foo bar baz')
        self.assertEqual(instruction.get_text_color(), None)

    def test_instruction_sans_groupe_sans_couleur(self):
        group, instruction = parse_line('#PAINT([0,1],text="foo bar baz")')
        self.assertEqual(group, None)
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), None)
        self.assertEqual(instruction.get_text(), 'foo bar baz')
        self.assertEqual(instruction.get_text_color(), None)

    def test_instruction_sans_groupe_sans_texte(self):
        group, instruction = parse_line('#PAINT([0,1],color=#00FF00)')
        self.assertEqual(group, None)
        self.assertEqual(instruction.get_cell(), (0, 1))
        self.assertEqual(instruction.get_color(), '#00FF00')
        self.assertEqual(instruction.get_text(), None)
        self.assertEqual(instruction.get_text_color(), None)

    def test_instruction_sans_texte_sans_couleur(self):
        group, instruction = parse_line('#PAINT([0,1],group=foo-bar_baz)')
        self.assertEqual(group, None)
        self.assertEqual(instruction, None)

    def test_instruction_sans_groupe_sans_texte_sans_couleur(self):
        group, instruction = parse_line('#PAINT([0,1])')
        self.assertEqual(group, None)
        self.assertEqual(instruction, None)

    def test_instruction_sans_cellule(self):
        group, instruction = parse_line('#PAINT(color=#00FF00,text="foo bar baz",group=foo-bar_baz)')
        self.assertEqual(group, None)
        self.assertEqual(instruction, None)

    def test_instruction_totalement_invalide(self):
        group, instruction = parse_line('Je ne ressemble pas du tout à une instruction')
        self.assertEqual(group, None)
        self.assertEqual(instruction, None)
