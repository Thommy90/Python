import random
import time
from queue import Queue
from threading import Thread

def fill_list(numbers):
    print("Start filling list")
    for _ in range(10_000):
        numbers.append(random.randint(1, 10000))
    print("List is filled")

def calculate_sum(numbers):
    print("Start finds the sum of the elements of the list")
    if len(numbers) > 0:
        total_sum = sum(numbers)
        print(f"Sum of the elements = {total_sum}")
    else:
        raise ValueError("The list is empty")

def calculate_average(numbers):
    print("Start finds the arithmetic average of the elements of the list")
    if len(numbers) > 0:
        average = sum(numbers) / len(numbers)
        print(f"Average of elements = {average:.2f}")
    else:
        raise ValueError("The list is empty")

def get_primes_amount(num: int, queue: Queue):
    if num < 2:
        return
    for j in range(2, int(num ** 0.5) + 1):
        if num % j == 0:
            return
    queue.put(1)


def main():
    numbers = []

    t1 = Thread(target=fill_list, args=(numbers,))
    t2 = Thread(target=calculate_sum, args=(numbers,))
    t3 = Thread(target=calculate_average, args=(numbers,))


    t1.start()
    t1.join()

    t2.start()
    t3.start()

    t2.join()
    t3.join()

    numbers_two = [40000, 400, 1000000, 700, 2, 3, 4]

    threads = []
    queue = Queue()

    for number in numbers_two:
        thread = Thread(target=get_primes_amount, args=(number, queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"The number of prime numbers: {queue.qsize()}")


if __name__ == "__main__":
    main()
