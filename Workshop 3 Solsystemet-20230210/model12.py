import time, random
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# TODO

# https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html

class G:
    pass

# Use a global structure to store all values that need to be
# used in several different functions
g = G()
g.ax = plt.gca()


def main():
    g.t = 10000 * random.random()

    get_settings(g.t)
    update_cx_cy(g.t)
    init_figure()
    create_balls()
    g.tic = time.time()  # reset timer

    def update_graphics(i):

        dt = time.time() - g.tic    # get time since last bounce
        g.t = g.t + g.v * dt
        update_cx_cy(g.t)

        # Iterate each planet
        for planet in g.planets.values():

            # Get planet attributes
            cx, cy = planet["cx"], planet["cy"]
            bx, by = planet["bx"], planet["by"]
            tx, ty = planet["tx"], planet["ty"]

            # Update 'ball' position
            b = np.array([bx + cx, by + cy]).T
            planet["patch"].set_xy(b)

            # Update 'trace' position
            tx = np.insert(tx[:-1], 0, cx, axis=0)
            ty = np.insert(ty[:-1], 0, cy, axis=0)
            planet["tx"], planet["ty"] = tx, ty
            planet["trace"].set_data(tx, ty)

            # Update 'text'
            planet["label"].set_position([cx, cy])
            planet["label"].set_visible(g.textvisible)

    g.anim = animation.FuncAnimation(
        g.fig, update_graphics,
        interval=30, cache_frame_data=False)

    plt.show()

    print('Tak fordi du spillede!')


def buttonpush(event):

    size = zoom = 1

    match event.key:

        case ' ':
            g.moving = 1 - g.moving
            if g.moving: g.anim.resume()
            else: g.anim.pause()

        case 'up':      zoom = 0.5
        case 'down':    zoom = 2
        case 'q':       exit()
        case 'tab':     g.moving = 2
        case 'left':    size = 0.5
        case 'right':   size = 2
        case ',':       g.v *= 0.5
        case '.':       g.v *= 2
        case 't':       g.textvisible = 1 - g.textvisible
        case _:         print(f'{event.key=}')  # show key info

    if event.key == "up" or event.key == "down":
        g.xmax *= zoom
        g.ymax *= zoom
        g.ax.set_xlim([-g.xmax, g.xmax])
        g.ax.set_ylim([-g.ymax, g.ymax])
        g.info.set_position([-g.xmax, -g.ymax])

    if event.key == 'left' or event.key == 'right':
        for planet in g.planets.values():
            planet["r"] *= size
            b = create_ball(planet)
            planet["patch"].set_xy(b)


