import sys

i = 3
while True:
    print(f"error test i = {i}", file=sys.stderr)
    if i:
        i-=1
        print("UP")
    else:
        print("RIGHT")