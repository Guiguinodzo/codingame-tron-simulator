import statistics
import sys
import time

# Performance ratio : 1/(50% quartile of benchmark in 1/1000 of ms)
CODINGAME_SCORE=1/250
H0ST_SCORE=1/190

HOST_MALUS=CODINGAME_SCORE/H0ST_SCORE

MAX_TIME = .095 * HOST_MALUS

DUMMY_ARRAY = [-1] * 600
iteration_durations = []

def debug(log):
    print(log, file=sys.stderr)

def dummy_operation():
    for _ in range(10):
        for index in range(len(DUMMY_ARRAY)):
            DUMMY_ARRAY[index] = DUMMY_ARRAY[index] + 1

def benchmark():
    start = time.time()
    after = start
    count = 0

    while after - start < MAX_TIME:
        before = time.time()
        dummy_operation()
        after = time.time()
        iteration_durations.append(after - before)
        count += 1

    debug(f"Executed {count} in {(after - start) * 1000:.2f} ms")
    for index, quantile in enumerate(statistics.quantiles(iteration_durations, n=10, method="inclusive")):
        debug(f"Quantile {(index+1)*10:02d}% : {(quantile*1000):.3f} ms")


i=0
moves = ['UP', 'RIGHT', 'DOWN', 'RIGHT']

while True:
    n, my_id = map(int, input().split())
    for j in range(n):
        x0, y0, x1, y1 = map(int, input().split())

    benchmark()

    move = moves[i % len(moves)]
    print(move)
    i += 1
