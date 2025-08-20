from utils.color_palette import ColorPalette
import numpy as np
import time
import matplotlib.pyplot as plt

# Definition of the algorithms

#---------Linear search--------------#
def linear_search(list1, target1):
    for index, i in enumerate(list1):
        if i == target1:
            return index
    return -1

#---------Binary search--------------#
def binary_search(list2, low, high, target2):
    if high >= low:
        mid = (high + low) // 2
        if list2[mid] == target2:
            return mid
        elif list2[mid] > target2:
            return binary_search(list2, low, mid - 1, target2)
        else:
            return binary_search(list2, mid + 1, high, target2)
    else:
        return -1

# This function is no longer needed in the GUI version but kept for compatibility
def run_comparison():
    # All the usable sizes for the lists
    sizes = [100, 1000, 10000, 100000]
    element_range = 1000

    # Ask for the value to find 
    target1 = int(input("Enter the int value for the target of the linear search: "))
    target2 = int(input("Enter the int value for the target of the binary search: "))

    # List to storage the time of each cycle
    linear_times = []
    binary_times = []

    # Number of repetitions
    reps = 5

    # Time measuring
    for size in sizes:
        list1 = [int(x) for x in np.random.randint(0, element_range, size)]
        list2 = sorted([int(x) for x in np.random.randint(0, element_range, size)])

        if not list1 or not list2:
            print("No data was generated, cancelling process...")
            break

        l_times = []
        b_times = []
        for _ in range(reps):
            # Linear search
            start = time.perf_counter()
            linear_search(list1, target1)
            end = time.perf_counter()
            l_times.append(end - start)

            # Binary search
            start = time.perf_counter()
            binary_search(list2, 0, len(list2) - 1, target2)
            end = time.perf_counter()
            b_times.append((end - start) * 1000)

        linear_times.append(np.mean(l_times))
        binary_times.append(np.mean(b_times))

    # ---------------- Comparative graphic creation ----------------
    plt.plot(sizes, linear_times, marker='o', label="Linear Search", color=ColorPalette.get_hex("Azalea Pink"))
    plt.plot(sizes, binary_times, marker='o', label="Binary Search", color=ColorPalette.get_hex("Spring Green"))
    plt.title("Performance Comparison: Linear vs Binary Search", color=ColorPalette.get_hex("Denim Blue"))
    plt.xlabel("List size", color=ColorPalette.get_hex("Denim Blue"))
    plt.ylabel("Average Time (miliseconds)", color=ColorPalette.get_hex("Denim Blue"))
    plt.legend()
    plt.grid(True, color=ColorPalette.get_hex("Baby Blue"), alpha=0.3)
    plt.show()

# Only run the comparison if this script is executed directly
if __name__ == "__main__":
    run_comparison()