import time

import numpy as np
import random
from matplotlib import pyplot as plt



class Planet():
    pass
class G:
    playing = True
    planets = []
    patches = []
    xy_list = []

#fig = plt.figure(figsize=(10, 7))
ax = plt.gca()
g = G()

def main():
    # use a global structure to store all values that need to be
    # used in several different functions
    #global g

    t = 10000 * random.random()
    g.t = t

    get_settings()
    init_figure()
    create_ball()

    tic = time.time() # start timer
    while g.playing:

        if g.moving == 0:
            #tics
            #drawnow
            continue

        if g.moving == 1:
            dt = time.time() - tic # get time np.since last bounce
        else:
            dt = .01
            g.moving = 0

        # prevents updates of less than 1 / 20 of a second
        if dt < min(.05 / g.v, .05): continue

        tic = time.time() # reset timer

        t = t + g.v * dt

        # new position
        g.earthcx = 100.0000180000000 * np.cos(t) - 1.6731633011693
        g.earthcy = 99.9860196455882 * np.sin(t)

        g.halleycx = 1783.41442925537 * np.cos(t / 75.32) - 1724.8166181036783
        g.halleycy = 107.3639924082853 * np.sin(t / 75.32)

        g.mercurycx = 38.7098430000000 * np.cos(t / 0.240846) - 7.9601608881522
        g.mercurycy = 37.8825524974147 * np.sin(t / 0.240846)

        g.marscx = 152.3712430000000 * np.cos(t / 1.881) - 14.2261578635317
        g.marscy = 151.7056759841467 * np.sin(t / 1.881)

        g.jupitercx = 520.2480190000000 * np.cos(t / 11.86) - 25.2507058253821
        g.jupitercy = 519.6348748195645 * np.sin(t / 11.86)

        g.saturncx = 954.1498830000000 * np.cos(t / 29.46) - 52.9631902430348
        g.saturncy = 952.6788019622321 * np.sin(t / 29.46)

        g.uranuscx = 1918.7979479999999 * np.cos(t / 84.01) - 89.9098829686152
        g.uranuscy = 1916.6903188031135 * np.sin(t / 84.01)

        g.neptunecx = 3006.9527520000001 * np.cos(t / 164.8) - 26.9254276529813
        g.neptunecy = 3006.8321991933768 * np.sin(t / 164.8)

        g.venuscx = 72.3321020000000 * np.cos(t / 0.615) - 0.4892536146070
        g.venuscy = 72.3304473277955 * np.sin(t / 0.615)

        g.plutocx = 3948.6860350000001 * np.cos(t / 247.92065) - 982.06399176825134
        g.plutocy = 3824.4660013106305 * np.sin(t / 247.92065)

        update_graphics()

    print('Tak fordi du spillede!')

    return

