function blatt2_aufgabe1

A1=[2 -1 0; -1 2 -1; 0 -1 2]
A2=[1 1 0; 1 1 1; 0 1 0]
b=[0; 0; -1]

x1=GAUSS(A1,b)
disp('Probe: A1*x1 ='), disp(A1*x1)

x2=GAUSS(A2,b)
disp('Probe: A2*x2 ='), disp(A2*x2)

quit;
end % end of function

function [x] = GAUSS(A,b)
% function [x] = GAUSS(A,b)
% Gauss-Algorithmus (ohne Pivotisierung)
%
% Input:  A   Matrix in R^{n x n}
%           b   Vektor in R^{n}
% Output: x   Vektor in R^{n} - Loesung von Ax=b
%
% Der Gauss-Algorithmus ueberfuehrt das Gleichungssystem Ax=b in ein
% aequivalentes Gleichungssystem Rx=b, mit einer oberen Dreiecksmatrix
% R in R^{n x n}, dessen Loesung leichter berechnet werden kann.
% (Beachte: die rechten Seiten b sind nicht dieselben!)

n = length(b);
x = zeros(n,1);

% Elimination
for k = 1:(n-1)                 % k-ter Eliminationsschritt
  p = A(k,k);                   % k-tes Pivotelement
  if p==0
    error('Das System ist nicht loesbar. Das %d-te Pivotelement ist 0.',k)
  end
  for i = k+1:n                 % Spalte
    l = -A(i,k)/p;
    A(i,k) = 0;
    for j = k+1:n               % Zeile
      A(i,j) = A(i,j)+l*A(k,j); % j-te Zeile umformen
    end 
    b(i) = b(i)+l*b(k);         % rechte Seite umformen
  end
end

%  Rueckwaertseinsetzen
x(n) = b(n)/A(n,n);
for k = n-1:-1:1
  x(k) = (b(k)-A(k,k+1:n)*x(k+1:n))/A(k,k);
end
end % end of function
