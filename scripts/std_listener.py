import subprocess
import threading
import queue
import time

commands = [
    ["python", "ping.py"],
    ["python", "ping.py"],
    ["python", "ping.py"],
    ["python", "ping.py"],
]

process_list = []
stdout_logs = [[] for _ in commands]
stderr_logs = [[] for _ in commands]
event_queues = []

threads = []

stop_event = threading.Event()

def stream_reader(pipe, event_queue, process_index, stream_type):
    while not stop_event.is_set():
        line = pipe.readline()
        if not line:
            break
        event_queue.put((process_index, stream_type, line.rstrip()))


for index, command in enumerate(commands):
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    event_queue = queue.Queue()
    event_queues.append(event_queue)
    process_list.append(process)

    t = threading.Thread(
        target=stream_reader,
        args=(process.stdout, event_queue, index, "stdout"),
        daemon=True
    )
    t.start()
    threads.append(t)

    t = threading.Thread(
        target=stream_reader,
        args=(process.stderr, event_queue, index, "stderr"),
        daemon=True
    )
    t.start()
    threads.append(t)


# --- boucle principale ---
running = True
while running:
    running = False

    for process in process_list:
        if process.poll() is None:
            running = True

    for event_queue in event_queues:
        while not event_queue.empty():
            process_index, stream_type, message = event_queue.get()

            if stream_type == "stdout":
                stdout_logs[process_index].append(message)
                print(f"[{process_index} STDOUT] {message}")

                if "ping" in message:
                    process_list[process_index].stdin.write("pong\n")
                    process_list[process_index].stdin.flush()

            else:
                stderr_logs[process_index].append(message)
                print(f"[{process_index} STDERR] {message}")

    time.sleep(0.01)

stop_event.set()
for t in threads:
    t.join()

print("\n=== STDOUT LOGS ===")
print(stdout_logs)

print("\n=== STDERR LOGS ===")
print(stderr_logs)