def buttonpush(event):

    '''
    dv = 10
    if len(event.Modifier) > 0:
        dv = 1
    # shift, ctrl, alt all set dv = 1
    '''

    match event.key:
        case 'q':
            g.playing = 0
        case 'space':
            if g.moving:
                g.moving = 0
            else:
                g.moving = 1
        case 'tab':
            g.moving = 2
        case 'leftarrow':
            t = np.linspace(0, 2 * np.pi, 200)

            g.sunr = g.sunr / 2
            g.sunbx = g.sunr * np.cos(t)
            g.sunby = g.sunr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 20)
            g.earthr = g.earthr / 2
            g.earthbx = g.earthr * np.cos(t)
            g.earthby = g.earthr * np.sin(t)

            g.halleyr = g.halleyr / 2
            g.halleybx = g.halleyr * np.cos(t)
            g.halleyby = g.halleyr * np.sin(t)

            g.mercuryr = g.mercuryr / 2
            g.mercurybx = g.mercuryr * np.cos(t)
            g.mercuryby = g.mercuryr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 80)

            g.jupiterr = g.jupiterr / 2
            g.jupiterbx = g.jupiterr * np.cos(t)
            g.jupiterby = g.jupiterr * np.sin(t)

            g.saturnr = g.saturnr / 2
            g.saturnbx = g.saturnr * np.cos(t)
            g.saturnby = g.saturnr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 20)

            g.uranusr = g.uranusr / 2
            g.uranusbx = g.uranusr * np.cos(t)
            g.uranusby = g.uranusr * np.sin(t)

            g.neptuner = g.neptuner / 2
            g.neptunebx = g.neptuner * np.cos(t)
            g.neptuneby = g.neptuner * np.sin(t)

            g.marsr = g.marsr / 2
            g.marsbx = g.marsr * np.cos(t)
            g.marsby = g.marsr * np.sin(t)

            g.venusr = g.venusr / 2
            g.venusbx = g.venusr * np.cos(t)
            g.venusby = g.venusr * np.sin(t)

            g.plutor = g.plutor / 2
            g.plutobx = g.plutor * np.cos(t)
            g.plutoby = g.plutor * np.sin(t)

        case 'rightarrow':
            t = np.linspace(0, 2 * np.pi, 200)

            g.sunr = g.sunr * 2
            g.sunbx = g.sunr * np.cos(t)
            g.sunby = g.sunr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 20)
            g.earthr = g.earthr * 2
            g.earthbx = g.earthr * np.cos(t)
            g.earthby = g.earthr * np.sin(t)

            g.halleyr = g.halleyr * 2
            g.halleybx = g.halleyr * np.cos(t)
            g.halleyby = g.halleyr * np.sin(t)

            g.mercuryr = g.mercuryr * 2
            g.mercurybx = g.mercuryr * np.cos(t)
            g.mercuryby = g.mercuryr * np.sin(t)

            g.marsr = g.marsr * 2
            g.marsbx = g.marsr * np.cos(t)
            g.marsby = g.marsr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 80)

            g.jupiterr = g.jupiterr * 2
            g.jupiterbx = g.jupiterr * np.cos(t)
            g.jupiterby = g.jupiterr * np.sin(t)

            g.saturnr = g.saturnr * 2
            g.saturnbx = g.saturnr * np.cos(t)
            g.saturnby = g.saturnr * np.sin(t)

            t = np.linspace(0, 2 * np.pi, 20)

            g.uranusr = g.uranusr * 2
            g.uranusbx = g.uranusr * np.cos(t)
            g.uranusby = g.uranusr * np.sin(t)

            g.neptuner = g.neptuner * 2
            g.neptunebx = g.neptuner * np.cos(t)
            g.neptuneby = g.neptuner * np.sin(t)

            g.venusr = g.venusr * 2
            g.venusbx = g.venusr * np.cos(t)
            g.venusby = g.venusr * np.sin(t)

            g.plutor = g.plutor * 2
            g.plutobx = g.plutor * np.cos(t)
            g.plutoby = g.plutor * np.sin(t)

        case 'uparrow':
            g.xmax = g.xmax / 2
            g.ymax = g.ymax / 2
            set(g.text, 'Position', [.8 * g.xmax, g.ymax])
        case 'downarrow':
            g.xmax = 2 * g.xmax
            g.ymax = 2 * g.ymax
            set(g.text, 'Position', [.8 * g.xmax, g.ymax])
        case 'comma':
            g.v = g.v / 2
        case 'period':
            g.v = g.v * 2
        case 't':
            g.textvisible = g.textvisible + 1
        case _:
            print(f'{event.key=}') # show key info
    return

