function callGAUSS

% Aufruf von GAUSS

A=hilb(5);
b=ones(1,5);

[x] = GAUSS(A,b)

quit
function [x] = GAUSS(A,b)

% function [x] = GAUSS(A,b)
% Gauss-Algorithmus (ohne Pivotisierung)
%
% Input:  A   Matrix in IR^{n x n}
%         b   Vektor in IR^{n}
% Output: x   Vektor in IR^{n} - Lösung von Ax=b
%
% Der Gauss-Algorithmus ueberfuehrt das Gleichungssystem Ax=b in ein
% aequivalentes Gleichungssystem Rx=b, mit einer oberen Dreiecksmatrix
% R in IR^{n x n}, dessen Loesung leichter berechnet werden kann.
% (Beachte: die rechten Seiten b sind nicht dieselben!)
%
%
%
% Schreiben Sie ab hier den Funktions-Code.

%%% Init %%%
n = length(b);
x = zeros(n,1);

%%%%%%%%%%%%%%%%%%%%%%%   Elimination   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for k = 1:(n-1)                         % k-ter Eliminationsschritt
    p = A(k,k);                         % k-tes Pivotelement
    if p==0
        error('Das System ist nicht loesbar. Das %d-te Pivotelement ist 0.',k)
    end
    for i = k+1:n                       % Spalte
       l = -A(i,k)/p;
       A(i,k) = 0;
       for j = k+1:n                    % Zeile
          A(i,j) = A(i,j)+l*A(k,j);     % j-te Zeile umformen
       end 
       b(i) = b(i)+l*b(k);              % rechte Seite umformen
    end
end

%%%%%%%%%%%%%%%%%%%%%%%   Rückwärtseinsetzen   %%%%%%%%%%%%%%%%%%%%%%%%%%%%
x(n) = b(n)/A(n,n);
for k = (n-1):-1:1                      % zeilenweise von unten nach oben 
                                      % nach den Unbekannten auf der 
                                      % Diagonalen aufl?sen
   c = 0;
   for j = (k+1):n
      c = c+A(k,j)*x(j);
      x(k) = (b(k)-c)/A(k,k);
   end
end
