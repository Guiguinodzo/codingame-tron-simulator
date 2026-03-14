import sys

def paint(x, y, color, text, group='default'):
    command = f'#PAINT([{x},{y}]'
    if color:
        command += f',color={color}'
    if text:
        command += f',text="{text}"'
    if group:
        command += f',group={group}'
    command += ')'
    print(command, file=sys.stderr)

def smiley(x0, y0, fg_color, bg_color, text, group='default'):
    draw = lambda x,y : paint(x0 + x, y0 + y, fg_color, text, group)
    fill_line = lambda x,y, l : [paint(x0 + x + index, y0 + y, bg_color, text, group) for index in range(l)]

    draw(5, 0); draw(6, 0); draw(7, 0); draw(8, 0); draw(9, 0)
    draw(3, 1); draw(4, 1); fill_line(5, 1, 5); draw(10, 1); draw(11, 1)
    draw(2, 2); fill_line(3, 2, 9); draw(12, 2)
    draw(1, 3); fill_line(2, 3, 11); draw(13, 3)
    draw(1, 4); fill_line(2, 4, 2); draw(4, 4); fill_line(5, 4, 5); draw(10, 4); fill_line(11, 4, 2); draw(13, 4)
    draw(0, 5); fill_line(1, 5, 13); draw(14, 5)
    draw(0, 6); fill_line(1, 6, 13); draw(14, 6)
    draw(0, 7); fill_line(1, 7, 4); draw(5, 7); draw(6, 7); draw(7, 7); draw(8, 7); draw(9, 7); fill_line(10, 7, 4); draw(14, 7)
    draw(0, 8); fill_line(1, 8, 3); draw(4, 8); fill_line(5, 8, 5); draw(10, 8); fill_line(11, 8, 3); draw(14, 8)
    draw(1, 9); fill_line(2, 9, 3); draw(5, 9); fill_line(6, 9, 3); draw(9, 9); fill_line(10, 9, 3); draw(13, 9)
    draw(1, 10); fill_line(2, 10, 4); draw(6, 10); draw(7, 10); draw(8, 10); fill_line(9, 10, 4); draw(13, 10)
    draw(2, 11); fill_line(3, 11, 9); draw(12, 11)
    draw(3, 12); draw(4, 12); fill_line(5, 12, 5); draw(10, 12); draw(11, 12)
    draw(5, 13); draw(6, 13); draw(7, 13); draw(8, 13); draw(9, 13)


i = 0
a = 1
b = 1
countdown = 1

move_index = 0

moves = ['UP', 'RIGHT', 'DOWN', 'LEFT']

while True:
    n, my_id = map(int, input().split())
    for j in range(n):
        x0, y0, x1, y1 = map(int, input().split())

    print(f"my_id={my_id} - i = {i} : a={a} b={b} countdown={countdown} move_index={move_index}", file=sys.stderr)
    i += 1

    move = moves[move_index]
    if countdown == 0:
        countdown = a + b
        a = b
        b = countdown
        move_index = (move_index + 1) % 4
    else:
        countdown -= 1

    for smiley_index in range(10):
        smiley(smiley_index, smiley_index, '#000000', '#ffeb3b', f'{smiley_index}', f'Smiley_{smiley_index}')

    print(move)

