function int = trapezreglen(f,a,b,N)
%Funktion der approksimerer integralet int_a^b f(x) dx numerisk vha.
%trapezreglen.
n = 0;

for x = b+a/N : +a/N : N
    
    n = n + ((f(x) - f(x-1)) / 2) * (x - (x-1));
    
end

int = n;

end