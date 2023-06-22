classdef Sun
    %Class for a Sun
    
    properties
        name='Sun'
        coordinates=[0;0];
        radius
        color='y';
        resolution=500
        ball
        text
    end
    
    methods
        function obj = Sun(r)
            %Constructer.
                obj.radius=r;
                circle=obj.make_circle();
                obj.ball=patch(circle(1,:),circle(2,:),obj.color,'visible','off');
                obj.text=text(obj.coordinates(1),obj.coordinates(2),obj.name);
        end
        
        function circle=make_circle(obj)
            t=linspace(0,2*pi,obj.resolution);
            circle=obj.radius*[cos(t);sin(t)];    
        end
        
        
        function obj=update(obj)
            circle=obj.make_circle();
            set(obj.ball, 'XData', circle(1,:),'YData',circle(2,:),'Visible','off');        end
    end
end

