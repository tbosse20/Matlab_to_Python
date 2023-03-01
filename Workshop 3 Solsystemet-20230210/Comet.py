classdef Comet <handle
    # COMET Class. Uses the data from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr=1P
properties
        name
        radius
        coordinates = [0, 0]
        color
        resolution = 200
        a           # halve storakse
        da          # ændring i halve storakse pr. århundrede
        e           # excentricitet
        de          # ændring i excentricitet pr. århundrede
        M_0
        t_0
        n
        t           # tid
        trace
        trace_length = 200
        ball
        text
    end