def get_settings():
    # p = { 'X-acceleration', 'Y-acceleration',
    # 'Restitutionskoefficient', 'Begyndelsesretning (0 til 360 grader)',
    # 'Begyndelsesvinkel (0 til 90 grader)', 'Begyndelseshastighed'
    # }
    # t = 'Hoppeboldspil'
    # d = {'0', '0', '1', '0', '0', '0'}
    # a = inputdlg(p, t, 1, d)
    # if length(a) == 0, error('Cancelled') end # user pushed close or cancel

    g.v = 1
    g.textvisible = 0

    # hardcoded values
    g.playing = g.moving = 1
    g.xmax, g.ymax = 4600, 3200

    g.earthcx = 100.0000180000000 * np.cos(g.t) - 1.6731633011693
    g.earthcy = 99.9860196455882 * np.sin(g.t)

    g.halleycx = 1783.41442925537 * np.cos(g.t / 75.32) - 1724.8166181036783
    g.halleycy = 107.3639924082853 * np.sin(g.t / 75.32)

    g.mercurycx = 38.7098430000000 * np.cos(g.t / 0.240846) - 7.9601608881522
    g.mercurycy = 37.8825524974147 * np.sin(g.t / 0.240846)

    g.marscx = 152.3712430000000 * np.cos(g.t / 1.881) - 14.2261578635317
    g.marscy = 151.7056759841467 * np.sin(g.t / 1.881)

    g.jupitercx = 520.2480190000000 * np.cos(g.t / 11.86) - 25.2507058253821
    g.jupitercy = 519.6348748195645 * np.sin(g.t / 11.86)

    g.saturncx = 954.1498830000000 * np.cos(g.t / 29.46) - 52.9631902430348
    g.saturncy = 952.6788019622321 * np.sin(g.t / 29.46)

    g.uranuscx = 1918.7979479999999 * np.cos(g.t / 84.01) - 89.9098829686152
    g.uranuscy = 1916.6903188031135 * np.sin(g.t / 84.01)

    g.neptunecx = 3006.9527520000001 * np.cos(g.t / 164.8) - 26.9254276529813
    g.neptunecy = 3006.8321991933768 * np.sin(g.t / 164.8)

    g.venuscx = 72.3321020000000 * np.cos(g.t / 0.615) - 0.4892536146070
    g.venuscy = 72.3304473277955 * np.sin(g.t / 0.615)

    g.plutocx = 3948.6860350000001 * np.cos(g.t / 247.92065) - 982.06399176825134
    g.plutocy = 3824.4660013106305 * np.sin(g.t / 247.92065)

    return

