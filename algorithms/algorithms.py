import numpy as np

# Pide el tamaño de la lista al usuario
list_size = int(input("Enter the list size (10, 100, 1000, 10000): "))

# Mientras no esté en los valores permitidos, repite la pregunta
while list_size not in (10, 100, 1000, 10000):
    print("Invalid size. Please enter 10, 100, 1000, or 10000.")
    list_size = int(input("Enter the list size: "))

#Pide el target de las búsquedas

target1 = int(input("Enter the int value for the target of the linear search: "))

target2 = int(input("Enter the int value for the target of the binary search: "))

#Generación de listas de forma random
list1 = [int(x) for x in np.random.randint(0, 100, list_size)]
list2 = [int(x) for x in np.random.randint(0, 100, list_size)]

#Ordenar lista que es usada para la búsqueda binaria

list2=sorted(list2)

#Definición de límites para la búsqueda binaria
low = 0
high = list_size - 1

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
         return binary_search(list2, low, mid - 1, target2)
      else:
         return binary_search(list2, mid + 1, high, target2)
   else:
      return -1
         

#Impresión de resultados

print(list1)
print(linear_search(list1, target1))

print(list2)
print(binary_search(list2, low, high,target2))


