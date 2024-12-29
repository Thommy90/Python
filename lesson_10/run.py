import random
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



result = 0

def count_prime(num):
    global result
    counter = 0
    for j in range(1, num + 1):
        if num % j == 0:
            counter += 1
        if counter > 2:
            return
    result += 1

def get_primes_amount(nums):
    global result
    result = 0
    threads = []

    for num in nums:
        thread = Thread(target=count_prime, args=(num,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result


def main():
    numbers = []

    t1 = Thread(target=fill_list, args=(numbers,))
    t2 = Thread(target=lambda: (t1.join(), calculate_sum(numbers)))
    t3 = Thread(target=lambda: (t1.join(), calculate_average(numbers)))

    t1.start()
    t2.start()
    t3.start()

    numbers_two = [40000, 400, 1000000, 700, 2]
    print("The number of prime numbers: ", get_primes_amount(numbers_two))


if __name__ == "__main__":
    main()
