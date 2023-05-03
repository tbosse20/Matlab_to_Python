import numpy as np


def resize_image(A, scale, method):
    # Denne funktion skalerer et billede med en faktor givet af variablen scale.
    # Der kan anvendes følgende metoder:
    #  'nearest': Nærmeste nabo interpolation
    #  'linear' : Lineær interpolation
    #  'cubic'  : Kubisk Hermite interpolation

    # Vi bestemmer første størrelsen af det
    # skalerede billede ud fra størrelsen af A
    m, n = A.shape
    new_cols = round(scale * n)
    new_rows = round(scale * m)
    # Vi interpolerer nu rækkerne
    A1 = unit_step_row_interpolate(A, new_cols, method)
    # Og til sidst interpolerer vi søjlerne
    A2 = unit_step_column_interpolate(A1, new_rows, method)
    return A2


def unit_step_row_interpolate(A, new_cols, method):
    #  I denne funktion interpolerer vi rækkerne i matricen A. Således at
    #  hvis A er en m x n matrix så er den resulterende matrix A1 en m x
    #  new_cols

    m, n = A.shape
    # Vi laver en matrix X som er m x new_cols og hvor rækkerne
    # alle sammen er på formen [1, 1+(n-1)/(new_cols-1),..., n]
    X = np.tile(np.linspace(1, n, new_cols), (m, 1))
    # Hvis nærmeste nabo interpolation er valgt:
    if method == 'nearest':
        # Indgangene i X afrundes til nærmeste heltal
        X = np.round(X).astype(int)
        # Vi tæller hvor mange gange søjlerne i X gentages
        repvec, _ = np.histogram(X[0, :], bins=np.arange(1, n + 2))
        # Vi gentager søjlerne i A i forhold til hvor mange gange
        # tilsvarende søjle gentages i X.
        A1 = np.repeat(A, repvec, axis=1)

    else:
        # Hvis ikke nærmeste nabo interpolation er valgt skal vi udregne
        # de interpolerede værdier.

        # Vi definerer en m x n matrix hvor søjle j er givet ved [jjj...j]
        AX = np.tile(np.arange(1, n + 1), (m, 1))

        # Vi skal nu bestemme hvor mange værdier i X's rækker der falder
        # intervallerne [1,2), [2,3), osv. Ud fra dette laver vi en matrix k
        # hvor hver række er på formen [1,1,1,dots,1,2,2,dots,2,dots,n] hvor
        # j gentages lige så mange gange som X har værdier der falder i
        # intervallet [j,j+1).

        k = np.ones(new_cols)
        #k = np.ones((1, new_cols))
        repvec = np.zeros(n - 1)
        #repvec = np.zeros((1, n - 1))
        print(repvec.shape)
        n_zeros = 0

        for j in range(1, n - 1):
            idx = AX[0, j] <= X[0, :]
            nnz = np.count_nonzero(~idx)
            repvec[j - 1] = nnz - n_zeros
            n_zeros = nnz
            k[AX[0, j] <= X[0, :]] = j

        repvec[-1:] = new_cols - n_zeros
        repvec = repvec.astype(np.int32)
        k = np.tile(k, (m, 1))

        # Vi definerer nu variablen s hvor indgangene i
        # hver række svarer til x-x_j i workshoppen.
        s = X - k

        # Indsat:
        s2 = s * s
        s3 = s2 * s
        # "*" gør at det bliver ganget på direkte i stedet
        # for hvordan man normalt ville gange:
        # A * B -> [A_11 * B_12 + A_21 * B_12, A_21 * B_22 + A_11 * B_21]
        #          [A_22 * B_12 + A_12 * B_11, A_22 * B_22 + A_12 * B_21]
        #
        # A .* B -> [A_11 * B_11, A_21 * B_21]
        #           [A_12 * B_12, A_22 * B_22]

        # Vi definerer nu y-koefficienterne. Bemærk at disse er matricer.
        y0 = np.hstack([A[:, 0].reshape(-1, 1), A[:, 0:-2]])
        y1 =  A[:, 1:] #y1 = A[:, 0:-1]
        y2 =  A[:, 1:]
        y3 = np.hstack([A[:, 2:], A[:, -1].reshape(-1, 1)])

        # Hvis lineær interpolation er valgt:
        if method == 'linear':
            # Vi definerer a og b som de er i delopgave 2 (iii).
            a = y2 - y1
            b = y1

            # Vi udvider nu koefficienterne så der er en
            # koefficient til hver indgang i matricen X.
            a = np.repeat(a, repvec, axis=1)
            b = np.repeat(b, repvec, axis=1)

            # Vi udregner den resulterence matrix ved at anvende
            # indgangsvise matrixoperationer. Dette er hurtigere end at
            # anvende for-loops.
            A1 = a * s + b

        else:
            # Hvis kubisk Hermite interpolation anvendes:
            # raise('kubisk Hermite interpolation er endnu ikke implementeret')
            # Hvis kubisk Hermite interpolation anvendes:
            if method == 'cubic':
                # Vi definerer alpha, beta, og delta, som der er defineret i del opgave 2.7
                alpha = -0.5 * y0 + 1.5 * y1 - 1.5 * y2 + 0.5 * y3
                beta = y0 - 2.5 * y1 + 2 * y2 - 0.5 * y3
                gamma = -0.5 * y0 + 0.5 * y2
                delta = y1

                # Vi udvider nu koefficienterne så der er en
                # koefficient til hver indgang i matricen X.
                alpha = np.repeat(alpha, repvec, axis=1)
                beta = np.repeat(beta, repvec, axis=1)
                gamma = np.repeat(gamma, repvec, axis=1)
                delta = np.repeat(delta, repvec, axis=1)

                # Indangsvis matrix operation
                A1 = alpha * s3 + beta * s2 + gamma * s + delta

            else:
                raise('kubisk Hermite interpolation er endnu ikke implementeret')
    return A1


def unit_step_column_interpolate(A1, new_rows, method):
    #  I denne funktion interpolerer vi søjlerne i matricen A1. Således at
    #  hvis A1 er en m x n matrix så er den resulterende matrix A1 en
    #  new_rows x n matrix.
    #raise ('Denne funktion er endnu ikke implementeret')

    A2 = np.transpose(unit_step_row_interpolate(np.transpose(A1), new_rows, method))

    return A2


if __name__ == "__main__":

    from matplotlib import pyplot as plt

    A = np.loadtxt('delopgave3_1.txt')

    plt.imshow(A, cmap='gray')
    plt.show()

    E = resize_image(A, 128, "cubic")

    plt.imshow(E, cmap='gray')
    plt.show()
