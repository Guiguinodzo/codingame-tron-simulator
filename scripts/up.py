import sys

i = 0
while True:
    n, my_id = map(int, input().split())
    for j in range(n):
        x0, y0, x1, y1 = map(int, input().split())
    print(f"my_id={my_id} - i = {i}", file=sys.stderr)
    if i < 3:
        print("UP")
    else:
        print("RIGHT")
    i += 1