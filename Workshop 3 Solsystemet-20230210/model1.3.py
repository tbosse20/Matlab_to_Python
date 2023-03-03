import time, random
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html


class Planet:
    def __init__(self, name, ax, addx, ay, addy, movement, r, res, color):
        self.name = name
        self.ax = ax
        self.kx = addx
        self.ay = ay
        self.ky = addy
        self.movement = movement
        self.r = r
        self.res = res
        self.color = color


class System:
    t = 10000 * random.random()
    ax = plt.gca()
    anim = fig = info = None
    tic = time.time()  # reset timer

    planets = [
        Planet("Sun", 1, 0, 1, 0, 1, 696.340, 80, "yellow"),
        Planet("Earth", 100.0000180000000, -1.6731633011693, 99.9860196455882, 0, 1, 6.371, 80, "blue"),
        Planet("Halley", 1783.41442925537, -1724.8166181036783, 107.3639924082853, 0, 75.32, 0.011, 80, "blue"),
        Planet("Mercury", 38.7098430000000, -7.9601608881522, 37.8825524974147, 0, 0.240846, 2.4397, 80, [0.75, 0.75, 0.75]),
        Planet("Mars", 152.3712430000000, -14.2261578635317, 151.7056759841467, 0, 1.881, 3.3895, 80, "red"),
        Planet("Jupiter", 520.2480190000000, -25.2507058253821, 519.6348748195645, 0, 11.86, 69.911, 80, "red"),
        Planet("Saturn", 954.1498830000000, -52.9631902430348, 952.6788019622321, 0, 29.46, 58.232, 80, [0.7, 0.0, 0.7]),
        Planet("Uranus", 1918.7979479999999, -89.9098829686152, 1916.6903188031135, 0, 84.01, 25.362, 80, [0.7, 0.7, 0.0]),
        Planet("Neptune", 3006.9527520000001, -26.9254276529813, 3006.8321991933768, 0, 164.8, 24.622, 80, [0.0, 0.7, 0.7]),
        Planet("Venus", 72.3321020000000, -0.4892536146070, 72.3304473277955, 0, 0.615, 6.0518, 80, [1.0, 0.4, 0.6]),
        Planet("Pluto", 3948.6860350000001, -982.06399176825134, 3824.4660013106305, 0, 247.92065, 1.1883, 80, [0.5, 0.5, 0.5])
    ]

    v = textvisible = playing = moving = 1
    xmax, ymax = 4600, 3200
    trace_visible = 'on'
    tlen = 500


# Use a global structure to store all values that need to be
# used in several different functions
system = System()


def main():
    update_cx_cy(system.t)
    init_figure()
    create_elements()
    system.anim = animation.FuncAnimation(system.fig, update_graphics, interval=30, cache_frame_data=False)
    plt.show()
    print('Tak fordi du spillede!')


def btn(event):
    size = zoom = 1

    match event.key:

        case ' ':
            system.moving = 1 - system.moving
            if system.moving: system.anim.resume()
            else: system.anim.pause()

        case 'up':      zoom = 0.5
        case 'down':    zoom = 2
        case 'q':       exit()
        case 'tab':     system.moving = 2
        case 'left':    size = 0.5
        case 'right':   size = 2
        case ',':       system.v *= 0.5
        case '.':       system.v *= 2
        case 't':       system.textvisible = 1 - system.textvisible
        case _:         print(f'{event.key=}')  # show key info

    if event.key == "up" or event.key == "down":
        system.xmax *= zoom
        system.ymax *= zoom
        system.ax.set_xlim([-system.xmax, system.xmax])
        system.ax.set_ylim([-system.ymax, system.ymax])
        system.info.set_position([-system.xmax, -system.ymax])

    if event.key == 'left' or event.key == 'right':
        for planet in system.planets:
            planet.r *= size
            ball = create_ball(planet)
            planet.patch.set_xy(ball)


def update_cx_cy(t):
    for planet in system.planets:
        movement = planet.movement
        planet.cx = planet.ax * np.cos(t / movement) + planet.kx
        planet.cy = planet.ay * np.sin(t / movement) + planet.ky


def create_ball(planet):
    t = np.linspace(0, 2 * np.pi, planet.res)
    planet.bx = planet.r * np.cos(t)
    planet.by = planet.r * np.sin(t)
    ball = np.array([planet.bx, planet.by]).T

    return ball


def create_elements():
    # Create each 'ball', 'trace', and 'text'
    for planet in system.planets:

        # Create 'ball'
        ball = create_ball(planet)
        patch = patches.Polygon(ball, color=planet.color)
        planet.patch = patch
        system.ax.add_patch(patch)

        # Create 'trace'
        planet.tx, planet.ty = np.ones(system.tlen) * planet.cx, np.ones(system.tlen) * planet.cy
        trace, = system.ax.plot(planet.tx, planet.ty, 'b:')
        planet.trace = trace

        # Create 'text'
        label = system.ax.text(planet.cx, planet.cy, planet.name)
        planet.label = label


def init_figure():

    # Set up figure window
    system.fig = plt.figure()
    system.ax = plt.axes(xlim=(-system.xmax, system.xmax), ylim=(-system.ymax, system.ymax))
    plt.title("Solsystemet")
    plt.axis('off')
    system.fig.canvas.mpl_connect('key_press_event', btn) # Set the function that gets called when a key is pressed

    # Instructions
    system.info = system.ax.text(
        -system.xmax, -system.ymax,
        'q: afslut spillet \n'
        'mellemrum: pause/genoptag \n'
        'piletaster: skalér/zoom \n'
        't: tekster til/fra \n'
        'komma/punktum: hastighed ned/op')


def update_graphics(i):
    dt = time.time() - system.tic  # get time since last bounce
    system.t = system.t + system.v * dt
    update_cx_cy(system.t)

    # Iterate each planet
    for planet in system.planets:

        # Update 'ball' position
        ball = np.array([planet.bx + planet.cx, planet.by + planet.cy]).T
        planet.patch.set_xy(ball)

        # Update 'trace' position
        planet.tx = np.insert(planet.tx[:-1], 0, planet.cx, axis=0)
        planet.ty = np.insert(planet.ty[:-1], 0, planet.cy, axis=0)
        planet.trace.set_data(planet.tx, planet.ty)

        # Update 'text'
        planet.label.set_position([planet.cx, planet.cy])
        planet.label.set_visible(system.textvisible)

if __name__ == "__main__":
    main()
