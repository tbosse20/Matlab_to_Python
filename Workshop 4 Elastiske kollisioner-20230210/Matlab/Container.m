classdef Container<handle
    %Klasse til modellens beholder. Denne består af siderne til beholderen,
    %samt metoder to at bestemme om et koordinat er i beholderen eller ej,
    %samt til at reflektere en vektor i en af beholderens sider.
    
    properties
        n
        vertices
        normals
        minx
        maxx
        miny
        maxy
        shape
    end
    
    methods
        function obj = Container(n)
            %Constructor der generer punkterne der i beholderen, samt
            %sidernes normalvektorer.
            obj.n=n;
            x=linspace(0,2*pi,n+1);
            obj.vertices=[cos(x);sin(x)];
            obj.normals=obj.normal_hat(obj.vertices(:,2:end)-obj.vertices(:,1:end-1));
            obj.minx=min(obj.vertices(1,:));
            obj.maxx=max(obj.vertices(1,:));
            obj.miny=min(obj.vertices(2,:));
            obj.maxy=max(obj.vertices(2,:));   
            obj.shape=patch(obj.vertices(1,:),obj.vertices(2,:),'k');
            set(obj.shape,'FaceColor','none');
        end
        
        function in = in_container(obj,x)
            %afgører om søjlerne i x er indenfor beholderen
            
            in=inpolygon(x(1,:),x(2,:),obj.vertices(1,:),obj.vertices(2,:));
            
        end
        function hatvec=normal_hat(obj,x)
            %normaliseret hatvektor
            hatvec=[x(2,:);-x(1,:)]./vecnorm(x);
        end
        
        function reflected_vec = reflect_edge(obj,x,edge)
            %Reflekterer x i kant nr. edge. Se også Delopgave 4
            if(length(edge) ~=length(x(1,:)))
                error('incompatible lengths')
            end
            reflected_vec=x-2*dot(obj.normals(:,edge),x).*obj.normals(:,edge);
        end
        
        function [dist,idx]=dist_to_boundary(obj,x)
            %Udregner afstanden fra x til kanterne i beholderen. Se også
            %delopgave 4
            
            
            m=length(x(1,:));
            
            x=kron(x,ones(1,obj.n));
            
            x_0=repmat(obj.vertices(:,1:end-1),[1,m]);
            
            normals=repmat(obj.normals,[1,m]);
            
            dist=dot(normals,x-x_0);
            
        end
        
        function plot_container(obj)
            plot(obj.vertices(1,:),obj.vertices(2,:))
        end
        

    end
end

