import math
import numpy as np

## Solsystemet
# Denne fil indeholder Matlabkode vedrørende workshoppen om solsystemet.

## Delopgave 1 (iv)
# I denne opgave skal vi undersøge modellen af Solsystemet som findes i
# filen "model1.m". Vi kan se modellen ved kalde filnavnet (model1.m
# ligger i samme mappe som filen solsystem.m
import model13
model13.main()


# # Delopgave 1 (v)
# Vi har følgende omløbstider (i år) for planeterne, Pluto samt Halleyskomet:
     # Merkur    # Venus    # Jorden    # Mars   # Jupiter   # Saturn   # Uranus   # Neptun   # Pluto  # Halleys komet
T = [0.2408467, 0.61519726, 1.0000174, 1.8808476, 11.862615, 29.447498, 84.016846, 164.79132, 247.92065, 75.32]
# og vi har følgende halve storeakser (i enheden AU):
a = [0.38709843, 0.72332102, 1.00000018, 1.52371243, 5.20248019, 9.54149883, 19.18797948, 30.06952752, 39.48686035, 17.8341442925537]

# Vi plotter punkterne i et dobbeltlogaritmisk koordinatsystem:
#scatter(T, a)
#set(gca, 'xscale', 'log', 'yscale', 'log')

# # Delopgave 2 (iv)
# Vi har følgende data for Jorden:
a = 1.00000018
e = 0.01673163

# Implementer trapezreglen i filen trapezreglen.m og brug følgende kode til at
from trapezreglen import *
dist = a * trapezreglen(math.sqrt(1 + np.pow(math.e, 2) * np.pow(np.sin(t), 2) - np.pow(math.e, 2)), 0, 2 * np.pi, 10000)

# # Delopgave 3
# I denne opgave skal Newtons metode implementeres i filen newtons_method.m
# Når det er gjort vil den anden model af solsystemet, der opfylder Keplers
# anden lov, virke. Vi starter med at rydde gemte variable og eksisterende
# figurer.

# Planet (og Pluto) data
planet_data = readmatrix('planet_data1.txt')
planet_names = {'Merkur', 'Venus', 'Jorden', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptun', 'Pluto'}
planet_colors = {[.75, .75, .75], [1, 0.4, 0.6], [0, 0, 1], [1, 0, 0], [0, 1, 0], [0.7, 0, 0.7], [0.7, 0.7, 0], [0, 0.7, 0.7], [0.5, 0.5, 0.5]}
# Komet data
halleys = [11, 17.8341442925537	, 0.967142908462304, 38.3842644764388, 2449400.5, 0.01308656479244564]

# Vi laver et tomt solsystem
S = solar_system
# Vi tilføjer Solen
S.add_sun(696340)
# Vi tilføjer planeterne (og Pluto)
S.add_planets(planet_names, planet_colors, planet_data)
# Vi tilføjer Halleys komet
S.add_comets({'Halleys komet'}, {[0, 0, 0]}, halleys)
# Vi laver passende skaleringer af solsystemet
S.scale_radii(2^(-14))
S.scale_distances(2)
# Vi starter modellen til tiden 3000 e.Kr. Tallet 0.4 nedenfor afgør hvor
# hurtigt planeterne bevæger sig i modellen.
S.run(-3000, 0.4)