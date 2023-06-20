from Model import Model

## Introduktion
#Denne fil kan bruges til lave og køre modellen der arbejdes med i
#workshoppen "kolisioner". Denne model viser et antal boldes bevægelse i en
#beholder. Dette er sammenligneligt med molekylerne i en gas,  eller
#kuglerne i et spil billiard.

## Eksempel 1.
nballs = 5
nsides = 4
A = Model(nsides, nballs, 'equal')
A.run()

## Eksempel 2.

nballs = 20
nsides = 100
A = Model(nsides, nballs, '')
A.run()

## Eksempel 3
nballs = 3
nsides = 5
A = Model(nsides, nballs, '')
A.run()