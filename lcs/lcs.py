def lcs_recursivo(X, Y, m, n):
    """
    Calcula la longitud de la LCS usando recursividad (Divide y Vencerás).
    m y n son las longitudes actuales de X e Y.
    """
    # Caso base
    if m == 0 or n == 0:
        return 0

    # Si los últimos caracteres coinciden
    elif X[m-1] == Y[n-1]:
        return 1 + lcs_recursivo(X, Y, m-1, n-1)

    # Si no coinciden, se divide en dos subproblemas
    else:
        return max(lcs_recursivo(X, Y, m, n-1), lcs_recursivo(X, Y, m-1, n))


def lcs_dinamico(X, Y):
    """
    Calcula la longitud de la LCS usando Programación Dinámica (Bottom-Up).
    """
    m = len(X)
    n = len(Y)

    # Crear la tabla para almacenar los resultados
    L = [[0]*(n+1) for i in range(m+1)]

    # Construir la tabla L[i][j] de abajo hacia arriba
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    return L[m][n]

def reconstruir_lcs(L, X, Y):
    """
    Reconstruye la subsecuencia común (no sólo la longitud) haciendo backtracking en la tabla L.
    """
    i, j = len(X), len(Y)
    lcs_chars = []
    # Backtrack
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_chars.append(X[i-1])
            i -= 1
            j -= 1
        else:
            if L[i-1][j] >= L[i][j-1]:
                i -= 1
            else:
                j -= 1
    return "".join(reversed(lcs_chars))

def lcs_dinamico_tabla(X, Y):
    """
    Calcula la tabla L (m+1 x n+1) y devuelve la tabla y la longitud L[m][n].
    """
    m, n = len(X), len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L, L[m][n]