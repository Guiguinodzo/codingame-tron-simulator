import time

for i in range(3):
    print("ping", i, flush=True)
    if i == 1:
        print("")
    r = input()
    print("recu:", r, flush=True)
    time.sleep(1)
