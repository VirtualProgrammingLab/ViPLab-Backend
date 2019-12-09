function Aufgabe_1_Blatt_2()

  dx = 0.1;
  dy = 0.1;

  nx = 1 / dx - 1;
  ny = 1 / dy - 1;

  % Matrizen definieren
  x=zeros(nx,1);
  y=zeros(ny,1);
  A=zeros(nx*ny,nx*ny);
  r=zeros(nx*ny,1);

  % Gitterpositionen festlegen
  for i=1:nx
    x(i,1) = dx*i;
  end

  for j=1:ny
    y(j,1) = dx*j;
  end

  % Matrizen befuellen
  for j=1:ny
    for i=1:nx



      r(i+(j-1)*nx,1) = f(x(i,1),y(j,1));

      % Anteil des Elements selbst
      A(i+(j-1)*nx,i+(j-1)*nx) = -2/dx^2-2/dy^2;

      % rechter Nachbar
      if i < nx
        A(i+(j-1)*nx,i+1+(j-1)*nx) = 1/dx^2;
      else
        r(i+(j-1)*nx,1) = r(i+(j-1)*nx,1)-1/dx^2*g(x(i,1)+dx,y(j,1));
      end

      % linker Nachbar
      if i > 1 
        A(i+(j-1)*nx,i-1+(j-1)*nx) = 1/dx^2;
      else
        r(i+(j-1)*nx,1) = r(i+(j-1)*nx,1)-1/dx^2*g(x(i,1)-dx,y(j,1));
      end

      % oberer Nachbar
      if j < ny 
        A(i+(j-1)*nx,i+j*nx) = 1/dy^2;
      else
        r(i+(j-1)*nx,1) = r(i+(j-1)*nx,1)-1/dy^2*g(x(i,1),y(j,1)+dy);
      end

      % unterer Nachbar
      if j > 1 
        A(i+(j-1)*nx,i+(j-2)*nx) = 1/dy^2;
      else
        r(i+(j-1)*nx,1) = r(i+(j-1)*nx,1)-1/dy^2*g(x(i,1),y(j,1)-dy);
      end
    end
  end

  % LGS loesen
  u=GaussSeidel(A,r,nx,ny);

  % Loesung ausgeben
  visualize(u,nx,ny,dx,dy);

end


function u=GaussSeidel(A,r,nx,ny)

  % Konstanten definieren
  iter = 0;
  maxiter = 10000;
  eps = 1e-8;
  res = 2*eps;
  
  % Matrizen vorbereiten
  u=zeros(nx*ny,1);
  utilde=zeros(nx*ny,1);

  % Iterationsschleife, bis Abbruchbedingung erfuellt
  while iter<maxiter & res>eps
    iter = iter + 1;

    for i=1:nx*ny
      utilde(i,1)=r(i,1);
      for j=1:i-1
        utilde(i,1)=utilde(i,1)-A(i,j)*utilde(j,1);
      end
      for j=i+1:nx*ny
        utilde(i,1)=utilde(i,1)-A(i,j)*u(j,1);
      end
      utilde(i,1)=utilde(i,1)/A(i,i);
    end
    u = utilde;
    
    % Residuum berechnen
    res=max(abs(A*u-r));
  end
 
end


function f=f(x,y)
  f=sin(pi*x)*sin(pi*y);
end

function g=g(x,y)
  >+0.02*x+0.05*y;
end
