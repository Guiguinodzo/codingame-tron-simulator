import sys

i = 3
while True:
    n, my_id = map(int, input().split())
    for j in range(n):
        x0, y0, x1, y1 = map(int, input().split())
    print(f"error test i = {i}", file=sys.stderr)
    if i:
        i-=1
        print("UP")
    else:
        print("RIGHT")