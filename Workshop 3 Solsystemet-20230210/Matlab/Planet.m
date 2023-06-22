classdef Planet <handle
    %PLANET Class. Based on the method of https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf

    properties
        name
        radius
        coordinates=[0;0];
        color
        resolution=200
        a           %halve storakse
        da          %ændring i halve storakse pr. århundrede
        e           %excentricitet
        de          %ændring i excentricitet pr. århundrede
        L           %middelbreddegrad
        dL          %ændring i middelbreddegrad pr. århundrede
        baromega    %breddegrad af periapsis
        dbaromega   %ændring i breddegrad af periapsis pr. århundrede
        t           %tid
        b           %parameter
        c           %parameter
        s           %parameter
        f           %parameter
        trace
        trace_length=200
        ball
        text
    end

    methods
        function obj=Planet(name,color,planet_data)
            %Constructer
            if nargin>0
                obj.name=name;
                obj.color=color;
                obj.radius=planet_data(1);
                obj.a=planet_data(2);
                obj.da=planet_data(3);
                obj.e=planet_data(4);
                obj.de=planet_data(5);
                obj.L=planet_data(6);
                obj.dL=planet_data(7);
                obj.baromega=planet_data(8);
                obj.dbaromega=planet_data(9);
                obj.b=planet_data(10);
                obj.c=planet_data(11);
                obj.s=planet_data(12);
                obj.f=planet_data(13);
             end
        end




        function obj=update(obj,t)
            %Method for calculating the position of the planet at time t.
            if (t<-3000 || t>3000)
                error('t must be in [-3000,3000] for the model to be accurate')
            end
            obj.t=t;
            %Convert t to the correct time relative to the Julian Ephemeris
            %Date:
            t=obj.time_converter(t);
            a=obj.a+obj.da*t;
            e=obj.e+obj.de*t;
            L=obj.L+obj.dL*t;
            baromega=obj.baromega+obj.dbaromega*t;
            %We calculate M from the available data
            M=L-baromega+obj.b*t^2+obj.c*cosd(obj.f*t)+obj.s*sind(obj.f*t);
            M=obj.mod_M(M);
            estar=180/pi*e;
            %Our initial guess in Newtons method
            E_0=M+estar*sind(M);
            %We apply Newtons method to find E(t).
            E=newtons_method(E_0,@(E) E-estar*sind(E)-M, @(E) 1-e*cosd(E),10^(-6));
            %We calculate the coordinates of the planet at time t.
            obj.coordinates=[a*(cosd(E)-e), a*sqrt(1-e^2)*sind(E)]';
            if isempty(obj.ball)
                obj.make_planet();
            else
                obj.update_planet();
            end
        end

        function circle=make_circle(obj)
            t=linspace(0,2*pi,obj.resolution);
            circle=obj.coordinates+obj.radius*[cos(t);sin(t)];
        end

        function obj=make_planet(obj)
            circle=obj.make_circle();
            obj.ball=patch(circle(1,:),circle(2,:),obj.color,'visible','off');
            obj.text=text(obj.coordinates(1),obj.coordinates(2),obj.name);
            trace=obj.coordinates.*ones(2,obj.trace_length);
            obj.trace=plot(trace(1,:),trace(2,:));
        end

        function obj=update_planet(obj,d)
            circle=obj.make_circle();
            set(obj.ball, 'XData', circle(1,:),'YData',circle(2,:),'Visible','off')
            set(obj.text, 'Position', [obj.coordinates(1),obj.coordinates(2)]);
            set(obj.trace, 'XData', [obj.coordinates(1) obj.trace.XData(1:end-1)],'YData', [obj.coordinates(2) obj.trace.YData(1:end-1)]);
        end

        function t=time_converter(obj,t)
            %Method for converting t to Julian Ephemeris Date and then to
            %centuries past J2000.0.  This is because of the available data.
            t=(2816788-625674)*(t+3001)/(3000+3001)+625674;
            t= (t-2451545)/36525;
        end

        function M=mod_M(obj,M)
            %Convert M to a value between -180 deg and 180 deg.
            M=mod(M,360)-(mod(M,360)>=180)*360;
        end

    end
end

