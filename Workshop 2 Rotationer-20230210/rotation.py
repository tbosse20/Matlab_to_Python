import numpy as np
from matplotlib import pyplot as plt
from Hjaelpefunktioner import *
import matplotlib.animation as animation

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
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.view_init(30, 45)
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
    [cos,  0,  sin],
    [ 0,   1,   0 ],
    [-sin, 0,  cos],
]

# Roter punkterne på kuglen
A = np.matmul(R, A)

# Omtransformer til matricer og plot resultatet:
X = A[0].reshape([m, n])
Y = A[1].reshape([m, n])
Z = A[2].reshape([m, n])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.view_init(30, 45)
ax.plot_surface(X, Y, Z)
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
fig = plt.figure(figsize=(6, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1, 1, 1])
ax.view_init(30, 45)

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
    #L = left_multiplication(0000, 0000)
    L = left_multiplication(s, l * v)
    #R = right_multiplication(0000, 0000)
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

    # Vi plotter rotationsaksen
    ax.clear()
    ax.plot_surface(X, Y, Z, color='b')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

ani = animation.FuncAnimation(
    fig, update, frames=n_frames,
    interval=1000/fps)

writer = animation.PillowWriter(fps=30)
ani.save('animation.gif', writer=writer)