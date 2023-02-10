function [A2]=resize_image(A,scale,method)
%Denne funktion skalerer et billede med en faktor givet af variablen scale.
%Der kan anvendes f�lgende metoder:
% 'nearest': N�rmeste nabo interpolation
% 'linear' : Line�r interpolation
% 'cubic'  : Kubisk Hermite interpolation
%
%

%Vi bestemmer f�rste st�rrelsen af det skalerede billede ud fra st�rrelsen
%af A
[m,n]=size(A);
new_cols=round(scale*n);
new_rows=round(scale*m);
%Vi interpolerer nu r�kkerne
A1=unit_step_row_interpolate(A,new_cols,method);
%Og til sidst interpolerer vi s�jlerne
A2=unit_step_column_interpolate(A1,new_rows,method);
end

function A1=unit_step_row_interpolate(A,new_cols,method)
    % I denne funktion interpolerer vi r�kkerne i matricen A. S�ledes at
    % hvis A er en m x n matrix s� er den resulterende matrix A1 en m x
    % new_cols
    %
    %
    %
    %
    %
    [m,n]=size(A);
    %Vi laver en matrix X som er m x new_cols og hvor r�kkerne alle sammen
    %er p� formen [1, 1+(n-1)/(new_cols-1),..., n]
    X=repmat(linspace(1,n,new_cols),m,1);
    %Hvis n�rmeste nabo interpolation er valgt:
    if strcmp(method,'nearest')
        %Indgangene i X afrundes til n�rmeste heltal
        X=round(X);
        %Vi t�ller hvor mange gange s�jlerne i X gentages
        repvec=histcounts(X(1,:),1:n+1);
        %Vi gentager s�jlerne i A i forhold til hvor mange gange
        %tilsvarende s�jle gentages i X.
        A1=repelem(A,1,repvec);
    else
        %Hvis ikke n�rmeste nabo interpolation er valgt skal vi udregne
        %de interpolerede v�rdier. 
        
        %Vi definerer en m x n matrix hvor s�jle j er givet ved
        %[j;j;j;...;j]
        AX=repmat(1:n,m,1);
        %Vi skal nu bestemme hvor mange v�rdier i X's r�kker der falder
        %intervallerne [1,2), [2,3), osv. Ud fra dette laver vi en matrix k
        %hvor hver r�kke er p� formen [1,1,1,dots,1,2,2,dots,2,dots,n] hvor
        %j gentages lige s� mange gange som X har v�rdier der falder i
        %intervallet [j,j+1).
        k=ones(1,new_cols);
        repvec=zeros(1,n-1);
        n_zeros=0;
        for j = 2:n-1
            idx=AX(1,j)<=X(1,:);
            repvec(j-1)=nnz(~idx)-n_zeros;
            n_zeros=nnz(~idx);
            k(AX(1,j)<=X(1,:))=j;
        end
        repvec(end)=new_cols-n_zeros;
        k=repmat(k,m,1);
        %Vi definerer nu variablen s hvor indgangene i hver r�kke svarer
        %svarer til x-x_j i workshoppen.
        s=X-k;

        %Vi definerer nu y-koefficienterne. Bem�rk at disse er matricer.
        y0=[A(:,1), A(:,1:end-2)];
        y1=A(:,1:end-1);
        y2=A(:,2:end);
        y3=[A(:,3:end),A(:,end)];


        %Hvis line�r interpolation er valgt:
        if strcmp(method,'linear')
            %Vi definerer a og b som de er i delopgave 2(iii).
            a=y2-y1;
            b=y1;
            %Vi udvider nu koefficienterne s� der er en koefficient til
            %hver indgang i matricen X.
            a=repelem(a,1,repvec);
            b=repelem(b,1,repvec);
            %Vi udregner den resulterence matrix ved at anvende
            %indgangsvise matrixoperationer. Dette er hurtigere end at
            %anvende for-loops.
            A1=a.*s+b;

        else
            %Hvis kubisk Hermite interpolation anvendes:
            error('kubisk Hermite interpolation er endnu ikke implementeret')
        end   
    
    end
end

function A2 = unit_step_column_interpolate(A1,new_rows,method)
% I denne funktion interpolerer vi s�jlerne i matricen A1. S�ledes at
% hvis A1 er en m x n matrix s� er den resulterende matrix A1 en
% new_rows x n matrix.      
error('Denne funktion er endnu ikke implementeret')

end