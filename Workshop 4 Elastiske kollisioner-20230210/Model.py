import time

from Ball import *
from Container import Container
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

        fig, ax = plt.subplots()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        self.fig, self.ax = fig, ax

        self.container = Container(ngon, self.ax)
        self.nballs = nballs
        self.balls = self.make_balls(nballs, option)
        # set(gcf, 'WindowKeyPressFcn', @ self.buttonpush)
        self.text = plt.text(0.4, 1,
                             'q: afslut\n'
                             'mellemrum: pause/genoptag\n'
                             'piletaster op/ned: skalér hastighed\n'
                             't: tekster til/fra', verticalalignment='top')

    def make_balls(self, nballs, option):
        # tilfældig generation af et antal bolde.
        balls = [None] * nballs  # balls = cell(1, nballs)
        # Generer hastighederne
        velocities = np.random.uniform(low=-5, high=5, size=(2, nballs))
        print(velocities)
        # Generer boldene, med radius og proportionelle masser:
        [positions, radii, masses] = self.generate_positions_and_radii(option)
        for i in range(nballs):
            balls[i] = Ball(
                masses[i], radii[i], velocities[:, i],
                positions[:, i], 'b', str(i), self.ax)
        return balls

    def run(self):
        # Kør modellen.
        self.playing = 1
        while self.playing == 1:
            if self.paused:
                time.sleep(0.01)
                continue

            self.update(self.dt)
            self.fig.canvas.draw()

    def update(self, t):
        # Opdater modellen frem til tiden t.
        # Dette kan lave yderligere af tidstrinnet
        # t afhængigt af antallet af kollisioner.
        new_time = self.collision_detection(t)
        self.update_positions(new_time)
        plt.pause(t)

    def update_positions(self, t):
        for ball in self.balls:
            ball.update_position(t)

    def scale_velocities(self, scale):
        for ball in self.balls:
            ball.velocity = ball.velocity * scale

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
        pass_through = False
        for i in range(self.nballs - 1):
            for j in range(i + 1, self.nballs):
                x1, x2 = self.balls[i].position.reshape((2,)), positions[:, i]
                u1, u2 = self.balls[j].position.reshape((2,)), positions[:, j]
                if self.pass_through(x1, x2, u1, u2):
                    pass_through = True
                    break
            if pass_through:
                break

        in_container = self.container.in_container(positions)
        zero_in_container = np.count_nonzero(in_container) < self.nballs
        if zero_in_container or pass_through:
            new_time = self.collision_detection(new_time / 2)

        else:
            # Hvis ikke overnævnte tilfælde sker kan vi bestemme
            # kollisionerne og finde den første.
            for i in range(self.nballs):
                position = positions[:, i].reshape((2, 1))
                radius = radii[i]
                velocity = velocities[:, i].reshape((2, 1))

                if i < self.nballs:
                    remaining_positions = positions[:, i + 1: self.nballs]
                    remaining_radii = self.get_radii(range(i + 1, self.nballs))
                    ball_collisions = self.ball_collisions(position, radius, remaining_positions, remaining_radii)
                else:
                    ball_collisions = 0

                # Hvis der er bolde der kolliderer udregner vi de eksakte tidspunkter.
                n_collisions = np.count_nonzero(ball_collisions)
                if n_collisions > 0:
                    ball_idx = i + np.flatnonzero(ball_collisions)
                    print(f'{positions=}')
                    print(f'{position=}')
                    print(f'{velocities=}')
                    print(f'{velocity=}')
                    u = positions[:, ball_idx] - position.reshape((2,))
                    v = velocities[:, ball_idx] - velocity.reshape((2,))
                    print(f'{u=}')
                    print(f'{v=}')
                    u = u.reshape((2,1))
                    v = v.reshape((2,1))
                    udotv = np.dot(u.T, v)
                    vv = np.dot(v.T, v)
                    uu = np.dot(u.T, u)
                    print(f'{udotv=}')
                    print(f'{vv=}')
                    print(f'{uu=}')
                    r = radii[ball_idx] + radius
                    d = np.sqrt(udotv ** 2 - vv * (uu - r ** 2))
                    time_of_collisions = dt - (udotv + d) / vv
                    # [time, idx] = min(time_of_collisions)
                    time = min(time_of_collisions)
                    if time < first_collision[2]:
                        first_collision = [i, ball_idx, time]
                        # first_collision = [i, ball_idx[idx], time]

                # Vi udregner de eksakte tidspunkter for kollisioner med beholderen.
                [edge_collisions, edge_idx, edge_dists] = self.edge_collisions(position, radius)
                n_collisions = np.count_nonzero(edge_collisions)

                if n_collisions > 0:
                    n = self.container.normals[:, edge_idx].reshape((2, 1))
                    vel = np.tile(velocity, (n[0].size, 1)).reshape((2, 1)).T
                    time_of_collisions = dt - (edge_dists + radius) / np.dot(n, vel).flatten()
                    time = min(time_of_collisions)
                    idx = np.where(time_of_collisions == time)
                    if time < first_collision[2]:
                        first_collision = [i, -edge_idx, time]
                        # first_collision = [i, -edge_idx[idx], time]

            print(f'{first_collision=}')
            # Updater positionerne til første kollision og opdater hastighedvektorerne for de involverede selfekter.
            if first_collision[2] < dt:
                self.update_positions(first_collision[2])
                if first_collision[1] > 0:
                    self.ball_collision_update(first_collision[0], first_collision[1])
                else:
                    self.edge_collision_update(first_collision[0], -first_collision[1])
                new_time = dt - first_collision[2]

                # Test for flere kollisioner i den restee tid af tidstrinnet.
                new_time = self.collision_detection(new_time)

        return new_time

    def edge_collision_update(self, ball_idx, edge_idx):
        # opdater bold nr ball_idx hastighedsvektor efter kollision
        # med kant edge_idx.Her anes reflektioner fra delopgave 4, # se mere i filen Container.m
        ball: Ball = self.balls[ball_idx]
        ball.velocity = ball.velocity.reshape((2, 1))
        ball.velocity = self.container.reflect_edge(ball.velocity, edge_idx)
        return self

    def ball_collision_update(self, ball1_idx, ball2_idx):
        # opdater hastighederne på bold ball1_idx og ball2_idx efter # deres kollision.Bemærk at der her bruges teorien om elastiske
        # kollisioner fra delopgave 4

        mass1 = self.balls[ball1_idx].mass
        position1 = self.balls[ball1_idx].position
        velocity1 = self.balls[ball1_idx].velocity.reshape((2,1))

        mass2 = self.balls[ball2_idx].mass
        position2 = self.balls[ball2_idx].position
        velocity2 = self.balls[ball2_idx].velocity.reshape((2,1))

        position_difference = position2 - position1
        velocity_difference = velocity2 - velocity1
        normal_vector = position_difference / np.linalg.norm(position_difference)
        projection = np.dot(velocity_difference, normal_vector) * normal_vector
        velocity1 = velocity1 + 2 * mass2 / (mass1 + mass2) * projection
        velocity2 = velocity2 - 2 * mass1 / (mass1 + mass2) * projection

        # TODO: Check why velocity becomes (2, 2) and not (2, 1)
        print(f'{velocity1=}')
        print(f'{velocity2=}')
        self.balls[ball1_idx].velocity = velocity1.reshape((2,))
        self.balls[ball2_idx].velocity = velocity2.reshape((2,))

        return self

    def get_velocities(self, idx):
        velocities = np.zeros((2, len(idx)))
        counter = 0
        for i in idx:
            velocities[:, counter] = self.balls[i].velocity
            counter += 1
        return velocities

    def get_positions_at_time_step(self, idx, dt):
        positions = np.zeros((2, len(idx))).reshape(2, len(idx))
        for counter in idx:
            ball: Ball = self.balls[counter]
            positions[:, counter] = ball.get_position_at_time_step(dt)
        return positions

    def pass_through(self, x1, x2, u1, u2):
        # Funktion der undersøger om to bolde er passeret igennem
        # hinanden.Dette sker kun ved meget store hastigheder og små
        # bolde.Funktionen ser om der er en skæring i de to baner som
        # boldene følger.
        bool = 0
        sort1 = np.sort([x1, x2], axis=1)
        sort2 = np.sort([u1, u2], axis=1)
        x_min = sort1[0, 0]
        x_max = sort1[0, 1]
        y_min = sort1[1, 0]
        y_max = sort1[1, 1]
        u_min = sort2[0, 0]
        u_max = sort2[0, 1]
        v_min = sort2[1, 0]
        v_max = sort2[1, 1]

        x_min = max([x_min, u_min])
        x_max = min([x_max, u_max])
        y_min = max([y_min, v_min])
        y_max = min([y_max, v_max])

        slope1 = (x2[1] - x1[1]) / (x2[0] - x1[0])
        slope2 = (u2[1] - u1[1]) / (u2[0] - u1[0])

        if not slope1 == slope2:
            x = u1[1] - x1[1] + slope1 * x1[0] - slope2 * u1[0]
            y = slope1 * (x - x1[0]) + x1[1]
            if x_min <= x and x <= x_max and \
                    y_min <= y and y <= y_max:
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
        if len(positions) == 0:
            collisions = 0
        else:
            position = np.reshape(position, (2, 1))
            dists = np.linalg.norm(positions - position, axis=0)
            # print(dists)
            # print(radii)
            # print(radius)
            # print(dists, radii + radius)
            # print(dists <= radii + radius)
            # print()
            collisions = dists <= radii + radius
            # print(f'{collisions=}')
        return collisions

    def edge_collisions(self, position, radius):
        # Algoritme til at afgøre om en bold er kollideret med en kant.
        # Se også delopgave 2.
        dists, _ = self.container.dist_to_boundary(position)
        collisions = np.absolute(dists) < radius
        edge_idx = np.where(collisions == True)[0]
        if len(edge_idx) > 0:
            edge_idx = edge_idx[0]
        dists = dists[edge_idx]
        return [collisions, edge_idx, dists]

    def is_collision(self, position, radius, positions, radii):
        d0 = self.ball_collisions(position, radius, positions, radii)
        d1 = np.count_nonzero(d0) > 0
        w0 = self.edge_collisions(position, radius)[0]
        w1 = np.count_nonzero(w0) > 0
        return 1 if d1 or w1 else 0

    def rand_positions(self, n):
        random_numbers = np.vstack([
            np.random.uniform(low=self.container.minx, high=self.container.maxx, size=n),
            np.random.uniform(low=self.container.miny, high=self.container.maxy, size=n)
        ])
        return random_numbers

    def generate_positions_and_radii(self, option):
        # Algoritme til at generere boldenes initielle positioner og
        # radiier. Dette gøres med trial & error
        balls_generated = 0
        number_of_tries = 0
        positions = np.zeros((2, self.nballs))
        radii = np.zeros(self.nballs)
        max_r = 1 / self.nballs
        min_r = 1 / (10 * self.nballs)
        while balls_generated < self.nballs:
            position = self.rand_positions(1)
            if option == 'equal':
                radius = 0.5 * (min_r + max_r)
            else:
                radius = min_r + np.random.random() * (max_r - min_r)

            number_of_tries = number_of_tries + 1
            t0 = not self.is_collision(position, radius, positions[:, :balls_generated], radii[:balls_generated])
            g2 = self.container.in_container(position)
            g0 = np.count_nonzero(g2) > 0
            if t0 and g0:
                positions[:, balls_generated] = position.T
                radii[balls_generated] = radius
                balls_generated = balls_generated + 1
                number_of_tries = 0

        masses = 10 * radii

        return [positions, radii, masses]

    def show_hide_text(self):
        if self.show_text == 1:
            self.text.visible = True
            for ball in self.balls:
                ball.text.visible = True

        else:
            self.text.visible = True
            for ball in self.balls:
                ball.text.visible = True

    def buttonpush(self, src, ed):
        # Håndterer keyboard input.
        if ed.key == 'q':
            self.playing = 0
        elif ed.key == 'space':
            self.paused = not self.paused
        elif ed.key == 'uparrow':
            self.scale_velocities(2)
        elif ed.key == 'downarrow':
            self.scale_velocities(0.5)
        elif ed.key == 't':
            self.show_text = not self.show_text
            self.show_hide_text()

if __name__ == "__main__":
    pass