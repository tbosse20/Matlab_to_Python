import cv2
import numpy as np
from matplotlib import pyplot as plt
from log_transform import *

# Delopgave 1
# I denne delopgave skal vi anvende funktionen
# log_transform fra delopgave 1 (iii)

A = np.loadtxt('delopgave1.txt')

fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 3

fig.add_subplot(rows, columns, 1)
plt.imshow(A)
plt.axis('off')
plt.title("imshow(A,[])")

fig.add_subplot(rows, columns, 2)
plt.imshow(A)
plt.axis('off')
plt.title("imshow(A,[])")

fig.add_subplot(rows, columns, 3)
plt.imshow(log_transform(A, 1/7))
plt.axis('off')
plt.title("imshow(log_transform(A,1/7))")

plt.show()

## Delopgave 3
# I denne opgave skal vi prøve at anvende de funktioner
# der er implementeret i .m-filen resize_image.m.
# Først skal vi have loaded de billeder vi skal bruge.
# Disse er gemt som .txt dokumenter, men kan nemt hentes
# ind i matlab(PYTHON) ved at bruge funktionen dlread(np.loadtxt).

A = np.loadtxt('delopgave3_1.txt')
B = np.loadtxt('delopgave3_2.txt')

# Vi får matlab til at vise de to billeder:
fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 2

fig.add_subplot(rows, columns, 1)
plt.axis('off')
plt.imshow(A)

fig.add_subplot(rows, columns, 2)
plt.axis('off')
plt.imshow(B)

plt.show()


# A er et meget lille (16x16) billede.
# Hvis vi forstørre det ser vi hvad der
# sker når man anvender de forskellige
# interpolationsmetoder.

def show_scaled_image(A, scale):
    interpolations = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC]

    fig = plt.figure(figsize=(10, 7))
    rows, columns = 1, 3

    width = int(A.shape[1] * scale)
    height = int(A.shape[0] * scale)
    dim = (width, height)

    for i, interpolation in enumerate(interpolations):
        E = cv2.resize(A, dim, interpolation=interpolation)
        fig.add_subplot(rows, columns, i + 1)
        plt.axis('off')
        plt.imshow(E)

    plt.show()


show_scaled_image(A, 128)
show_scaled_image(A, 0.5)  # Now with scale at 0.5
show_scaled_image(B, 0.73)  # Vi kan prøve at gøre noget lignende med B


# ------------------ #
def plotFigures(figures: dict):
    fig = plt.figure(figsize=(10, 7))
    rows, columns = 1, len(figures)

    for i, (title, figure) in enumerate(figures.items()):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(figure)
        plt.axis('off')
        plt.title(title)

    plt.show()
