import numpy as np


def resize_image(A, scale, method):
    # Denne funktion skalerer et billede med en faktor givet af variablen scale.
    # Der kan anvendes følgende metoder:
    #  'nearest': Nærmeste nabo interpolation
    #  'linear' : Lineær interpolation
    #  'cubic'  : Kubisk Hermite interpolation

    # Vi bestemmer første størrelsen af det
    # skalerede billede ud fra størrelsen af A
    [m, n] = A.shape
    new_cols = round(scale * n)
    new_rows = round(scale * m)
    # Vi interpolerer nu rækkerne
    A1 = unit_step_row_interpolate(A, new_cols, method)
    # Og til sidst interpolerer vi søjlerne
    A2 = unit_step_column_interpolate(A1, new_rows, method)
    return [A2]


def unit_step_row_interpolate(A, new_cols, method):
    #  I denne funktion interpolerer vi rækkerne i matricen A. Således at
    #  hvis A er en m x n matrix så er den resulterende matrix A1 en m x
    #  new_cols

    [m, n] = A.shape
    # Vi laver en matrix X som er m x new_cols og hvor rækkerne alle sammen
    # er på formen [1, 1+(n-1)/(new_cols-1),..., n]
    X = np.tile(np.linspace(1, n, new_cols), (m, 1))
    # Hvis nærmeste nabo interpolation er valgt:
    if method == 'nearest':
        # Indgangene i X afrundes til nærmeste heltal
        X = round(X)
        # Vi tæller hvor mange gange søjlerne i X gentages
        repvec = np.digitize(X[1, :], range(1, n + 1))
        # Vi gentager søjlerne i A i forhold til hvor mange gange
        # tilsvarende søjle gentages i X.
        A1 = np.repeat(A, 1, repvec)
    else:
        # Hvis ikke nærmeste nabo interpolation er valgt skal vi udregne
        # de interpolerede værdier.

        # Vi definerer en m x n matrix hvor
        # søjle j er givet ved [jjj...j]
        AX = np.tile(range(1, n), (m, 1))

        # Vi skal nu bestemme hvor mange værdier i X's rækker der falder
        # intervallerne [1,2), [2,3), osv. Ud fra dette laver vi en matrix k
        # hvor hver række er på formen [1,1,1,dots,1,2,2,dots,2,dots,n] hvor
        # j gentages lige så mange gange som X har værdier der falder i
        # intervallet [j,j+1).

        k = np.ones(new_cols)
        repvec = np.zeros(n - 1)
        n_zeros = 0

        for j in range(2, n - 1):
            idx = AX[1, j] <= X[1, :]
            nnz = np.count_nonzero(idx == False)
            repvec[j - 1] = nnz - n_zeros
            n_zeros = nnz
            k[AX[1, j] <= X[1, :]] = j

        repvec[:] = new_cols - n_zeros
        k = np.tile(k, (m, 1))

        # Vi definerer nu variablen s hvor indgangene i hver række svarer
        # svarer til x-x_j i workshoppen.
        s = X - k

        # Vi definerer nu y-koefficienterne. Bemærk at disse er matricer.
        y0 = [A[:, 1], A[:, 1:-2]]
        y1 = A[:, 1:-1]
        y2 = A[:, 2:]
        y3 = [A[:, 3:], A[:, ]]

        # Hvis lineær interpolation er valgt:
        if method == 'linear':
            # Vi definerer a og b som de er i delopgave 2 (iii).
            a = y2 - y1
            b = y1

            # Vi udvider nu koefficienterne så der er en
            # koefficient til hver indgang i matricen X.
            repvec = repvec.astype(np.int32)
            print(a, repvec)
            print(A)
            a = np.tile(a, repvec)
            b = np.repeat(b, repvec)

            # Vi udregner den resulterence matrix ved at anvende
            # indgangsvise matrixoperationer. Dette er hurtigere end at
            # anvende for-loops.
            A1 = a * s + b

        else:
            # Hvis kubisk Hermite interpolation anvendes:
            raise ('kubisk Hermite interpolation er endnu ikke implementeret')

    return A1


def unit_step_column_interpolate(A1, new_rows, method):
    #  I denne funktion interpolerer vi søjlerne i matricen A1. Således at
    #  hvis A1 er en m x n matrix så er den resulterende matrix A1 en
    #  new_rows x n matrix.
    raise ('Denne funktion er endnu ikke implementeret')

    return A2


if __name__ == "__main__":
    resize_image(np.loadtxt('delopgave1.txt'), 10, "linear")
