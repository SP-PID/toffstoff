import time


def get_time():
    return time.time()


def main():
    time_1 = get_time()
    time.sleep(1)
    time_2 = get_time()
    time_diff = time_2 - time_1
    print("Time 1: " + str(time_1) + " Time 2: " + str(time_2))
    print("Time difference: " + str(time_diff))

if __name__ == "__main__":
    main()