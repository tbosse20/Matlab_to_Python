%% Delopgave 1
%I denne delopgave skal vi anvende funktionen log_transform fra delopgave
%1(iii)

figure
A=dlmread('delopgave1.txt');
getrangefromclass(A)
subplot(1,3,1)
imshow(A)
title('imshow(A)')
subplot(1,3,2)
imshow(A,[])
title('imshow(A,[])')
subplot(1,3,3)
imshow(log_transform(A,1/7))
title('imshow(log\_transform(A,1/7))')


%% Delopgave 3
%I denne opgave skal vi prøve at anvende de funktioner der er implementeret i
%.m-filen resize_image.m. Først skal vi have loaded de billeder vi skal 
%bruge. Disse er gemt som .txt dokumenter, men kan nemt hentes ind i
%matlab ved at bruge funktionen dlread.

A=dlmread('delopgave3_1.txt');
B=dlmread('delopgave3_2.txt');

%Vi får matlab til at vise de to billeder:
subplot(1,2,1)
imshow(A,'InitialMagnification','fit')
subplot(1,2,2)
imshow(B,'InitialMagnification','fit')

%A er et meget lille (16x16) billede. Hvis vi forstørre det ser vi hvad der
%sker når man anvender de forskellige interpolationsmetoder.

figure
scale=128;
subplot(1,3,1)
E=resize_image(A,scale,'nearest');
imshow(E,'InitialMagnification','fit')
subplot(1,3,2)
E=resize_image(A,scale,'linear');
imshow(E,'InitialMagnification','fit')
subplot(1,3,3)
E=resize_image(A,scale,'cubic');
imshow(E,'InitialMagnification','fit')

figure
scale=0.5;
subplot(1,3,1)
E=resize_image(A,scale,'nearest');
imshow(E,'InitialMagnification','fit')
subplot(1,3,2)
E=resize_image(A,scale,'linear');
imshow(E,'InitialMagnification','fit')
subplot(1,3,3)
E=resize_image(A,scale,'cubic');
imshow(E,'InitialMagnification','fit')

%Vi kan prøve at gøre noget lignende med B
scale=3.75;
figure
subplot(1,3,1)
E=resize_image(B,scale,'nearest');
imshow(E,'InitialMagnification','fit')
subplot(1,3,2)
E=resize_image(B,scale,'linear');
imshow(E,'InitialMagnification','fit')
subplot(1,3,3)
E=resize_image(B,scale,'cubic');
imshow(E,'InitialMagnification','fit')

scale=0.73;
figure
subplot(1,3,1)
E=resize_image(B,scale,'nearest');
imshow(E,'InitialMagnification','fit')
subplot(1,3,2)
E=resize_image(B,scale,'linear');
imshow(E,'InitialMagnification','fit')
subplot(1,3,3)
E=resize_image(B,scale,'cubic');
imshow(E,'InitialMagnification','fit')
