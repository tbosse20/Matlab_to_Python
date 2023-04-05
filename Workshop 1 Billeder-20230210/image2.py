

import cv2
import numpy as np
from matplotlib import pyplot as plt
from log_transform import *
from resize_image import *

# Delopgave 1
# I denne delopgave skal vi anvende funktionen
# log_transform fra delopgave 1(iii)

A = np.loadtxt('delopgave1.txt')

fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 3

fig.add_subplot(rows, columns, 1)
plt.imshow(A, cmap='gray')
plt.axis('off')
plt.title("imshow(A)")

fig.add_subplot(rows, columns, 2)
plt.imshow(A, cmap='gray')
plt.axis('off')
plt.title("imshow(A,[])")

fig.add_subplot(rows, columns, 3)
plt.imshow(log_transform(A, 1/7), cmap='gray')
plt.axis('off')
plt.title("imshow(log\_transform(A,1/7))")

plt.show()

## Delopgave 3
# I denne opgave skal vi prøve at anvende de funktioner
# der er implementeret i .m-filen resize_image.m.
# Først skal vi have loaded de billeder vi skal bruge.
# Disse er gemt som .txt dokumenter, men kan nemt hentes
# ind i matlab(PYTHON) ved at bruge funktionen dlread(np.loadtxt).

A = np.loadtxt('delopgave3_1.txt')
B = np.loadtxt('delopgave3_2.txt')

#Vi får matlab til at vise de to billeder:
fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 2

fig.add_subplot(rows, columns, 1)
plt.axis('off')
plt.imshow(A, cmap='gray')

fig.add_subplot(rows, columns, 2)
plt.axis('off')
plt.imshow(B, cmap='gray')

plt.show()

# A er et meget lille (16x16) billede.
# Hvis vi forstørre det ser vi hvad der
# sker når man anvender de forskellige
# interpolationsmetoder.
scale = 128

#width = int(A.shape[1] * scale / 100)
#height = int(A.shape[0] * scale / 100)
#dim = (width, height)

fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 3

#E = cv2.resize(A, dim, interpolation=cv2.INTER_NEAREST)
E = resize_image(A, scale, "nearest")
fig.add_subplot(rows, columns, 1)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = resize_image(A, scale, "linear")
fig.add_subplot(rows, columns, 2)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = resize_image(A, scale, "cubic")
fig.add_subplot(rows, columns, 3)
plt.axis('off')
plt.imshow(E, cmap='gray')

plt.show()

# Now with scale at 0.5
scale = 0.5

width = int(A.shape[1] * scale)
height = int(A.shape[0] * scale)
dim = (width, height)

fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 3
E = cv2.resize(A, dim, interpolation=cv2.INTER_NEAREST)
fig.add_subplot(rows, columns, 1)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = cv2.resize(A, dim, interpolation=cv2.INTER_LINEAR)
fig.add_subplot(rows, columns, 2)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = cv2.resize(A, dim, interpolation=cv2.INTER_CUBIC)
fig.add_subplot(rows, columns, 3)
plt.axis('off')
plt.imshow(E, cmap='gray')

plt.show()

#Vi kan prøve at gøre noget lignende med B
scale = 0.73

width = int(A.shape[1] * scale)
height = int(A.shape[0] * scale)
dim = (width, height)

fig = plt.figure(figsize=(10, 7))
rows, columns = 1, 3

E = cv2.resize(B, dim, interpolation=cv2.INTER_NEAREST)
fig.add_subplot(rows, columns, 1)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = cv2.resize(B, dim, interpolation=cv2.INTER_LINEAR)
fig.add_subplot(rows, columns, 2)
plt.axis('off')
plt.imshow(E, cmap='gray')

E = cv2.resize(B, dim, interpolation=cv2.INTER_CUBIC)
fig.add_subplot(rows, columns, 3)
plt.axis('off')
plt.imshow(E, cmap='gray')

plt.show()