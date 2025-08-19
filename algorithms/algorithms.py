import numpy as np
import time
import matplotlib.pyplot as plt

#All the usable sizes for the lists

sizes = [100, 1000, 10000, 100000]

#Pide el target de las búsquedas

target1 = int(input("Enter the int value for the target of the linear search: "))

target2 = int(input("Enter the int value for the target of the binary search: "))

#Definición de funciones de búsqueda

def  linear_search(list1, target1):

    for index, i in enumerate(list1):
        if i == target1:
         return index
    return -1

def binary_search(list2, low, high, target2):
   if high >= low:
      mid = (high+low)//2
      if list2[mid] == target2:
         return mid
      elif list2[mid] > target2:
         return binary_search(list, low, mid - 1, target2)
      else:
         return binary_search(list2, mid + 1, high, target2)
   else:
      return -1
         

#Listas para la medición del tiempo

linear_times = []
binary_times = []

#Medición del tiempo de respuesta de la función linear search 

for size in sizes:
    # Generar listas aleatorias
    list1 = [int(x) for x in np.random.randint(0, 100, size)]
    list2 = sorted([int(x) for x in np.random.randint(0, 100, size)])

    # Medir tiempo Linear Search
    start = time.perf_counter()
    linear_search(list1, target1)
    end = time.perf_counter()
    linear_times.append(end - start)

    # Medir tiempo Binary Search
    start = time.perf_counter()
    binary_search(list2, 0, len(list2)-1, target2)
    end = time.perf_counter()
    binary_times.append(end - start)

# -------- Graficar --------

plt.figure(figsize=(10,5))

# Gráfica Linear Search
plt.plot(sizes, linear_times, marker='o')
plt.title("Tiempo de ejecución - Linear Search")
plt.xlabel("Tamaño de lista")
plt.ylabel("Tiempo (segundos)")
plt.grid(True)
plt.show()

# Gráfica Binary Search
plt.plot(sizes, binary_times, marker='o', color="red")
plt.title("Tiempo de ejecución - Binary Search")
plt.xlabel("Tamaño de lista")
plt.ylabel("Tiempo (segundos)")
plt.grid(True)
plt.show()

