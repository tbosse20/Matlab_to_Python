classdef Model<handle
    %Klasse til at modellere bolde der bevæger sig i en beholder.
    
    properties
        nballs
        balls
        container
        t=0
        dt=0.001
        playing
        paused=0
        text
        show_text=1;
        show_velocities=1;
    end
    
    methods
        function obj = Model(ngon,nballs,option)
            %Constructer, der laver en beholder og placerer et passende
            %antal bolde i beholderen. Dette gøres tilfældigt.
            obj.container=Container(ngon);
            obj.nballs=nballs;
            obj.balls=obj.make_balls(nballs,option);
            set(gcf,'WindowKeyPressFcn',@obj.buttonpush);
            obj.text=text(.4,1,{'q: afslut','mellemrum: pause/genoptag',...
    'piletaster op/ned: skalér hastighed', ...
    't: tekster til/fra'}, 'verticalalign','top' );
            xlim([-1,1])
            ylim([-1,1])
            axis square
        end
        
        function balls = make_balls(obj,nballs,option)
            %tilfældig generation af et antal bolde.
            balls=cell(1,nballs);
            %Generer hastighederne
            velocities=6*rand(2,nballs)-1;
            %Generer boldene, med radius og proportionelle masser:
            [positions,radii,masses]=obj.generate_positions_and_radii(option);
            for i =1:nballs
                balls{i}=Ball(masses(i),radii(i),velocities(:,i),positions(:,i),'b',num2str(i));
            end
        end
        
        function obj=run(obj)
            %Kør modellen.
            obj.playing=1;
            while obj.playing==1
                if obj.paused
                     pause(0.01)
                     continue
                end
                obj.update(obj.dt);
                drawnow
            end
            %close(1)
            
        end
        
        function obj=update(obj,t)
            %opdater modellen frem til tiden t. Dette kan lave yderligere
            %af tidstrinnet t afhængigt af antallet af kollisioner.
            new_time=obj.collision_detection(t);
            obj.update_positions(new_time);
        end
        
        function obj=update_positions(obj,t)
            for i=1:obj.nballs
                obj.balls{i}.update_position(t);
            end
        end
        
        
        function obj=scale_velocities(obj,scale)
            for i=1:obj.nballs
                obj.balls{i}.velocity=obj.balls{i}.velocity*scale;
            end
        end
        
        function new_time=collision_detection(obj,dt)
            %Find første kollision i tidstrinnet dt..
            new_time=dt;
            first_collision=[0,0,dt];
            positions=obj.get_positions_at_time_step(1:obj.nballs,dt);
            radii=obj.get_radii(1:obj.nballs);
            velocities=obj.get_velocities(1:obj.nballs);
            %Hvis hastighederne er store kan vi risikere at bolde kan ryge
            %ud af beholderen eller passere igennem hinanden. Nedenstående
            %loop detekterer dette og reducerer tidstrinnet om nødvendigt.
            in_container=obj.container.in_container(positions);
            pass_through=0;
            for i =1:obj.nballs-1
                for j= i+1:obj.nballs
                    if obj.pass_through(obj.balls{i}.position,positions(:,i),obj.balls{j}.position,positions(:,j))
                        pass_through=1;
                        break
                    end
                end
                if pass_through
                    disp('break_through')
                    break;
                end
            end
            if nnz(in_container)<obj.nballs || pass_through 
                new_time=obj.collision_detection(new_time/2);
            else    
                %Hvis ikke overnævnte tilfælde sker kan vi bestemme
                %kollisionerne og finde den første.
                for i =1:obj.nballs
                    position=positions(:,i);
                    radius=radii(i);
                    velocity=velocities(:,i);

                    if i<obj.nballs
                        remaining_positions=positions(:,i+1:obj.nballs);
                        remaining_radii=obj.get_radii(i+1:obj.nballs);
                        ball_collisions=obj.ball_collisions(position,radius,remaining_positions,remaining_radii);
                    else
                        ball_collisions=0;
                    end
                    n_collisions=nnz(ball_collisions);
                    %Hvis der er bolde der kolliderer udregner vi de eksakte
                    %tidspunkter.
                    if n_collisions>0 
                        ball_idx=i+find(ball_collisions);
                        u=positions(:,ball_idx)-position;
                        v=velocities(:,ball_idx)-velocity;
                        udotv=dot(u,v);
                        vv=dot(v,v);
                        uu=dot(u,u);
                        r=radii(ball_idx)+radius;
                        time_of_collisions=dt-(udotv+sqrt(udotv.^2-vv.*(uu-r.^2)))./vv;
                        [time,idx]=min(time_of_collisions);
                        if time<first_collision(3)
                            first_collision=[i,ball_idx(idx),time];
                        end
                    end     
                    %Vi udregner de eksakte tidspunkter for kollisioner med
                    %beholderen.
                    [edge_collisions,edge_idx,edge_dists]=obj.edge_collisions(position,radius);
                    n_collisions=nnz(edge_collisions);

                    if n_collisions>0
                        n=obj.container.normals(:,edge_idx);
                        vel=repmat(velocity,[1,length(n(1,:))]);
                        time_of_collisions=dt-(edge_dists+radius)./dot(n,vel);
                        [time,idx]=min(time_of_collisions);
                        if time<first_collision(3)
                            first_collision=[i,-edge_idx(idx),time];
                        end
                    end
                end
                %Updater positionerne til første kollision og opdater
                %hastighedvektorerne for de involverede objekter.
                if first_collision(3)<dt
                    obj.update_positions(first_collision(3));
                    if first_collision(2)>0
                        obj.ball_collision_update(first_collision(1),first_collision(2));
                    else
                        obj.edge_collision_update(first_collision(1),-first_collision(2));
                    end
                    new_time=dt-first_collision(3);
                    %Test for flere kollisioner i den resterende tid af
                    %tidstrinnet.
                    new_time=obj.collision_detection(new_time);
                end
            end
        end
        
        function obj=edge_collision_update(obj,ball_idx,edge_idx)
            %opdater bold nr ball_idx hastighedsvektor efter kollision 
            %med kant edge_idx. Her anvendes reflektioner fra delopgave 4,
            %se mere i filen Container.m
            ball=obj.balls{ball_idx};
            ball.velocity=obj.container.reflect_edge(ball.velocity,edge_idx);
        end
        
        function obj=ball_collision_update(obj,ball1_idx,ball2_idx)
            %opdater hastighederne på bold ball1_idx og ball2_idx efter
            %deres kollision. Bemærk at der her bruges teorien om elastiske
            %kollisioner fra delopgave 4
            mass1=obj.balls{ball1_idx}.mass;
            position1=obj.balls{ball1_idx}.position;
            velocity1=obj.balls{ball1_idx}.velocity;
            mass2=obj.balls{ball2_idx}.mass;
            position2=obj.balls{ball2_idx}.position;
            velocity2=obj.balls{ball2_idx}.velocity;
            position_difference=position2-position1;
            velocity_difference=velocity2-velocity1;
            normal_vector=position_difference/norm(position_difference);
            projection=dot(velocity_difference,normal_vector)*normal_vector;
            velocity1=velocity1+2*mass2/(mass1+mass2)*projection;
            velocity2=velocity2-2*mass1/(mass1+mass2)*projection;
            
            obj.balls{ball1_idx}.velocity= velocity1;
            obj.balls{ball2_idx}.velocity= velocity2;
        end
            
                    
        function velocities=get_velocities(obj,idx)
            velocities=zeros(2,length(idx));
            counter=1;
            for i =idx
                velocities(:,counter)=obj.balls{i}.velocity;
                counter=counter+1;
            end
        end        
        function positions=get_positions_at_time_step(obj,idx,dt)
            positions=zeros(2,length(idx));
            counter=1;
            for i = idx
                positions(:,counter)=obj.balls{i}.get_position_at_time_step(dt);
                counter=counter+1;
            end
        end
        
        function bool=pass_through(obj,x1,x2,u1,u2)
            %Funktion der undersøger om to bolde er passeret igennem
            %hinanden. Dette sker kun ved meget store hastigheder og små
            %bolde. Funktionen ser om der er en skæring i de to baner som
            %boldene følger.
            bool=0;
            sort1=sort([x1,x2],2);
            sort2=sort([u1,u2],2);
            x_min=sort1(1,1);
            x_max=sort1(1,2);
            y_min=sort1(2,1);
            y_max=sort1(2,2);
            u_min=sort2(1,1);
            u_max=sort2(1,2);
            v_min=sort2(2,1);
            v_max=sort2(2,2);
            
            x_min=max([x_min,u_min]);
            x_max=min([x_max,u_max]);
            y_min=max([y_min,v_min]);
            y_max=min([y_max,v_max]);
            % x2(1)-x1(1)
            if (x2(1)-x1(1) == 0.0)
                "AD"
            end
            slope1=(x2(2)-x1(2))/(x2(1)-x1(1));
            slope2=(u2(2)-u1(2))/(u2(1)-u1(1));
            
            if slope1~=slope2
                x=u1(2)-x1(2)+slope1*x1(1)-slope2*u1(1);
                y=slope1*(x-x1(1))+x1(2);
                if x_min<=x && x<=x_max && y_min<=y&&y<=y_max
                    bool=1;
                end
            end
        end

        function radii=get_radii(obj,idx)
            radii=zeros(1,length(idx));
            counter=1;
            for i = idx
                radii(counter)=obj.balls{i}.radius;
                counter=counter+1;
            end
        end
        
        function collisions= ball_collisions(obj,position,radius,positions,radii)
            %Algoritme til at afgøre om bolde er kollideret. Se også
            %delopgave 1.
            if isempty(positions)
                collisions=0;
            else
                dists=vecnorm(positions-position);
                collisions=dists<=radii+radius;
            end
        end
        
        function [collisions,edge_idx,dists]=edge_collisions(obj,position,radius)
            %Algoritme til at afgøre om en bold er kollideret med en kant.
            %Se også delopgave 2.
            dists=obj.container.dist_to_boundary(position);
            collisions=abs(dists) < radius;
            edge_idx=find(collisions > 0);
            dists=dists(edge_idx);
        end
        
        function bool = is_collision(obj,position,radius,positions,radii)
            d0 = obj.ball_collisions(position,radius,positions,radii);
            w0 = obj.edge_collisions(position,radius);
            if nnz(d0) > 0 || nnz(w0) > 0
                bool=1;
            else
                bool=0;
            end
        end
        
        function random_numbers=rand_positions(obj,n)
            random_numbers=[(obj.container.maxx-obj.container.minx).*rand(1,n)+obj.container.minx;(obj.container.maxy-obj.container.miny).*rand(1,n)+obj.container.miny];
        end
        
        function [positions,radii,masses]=generate_positions_and_radii(obj,option)
            %Algoritme til at generere boldenes initielle positioner og
            %radiier. Dette gøres med trial&error
            balls_generated=0;
            number_of_tries=0;
            positions=zeros(2,obj.nballs);
            radii=zeros(1,obj.nballs);
            max_r=1/obj.nballs;
            min_r=1/(10*obj.nballs);
            while balls_generated<obj.nballs
                position=obj.rand_positions(1);
                if strcmp(option,'equal')
                    radius=0.5*(min_r+max_r);
                else
                    radius=min_r+rand()*(max_r-min_r);
                end
                number_of_tries=number_of_tries+1;
                
                if ~obj.is_collision(position,radius,positions(:,1:balls_generated),radii(1:balls_generated) ) &&nnz(obj.container.in_container(position))>0
                    positions(:,balls_generated+1)=position;
                    radii(balls_generated+1)=radius;
                    
                    balls_generated=balls_generated+1;
                    number_of_tries=0;
                end
            end
            masses=10*radii;
        end
        function obj=show_hide_text(obj)
            if obj.show_text==1
                set(obj.text,'Visible','on')
                for i =1:obj.nballs
                    set(obj.balls{i}.text,'Visible','on')
                end
            else
                set(obj.text,'Visible','off')
                for i =1:obj.nballs
                    set(obj.balls{i}.text,'Visible','off')
                end
            end
        end
%         
            function buttonpush(obj,src,ed)
            %Håndterer keyboard input.
            switch ed.Key
                case 'q'
                    obj.playing=0;
                case 'space'
                    if obj.paused
                        obj.paused=0;
                    else
                        obj.paused=1;
                    end
                case 'uparrow'
                    obj.scale_velocities(2);
                case 'downarrow'
                    obj.scale_velocities(0.5);
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

