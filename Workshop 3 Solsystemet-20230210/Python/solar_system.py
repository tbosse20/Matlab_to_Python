import time

import matplotlib.pyplot
import matplotlib.pyplot as plt
from Planet import Planet
from Comet import Comet
from Sun import Sun
import numpy as np


class Solar_system:
    def __init__(self):
        self.planets: Planet = list()
        self.comets: Comet = list()
        self.t = -3000
        self.dt = 10
        self.playing = False
        self.paused = False
        self.axis_lim = [-40, 40, -40, 40]
        self.show_text = True

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('key_press_event', lambda event: self.buttonpush(event))

        plt.axis('equal')
        plt.title('Solsystemet')
        plt.axis(self.axis_lim)
        self.text = plt.text(
            0.8 * self.axis_lim[1], self.axis_lim[3],
            '', verticalalignment='top')

    def add_planets(self, names, colors, planet_data):
        l = len(names)
        self.planets = list()
        # Sort the planets wrt radius
        idx = np.argsort(np.array(planet_data)[:, 0])
        names = [names[i] for i in idx]
        colors = [colors[i] for i in idx]
        planet_data = [planet_data[i] for i in idx]
        for i in range(l):
            planet = Planet(names[i], colors[i], planet_data[i], self.ax)
            self.planets.append(planet)

    def add_comets(self, names, colors, comet_data):
        l = len(names)
        self.comets = list()
        # Sort the comets wrt radius
        idx = np.argsort(np.array(comet_data)[:, 0])
        names = [names[i] for i in idx]
        colors = [colors[i] for i in idx]
        comet_data = [comet_data[i] for i in idx]
        for i in range(l):
            comet = Comet(names[i], colors[i], comet_data[i], self.ax)
            self.comets.append(comet)

    def add_sun(self, radius):
        self.sun = Sun(radius, self.ax)

    def update(self, t):
        self.t = t
        for planet in self.planets:
            planet.update(t)
        for comet in self.comets:
            comet.update(t)
        if hasattr(self, "sun"):
            self.sun.update()

    def draw_system(self):
        for planet in self.planets:
            planet.ball.set_visible(True)
            if self.show_text and \
                    self.axis_lim[0] <= planet.coordinates[0] <= self.axis_lim[1] and \
                    self.axis_lim[2] <= planet.coordinates[1] <= self.axis_lim[3]:
                planet.text.set_visible(True)
            else:
                planet.text.set_visible(False)

        for comet in self.comets:
            comet.ball.set_visible(True)
            if self.show_text and \
                    self.axis_lim[0] <= comet.coordinates[0] <= self.axis_lim[1] and \
                    self.axis_lim[2] <= comet.coordinates[1] <= self.axis_lim[3]:
                comet.text.set_visible(True)
            else:
                comet.text.set_visible(False)

        if hasattr(self, "sun"):
            self.sun.ball.set_visible(True)
            self.sun.text.set_visible(self.show_text)

        self.text.set_text(
            'q: afslut spillet\n'
            'mellemrum: pause/genoptag\n'
            'piletaster: skalér/zoom\n'
            't: tekster til/fra\n'
            'punktum/komma: hastighed op/ned\n'
            f'dato: {self.time_to_date(self.t)}')
        self.text.set_position([0.9 * self.axis_lim[1], 0.9 * self.axis_lim[3]])

        plt.axis(self.axis_lim)

    def scale_distances(self, scale):
        for planet in self.planets:
            planet.a *= scale
        for comet in self.comets:
            comet.a *= scale

    def scale_radii(self, scale):
        for planet in self.planets:
            planet.radius *= scale
        for comet in self.comets:
            comet.radius *= scale
        if hasattr(self, "sun"):
            self.sun.radius *= scale

    @staticmethod
    def time_to_date(t):
        year = int(t)
        fractional_part = t - year
        day = abs(int(365.25 * fractional_part)) + 1
        if year < 1:
            year = abs(year - 1)
            prefix = 'BC'
        else:
            prefix = 'AD'

        if 0 <= day <= 31:
            month = 'Jan'
        elif 31 < day <= 59:
            month = 'Feb'
            day -= 31
        elif 59 < day <= 90:
            month = 'Mar'
            day -= 59
        elif 90 < day <= 120:
            month = 'Apr'
            day -= 90
        elif 120 < day <= 151:
            month = 'May'
            day -= 120
        elif 151 < day <= 181:
            month = 'Jun'
            day -= 151
        elif 181 < day <= 212:
            month = 'Jul'
            day -= 181
        elif 212 < day <= 243:
            month = 'Aug'
            day -= 212
        elif 243 < day <= 273:
            month = 'Sep'
            day -= 243
        elif 273 < day <= 304:
            month = 'Oct'
            day -= 273
        elif 304 < day <= 334:
            month = 'Nov'
            day -= 304
        else:
            month = 'Dec'
            day -= 334
        if day > 31: day = 31

        date = f'{day}. {month} {year} {prefix}'
        return date

    def run(self, t, dt, refresh_rate):
        self.playing = True
        self.dt = dt
        start_time = time.time()
        while self.playing and t <= 3000:
            plt.pause(refresh_rate)
            if self.paused:
                self.draw_system()
                continue
            self.update(t)
            self.draw_system()
            time_elapsed = (time.time() - start_time) * refresh_rate
            t += self.dt * time_elapsed
            self.fig.canvas.draw()

    def buttonpush(self, event):
        if event.key == 'q':
            self.playing = False
        elif event.key == ' ':
            self.paused = not self.paused
        elif event.key == 'left':
            self.scale_radii(0.5)
        elif event.key == 'right':
            self.scale_radii(2)
        elif event.key == 'down':
            self.axis_lim = [x * 2 for x in self.axis_lim]
        elif event.key == 'up':
            self.axis_lim = [x / 2 for x in self.axis_lim]
        elif event.key == ',':
            self.dt /= 2
            for planet in self.planets:
                planet.trace_length += 20
        elif event.key == '.':
            self.dt *= 2
            for planet in self.planets:
                planet.trace_length -= 20
        elif event.key == 't':
            self.show_text = not self.show_text
            self.show_hide_text()

    def show_hide_text(self):

        self.sun.text.set_visible(self.show_text)

        for planet in self.planets:
            if self.show_text and \
                    self.axis_lim[0] <= planet.coordinates[0] <= self.axis_lim[1] and \
                    self.axis_lim[2] <= planet.coordinates[1] <= self.axis_lim[3]:
                planet.text.set_visible(True)
            else:
                planet.text.set_visible(False)

        for comet in self.comets:
            if self.show_text and \
                    self.axis_lim[0] <= comet.coordinates[0] <= self.axis_lim[1] and \
                    self.axis_lim[2] <= comet.coordinates[1] <= self.axis_lim[3]:
                comet.text.set_visible(True)
            else:
                comet.text.set_visible(False)

        self.text.set_text(['q: afslut spillet',
                            'mellemrum: pause/genoptag',
                            'piletaster: skalér/zoom',
                            't: tekster til/fra',
                            'punktum/komma: hastighed op/ned',
                            ['dato: ', self.time_to_date(self.t)]])
        self.text.set_position([0.9 * self.axis_lim[1], 0.9 * self.axis_lim[3]])


