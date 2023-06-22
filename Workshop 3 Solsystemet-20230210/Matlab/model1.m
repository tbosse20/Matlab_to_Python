function main
clear all; close all; clc;
format compact;

% use a global structure to store all values that need to be
% used in several different functions
global g;

t=10000*rand();
g.t=t;

get_settings();
init_figure();
create_ball();

tic % start timer
while g.playing
    if g.moving==0, tic; drawnow; continue; end
    if g.moving==1, dt=toc; % get time since last bounce
    else, dt=.01; g.moving=0;
    end
    if dt<min(.05/g.v,.05), continue; end % prevents updates of less than 1/20 of a second
    tic; % reset timer
    t=t+g.v*dt;
    % new position
    g.earthcx=100.0000180000000*cos(t)-1.6731633011693;
    g.earthcy=   99.9860196455882*sin(t);

    g.halleycx=1783.41442925537*cos(t/75.32)-1724.8166181036783;
    g.halleycy=107.3639924082853*sin(t/75.32);
    
    g.mercurycx=38.7098430000000*cos(t/0.240846)-7.9601608881522;
    g.mercurycy=37.8825524974147*sin(t/0.240846);
        
    g.marscx=   152.3712430000000*cos(t/1.881)- 14.2261578635317;
    g.marscy=   151.7056759841467*sin(t/1.881);

    g.jupitercx=   520.2480190000000*cos(t/11.86)-  25.2507058253821;
    g.jupitercy=   519.6348748195645*sin(t/11.86);

    g.saturncx=      954.1498830000000*cos(t/29.46)- 52.9631902430348;
    g.saturncy=   952.6788019622321*sin(t/29.46);

    g.uranuscx=  1918.7979479999999*cos(t/84.01)-  89.9098829686152;
    g.uranuscy=  1916.6903188031135*sin(t/84.01);

    g.neptunecx=  3006.9527520000001*cos(t/164.8)-  26.9254276529813;
    g.neptunecy=  3006.8321991933768*sin(t/164.8);

    g.venuscx=   72.3321020000000*cos(t/0.615)-   0.4892536146070;
    g.venuscy= 72.3304473277955*sin(t/0.615);
    
    g.plutocx= 3948.6860350000001*cos(t/247.92065)-     982.06399176825134;
    g.plutocy=   3824.4660013106305*sin(t/247.92065);
        update_graphics
end
close(1)
% msgbox('Tak fordi du spillede!')

return

function buttonpush(src,ed)
global g
dv=10;
if length(ed.Modifier)>0
    dv=1; 