def create_ball():
    # create a 'ball'
    t = np.linspace(0, 2 * np.pi, 200)

    g.sunr = 696.340
    g.sunbx = g.sunr * np.cos(t)
    g.sunby = g.sunr * np.sin(t)

    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)

    #g.sunball = ax.add_patch((g.sunbx, g.sunby), 'y')
    #print((g.sunbx, g.sunby))
    #g.sunball = plt.Circle((g.sunbx, g.sunby), 0.15)
    #ax.add_patch(g.sunball)
    #g.suntext = plt.text(0, 0, "Solen")

    g.jupiterr = 69.911
    g.jupiterbx = g.jupiterr * np.cos(t)
    g.jupiterby = g.jupiterr * np.sin(t)
    #g.jupiterball = patch(g.jupiterbx, g.jupiterby, 'g')
    #g.jupitertext = plt.text(g.jupitercx, g.jupitercy, "Jupiter")

    # trace(tail)
    tlen = 500
    g.jupitertrace = Planet()
    g.jupitertrace.x = np.ones(tlen) * g.jupitercx
    g.jupitertrace.y = np.ones(tlen) * g.jupitercy
    #g.jupitertrace.h = plt.plot(g.jupitertrace.x, g.jupitertrace.y, 'b:')
    g.jupitertrace.visible = 'on'

    g.saturnr = 58.232
    g.saturnbx = g.saturnr * np.cos(t)
    g.saturnby = g.saturnr * np.sin(t)
    #g.saturnball = patch(g.saturnbx, g.saturnby, [0.7, 0, 0.7])
    #g.saturntext = plt.text(g.saturncx, g.saturncy, "Saturn")

    # trace(tail)
    tlen = 500
    g.saturntrace = Planet()
    g.saturntrace.x = np.ones(tlen) * g.saturncx
    g.saturntrace.y = np.ones(tlen) * g.saturncy
    #g.saturntrace.h = plt.plot(g.saturntrace.x, g.saturntrace.y, 'b:')
    g.saturntrace.visible = 'on'

    t = np.linspace(0, 2 * np.pi, 20)

    g.uranusr = 25.362
    g.uranusbx = g.uranusr * np.cos(t)
    g.uranusby = g.uranusr * np.sin(t)
    #g.uranusball = patch(g.uranusbx, g.uranusby, [0.7, 0.7, 0])
    #g.uranustext = plt.text(g.marscx, g.uranuscy, "Uranus")

    # trace(tail)
    tlen = 500
    g.uranustrace = Planet()
    g.uranustrace.x = np.ones(tlen) * g.uranuscx
    g.uranustrace.y = np.ones(tlen) * g.uranuscy
    #g.uranustrace.h = plt.plot(g.uranustrace.x, g.uranustrace.y, 'b:')
    g.uranustrace.visible = 'on'

    g.neptuner = 24.622
    g.neptunebx = g.neptuner * np.cos(t)
    g.neptuneby = g.neptuner * np.sin(t)
    #g.neptuneball = patch(g.neptunebx, g.neptuneby, [0, .7, .7])
    #g.neptunetext = plt.text(g.neptunecx, g.neptunecy, "Neptun")

    # trace(tail)
    tlen = 500
    g.neptunetrace = Planet()
    g.neptunetrace.x = np.ones(tlen) * g.neptunecx
    g.neptunetrace.y = np.ones(tlen) * g.neptunecy
    #g.neptunetrace.h = plt.plot(g.neptunetrace.x, g.neptunetrace.y, 'b:')
    g.neptunetrace.visible = 'on'

    t = np.linspace(0, 2 * np.pi, 20)
    g.earthr = 6.371
    g.earthbx = g.earthr * np.cos(t)
    g.earthby = g.earthr * np.sin(t)
    #g.earthball = patch(g.earthbx, g.earthby, 'b')
    print(g.earthcx, g.earthcy)
    g.earthball = plt.Circle((g.earthcx, g.earthcy), 100)
    #g.earthtext = plt.text(g.earthcx, g.earthcy, "Jorden")

    # trace(tail)
    tlen = 500
    g.earthtrace = Planet()
    g.earthtrace.x = np.ones(tlen) * g.earthcx
    g.earthtrace.y = np.ones(tlen) * g.earthcy
    #g.earthtrace.h = plt.plot(g.earthtrace.x, g.earthtrace.y, 'b:')
    g.earthtrace.visible = 'on'

    g.venusr = 6.0518
    g.venusbx = g.venusr * np.cos(t)
    g.venusby = g.venusr * np.sin(t)
    #g.venusball = patch(g.venusbx, g.venusby, [1, 0.4, 0.6])
    g.venusball = plt.Circle((g.venuscx, g.venuscy), 100)
    #g.venustext = plt.text(g.venuscx, g.venuscy, "Venus")

    # trace(tail)
    tlen = 50
    g.venustrace = Planet()
    g.venustrace.x = np.ones(tlen) * g.venuscx
    g.venustrace.y = np.ones(tlen) * g.venuscy
    #g.venustrace.h = plt.plot(g.venustrace.x, g.venustrace.y, 'b:')
    g.venustrace.visible = 'on'

    g.marsr = 3.3895
    g.marsbx = g.marsr * np.cos(t)
    g.marsby = g.marsr * np.sin(t)
    #g.marsball = patch(g.marsbx, g.marsby, 'r')
    #g.marstext = plt.text(g.marscx, g.marscy, "Mars")

    # trace(tail)
    tlen = 50
    g.marstrace = Planet()
    g.marstrace.x = np.ones(tlen) * g.marscx
    g.marstrace.y = np.ones(tlen) * g.marscy
    #g.marstrace.h = plt.plot(g.marstrace.x, g.marstrace.y, 'b:')
    g.marstrace.visible = 'on'

    g.mercuryr = 2.4397
    g.mercurybx = g.mercuryr * np.cos(t)
    g.mercuryby = g.mercuryr * np.sin(t)
    #g.mercuryball = patch(g.mercurybx, g.mercuryby, [.75, .75, .75])
    #g.mercurytext = plt.text(g.mercurycx, g.mercurycy, "Merkur")

    # trace(tail)
    tlen = 250
    g.mercurytrace = Planet()
    g.mercurytrace.x = np.ones(tlen) * g.mercurycx
    g.mercurytrace.y = np.ones(tlen) * g.mercurycy
    #g.mercurytrace.h = plt.plot(g.mercurytrace.x, g.mercurytrace.y, 'b:')
    g.mercurytrace.visible = 'on'

    t = np.linspace(0, 2 * np.pi, 80)

    g.plutor = 1.1883
    g.plutobx = g.plutor * np.cos(t)
    g.plutoby = g.plutor * np.sin(t)
    #g.plutoball = patch(g.plutobx, g.plutoby, [0.5, 0.5, 0.5])
    #g.plutotext = plt.text(g.plutocx, g.plutocy, "Pluto")

    # trace(tail)
    tlen = 50
    g.plutotrace = Planet()
    g.plutotrace.x = np.ones(tlen) * g.plutocx
    g.plutotrace.y = np.ones(tlen) * g.plutocy
    #g.plutotrace.h = plt.plot(g.plutotrace.x, g.plutotrace.y, 'b:')
    g.plutotrace.visible = 'on'

    g.halleyr = 0.011
    g.halleybx = g.halleyr * np.cos(t)
    g.halleyby = g.halleyr * np.sin(t)
    #g.halleyball = patch(g.halleybx, g.halleyby, 'b')
    #g.halleytext = plt.text(g.halleycx, g.halleycy, "Halleys komet")

    g.halleytrace = Planet()
    g.halleytrace.x = np.ones(tlen) * g.halleycx
    g.halleytrace.y = np.ones(tlen) * g.halleycy
    #g.halleytrace.h = plt.plot(g.halleytrace.x, g.halleytrace.y, 'b:')
    g.halleytrace.visible = 'on'

    return