if __name__ == "__main__":
    # # Delopgave 3
    # I denne opgave skal Newtons metode implementeres i filen newtons_method.m
    # Når det er gjort vil den anden model af solsystemet, der opfylder Keplers
    # anden lov, virke. Vi starter med at rydde gemte variable og eksisterende
    # figurer.

    # Planet (og Pluto) data
    planet_data = np.loadtxt('planet_data1.txt', delimiter=',')
    planet_names = [
        'Merkur', 'Venus', 'Jorden', 'Mars', 'Jupiter',
        'Saturn', 'Uranus', 'Neptun', 'Pluto'
    ]
    planet_colors = [
        [.75, .75, .75], [1, 0.4, 0.6], [0, 0, 1], [1, 0, 0], [0, 1, 0],
        [0.7, 0, 0.7], [0.7, 0.7, 0], [0, 0.7, 0.7], [0.5, 0.5, 0.5]
    ]

    # Komet data
    halleys = [11, 17.8341442925537, 0.967142908462304,
               38.3842644764388, 2449400.5, 0.01308656479244564]

    # Vi laver et tomt solsystem
    S = Solar_system()
    # Vi tilføjer Solen
    S.add_sun(696340)
    # Vi tilføjer planeterne (og Pluto)
    S.add_planets(planet_names, planet_colors, planet_data)
    # Vi tilføjer Halleys komet
    S.add_comets(['Halleys komet'], [[0, 0, 0]], [halleys])
    # Vi laver passende skaleringer af solsystemet
    S.scale_radii(2 ** (-14))
    S.scale_distances(2)
    # Vi starter modellen til tiden 3000 e.Kr. Tallet 0.4 nedenfor afgør hvor
    # hurtigt planeterne bevæger sig i modellen.
    S.run(-3000, 0.4, 0.01)
