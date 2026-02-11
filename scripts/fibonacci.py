import sys

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
    print(move)
