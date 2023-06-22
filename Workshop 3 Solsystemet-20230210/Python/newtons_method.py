def newtons_method(x_0, f, df, tol):
    x_old = x_0
    while 1:
        x_new = x_old - f(x_old) / df(x_old)
        if abs(x_old - x_new) < tol: break
        x_old=x_new
    return x_new