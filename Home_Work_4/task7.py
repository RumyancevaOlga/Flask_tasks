# � Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.
import multiprocessing
from random import randint as rnd
import threading
from multiprocessing import Process
import asyncio
import time

# генерация массива
arr = [rnd(1, 101) for i in range(1_000_000)]


# функция для обычного подсчета
def summa(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    print(f"Сумма посчитанная обычным методом = {result}. Посчитано за {time.time() - start_time:.2f} секунд")


# функция для многопоточного подсчета
def thread_sum_arr(arr):
    global thread_result
    for i in range(len(arr)):
        thread_result += arr[i]
    print(f"Многопоточный подсчет суммы пока что = {thread_result}. Посчитано за {time.time() - start_time:.2f} секунд")


# разбиение массива на 10 частей для подсчета суммы разными методами
chunk_size = 100000
split_list = list()

for i in range(0, len(arr), chunk_size):
    split_list.append(arr[i:i+chunk_size])


# переменные для многопроцессорного подсчета
proc_result = multiprocessing.Value('i', 0)
processes = []
start_time = time.time()


# функция для многопроцессорного подсчета
def proc_sum_arr(arr, cnt):
    for i in range(len(arr)):
        with cnt.get_lock():
            cnt.value += arr[i]
    print(f"Многопроцессорный подсчет суммы пока что = {cnt.value}. Посчитано за {time.time() - start_time:.2f} секунд")


# функции для асинхронного подсчета
async def async_sum_arr(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    print(f"Асинхронный подсчет суммы пока что = {result}. Посчитано за {time.time() - start_time:.2f} секунд")
    return result


async def main():
    result = 0
    for item in split_list:
        result_async = await asyncio.gather(async_sum_arr(item))
        result += int(result_async[0])
    print(f"Асинхронный подсчет суммы в финале = {result}.")

if __name__ == '__main__':
    # переменные для многопоточного подсчета
    thread_result = 0
    threads = []
    start_time = time.time()

    # многопоточный подсчет
    for item in split_list:
        thread = threading.Thread(target=thread_sum_arr, args=[item])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Многопоточный подсчет суммы в финале = {thread_result}.")

    # обычный подсчет
    start_time = time.time()
    summa(arr)

    # многопроцессоный подсчет
    for item in split_list:
        process = Process(target=proc_sum_arr, args=[item, proc_result])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # асинхронный подсчет
    start_time = time.time()
    asyncio.run(main())
