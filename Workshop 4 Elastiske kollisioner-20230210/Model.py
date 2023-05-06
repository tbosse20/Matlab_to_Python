import time

from matplotlib import pyplot as plt

from Container import Container
from Ball import Ball
import numpy as np

class Model:
    # Klasse til at modellere bolde der bevæger sig i en beholder.

    t = 0
    dt = 0.001
    paused = 0
    show_text = 1
    show_velocities = 1

    def __init__(self, ngon, nballs, option):
        # Constructer, der laver en beholder og placerer et pase
        # antal bolde i beholderen. Dette gøres tilfældigt.
        self.container = Container(ngon)
        self.nballs = nballs
        self.balls = self.make_balls(nballs, option)
        #set(gcf, 'WindowKeyPressFcn', @ self.buttonpush)
        self.text = plt.text(0.4, 1,
             'q: afslut\n'
             'mellemrum: pause/genoptag\n'
             'piletaster op/ned: skalér hastighed\n'
             't: tekster til/fra', verticalalignment='top')

        #xlim([-1, 1])
        #ylim([-1, 1])
        #axis
        #square

    def make_balls(self, nballs, option):
        # tilfældig generation af et antal bolde.
        balls = [None] * nballs # balls = cell(1, nballs)
        # Generer hastighederne
        velocities = np.random.uniform(low=-1, high=5, size=(2, nballs))
        # Generer boldene, med radius og proportionelle masser:
        [positions, radii, masses] = self.generate_positions_and_radii(option)
        for i in range(nballs):
            balls[i] = Ball(masses(i), radii(i), velocities[:, i], positions[:, i], 'b', str(i))

    def run(self):
        # Kør modellen.
        self.playing = 1
        while self.playing == 1:
            if self.paused:
                time.sleep(0.01)
                continue

            self.update(self.dt)
            #drawnow

        # close[1]

    def update(self, t):
        # Opdater modellen frem til tiden t.
        # Dette kan lave yderligere af tidstrinnet
        # t afhængigt af antallet af kollisioner.
        new_time = self.collision_detection(t)
        self.update_positions(new_time)

    def update_positions(self, t):
        for i in range(self.nballs):
            self.balls[i].update_position(t)

    def scale_velocities(self, scale):
        for i in range(self.nballs):
            self.balls[i].velocity = self.balls[i].velocity * scale

    def collision_detection(self, dt):
        # Find første kollision i tidstrinnet dt.
        new_time = dt
        first_collision = [0, 0, dt]
        positions = self.get_positions_at_time_step(range(self.nballs), dt)
        radii = self.get_radii(range(self.nballs))
        velocities = self.get_velocities(range(self.nballs))
        # Hvis hastighederne er store kan vi risikere
        # at bolde kan ryge ud af beholderen eller
        # passere igennem hinanden. Nedenste loop detekterer
        # dette og reducerer tidstrinnet om nødigt.
        in_container = self.container.in_container(positions)
        pass_through = 0
        for i in range(self.nballs - 1):
            for j in range(i+1, self.nballs):
                if self.pass_through(self.balls[i].position, positions[:, i], self.balls[j].position, positions[:, j]):
                    pass_through = 1
                    break
            if pass_through:
                #disp('break_through')
                break
        if np.count_nonzero(in_container) < self.nballs or pass_through:
            new_time = self.collision_detection(new_time / 2)
        else:
            # Hvis ikke overnævnte tilfælde sker kan vi bestemme
            # kollisionerne og finde den første.
            for i in range(self.nballs):
                position = positions[:, i]
                radius = radii[i]
                velocity = velocities[:, i]

                if i < self.nballs:
                    remaining_positions = positions[:, i + 1: self.nballs]
                    remaining_radii = self.get_radii(range(i, self.nballs))
                    ball_collisions = self.ball_collisions(position, radius, remaining_positions, remaining_radii)
                else: ball_collisions = 0

                n_collisions = np.count_nonzero(ball_collisions)
                # Hvis der er bolde der kolliderer udregner vi de eksakte tidspunkter.
                if n_collisions > 0:
                    ball_idx = i + np.flatnonzero(ball_collisions)
                    u = positions[:, ball_idx] - position
                    v = velocities[:, ball_idx] - velocity
                    udotv = np.dot(u, v)
                    vv = np.dot(v, v)
                    uu = np.dot(u, u)
                    r = radii[ball_idx] + radius
                    time_of_collisions = dt - (udotv + np.sqrt(udotv ** 2 - vv * (uu - r ** 2))) / vv
                    [time, idx] = min(time_of_collisions)
                    if time < first_collision[3]:
                        first_collision = [i, ball_idx[idx], time]


                # Vi udregner de eksakte tidspunkter for kollisioner med beholderen.
                [edge_collisions, edge_idx, edge_dists] = self.edge_collisions(position, radius)
                n_collisions = np.count_nonzero(edge_collisions)

                if n_collisions > 0:
                    n = self.container.normals[:, edge_idx]
                    vel = np.tile(velocity, (len(n[0]), 1)).T
                    time_of_collisions = dt - (edge_dists + radius) / np.dot(n.T, vel).flatten()
                    [time, idx] = min(time_of_collisions)
                    if time < first_collision[3]: first_collision = [i, -edge_idx(idx), time]

            # Updater positionerne til første kollision og opdater hastighedvektorerne for de involverede selfekter.
            if first_collision[3] < dt:
                self.update_positions(first_collision[3])
                if first_collision[2] > 0: self.ball_collision_update(first_collision[1], first_collision[2])
                else: self.edge_collision_update(first_collision[1], -first_collision[2])
                new_time = dt - first_collision[3]
                # Test for flere kollisioner i den restee tid af tidstrinnet.
                new_time = self.collision_detection(new_time)
        return new_time

    def edge_collision_update(self, ball_idx, edge_idx):
        # opdater bold nr ball_idx hastighedsvektor efter kollision
        # med kant edge_idx.Her anes reflektioner fra delopgave 4, # se mere i filen Container.m
        ball = self.balls[ball_idx]
        ball.velocity = self.container.reflect_edge(ball.velocity, edge_idx)
        return self

    def ball_collision_update(self, ball1_idx, ball2_idx):
        # opdater hastighederne på bold ball1_idx og ball2_idx efter # deres kollision.Bemærk at der her bruges teorien om elastiske
        # kollisioner fra delopgave 4
        mass1 = self.balls[ball1_idx].mass
        position1 = self.balls[ball1_idx].position
        velocity1 = self.balls[ball1_idx].velocity

        mass2 = self.balls[ball2_idx].mass
        position2 = self.balls[ball2_idx].position
        velocity2 = self.balls[ball2_idx].velocity

        position_difference = position2 - position1
        velocity_difference = velocity2 - velocity1
        normal_vector = position_difference / np.linalg.norm(position_difference)
        projection = np.dot(velocity_difference, normal_vector) * normal_vector
        velocity1 = velocity1 + 2 * mass2 / (mass1 + mass2) * projection
        velocity2 = velocity2 - 2 * mass1 / (mass1 + mass2) * projection

        self.balls[ball1_idx].velocity = velocity1
        self.balls[ball2_idx].velocity = velocity2

        return self

    def get_velocities(self, idx):
        velocities = np.zeros((2, len(idx)))
        counter = 0
        for i in idx:
            velocities[:, counter] = self.balls[i].velocity
            counter += 1
        return velocities

    def get_positions_at_time_step(self, idx, dt):
        positions = np.zeros((2, len(idx)))
        counter = 0
        for i in idx:
            positions[:, counter] = self.balls[i].get_position_at_time_step(dt)
            counter += 1
        return positions

    def pass_through(self, x1, x2, u1, u2):
        # Funktion der undersøger om to bolde er passeret igennem
        # hinanden.Dette sker kun ved meget store hastigheder og små
        # bolde.Funktionen ser om der er en skæring i de to baner som
        # boldene følger.
        bool = 0
        sort1 = np.sort([x1, x2], axis=1)
        sort2 = np.sort([u1, u2], axis=1)
        x_min = sort1[1, 1]
        x_max = sort1[1, 2]
        y_min = sort1[2, 1]
        y_max = sort1[2, 2]
        u_min = sort2[1, 1]
        u_max = sort2[1, 2]
        v_min = sort2[2, 1]
        v_max = sort2[2, 2]

        x_min = max([x_min, u_min])
        x_max = min([x_max, u_max])
        y_min = max([y_min, v_min])
        y_max = min([y_max, v_max])

        slope1 = (x2[2] - x1[2]) / (x2[1] - x1[1])
        slope2 = (u2[2] - u1[2]) / (u2[1] - u1[1])

        if not slope1 == slope2:
            x = u1[2] - x1[2] + slope1 * x1[1] - slope2 * u1[1]
            y = slope1 * (x - x1[1]) + x1[2]
            if x_min <= x and x <= x_max and y_min <= y and y <= y_max:
                bool = 1
        return bool

    def get_radii(self, idx):
        radii = np.zeros(len(idx))
        counter = 0
        for i in idx:
            radii[counter] = self.balls[i].radius
            counter += 1
        return radii

    def ball_collisions(self, position, radius, positions, radii):
        # Algoritme til at afgøre om bolde er kollideret. Se også delopgave 1.
        if len(positions) == 0: collisions = 0
        else:
            print(positions, position)
            dists = np.linalg.norm(positions - position, axis=0)
            collisions = dists <= radii + radius
        return collisions

    def edge_collisions(self, position, radius):
        # Algoritme til at afgøre om en bold er kollideret med en kant.
        # Se også delopgave 2.
        dists = self.container.dist_to_boundary(position)
        collisions = abs(dists) < radius
        edge_idx = np.where(collisions > 0)[0]
        dists = dists(edge_idx)
        return [collisions, edge_idx, dists]

    def is_collision(self, position, radius, positions, radii):
        print(positions)
        if np.count_nonzero(
                self.ball_collisions(position, radius, positions, radii)) > 0 or \
            np.count_nonzero(self.edge_collisions(position, radius)) > 0:
            return 1
        return 0

    def rand_positions(self, n):
        random_numbers = np.vstack([
            np.random.uniform(low=self.container.minx, high=self.container.maxx, size=n),
            np.random.uniform(low=self.container.miny, high=self.container.maxy, size=n)
        ]).T
        return random_numbers

    def generate_positions_and_radii(self, option):
        # Algoritme til at generere boldenes initielle positioner og
        # radiier. Dette gøres med trial & error
        balls_generated = 0
        number_of_tries = 0
        print(self.nballs)
        positions = np.zeros((2, self.nballs))
        radii = np.zeros((1, self.nballs))
        max_r = 1 / self.nballs
        min_r = 1 / (10 * self.nballs)
        while balls_generated < self.nballs:
            position = self.rand_positions(1)
            if option == 'equal': radius = 0.5 * (min_r + max_r)
            else: radius = min_r + np.random.random() * (max_r - min_r)

            number_of_tries = number_of_tries + 1
            print(positions)
            print(balls_generated)
            if (not self.is_collision(position, radius, positions[:, :balls_generated],
                                      radii[:balls_generated])) and np.count_nonzero(
                    self.container.in_container(position)) > 0:
                positions[:, balls_generated] = position
                radii[balls_generated] = radius
                balls_generated = balls_generated + 1
                number_of_tries = 0

        masses = 10 * radii

        return [positions, radii, masses]

    def show_hide_text(self):
        if self.show_text == 1:
            self.text.visible = True
            for i in range(self.nballs):
                self.balls[i].text.visible = True

        else:
            self.text.visible = True
            for i in range(self.nballs):
                self.balls[i].text.visible = True

    def buttonpush(self, src, ed):
        # Håndterer keyboard input.
        if ed.key == 'q':           self.playing = 0
        elif ed.key == 'space':     self.paused = not self.paused
        elif ed.key == 'uparrow':   self.scale_velocities(2)
        elif ed.key == 'downarrow': self.scale_velocities(0.5)
        elif ed.key == 't':
            self.show_text = not self.show_text
            self.show_hide_text()