def init_figure():
    # set up figure window
    # global g

    plt.axis('off')
    plt.title("Solsystemet")
    plt.axis([-g.xmax, g.xmax, -g.ymax, g.ymax])

    #set(gca, 'visible', 'off')
    #set(gca, 'xtick', [])
    # xt = get(gca, 'XTick')
    # yt = get(gca, 'YTick')
    # lx = xlim
    # ly = ylim
    # plot([xt, xt], lx(:) * np.ones(size(xt)), 'k')       # Plot X - Grid
    # plot(ly(:)*np.ones(size(yt)), [yt, yt], 'k')         # Plot Y - Grid
    # plot(xt(end) * ly(2) * [1, 1], yt(end) * lx(2) * [1, 1], 'k') # Plot Vertical Z - Axis Line
    # axis off
    # rectangle('Position', [0, 0, 0, g.xmax, g.ymax, g.zmax])
    # set the function that gets called when a key is pressed
    #set(gcf, 'WindowKeyPressFcn', @ buttonpush)
    #cid = fig.canvas.mpl_connect('key_press_event', buttonpush)
    #print(f'{cid=}')
    # instructions
    '''
    g.text = plt.text(
        .8 * g.xmax, g.ymax,
        {'q: afslut spillet',
         'mellemrum: pause/genoptag',
         'piletaster: skalér/zoom',
         't: tekster til/fra',
         'punktum/komma: hastighed op/ned'},
        'verticalalign', 'top')
    '''
    #g.text = plt.text(
    #    .8 * g.xmax, g.ymax,
    #    'q: afslut spillet \n mellemrum: pause/genoptag')
    # status text
    # g.stattext_h = text(-30, 90, 'Test', 'verticalalign', 'top')
    return