end% shift, ctrl, alt all set dv=1
switch ed.Key
    case 'q'
        g.playing=0;
    case 'space'
        if g.moving, g.moving=0;
        else, g.moving=1;
        end
    case 'tab'
        g.moving=2;
    case 'leftarrow'
        t = linspace(0,2*pi,200);

        g.sunr=g.sunr/2;
        g.sunbx=g.sunr*cos(t);
        g.sunby=g.sunr*sin(t);

        t = linspace(0,2*pi,20);
        g.earthr=g.earthr/2;
        g.earthbx=g.earthr*cos(t);
        g.earthby=g.earthr*sin(t);

        g.halleyr=g.halleyr/2;
        g.halleybx=g.halleyr*cos(t);
        g.halleyby=g.halleyr*sin(t);
        
        g.mercuryr=g.mercuryr/2;
        g.mercurybx=g.mercuryr*cos(t);
        g.mercuryby=g.mercuryr*sin(t);

        t = linspace(0,2*pi,80);

        g.jupiterr=g.jupiterr/2;
        g.jupiterbx=g.jupiterr*cos(t);
        g.jupiterby=g.jupiterr*sin(t);

        g.saturnr=g.saturnr/2;
        g.saturnbx=g.saturnr*cos(t);
        g.saturnby=g.saturnr*sin(t);

        t = linspace(0,2*pi,20);

        g.uranusr=g.uranusr/2;
        g.uranusbx=g.uranusr*cos(t);
        g.uranusby=g.uranusr*sin(t);

        g.neptuner=g.neptuner/2;
        g.neptunebx=g.neptuner*cos(t);
        g.neptuneby=g.neptuner*sin(t);

        g.marsr=g.marsr/2;
        g.marsbx=g.marsr*cos(t);
        g.marsby=g.marsr*sin(t);

        g.venusr=g.venusr/2;
        g.venusbx=g.venusr*cos(t);
        g.venusby=g.venusr*sin(t);
        
        g.plutor=g.plutor/2;
        g.plutobx=g.plutor*cos(t);
        g.plutoby=g.plutor*sin(t);
    case 'rightarrow'
        t = linspace(0,2*pi,200);

        g.sunr=g.sunr*2;
        g.sunbx=g.sunr*cos(t);
        g.sunby=g.sunr*sin(t);

        t = linspace(0,2*pi,20);
        g.earthr=g.earthr*2;
        g.earthbx=g.earthr*cos(t);
        g.earthby=g.earthr*sin(t);

        g.halleyr=g.halleyr*2;
        g.halleybx=g.halleyr*cos(t);
        g.halleyby=g.halleyr*sin(t);
        
        g.mercuryr=g.mercuryr*2;
        g.mercurybx=g.mercuryr*cos(t);
        g.mercuryby=g.mercuryr*sin(t);
        
        g.marsr=g.marsr*2;
        g.marsbx=g.marsr*cos(t);
        g.marsby=g.marsr*sin(t);

        t = linspace(0,2*pi,80);

        g.jupiterr=g.jupiterr*2;
        g.jupiterbx=g.jupiterr*cos(t);
        g.jupiterby=g.jupiterr*sin(t);

        g.saturnr=g.saturnr*2;
        g.saturnbx=g.saturnr*cos(t);
        g.saturnby=g.saturnr*sin(t);

        t = linspace(0,2*pi,20);

        g.uranusr=g.uranusr*2;
        g.uranusbx=g.uranusr*cos(t);
        g.uranusby=g.uranusr*sin(t);

        g.neptuner=g.neptuner*2;
        g.neptunebx=g.neptuner*cos(t);
        g.neptuneby=g.neptuner*sin(t);

        g.venusr=g.venusr*2;
        g.venusbx=g.venusr*cos(t);
        g.venusby=g.venusr*sin(t);
        
        g.plutor=g.plutor*2;
        g.plutobx=g.plutor*cos(t);
        g.plutoby=g.plutor*sin(t);

    case 'uparrow'
        g.xmax=g.xmax/2;
        g.ymax=g.ymax/2;
        set(g.text, 'Position', [.8*g.xmax,g.ymax]);
    case 'downarrow'
        g.xmax=2*g.xmax;
        g.ymax=2*g.ymax;
        set(g.text, 'Position', [.8*g.xmax,g.ymax]);
    case 'comma'
        g.v=g.v/2;
    case 'period'
        g.v=g.v*2;
    case 't';
        g.textvisible=g.textvisible+1;
    otherwise
        ed  % show key info
end


return

