
class Instruction:

    _cell : tuple[int, int]
    """ Cellule (x, y) ciblée par l'instruction """

    _color: str | None
    """ Couleur (#0AF ou #00AAFF) dans laquelle la cellule doit être colorée. Peut être None = aucune coloration """

    _text: str | None
    """ Texte à écrire dans la cellule"""

    def __init__(self, cell: tuple[int, int], color: str, text: str):
        self._cell = cell
        self._color = color
        self._text = text

    def get_cell(self):
        return self._cell

    def get_color(self):
        return self._color

    def get_text(self):
        return self._text

    def __str__(self):
        return f'cell={self.get_cell()},color={self.get_color()},text={self.get_text()}'

class InstructionSet:

    _group_id: str | None
    """ Group id de l'instruction : caractères alphanumériques, tiret (-) et underscore (_)"""
    _instructions: list[Instruction]

    def __init__(self, group_id=None):
        self._group_id = group_id
        self._instructions = []

    def add_instruction(self, instruction: Instruction):
        self._instructions.append(instruction)

    def get_group_id(self):
        return self._group_id

    def get_instructions(self):
        return self._instructions

    def __str__(self):
        return f'group_id={self.get_group_id()},instructions={[str(instruction) for instruction in self.get_instructions()]}'
