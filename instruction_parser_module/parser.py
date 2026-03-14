import re
import sys

from instruction import Instruction

INSTRUCTION_START="#PAINT"
CELL_PATTERN="\\[\\-?\\d+,\\-?\\d\\]"
COLOR_PATTERN="color=#[A-Fa-f0-9]{3,6}"
TEXT_PATTERN='text=\\"[A-Za-z0-9 _\\-+*\\/\\\\#]+\\"'
GROUP_PATTERN='group=[A-Za-z0-9_\\\\-]+'
INSTRUCTION_PATTERN=f"^{INSTRUCTION_START}\\(({CELL_PATTERN}),({COLOR_PATTERN},?)?({TEXT_PATTERN},?)?({GROUP_PATTERN})?\\)$"

class InstructionParser:
    def __init__(self):
        pass

# ^#PAINT\(\[\-?\d+,\-?\d\],(color=#[A-Fa-f0-9]{3,6},?)?(text=\"[A-Za-z0-9 _\-+*\/\\#]+\",?)?(group=[A-Za-z0-9_\\-]+]?)?\)$
    def parse_line(self, line) -> tuple[str, Instruction] | None:

        print(INSTRUCTION_PATTERN)

        pattern = re.compile(INSTRUCTION_PATTERN)

        match = pattern.match(line)

        if not match:
            print("No match", file=sys.stderr)
            return None

        cell = match.group(1)
        color = match.group(2)
        text = match.group(3)
        group = match.group(4)

        print(f'cell match: {cell}')
        print(f'color match: {color}')
        print(f'text match: {text}')
        print(f'group match: {group}')

        return None

if __name__ == '__main__':

    parser = InstructionParser()

    parser.parse_line('#PAINT([0,1],color=#00FF00,text="foo bar baz",group=foo-bar_baz)')






