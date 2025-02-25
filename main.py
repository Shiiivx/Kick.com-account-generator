import console
import concurrent.futures
import time
import threading
from kick import create_account

print("\nKick.com account generator - https://github.com/fqw3 - Discord: 2yv\n\n")

success = 0
fail = 0
lock = threading.Lock()

def worker():
    global success, fail
    res = create_account()
    with lock:
        if res:
            success += 1
            console.success(f"Account created | {res} | success {success} | Fail {fail}")
        else:
            fail += 1
            console.error(f"Failed | success {success} | Fail {fail}")
    return res

def main(amount, threads):
    global success, fail
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(lambda _: worker(), range(amount)))

    print(f"\nTotal Generated: {success} | Failed: {fail} | Time: {time.time() - start_time:.2f}s")


amount = int(input("How many accounts? "))
threads = int(input("How many threads? "))
threads = min(threads, amount)

main(amount, threads)
console.success("Finished")
