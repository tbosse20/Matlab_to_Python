%% Introduktion
%Vi starter med at fjerne alle variabler der måtte være i vores workspace.
clc;clear;
%I denne Matlab-fil skal vi lave en animation af jordens rotation omkring
%sig selv. Vi modellerer Jorden som en kugle med radius 1 og med centrum i
%Origo. Vi kan nemt lave denne model vha. følgende kommando:
[X,Y,Z]=sphere;
%Bemærk at X, Y og Z er matricer således at (X(i,j),Y(i,j),Z(i,j)) er et
%punkt på kuglen. Til senere udregninger skal vi bruge dimensionerne af
%matricerne
[m,n]=size(X);
%Det er også mere bekvemt at arbejde med en matrix hvor søjlerne i matricen
%er punkter på kuglen:
A=[X(:)';Y(:)';Z(:)'];
%På denne måde kan man givet en 3x3 rotationsmatrix R roterere alle
%punkterne på kuglen på en gang ved at udregne R*A. Man kan efterfølgende
%transformere rækkerne i A tilbage til passende matricer med kommandoerne
%    X=reshape(A(1,:),[m,n]); 
%    Y=reshape(A(2,:),[m,n]); 
%    Z=reshape(A(3,:),[m,n]); 
%Man kan plotte kuglen med kommandoen
figure
surf(X,Y,Z);
axis equal
%% Opgave (i)
%I denne opgave skal vi roterere kuglen så den får den korrekte hældning.
%Husk at vi antager at nordpolen er placeret i punktet (0,0,1). Med denne
%antagelse giver plottet af X, Y og Z passende linjer for længde og
%breddegrader.

%Bestem først rotationsvinklen i radianer
theta=23.4*pi/180;
%Bestem Efterfølgende rotationsmatricen R der roterer med en vinkel theta
%omkring y-aksen
R=[cos(theta), 0, sin(theta); 0, 1 0; -sin(theta), 0, cos(theta)];
%Roter punkterne på kuglen
A=R*A;
%Omtransformer til matricer og plot resultatet:
X=reshape(A(1,:),[m,n]); 
Y=reshape(A(2,:),[m,n]); 
Z=reshape(A(3,:),[m,n]); 
figure;
surf(X,Y,Z);
axis equal

%% Opgave (ii)
%Vi skal i denne opgave bestemme en enhedsvektor der er parallel med linjen
%gennem nord og sydpolen. 
v=R*[0;0;1];

%% Opgave (iii)
%Vi skal i denne opgave lave en animation af Jordens rotation om sin egen
%akse. Dette gøres vha. Matlabs VideoWriter funktion. Vi skal sådan set
%bare tegne de frames der skal indgå i animationen så klarer Matlab resten.

%VI ønsker 60 fps og 3 sekunders video
fps=60;
seconds=3;
%Derfor får vi det totale antal frames
n_frames=fps*3;
%Vi laver nu figuren vi skal plotte i
h = figure;
h.Visible= 'off'; 
set(h, 'Position',  [100, 100,600, 800])
axis equal
axis([-2 2 -2 2 -2 2 ])
view(0,45)
ax=gca();
set(ax,'XColor', 'none','YColor','none')

%Bemærk at der ikke er grund til at se hvert plot så vi gør figuren usynlig
%Vi laver nu et videoobjekt
video = VideoWriter('rotation.mp4','MPEG-4');
video.Quality=100;
video.FrameRate=fps;
open(video);
%Nedenstående loop laver de frames der skal indgå i animationen.
for k =1:n_frames
    %Vi ønsker en enkelt rotation så vi sætter vinklen vi roterer jorden
    %med i frame k til at være
    theta=k*2*pi/n_frames;
    %Udregn s og lambda for den kvatanion som vi skal bruge for at rotere
    %med en vinkel theta omkring v
    s=cos(theta/2);
    lambda=sin(theta/2);
    %Brug funktionerne left_multiplication og right_multiplication til at
    %definere passende matricer til at udregne rotationen qpq^(-1) hvor
    %q=[s,lambda*v]
    L=left_multiplication(s,lambda*v);
    R=right_multiplication(s,-lambda*v);
    %Vi omdanner nu vektorerne i A til kvatanioner ved at sætte deres
    %skalardel lig 0.
    Q=[zeros(1,n*m);A];
    %Vi udregner rotationen omkring v vha. kvatanioner
    Q=L*R*Q;
    %Vi omdanner vores roterede kvatanioner til vektorer. Bemærk at vi
    %smider skalardelen væk, da den blot er 0.
    X=reshape(Q(2,:),[m,n]); 
    Y=reshape(Q(3,:),[m,n]); 
    Z=reshape(Q(4,:),[m,n]); 
    %Vi plotter den roterede kugle og sørger for at vores plot bliver en
    %frame i videoen. Bemærk at det er hurtigere i Matlab at plotte kuglen
    %første gang og efterfølgende bare opdatere plottets indhold.
    if k==1
        w=surf(ax,X,Y,Z);
    else
        set(w,'XData',X)
        set(w,'YData',Y)
        set(w,'ZData',Z)
    end
    hold on
    %Vi plotter rotationsaksen
    plot3(ax,[-2*v(1),2*v(1)],[-2*v(2),2*v(2)],[-2*v(3),2*v(3)],'b')
    axis equal
    axis([-2 2 -2 2 -2 2 ])
    drawnow();
    %Vi skriver den frame vi lige har plottet til vores video.
    writeVideo(video,getframe(ax));
end
%Vi afslutter vores video.
close(video)

%% Hjælpefunktioner 

function L = left_multiplication(s,v)
%Funktion der udregner matricen for venstre multiplikation med kvatanionen
%[s,v]
L=[
    s,-v(1),-v(2),-v(3);
    v(1),s,-v(3),v(2);
    v(2),v(3),s,-v(1);
    v(3),-v(2),v(1),s
    ];
end

function R = right_multiplication(s,v)
%Funktion der udregner matricen for højre multiplikation med kvatanionen
%[s,v]
R=[s,-v(1),-v(2),-v(3);
v(1),s,v(3),-v(2);
v(2),-v(3),s,v(1);
v(3),v(2),-v(1),s];
end
