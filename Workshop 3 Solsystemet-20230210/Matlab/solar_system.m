classdef solar_system<handle
    %Class for modeling the solar system
    
    properties
        sun
        planets
        comets
        t=-3000
        dt=10
        playing
        fig
        paused=0;
        axis_lim=[-40,40,-40,40];
        text
        show_text=1;
    end
    
    methods
        function obj = solar_system()
            %Constructer which initializes the figure window used to show
            %the model.
            obj.fig=figure(1);
            axis('equal')
            view(2);
            %hold off;
            axis equal;
            title('Solsystemet');
            axis(obj.axis_lim);
            set(gca,'visible','off')
            set(gca,'xtick',[])
            hold on;
            set(gcf,'WindowKeyPressFcn',@obj.buttonpush);
            obj.text=text(.8*obj.axis_lim(2),obj.axis_lim(4),{'q: afslut spillet',
    'mellemrum: pause/genoptag',
    'piletaster: skalér/zoom', 
    't: tekster til/fra',
    'punktum/komma: hastighed op/ned',
    ['dato: ',obj.time_to_date(obj.t)]}, 'verticalalign','top' );
        end
        
        
        
        function obj = add_planets(obj,names,colors,planet_data)
            %Method for adding planets to the solar system
            l=length(names);
            obj.planets=cell(1:l);
            %Sort the planets wrt radius
            [~,idx]=sort(planet_data(:,1));
            idx=flip(idx);
            names=names(idx);
            colors=colors(idx);
            planet_data=planet_data(idx,:);
            for i =1:l
                obj.planets{i}=Planet(names{i},colors{i},planet_data(i,:));
            end
        end
        function obj = add_comets(obj,names,colors,comet_data)
            %Method for adding comets to the solar system
            l=length(names);
            obj.comets=cell(1:l);
            %Sort the comets wrt radius
            sort(comet_data(:,1))
            [~,idx]=sort(comet_data(:,1));
            idx=flip(idx);
            names=names(idx);
            colors=colors(idx);
            for i =1:l
                obj.comets{i}=Comet(names{i},colors{i},comet_data(i,:));
            end
        end
        
        function obj=add_sun(obj,radius)
            %Method for adding a sun to the solar system
            obj.sun=Sun(radius);
        end
        
        function obj=update(obj,t)
            %Method for updating the solar system. This calculates the
            %positions of the objects in the solar system at the time t.
            obj.t=t;
            l=length(obj.planets);
            for i =1:l
                obj.planets{i}.update(t);
            end
            l=length(obj.comets);
            for i =1:l
                obj.comets{i}.update(t);
            end
            obj.sun.update();
        end
        function draw_system(obj)
            %Method for drawing the objects in the solar system at their
            %current coordinates.
            l=length(obj.planets);
            for i =1:l
                set(obj.planets{i}.ball, 'Visible', 'on')
                if obj.show_text && obj.axis_lim(1)<=obj.planets{i}.coordinates(1)&& obj.axis_lim(2)>=obj.planets{i}.coordinates(1)&&obj.axis_lim(3)<=obj.planets{i}.coordinates(2)&& obj.axis_lim(4)>=obj.planets{i}.coordinates(2)
                    set(obj.planets{i}.text,'Visible','on')
                else
                    set(obj.planets{i}.text,'Visible','off')
                end
            end
            l=length(obj.comets);
            for i =1:l
                set(obj.comets{i}.ball, 'Visible', 'on')
                if obj.show_text && obj.axis_lim(1)<=obj.comets{i}.coordinates(1)&& obj.axis_lim(2)>=obj.comets{i}.coordinates(1)&&obj.axis_lim(3)<=obj.comets{i}.coordinates(2)&& obj.axis_lim(4)>=obj.comets{i}.coordinates(2)
                    set(obj.comets{i}.text,'Visible','on')
                else
                    set(obj.comets{i}.text,'Visible','off')
                end
            end
            
            set(obj.sun.ball, 'Visible', 'on')
            if obj.show_text
                set(obj.sun.text,'Visible','on')
            else
                set(obj.sun.text,'Visible','off')
            end
            set(obj.text,'String', {'q: afslut spillet',
                'mellemrum: pause/genoptag',
                'piletaster: skalér/zoom', 
                't: tekster til/fra',
                'punktum/komma: hastighed op/ned',
                ['dato: ',obj.time_to_date(obj.t)]});
            set(obj.text,'Position',[0.9*obj.axis_lim(2),0.9*obj.axis_lim(4)]);
               
            drawnow
            axis('equal')
            axis(obj.axis_lim);
        end
        
        function obj=scale_distances(obj,scale)
             l=length(obj.planets);
            for i =1:l
                obj.planets{i}.a=obj.planets{i}.a*scale;
            end
            l=length(obj.comets);
            for i =1:l
                obj.comets{i}.a=obj.comets{i}.a*scale;
            end
        end
        
        function obj=scale_radii(obj,scale)
            l=length(obj.planets);
            for i =1:l
                obj.planets{i}.radius=obj.planets{i}.radius*scale;
            end
            
            l=length(obj.comets);
            for i =1:l
                obj.comets{i}.radius=obj.comets{i}.radius*scale;
            end
            obj.sun.radius=obj.sun.radius*scale;
        end
        
        
        function date=time_to_date(obj,t)
            %Method for converting the time of the system, measured in
            %years with 0 being 1BC to understandable date format.
            year=fix(t);
            fractional_part=t-year;
            day=abs(fix(365.25*fractional_part))+1;
            if year<1
                year=abs(year-1);
                prefix='BC';
            else 
                prefix='AD';
            end
            
            if 0<=day && day<=31
                month='Jan';
            elseif 31<day && day<=59
                month='Feb';
                day=day-31;
            elseif 59<day&& day<=90
                month='Mar';
                day=day-59;
            elseif 90<day && day<=120
                month='Apr';
                day=day-90;
            elseif 120<day&&day<=151
                month='May';
                day=day-120;
            elseif 151< day && day<=181
                month='Jun';
                day=day-151;
            elseif 181<day && day<=212
                month='Jul';
                day=day-181;
            elseif 212<day&&day<=243
                month='Aug';
                day=day-212;
            elseif 243<day&& day<=273
                month='Sep';
                day=day-243;
            elseif 273<day&& day<=304
                month='Oct';
                day=day-273;
            elseif 304<day &&day<= 334
                month='Nov';
                day=day-304;
            else 
                month='Dec';
                day=day-334;
            end
            if day>31
                day=31;
            end
            date=[num2str(day),'. ',month,' ',num2str(year),' ',prefix];
        end
        
        
        function run(obj,t,dt)
            %Method for running the model. This method updates the
            %positions for the planets and draws them for each time step
            obj.playing=1;
            obj.dt=dt;
            tic;
            while obj.playing==1 && t<=3000
                if obj.paused
                    obj.draw_system();
                    continue
                end
                obj.update(t);
                obj.draw_system();
                time_elapsed=toc;
                toc
                t=t+obj.dt*time_elapsed;
            end
            close(1)
        end
        
        function buttonpush(obj,src,ed)
            %Method for handling button pushes while the model is running.
            switch ed.Key
                case 'q'
                    obj.playing=0;
                case 'space'
                    if obj.paused
                        obj.paused=0;
                    else
                        obj.paused=1;
                    end
                case 'leftarrow'
                    obj.scale_radii(0.5);
                case 'rightarrow'
                    obj.scale_radii(2);
                case 'uparrow'
                    obj.axis_lim=obj.axis_lim*2;
                case 'downarrow'
                    obj.axis_lim=obj.axis_lim/2;
                case 'comma'
                    obj.dt=obj.dt/2;
                    for i =1:length(obj.planets)
                        obj.planets{i}.trace_length=obj.planets{i}.trace_length+20;
                    end
                case 'period'
                    obj.dt=obj.dt*2;
                    for i =1:length(obj.planets)
                        obj.planets{i}.trace_length=obj.planets{i}.trace_length-20;
                    end
                case 't'
                    if obj.show_text
                        obj.show_text=0;
                    else 
                        obj.show_text=1;
                    end
                    obj.show_hide_text();
            end
        end
    end
end