function get_settings
global g;
%p={'X-acceleration','Y-acceleration', 'Restitutionskoefficient', 'Begyndelsesretning (0 til 360 grader)', 'Begyndelsesvinkel (0 til 90 grader)', 'Begyndelseshastighed'};
%t='Hoppeboldspil';
%d={'0','0','1', '0', '0', '0'};
%a=inputdlg(p,t,1,d);
%if length(a)==0, error('Cancelled'); end  % user pushed close or cancel
g.v=1;
g.textvisible=0;
% hardcoded values
g.playing=1;
g.moving=1;
g.xmax=4600;
g.ymax=3200;

    g.earthcx=100.0000180000000*cos(g.t)-1.6731633011693;
    g.earthcy=   99.9860196455882*sin(g.t);

    g.halleycx=1783.41442925537*cos(g.t/75.32)-1724.8166181036783;
    g.halleycy=107.3639924082853*sin(g.t/75.32);
    
    g.mercurycx=38.7098430000000*cos(g.t/0.240846)-7.9601608881522;
    g.mercurycy=37.8825524974147*sin(g.t/0.240846);
        
    g.marscx=   152.3712430000000*cos(g.t/1.881)- 14.2261578635317;
    g.marscy=   151.7056759841467*sin(g.t/1.881);

    g.jupitercx=   520.2480190000000*cos(g.t/11.86)-  25.2507058253821;
    g.jupitercy=   519.6348748195645*sin(g.t/11.86);

    g.saturncx=      954.1498830000000*cos(g.t/29.46)- 52.9631902430348;
    g.saturncy=   952.6788019622321*sin(g.t/29.46);

    g.uranuscx=  1918.7979479999999*cos(g.t/84.01)-  89.9098829686152;
    g.uranuscy=  1916.6903188031135*sin(g.t/84.01);

    g.neptunecx=  3006.9527520000001*cos(g.t/164.8)-  26.9254276529813;
    g.neptunecy=  3006.8321991933768*sin(g.t/164.8);

    g.venuscx=   72.3321020000000*cos(g.t/0.615)-   0.4892536146070;
    g.venuscy= 72.3304473277955*sin(g.t/0.615);
    
    g.plutocx= 3948.6860350000001*cos(g.t/247.92065)-     982.06399176825134;
    g.plutocy=   3824.4660013106305*sin(g.t/247.92065);

return

function create_ball
global g;
% create a 'ball'
t = linspace(0,2*pi,200);

g.sunr=696.340;
g.sunbx=g.sunr*cos(t);
g.sunby=g.sunr*sin(t);
g.sunball=patch(g.sunbx,g.sunby,'y');
g.suntext=text(0,0,"Solen");


g.jupiterr=69.911;
g.jupiterbx=g.jupiterr*cos(t);
g.jupiterby=g.jupiterr*sin(t);
g.jupiterball=patch(g.jupiterbx,g.jupiterby,'g');
g.jupitertext=text(g.jupitercx,g.jupitercy,"Jupiter");

% trace (tail)
tlen=500;
g.jupitertrace.x=ones(1,tlen)*g.jupitercx;
g.jupitertrace.y=ones(1,tlen)*g.jupitercy;
g.jupitertrace.h=plot(g.jupitertrace.x,g.jupitertrace.y,'b:');
g.jupitertrace.visible='on';

g.saturnr=58.232;
g.saturnbx=g.saturnr*cos(t);
g.saturnby=g.saturnr*sin(t);
g.saturnball=patch(g.saturnbx,g.saturnby,[0.7 0 0.7]);
g.saturntext=text(g.saturncx,g.saturncy,"Saturn");

% trace (tail)
tlen=500;
g.saturntrace.x=ones(1,tlen)*g.saturncx;
g.saturntrace.y=ones(1,tlen)*g.saturncy;
g.saturntrace.h=plot(g.saturntrace.x,g.saturntrace.y,'b:');
g.saturntrace.visible='on';

t = linspace(0,2*pi,20);

g.uranusr=25.362;
g.uranusbx=g.uranusr*cos(t);
g.uranusby=g.uranusr*sin(t);
g.uranusball=patch(g.uranusbx,g.uranusby,[0.7 0.7 0]);
g.uranustext=text(g.marscx,g.uranuscy,"Uranus");


% trace (tail)
tlen=5;
g.uranustrace.x=ones(1,tlen)*g.uranuscx;
g.uranustrace.x
g.uranustrace.y=ones(1,tlen)*g.uranuscy;
g.uranustrace.h=plot(g.uranustrace.x,g.uranustrace.y,'b:');
g.uranustrace.h
g.uranustrace.visible='on';

g.neptuner=24.622;
g.neptunebx=g.neptuner*cos(t);
g.neptuneby=g.neptuner*sin(t);
g.neptuneball=patch(g.neptunebx,g.neptuneby,[0 .7 .7]);
g.neptunetext=text(g.neptunecx,g.neptunecy,"Neptun");

