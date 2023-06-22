classdef Comet <handle
    %COMET Class. Uses the data from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr=1P
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
        M_0
        t_0
        n
        t           %tid
        trace      
        trace_length=200
        ball
        text
    end
    
    methods 
        function obj=Comet(name,color,comet_data)
            %Constructor
            nargin
            if nargin>0
                obj.name=name;
                obj.color=color;
                obj.radius=comet_data(1);
                obj.a=comet_data(2);
                obj.e=comet_data(3);
                obj.M_0=comet_data(4);
                obj.t_0=comet_data(5);
                obj.n=comet_data(6);
             end
        end
               
        
        function obj=update(obj,t)
            %method for calculating the comets position at time t.
            if (t<-3000 || t>3000)
                error('t must be in [-3000,3000]') 
            end
            obj.t=t;
            %Convert t to the correct time relative to the Julian Ephemeris
            %Date:
            t=obj.time_converter(t);   
            %Calculate M from the available data
            M=obj.M_0+obj.n*(t-obj.t_0);
            M=obj.mod_M(M);
            estar=180/pi*obj.e;
            %Calculate initial guess for Newtons method
            E_0=M+estar*sind(M);
            %Apply Newtons method
            E=newtons_method(E_0,@(E) E-estar*sind(E)-M, @(E) 1-obj.e*cosd(E),10^(-6));
            %Update coordinates.
            obj.coordinates=[obj.a*(cosd(E)-obj.e), obj.a*sqrt(1-obj.e^2)*sind(E)]';
            if isempty(obj.ball)
                obj.make_ball();
            else
                obj.update_ball();
            end
        end
        
        function circle=make_circle(obj)
            t=linspace(0,2*pi,obj.resolution);
            circle=obj.coordinates+obj.radius*[cos(t);sin(t)];
        end
        
        function obj=make_ball(obj)
            circle=obj.make_circle();
            obj.ball=patch(circle(1,:),circle(2,:),obj.color,'visible','off');
            obj.text=text(obj.coordinates(1),obj.coordinates(2),obj.name);
            trace=obj.coordinates.*ones(2,obj.trace_length);
            obj.trace=plot(trace(1,:),trace(2,:));
        end
        
        function obj=update_ball(obj)
            circle=obj.make_circle();
            set(obj.ball, 'XData', circle(1,:),'YData',circle(2,:),'Visible','off')
            set(obj.text, 'Position', [obj.coordinates(1),obj.coordinates(2)]);
            set(obj.trace, 'XData', [obj.coordinates(1) obj.trace.XData(1:end-1)],'YData', [obj.coordinates(2) obj.trace.YData(1:end-1)]);
%             disp(obj.trace.XData(1))
        end
        
        function t=time_converter(obj,t)
            %Convert time t to Julian Ephemeris Date.
            t=(2816788-625674)*(t+3001)/(3000+3001)+625674;
        end
        
        function M=mod_M(obj,M)
            %Convert M such that M is between -180 deg and 180 deg.
            M=mod(M,360)-(mod(M,360)>=180)*360;
        end
    end
end



