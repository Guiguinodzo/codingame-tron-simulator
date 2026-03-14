import re

from instruction_parser_module.instruction import Instruction
from instruction_parser_module.instruction import InstructionSet

INSTRUCTION_START="#PAINT"
CELL_PATTERN="\\[(\\-?\\d+),(\\-?\\d)\\]"
COLOR_PATTERN="color=(#[A-Fa-f0-9]{3,6})"
TEXT_PATTERN='text=\\"(.+)\\"'
TEXT_COLOR_PATTERN="text_color=(#[A-Fa-f0-9]{3,6})"
GROUP_PATTERN='group=([\\w_\\-]+)'
INSTRUCTION_PATTERN=f"^{INSTRUCTION_START}\\(({CELL_PATTERN})(,{COLOR_PATTERN})?(,{TEXT_PATTERN})?(,{TEXT_COLOR_PATTERN})?(,{GROUP_PATTERN})?\\)$"

def parse_line(line) -> tuple[str, Instruction] | tuple[None,None]:

    pattern = re.compile(INSTRUCTION_PATTERN)

    match = pattern.match(line)

    if not match:
        return None, None

    cell_x, cell_y = int(match.group(2)), int(match.group(3))
    color = match.group(5)
    text = match.group(7)
    text_color = match.group(9)
    group = match.group(11)

    if not color and not text:
        return None, None

    return group, Instruction((cell_x, cell_y), color, text, text_color)

def parse_logs(lines: list[str]) -> list[InstructionSet]:
    if not lines:
        return []

    instruction_sets_by_group : dict[str, InstructionSet] = {}

    for line in lines:
        group, instruction = parse_line(line)
        if not instruction:
            continue
        if group not in instruction_sets_by_group:
            instruction_sets_by_group[group] = InstructionSet(group)
        instruction_sets_by_group[group].add_instruction(instruction)

    return [instruction_set for instruction_set in instruction_sets_by_group.values()]