def update_graphics():

    # move ball to new position
    # set(g.ball, 'XData', g.earthbx + g.earthcx)
    # set(g.ball, 'YData', g.earthby + g.earthcy)
    # set(g.ball, 'ZData', g.bz + g.cz)
    #axis([-g.xmax, g.xmax, -g.ymax, g.ymax])
    #fig.(g.sunball, 'XData', g.sunbx, 'YData', g.sunby)
    #ax.add_patch(g.sunball)
    #ax.add_patch(plt.Circle((0.7, 0.2), 1))
    #print(g.earthcx, g.earthcy)
    ax.add_patch(g.earthball)
    ax.add_patch(g.venusball)
    '''

    set(g.earthball, 'XData', g.earthbx + g.earthcx, 'YData', g.earthby + g.earthcy)
    set(g.halleyball, 'XData', g.halleybx + g.halleycx, 'YData', g.halleyby + g.halleycy)
    set(g.mercuryball, 'XData', g.mercurybx + g.mercurycx, 'YData', g.mercuryby + g.mercurycy)
    set(g.marsball, 'XData', g.marsbx + g.marscx, 'YData', g.marsby + g.marscy)
    set(g.jupiterball, 'XData', g.jupiterbx + g.jupitercx, 'YData', g.jupiterby + g.jupitercy)
    set(g.saturnball, 'XData', g.saturnbx + g.saturncx, 'YData', g.saturnby + g.saturncy)
    set(g.uranusball, 'XData', g.uranusbx + g.uranuscx, 'YData', g.uranusby + g.uranuscy)
    set(g.neptuneball, 'XData', g.neptunebx + g.neptunecx, 'YData', g.neptuneby + g.neptunecy)
    set(g.venusball, 'XData', g.venusbx + g.venuscx, 'YData', g.venusby + g.venuscy)
    set(g.plutoball, 'XData', g.plutobx + g.plutocx, 'YData', g.plutoby + g.plutocy)

    set(g.earthtext, 'Position', [g.earthcx, g.earthcy])
    set(g.halleytext, 'Position', [g.halleycx, g.halleycy])
    set(g.mercurytext, 'Position', [g.mercurycx, g.mercurycy])
    set(g.marstext, 'Position', [g.marscx, g.marscy])
    set(g.jupitertext, 'Position', [g.jupitercx, g.jupitercy])
    set(g.saturntext, 'Position', [g.saturncx, g.saturncy])
    set(g.uranustext, 'Position', [g.uranuscx, g.uranuscy])
    set(g.neptunetext, 'Position', [g.neptunecx, g.neptunecy])
    set(g.venustext, 'Position', [g.venuscx, g.venuscy])
    set(g.plutotext, 'Position', [g.plutocx, g.plutocy])

    # update trace
    g.earthtrace.x = [g.earthcx, g.earthtrace.x(1:end - 1)]
    g.earthtrace.y = [g.earthcy, g.earthtrace.y(1:end - 1)]
    set(g.earthtrace.h, 'XData', g.earthtrace.x, 'YData', g.earthtrace.y)

    g.halleytrace.x = [g.halleycx, g.halleytrace.x(1:end - 1)]
    g.halleytrace.y = [g.halleycy, g.halleytrace.y(1:end - 1)]
    set(g.halleytrace.h, 'XData', g.halleytrace.x, 'YData', g.halleytrace.y)

    g.mercurytrace.x = [g.mercurycx, g.mercurytrace.x(1:end - 1)]
    g.mercurytrace.y = [g.mercurycy, g.mercurytrace.y(1:end - 1)]
    set(g.mercurytrace.h, 'XData', g.mercurytrace.x, 'YData', g.mercurytrace.y)

    g.marstrace.x = [g.marscx, g.marstrace.x(1:end - 1)]
    g.marstrace.y = [g.marscy, g.marstrace.y(1:end - 1)]
    set(g.marstrace.h, 'XData', g.marstrace.x, 'YData', g.marstrace.y)

    g.jupitertrace.x = [g.jupitercx, g.jupitertrace.x(1:end - 1)]
    g.jupitertrace.y = [g.jupitercy, g.jupitertrace.y(1:end - 1)]
    set(g.jupitertrace.h, 'XData', g.jupitertrace.x, 'YData', g.jupitertrace.y)

    g.saturntrace.x = [g.saturncx, g.saturntrace.x(1:end - 1)]
    g.saturntrace.y = [g.saturncy, g.saturntrace.y(1:end - 1)]
    set(g.saturntrace.h, 'XData', g.saturntrace.x, 'YData', g.saturntrace.y)

    g.uranustrace.x = [g.uranuscx, g.uranustrace.x(1:end - 1)]
    g.uranustrace.y = [g.uranuscy, g.uranustrace.y(1:end - 1)]
    set(g.uranustrace.h, 'XData', g.uranustrace.x, 'YData', g.uranustrace.y)

    g.neptunetrace.x = [g.neptunecx, g.neptunetrace.x(1:end - 1)]
    g.neptunetrace.y = [g.neptunecy, g.neptunetrace.y(1:end - 1)]
    set(g.neptunetrace.h, 'XData', g.neptunetrace.x, 'YData', g.neptunetrace.y)

    g.venustrace.x = [g.venuscx, g.venustrace.x(1:end - 1)]
    g.venustrace.y = [g.venuscy, g.venustrace.y(1:end - 1)]
    set(g.venustrace.h, 'XData', g.venustrace.x, 'YData', g.venustrace.y)

    g.plutotrace.x = [g.plutocx, g.plutotrace.x(1:end - 1)]
    g.plutotrace.y = [g.plutocy, g.plutotrace.y(1:end - 1)]
    set(g.plutotrace.h, 'XData', g.plutotrace.x, 'YData', g.plutotrace.y)

    if np.mod(g.textvisible, 2) == 1:
        set(g.suntext, 'Visible', 'off')
        set(g.earthtext, 'Visible', 'off')
        set(g.halleytext, 'Visible', 'off')
        set(g.mercurytext, 'Visible', 'off')
        set(g.marstext, 'Visible', 'off')
        set(g.jupitertext, 'Visible', 'off')
        set(g.saturntext, 'Visible', 'off')
        set(g.uranustext, 'Visible', 'off')
        set(g.neptunetext, 'Visible', 'off')
        set(g.venustext, 'Visible', 'off')
        set(g.plutotext, 'Visible', 'off')

    else:
        set(g.suntext, 'Visible', 'on')
        set(g.earthtext, 'Visible', 'on')
        set(g.halleytext, 'Visible', 'on')
        set(g.mercurytext, 'Visible', 'on')
        set(g.marstext, 'Visible', 'on')
        set(g.jupitertext, 'Visible', 'on')
        set(g.saturntext, 'Visible', 'on')
        set(g.uranustext, 'Visible', 'on')
        set(g.neptunetext, 'Visible', 'on')
        set(g.venustext, 'Visible', 'on')
        set(g.plutotext, 'Visible', 'on')
    '''

    # update display
    #print("update")
    #plt.draw()
    plt.pause(0.0001)
    #plt.clf()

    return