% trace (tail)
tlen=500;
g.neptunetrace.x=ones(1,tlen)*g.neptunecx;
g.neptunetrace.y=ones(1,tlen)*g.neptunecy;
g.neptunetrace.h=plot(g.neptunetrace.x,g.neptunetrace.y,'b:');
g.neptunetrace.visible='on';


t = linspace(0,2*pi,20);
g.earthr=6.371;
g.earthbx=g.earthr*cos(t);
g.earthby=g.earthr*sin(t);
g.earthball=patch(g.earthbx,g.earthby,'b');
g.earthtext=text(g.earthcx,g.earthcy,"Jorden");

% trace (tail)
tlen=500;
g.earthtrace.x=ones(1,tlen)*g.earthcx;
g.earthtrace.y=ones(1,tlen)*g.earthcy;
g.earthtrace.h=plot(g.earthtrace.x,g.earthtrace.y,'b:');
g.earthtrace.visible='on';


g.venusr=6.0518;
g.venusbx=g.venusr*cos(t);
g.venusby=g.venusr*sin(t);
g.venusball=patch(g.venusbx,g.venusby,[1 0.4 0.6]);
g.venustext=text(g.venuscx,g.venuscy,"Venus");

% trace (tail)
tlen=50;
g.venustrace.x=ones(1,tlen)*g.venuscx;
g.venustrace.y=ones(1,tlen)*g.venuscy;
g.venustrace.h=plot(g.venustrace.x,g.venustrace.y,'b:');
g.venustrace.visible='on';



g.marsr=3.3895;
g.marsbx=g.marsr*cos(t);
g.marsby=g.marsr*sin(t);
g.marsball=patch(g.marsbx,g.marsby,'r');
g.marstext=text(g.marscx,g.marscy,"Mars");

% trace (tail)
tlen=50;
g.marstrace.x=ones(1,tlen)*g.marscx;
g.marstrace.y=ones(1,tlen)*g.marscy;
g.marstrace.h=plot(g.marstrace.x,g.marstrace.y,'b:');
g.marstrace.visible='on';


g.mercuryr=2.4397;
g.mercurybx=g.mercuryr*cos(t);
g.mercuryby=g.mercuryr*sin(t);
g.mercuryball=patch(g.mercurybx,g.mercuryby,[.75 .75 .75]);
g.mercurytext=text(g.mercurycx,g.mercurycy,"Merkur");

% trace (tail)
tlen=250;
g.mercurytrace.x=ones(1,tlen)*g.mercurycx;
g.mercurytrace.y=ones(1,tlen)*g.mercurycy;
g.mercurytrace.h=plot(g.mercurytrace.x,g.mercurytrace.y,'b:');
g.mercurytrace.visible='on';

t = linspace(0,2*pi,80);




g.plutor=1.1883;
g.plutobx=g.plutor*cos(t);
g.plutoby=g.plutor*sin(t);
g.plutoball=patch(g.plutobx,g.plutoby,[0.5,0.5,0.5]);
g.plutotext=text(g.plutocx,g.plutocy,"Pluto");

% trace (tail)
tlen=50;
g.plutotrace.x=ones(1,tlen)*g.plutocx;
g.plutotrace.y=ones(1,tlen)*g.plutocy;
g.plutotrace.h=plot(g.plutotrace.x,g.plutotrace.y,'b:');
g.plutotrace.visible='on';

g.halleyr=0.011;
g.halleybx=g.halleyr*cos(t);
g.halleyby=g.halleyr*sin(t);
g.halleyball=patch(g.halleybx,g.halleyby,'b');
g.halleytext=text(g.halleycx,g.halleycy,"Halleys komet");


g.halleytrace.x=ones(1,tlen)*g.halleycx;
g.halleytrace.y=ones(1,tlen)*g.halleycy;
g.halleytrace.h=plot(g.halleytrace.x,g.halleytrace.y,'b:');
g.halleytrace.visible='on';
return

