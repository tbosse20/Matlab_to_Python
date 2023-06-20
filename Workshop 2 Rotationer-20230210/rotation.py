import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm


## Hjælpefunktioner
def make_figure():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect([1, 1, 1])
    lim = 2
    ax.set_xlim([-lim, lim]), ax.set_ylim([-lim, lim]), ax.set_zlim([-lim, lim])
    ax.view_init(elev=30, azim=60)
    return fig, ax


def sphere():
    # https://www.tutorialspoint.com/plotting-points-on-the-surface-of-a-sphere-in-python-s-matplotlib

    u, v = np.mgrid[0:2 * np.pi:21j, 0:np.pi:21j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    return [x, y, z]


def left_multiplication(s, v):
    # Funktion der udregner matricen for venstre
    # multiplikation med kvatanionen [s, v]
    # TODO: raise ('Implementation mangler')
    L = [
        [s, -v[0], -v[1], -v[2]],
        [v[0], s, -v[2], v[1]],
        [v[1], v[2], s, -v[0]],
        [v[2], -v[1], v[0], s]
    ]
    return L


def right_multiplication(s, v):
    # Funktion der udregner matricen for højre
    # multiplikation med kvatanionen [s, v]
    # TODO: raise ('Implementation mangler')
    R = [
        [s, -v[0], -v[1], -v[2]],
        [v[0], s, v[2], -v[1]],
        [v[1], -v[2], s, v[0]],
        [v[2], v[1], -v[0], s]
    ]
    return R


## Introduktion
# I denne Python-fil skal vi lave en
# animation af jordens rotation omkring
# sig selv. Vi modellerer Jorden som
# en kugle med radius 1 og med centrum i Origo.

# Vi kan nemt lave denne model vha. følgende kommando:
[X, Y, Z] = sphere()

# Bemærk at X, Y og Z er matricer således
# at (X(i,j),Y(i,j),Z(i,j)) er et punkt på
# kuglen. Til senere udregninger skal vi
# bruge dimensionerne af matricerne
[m, n] = np.shape(X)

# Det er også mere bekvemt at arbejde
# med en matrix hvor søjlerne i matricen
# er punkter på kuglen:
A = [np.ravel(X), np.ravel(Y), np.ravel(Z)]

# På denne måde kan man givet en 3x3 rotationsmatrix
# R roterere alle punkterne på kuglen på en gang ved
# at udregne R*A. Man kan efterfølgende transformere
# rækkerne i A tilbage til passende matricer med kommandoerne
#       X = A[0].reshape([m, n])
#       Y = A[1].reshape([m, n])
#       Z = A[2].reshape([m, n])

# Man kan plotte kuglen med kommandoen
fig, ax = make_figure()
ax.plot_surface(X, Y, Z)
plt.show()

## Opgave (i)
# I denne opgave skal vi roterere kuglen så den
# får den korrekte hældning. Husk at vi antager
# at nordpolen er placeret i punktet (0,0,1).
# Med denne antagelse giver plottet af X, Y og
# Z passende linjer for længde og breddegrader.

# Bestem først rotationsvinklen i radianer
theta = 0000
theta = 23.4 * np.pi / 180
sin = np.sin(theta)
cos = np.cos(theta)

# Bestem Efterfølgende rotationsmatricen R der
# roterer med en vinkel theta omkring y-aksen
R = 0000
R = [
    [cos, 0, sin],
    [0, 1, 0],
    [-sin, 0, cos],
]

# Roter punkterne på kuglen
A = np.matmul(R, A)

# Omtransformer til matricer og plot resultatet:
X = A[0].reshape([m, n])
Y = A[1].reshape([m, n])
Z = A[2].reshape([m, n])

# Calculate the colors for each point on the sphere
# colors = np.zeros_like(x)
# colors = (u - np.min(u)) / (np.max(u) - np.min(u))
fig, ax = make_figure()
ax.plot_surface(X, Y, Z, shade=True)
plt.show()

## Opgave (ii)
# Vi skal i denne opgave bestemme en enhedsvektor
# der er parallel med linjen gennem nord og sydpolen.
v = 0000
v = np.matmul(R, [0, 0, 1])

## Opgave (iii)
# Vi skal i denne opgave lave en animation af
# Jordens rotation om sin egen akse. Dette
# gøres vha. Matlabs VideoWriter funktion. Vi
# skal sådan set bare tegne de frames der skal
# indgå i animationen så klarer Python resten.

# Vi ønsker 60 fps og 3 sekunders video
fps, seconds = 60, 3

# Derfor får vi det totale antal frames
n_frames = fps * seconds

# Vi laver nu figuren vi skal plotte i
fig, ax = make_figure()


# Nedenstående loop laver de frames der
# skal indgå i animationen.
def update(k):
    # Vi ønsker en enkelt rotation så vi
    # sætter vinklen vi roterer jorden
    # med i frame k til at være
    theta = k * 2 * np.pi / n_frames

    # Udregn s og lambda for den kvatanion
    # som vi skal bruge for at rotere
    # med en vinkel theta omkring v
    s = 0000
    s = np.cos(theta / 2)
    l = 0000  # lambda
    l = np.sin(theta / 2)  # lambda

    # Brug funktionerne left_multiplication og
    # right_multiplication til at definere
    # passende matricer til at udregne
    # rotationen qpq^(-1) hvor q=[s,lambda*v]
    # L = left_multiplication(0000, 0000)
    L = left_multiplication(s, l * v)
    # R = right_multiplication(0000, 0000)
    R = right_multiplication(s, -l * v)

    # Vi omdanner nu vektorerne i A til kvatanioner
    # ved at sætte deres skalardel lig 0.
    Q = np.vstack((np.zeros((1, n * m)), A))

    # Vi udregner rotationen omkring v vha. kvatanioner
    Q = np.dot(np.dot(L, R), Q)

    # Vi omdanner vores roterede kvatanioner til
    # vektorer. Bemærk at vi smider skalardelen væk,
    # da den blot er 0.
    X = Q[1, :].reshape((m, n))
    Y = Q[2, :].reshape((m, n))
    Z = Q[3, :].reshape((m, n))

    # Vi plotter den roterede kugle og sørger
    # for at vores plot bliver en frame i videoen.
    # Bemærk at det er hurtigere i Matlab at
    # plotte kuglen første gang og efterfølgende
    # bare opdatere plottets indhold.
    ax.clear()

    # https://stackoverflow.com/questions/49325704/unexpected-constant-color-using-matplotlib-surface-plot-and-facecolors
    phi = np.linspace(0, 2 * np.pi, 50)
    theta = np.linspace(0, np.pi, 25)
    PHI = np.outer(phi, np.ones(np.size(theta)))
    data = PHI / np.pi
    norm = plt.Normalize(vmin=data.min(), vmax=data.max())
    ax.plot_surface(X, Y, Z, facecolors=cm.jet(norm(data)))

    # Vi plotter rotationsaksen
    x = [-2 * v[0], 2 * v[0]]
    y = [-2 * v[1], 2 * v[1]]
    z = [-2 * v[2], 2 * v[2]]
    ax.plot(x, y, z, color='red')

    print(f'\rSaving gif ..', end='')


ani = animation.FuncAnimation(
    fig, update, frames=n_frames,
    interval=1000 / fps)

writer = animation.PillowWriter(fps=30)
ani.save('animation.gif', writer=writer)