if __name__ == "__main__":
    #main()

    '''

    #https://stackoverflow.com/questions/60542734/animating-multiple-circles-in-orbit
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib import animation
    import random

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)

    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    patch1 = plt.Circle((5, -5), 0.75, fc='y')
    patch2 = plt.Circle((5, -5), 0.75, fc='y')

    patch_list = [patch1, patch2]
    angle = np.linspace(0, 2 * np.pi, 100)
    xy1 = np.array([np.cos(angle) * 2,
                    np.sin(angle) * 1]).T
    xy2 = np.array([np.cos(angle) * 1,
                    np.sin(angle) * 2]).T

    xy_list = [xy1, xy2] # Initialize all lists

    def init():
        for p in patch_list:
            ax.add_patch(p)
        return patch_list

    def animate(i):
        for p, xy in zip(patch_list, xy_list):
            p.set_center(xy[i])
        return patch_list

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=360,
                                   interval=20,
                                   blit=True)

    plt.show()
    '''
    # https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)

    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    g = G()

    # new position
    g.t = 10000 * random.random()

    earth = Planet()
    earth.cx = 100.0000180000000 * np.cos(g.t) - 1.6731633011693
    earth.cy = 99.9860196455882 * np.sin(g.t)
    earth.r = 6.371
    g.planets.append(earth)

    halley = Planet()
    halley.cx = 1783.41442925537 * np.cos(g.t / 75.32) - 1724.8166181036783
    halley.cy = 107.3639924082853 * np.sin(g.t / 75.32)
    halley.r = 0.011
    g.planets.append(halley)

    for planet in g.planets:
        t = np.linspace(0, 2 * np.pi, 80)
        bx, by = planet.r * np.cos(t), planet.r * np.sin(t)
        planet.xy = np.array([bx, by]).T

        patch = plt.Circle((planet.cx, planet.cy), .5)
        g.patches.append(patch)

    def init():
        for patch in g.patches:
            ax.add_patch(patch)
        return g.patches

    def animate(i):
        for patch, planet in zip(g.patches, g.planets):
            patch.set_center(planet.xy[i])
        return g.patches

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=80,
                                   repeat=True,
                                   interval=1,
                                   blit=True)
    plt.show()

    exit()

    # https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)

    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    g = G()

    # new position
    g.t = 10000 * random.random()

    g.earthcx = 100.0000180000000 * np.cos(g.t) - 1.6731633011693
    g.earthcy = 99.9860196455882 * np.sin(g.t)

    g.halleycx = 1783.41442925537 * np.cos(g.t / 75.32) - 1724.8166181036783
    g.halleycy = 107.3639924082853 * np.sin(g.t / 75.32)

    t = np.linspace(0, 2 * np.pi, 20)
    g.earthr = 6.371
    g.earthbx = g.earthr * np.cos(t)
    g.earthby = g.earthr * np.sin(t)
    g.earthb = np.array([g.earthbx, g.earthby]).T
    #g.earthball = patch(g.earthbx, g.earthby, 'b')
    earthball = plt.Circle((g.earthcx, g.earthcy), .5)
    g.planets.append(earthball)
    #g.xy_list.append(g.earthb)
    g.xy_list.append(g.earthr)

    t = np.linspace(0, 2 * np.pi, 20)
    g.halleyr = 0.011
    g.halleybx = g.halleyr * np.cos(t)
    g.halleyby = g.halleyr * np.sin(t)
    g.halleyb = np.array([g.halleybx, g.halleyby]).T
    halleyball = plt.Circle((g.halleycx, g.halleycy), .5)
    g.planets.append(halleyball)
    #g.xy_list.append(g.halleyb)
    g.xy_list.append(g.halleyr)
    #g.halleytext = plt.text(g.halleycx, g.halleycy, "Halleys komet")

    print(g.planets, g.xy_list)

    def init():
        for planet in g.planets:
            ax.add_patch(planet)
        return g.planets

    def animate(i):
        for planet, xy in zip(g.planets, g.xy_list):
            #planet.set_center(xy[i])
            planet.set_center((xy * np.cos(i), xy * np.sin(i)))
        return g.planets

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   interval=.1,
                                   blit=True,
                                   save_count=50)

    #fig = plt.figure(figsize=(10, 7))
    for i in range(10):
        axtest = plt.gca()
        axtest.add_patch(plt.Circle((0.7, 0.2), 0.15))
        axtest.add_patch(plt.Circle((0, 0), i/10))

        plt.draw()
        plt.pause(0.0001)
        plt.clf()