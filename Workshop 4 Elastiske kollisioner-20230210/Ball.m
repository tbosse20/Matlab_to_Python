classdef Ball<handle
    %Klasse der beskriver boldene i vores model.
    
    properties
        mass
        radius
        velocity
        position
        ball
        color
        resolution=100;
        text
        velocity_vector
    end
    
    methods
        function obj = Ball(mass,radius,velocity,position,color,name)
            %Genererer en bold med given masse, radius, hastighed og
            %position.
            if nargin>0
                obj.mass=mass;
                obj.radius=radius;
                obj.velocity=velocity;
                obj.position=position;
                obj.color=color;
                circle=obj.make_circle();
                obj.ball=patch(circle(1,:),circle(2,:),obj.color);
                hold on
                obj.text=text(obj.position(1),obj.position(2),name);
            end
        end
        
        function obj = update_position(obj,t)
            obj.position=obj.get_position_at_time_step(t);
            circle=obj.make_circle();
            set(obj.ball,'XData', circle(1,:),'YData',circle(2,:));
            set(obj.text,'Position',obj.position');
        end
        function position=get_position_at_time_step(obj,dt)
            position=obj.position+dt*obj.velocity;
        end
        
        function circle= make_circle(obj)
            t=linspace(0,2*pi,obj.resolution);
            circle=[obj.position(1)+obj.radius*cos(t);obj.position(2)+obj.radius*sin(t)];
        end
    end
end

