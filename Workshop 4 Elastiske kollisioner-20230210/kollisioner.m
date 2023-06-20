%% Introduktion
%Denne fil kan bruges til lave og køre modellen der arbejdes med i
%workshoppen "kolisioner". Denne model viser et antal boldes bevægelse i en
%beholder. Dette er sammenligneligt med molekylerne i en gas, eller
%kuglerne i et spil billiard.

%% Eksempel 1.
clf
rng('default')
nballs=12;
nsides=4;
A=Model(nsides,nballs,'equal');
A.run()

%% Eksempel 2.

clf
rng('default')
nballs=20;
nsides=100;
A=Model(nsides,nballs,'');
A.run()

%% Eksempel 3
clf
rng('default')
nballs=3;
nsides=5;
A=Model(nsides,nballs,'');
A.run()