function init_figure
% set up figure window
global g;
figure(1);
view(2);
hold on;
%hold off;
axis equal;
title('Solsystemet');
axis([-g.xmax g.xmax -g.ymax g.ymax]);
set(gca,'visible','off')
set(gca,'xtick',[])
%xt = get(gca, 'XTick');
%yt = get(gca, 'YTick');
%lx = xlim;
%ly = ylim;
%plot([xt; xt], lx(:)*ones(size(xt)), 'k')                       % Plot X-Grid
%plot(ly(:)*ones(size(yt)), [yt; yt], 'k')                       % Plot Y-Grid
%plot(xt(end)*ly(2)*[1 1], yt(end)*lx(2)*[1 1], 'k')        % Plot Vertical Z-Axis Line 
%axis off;
%rectangle('Position',[0,0,0,g.xmax,g.ymax,g.zmax])
% set the function that gets called when a key is pressed
set(gcf,'WindowKeyPressFcn',@buttonpush);
% instructions
g.text=text(.8*g.xmax,g.ymax,{'q: afslut spillet',
    'mellemrum: pause/genoptag',
    'piletaster: skalér/zoom', 
    't: tekster til/fra',
    'punktum/komma: hastighed op/ned'}, 'verticalalign','top' );
% status text
%g.stattext_h=text(-30,90,'Test','verticalalign','top');
return

function update_graphics
global g;

% move ball to new position
%set(g.ball,'XData',g.earthbx+g.earthcx);
%set(g.ball,'YData',g.earthby+g.earthcy);
%set(g.ball,'ZData',g.bz+g.cz);

axis([-g.xmax g.xmax -g.ymax g.ymax]);
set(g.sunball, 'XData', g.sunbx, 'YData', g.sunby); 
set(g.earthball, 'XData', g.earthbx+g.earthcx, 'YData', g.earthby+g.earthcy); 
set(g.halleyball, 'XData', g.halleybx+g.halleycx, 'YData', g.halleyby+g.halleycy); 
set(g.mercuryball, 'XData', g.mercurybx+g.mercurycx, 'YData', g.mercuryby+g.mercurycy); 
set(g.marsball, 'XData', g.marsbx+g.marscx, 'YData', g.marsby+g.marscy); 
set(g.jupiterball, 'XData', g.jupiterbx+g.jupitercx, 'YData', g.jupiterby+g.jupitercy); 
set(g.saturnball, 'XData', g.saturnbx+g.saturncx, 'YData', g.saturnby+g.saturncy); 
set(g.uranusball, 'XData', g.uranusbx+g.uranuscx, 'YData', g.uranusby+g.uranuscy); 
set(g.neptuneball, 'XData', g.neptunebx+g.neptunecx, 'YData', g.neptuneby+g.neptunecy); 
set(g.venusball, 'XData', g.venusbx+g.venuscx, 'YData', g.venusby+g.venuscy); 
set(g.plutoball, 'XData', g.plutobx+g.plutocx, 'YData', g.plutoby+g.plutocy); 



set(g.earthtext, 'Position', [g.earthcx, g.earthcy]);
set(g.halleytext, 'Position', [g.halleycx, g.halleycy]);
set(g.mercurytext, 'Position', [g.mercurycx, g.mercurycy]);
set(g.marstext, 'Position', [g.marscx, g.marscy]);
set(g.jupitertext, 'Position', [g.jupitercx, g.jupitercy]);
set(g.saturntext, 'Position', [g.saturncx, g.saturncy]);
set(g.uranustext, 'Position', [g.uranuscx, g.uranuscy]);
set(g.neptunetext, 'Position', [g.neptunecx, g.neptunecy]);
set(g.venustext, 'Position', [g.venuscx, g.venuscy]);
set(g.plutotext, 'Position', [g.plutocx, g.plutocy]);

% update trace
g.earthcx
g.earthtrace.x=[g.earthcx g.earthtrace.x(1:end-1)];
g.earthtrace.y=[g.earthcy g.earthtrace.y(1:end-1)];
set(g.earthtrace.h,'XData',g.earthtrace.x,'YData',g.earthtrace.y);