def get_settings(t):

    # Hardcoded values
    g.v = g.textvisible = g.playing = g.moving = 1
    g.xmax, g.ymax = 4600, 3200
    g.trace_visible = 'on'
    g.tlen = 500

    g.planets = {
        "Sun": {
            "ax": 1,                    "addx": 0,
            "ay": 1,                    "addy": 0,
            "speed": 1,                 "r": 696.340,
            "res": 80,                  "color": "yellow",

        }, "Earth": {
            "ax": 100.0000180000000,    "addx": -1.6731633011693,
            "ay": 99.9860196455882,     "addy": 0,
            "speed": 1,                 "r": 6.371,
            "res": 80,                  "color": "blue",

        }, "Halley": {
            "ax": 1783.41442925537,     "addx": -1724.8166181036783,
            "ay": 107.3639924082853,    "addy": 0,
            "speed": 75.32,             "r": 0.011,
            "res": 80,                  "color": "blue",

        }, "Mercury": {
            "ax": 38.7098430000000,     "addx": -7.9601608881522,
            "ay": 37.8825524974147,     "addy": 0,
            "speed": 0.240846,          "r": 2.4397,
            "res": 80,                  "color": [0.75, 0.75, 0.75],

        }, "Mars": {
            "ax": 152.3712430000000,    "addx": -14.2261578635317,
            "ay": 151.7056759841467,    "addy": 0,
            "speed": 1.881,             "r": 3.3895,
            "res": 80,                  "color": "red",

        }, "Jupiter": {
            "ax": 520.2480190000000,    "addx": -25.2507058253821,
            "ay": 519.6348748195645,    "addy": 0,
            "speed": 11.86,             "r": 69.911,
            "res": 80,                  "color": "red",

        }, "Saturn": {
            "ax": 954.1498830000000,    "addx": -52.9631902430348,
            "ay": 952.6788019622321,    "addy": 0,
            "speed": 29.46,             "r": 58.232,
            "res": 80,                  "color": [0.7, 0.0, 0.7],

        }, "Uranus": {
            "ax": 1918.7979479999999,   "addx": -89.9098829686152,
            "ay": 1916.6903188031135,   "addy": 0,
            "speed": 84.01,             "r": 25.362,
            "res": 80,                  "color": [0.7, 0.7, 0.0],

        }, "Neptune": {
            "ax": 3006.9527520000001,   "addx": -26.9254276529813,
            "ay": 3006.8321991933768,   "addy": 0,
            "speed": 164.8,             "r": 24.622,
            "res": 80,                  "color": [0.0, 0.7, 0.7],

        }, "Venus": {
            "ax": 72.3321020000000,     "addx": -0.4892536146070,
            "ay": 72.3304473277955,     "addy": 0,
            "speed": 0.615,             "r": 6.0518,
            "res": 80,                  "color": [1.0, 0.4, 0.6],

        }, "Pluto": {
            "ax": 3948.6860350000001,   "addx": -982.06399176825134,
            "ay": 3824.4660013106305,   "addy": 0,
            "speed": 247.92065,         "r": 1.1883,
            "res": 80,                  "color": [0.5, 0.5, 0.5],
        }
    }

def update_cx_cy(t):
    for planet in g.planets.values():
        ax, addx = planet["ax"], planet["addx"]
        ay, addy = planet["ay"], planet["addy"]
        speed = planet["speed"]
        planet["cx"] = ax * np.cos(t / speed) + addx
        planet["cy"] = ay * np.sin(t / speed) + addy

def create_ball(planet):
    t = np.linspace(0, 2 * np.pi, planet["res"])
    r = planet["r"]
    planet["bx"] = bx = r * np.cos(t)
    planet["by"] = by = r * np.sin(t)
    b = np.array([bx, by]).T

    return b

def create_balls():

    # Create each 'ball', 'trace', and 'text'
    for name, planet in g.planets.items():

        # Create 'ball'
        b = create_ball(planet)
        patch = patches.Polygon(b, color=planet["color"])
        planet["patch"] = patch
        g.ax.add_patch(patch)

        # Create 'trace'
        cx, cy = planet["cx"], planet["cy"]
        tx, ty = np.ones(g.tlen) * cx, np.ones(g.tlen) * cy
        planet["tx"], planet["ty"] = tx, ty
        trace, = g.ax.plot(tx, ty, 'b:')
        planet["trace"] = trace

        # Create 'text'
        label = g.ax.text(cx, cy, name)
        planet["label"] = label

def init_figure():

    # Set up figure window
    g.fig = plt.figure()
    g.fig.set_dpi(100)
    g.fig.set_size_inches(7, 7)

    g.playing = g.moving = 1
    g.xmax, g.ymax = 4600, 3200
    g.ax = plt.axes(xlim=(-g.xmax, g.xmax), ylim=(-g.ymax, g.ymax))
    plt.title("Solsystemet")
    plt.axis('off')

    # Set the function that gets called when a key is pressed
    cid = g.fig.canvas.mpl_connect('key_press_event', buttonpush)

    # Instructions
    g.info = g.ax.text(
        -g.xmax, -g.ymax,
        'q: afslut spillet \n'
        'mellemrum: pause/genoptag \n'
        'piletaster: skalér/zoom \n'
        't: tekster til/fra \n'
        'komma/punktum: hastighed ned/op')

if __name__ == "__main__":
    main()