g.halleytrace.x=[g.halleycx g.halleytrace.x(1:end-1)];
g.halleytrace.y=[g.halleycy g.halleytrace.y(1:end-1)];
set(g.halleytrace.h,'XData',g.halleytrace.x,'YData',g.halleytrace.y);

g.mercurytrace.x=[g.mercurycx g.mercurytrace.x(1:end-1)];
g.mercurytrace.y=[g.mercurycy g.mercurytrace.y(1:end-1)];
set(g.mercurytrace.h,'XData',g.mercurytrace.x,'YData',g.mercurytrace.y);

g.marstrace.x=[g.marscx g.marstrace.x(1:end-1)];
g.marstrace.y=[g.marscy g.marstrace.y(1:end-1)];
set(g.marstrace.h,'XData',g.marstrace.x,'YData',g.marstrace.y);

g.jupitertrace.x=[g.jupitercx g.jupitertrace.x(1:end-1)];
g.jupitertrace.y=[g.jupitercy g.jupitertrace.y(1:end-1)];
set(g.jupitertrace.h,'XData',g.jupitertrace.x,'YData',g.jupitertrace.y);

g.saturntrace.x=[g.saturncx g.saturntrace.x(1:end-1)];
g.saturntrace.y=[g.saturncy g.saturntrace.y(1:end-1)];
set(g.saturntrace.h,'XData',g.saturntrace.x,'YData',g.saturntrace.y);

g.uranustrace.x=[g.uranuscx g.uranustrace.x(1:end-1)];
g.uranustrace.x;
g.uranustrace.y=[g.uranuscy g.uranustrace.y(1:end-1)];
set(g.uranustrace.h,'XData',g.uranustrace.x,'YData',g.uranustrace.y);

g.neptunetrace.x=[g.neptunecx g.neptunetrace.x(1:end-1)];
g.neptunetrace.y=[g.neptunecy g.neptunetrace.y(1:end-1)];
set(g.neptunetrace.h,'XData',g.neptunetrace.x,'YData',g.neptunetrace.y);

g.venustrace.x=[g.venuscx g.venustrace.x(1:end-1)];
g.venustrace.y=[g.venuscy g.venustrace.y(1:end-1)];
set(g.venustrace.h,'XData',g.venustrace.x,'YData',g.venustrace.y);

g.plutotrace.x=[g.plutocx g.plutotrace.x(1:end-1)];
g.plutocx
g.plutotrace.y=[g.plutocy g.plutotrace.y(1:end-1)];
set(g.plutotrace.h,'XData',g.plutotrace.x,'YData',g.plutotrace.y);




if mod(g.textvisible,2)==1
    set(g.suntext, 'Visible', 'off');
    set(g.earthtext, 'Visible', 'off');
    set(g.halleytext, 'Visible', 'off');
    set(g.mercurytext, 'Visible', 'off');
    set(g.marstext, 'Visible', 'off');
    set(g.jupitertext, 'Visible', 'off');
    set(g.saturntext, 'Visible', 'off');
    set(g.uranustext, 'Visible', 'off');
    set(g.neptunetext, 'Visible', 'off');
    set(g.venustext, 'Visible', 'off');
    set(g.plutotext, 'Visible', 'off');

else
    set(g.suntext, 'Visible', 'on');
    set(g.earthtext, 'Visible', 'on');
    set(g.halleytext, 'Visible', 'on');
    set(g.mercurytext, 'Visible', 'on');
    set(g.marstext, 'Visible', 'on');
    set(g.jupitertext, 'Visible', 'on');
    set(g.saturntext, 'Visible', 'on');
    set(g.uranustext, 'Visible', 'on');
    set(g.neptunetext, 'Visible', 'on');
    set(g.venustext, 'Visible', 'on');
    set(g.plutotext, 'Visible', 'on');
    
end
    % update display
drawnow
return
