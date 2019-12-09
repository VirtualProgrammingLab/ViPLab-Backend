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
  g>=1+0.02*x+0.05*y;
end
function [uexakt,xout,yout]=func_uexakt(dx,dy,nx,ny)

  xout=zeros(nx+2,1);
  yout=zeros(ny+2,1);
  uexakt=zeros(ny+2,nx+2);
  
  for i=1:nx+2
    xout(i,1) = dx*(i-1);
  end

  for j=1:ny+2
    yout(j,1) = dy*(j-1);
  end

  for j=1:ny+2
    for i=1:nx+2
      uexakt(j,i) = -1/(2*pi^2)*sin(pi*xout(i,1))*...
            sin(pi*yout(j,1))+0.02*xout(i,1)+0.05*yout(j,1)+1;
    end
  end

end

function visualize(u,nx,ny,dx,dy)

  nLevels = 21;

  [uexakt,xout,yout]=func_uexakt(dx,dy,nx,ny);

  uout=zeros(ny+2,nx+2);
  uout = uexakt;
  uout(2:ny+1,2:nx+1) = transpose(reshape(u,nx,ny));
  
  minval=min(min(min(uout)),min(min(uexakt)));
  maxval=max(max(max(uout)),max(max(uexakt)));

  figure();
  [xplot,yplot,typeplot,lineLengthTotal,levelValue]=createIsoLines(xout,yout,uout,minval,maxval,nLevels);
  plotIsolines(xplot,yplot,typeplot,lineLengthTotal);
  title('u');
  xlabel('x');
  ylabel('y');
  
  figure();
  [xplot,yplot,typeplot,lineLengthTotal,levelValue]=createIsoLines(xout,yout,uexakt,minval,maxval,nLevels);
  plotIsolines(xplot,yplot,typeplot,lineLengthTotal);
  title('u_exakt');
  xlabel('x');
  ylabel('y');
end

function [xplot,yplot,typeplot,lineLengthTotal,levelValue]=createIsoLines(x,y,uin,minval,maxval,nLevels)

  u=zeros(size(uin,1),size(uin,2),2);
  u(:,:,1) = uin;
  u(:,:,2) = uin;

  nLinesTotal=0;
  levelValue=zeros(nLevels,1);
  maxLineLength=0;

  for iLevel=1:nLevels
    levelValue(iLevel,1)=minval+iLevel*(maxval-minval)/(nLevels+1);
    [f,v]=isosurface(x,y,[0 1],u,levelValue(iLevel,1));

    f=f(find(sum(reshape(v(f,3),size(f)),2)==1),:);
    f=f.*reshape(1-v(f,3),size(f));
    f=sort(f,2);
    f=f(:,2:3);

    n=size(f,1);
    lineEnd = zeros(n,1);

    nLines=0;
    i=1;
    currentstart=f(i,1);
    while i<n
      if any(any(f(i+1:n,:)==f(i,2)))
        for j=i+1:n
          if any(f(j,:)==f(i,2))
            rdummy = f(j,:);
            if f(j,1)==f(i,2)
              f(j,:)=f(i+1,:);
              f(i+1,:)=rdummy;
            else
              f(j,:)=f(i+1,:);
              f(i+1,2)=rdummy(1,1);
              f(i+1,1)=rdummy(1,2);
            end
            if f(i+1,2)==currentstart
              nLines=nLines+1;
              lineEnd(nLines,1) = i+1;
              currentstart=f(min(i+2,n),1);
              i=i+2;
            else
              i=i+1;
            end
            break
          end
        end
      else
        nLines=nLines+1;
        lineEnd(nLines,1) = i;
        currentstart=f(i+1,1);
        i=i+1;
      end
    end
    if i==n
      nLines=nLines+1;
      lineEnd(nLines,1) = i;
    end

    if lineEnd(nLines)~=n
      nLines=nLines+1;
      lineEnd(nLines,1) = n;
    end

    lineEnd = lineEnd(1:nLines,1);

    lineLength=zeros(nLines,1);
    lineLength(1,1) = lineEnd(1,1)+1;
    lineLength(2:nLines,1) = lineEnd(2:nLines)-lineEnd(1:nLines-1)+1;

    points = zeros(nLines,n);
    for i=1:nLines
      points(i,1:lineLength(i,1)-1) = f(lineEnd(i,1)-lineLength(i,1)+2:lineEnd(i,1),1);
      points(i,lineLength(i,1)) = f(lineEnd(i,1),2);
    end

    for h=1:nLines
      for i=1:nLines
        for j=i+1:nLines
          if points(i,1)==points(j,1) & points(i,1)~=0;
            points(i,lineLength(j,1):lineLength(i,1)+lineLength(j,1)-1)=points(i,1:lineLength(i,1));
            for k=1:lineLength(j,1)-1
              points(i,k)=points(j,lineLength(j,1)-k+1);
            end
            points(j,:)=0;
            lineLength(i,1)=lineLength(i,1)+lineLength(j,1)-1;
            lineLength(j,1)=0;
          end
          if(lineLength(j,1)>0)
            if points(i,1)==points(j,lineLength(j,1)) & points(i,1)~=0;
              points(i,lineLength(j,1):lineLength(i,1)+lineLength(j,1)-1)=points(i,1:lineLength(i,1));
              points(i,1:lineLength(j,1)-1)=points(j,1:lineLength(j,1)-1);
              points(j,:)=0;
              lineLength(i,1)=lineLength(i,1)+lineLength(j,1)-1;
              lineLength(j,1)=0;
            end
          end
        end
      end
    end

    points=sortrows(points,-1);
    nLines=size(find(points(:,1)~=0),1);

    nLinesTotal=nLinesTotal+nLines;
    maxLineLength=max(maxLineLength,max(lineLength));
  end

  xplot=zeros(nLinesTotal,maxLineLength);
  yplot=zeros(nLinesTotal,maxLineLength);
  typeplot=zeros(nLinesTotal,1);
  lineLengthTotal=zeros(nLinesTotal,1);

  nLinesTotal=0;
  for iLevel=1:nLevels
    [f,v]=isosurface(x,y,[0 1],u,levelValue(iLevel,1));

    f=f(find(sum(reshape(v(f,3),size(f)),2)==1),:);
    f=f.*reshape(1-v(f,3),size(f));
    f=sort(f,2);
    f=f(:,2:3);

    n=size(f,1);
    lineEnd = zeros(n,1);

    nLines=0;
    i=1;
    currentstart=f(i,1);
    while i<n
      if any(any(f(i+1:n,:)==f(i,2)))
        for j=i+1:n
          if any(f(j,:)==f(i,2))
            rdummy = f(j,:);
            if f(j,1)==f(i,2)
              f(j,:)=f(i+1,:);
              f(i+1,:)=rdummy;
            else
              f(j,:)=f(i+1,:);
              f(i+1,2)=rdummy(1,1);
              f(i+1,1)=rdummy(1,2);
            end
            if f(i+1,2)==currentstart
              nLines=nLines+1;
              lineEnd(nLines,1) = i+1;
              currentstart=f(min(i+2,n),1);
              i=i+2;
            else
              i=i+1;
            end
            break
          end
        end
      else
        nLines=nLines+1;
        lineEnd(nLines,1) = i;
        currentstart=f(i+1,1);
        i=i+1;
      end
    end
    if i==n
      nLines=nLines+1;
      lineEnd(nLines,1) = i;
    end

    if lineEnd(nLines)~=n
      nLines=nLines+1;
      lineEnd(nLines,1) = n;
    end

    lineEnd = lineEnd(1:nLines,1);

    lineLength=zeros(nLines,1);
    lineLength(1,1) = lineEnd(1,1)+1;
    lineLength(2:nLines,1) = lineEnd(2:nLines)-lineEnd(1:nLines-1)+1;

    points = zeros(nLines,n);
    for i=1:nLines
      points(i,1:lineLength(i,1)-1) = f(lineEnd(i,1)-lineLength(i,1)+2:lineEnd(i,1),1);
      points(i,lineLength(i,1)) = f(lineEnd(i,1),2);
    end

    for h=1:nLines
      for i=1:nLines
        for j=i+1:nLines
          if points(i,1)==points(j,1) & points(i,1)~=0;
            points(i,lineLength(j,1):lineLength(i,1)+lineLength(j,1)-1)=points(i,1:lineLength(i,1));
            for k=1:lineLength(j,1)-1
              points(i,k)=points(j,lineLength(j,1)-k+1);
            end
            points(j,:)=0;
            lineLength(i,1)=lineLength(i,1)+lineLength(j,1)-1;
            lineLength(j,1)=0;
          end
          if(lineLength(j,1)>0)
            if points(i,1)==points(j,lineLength(j,1)) & points(i,1)~=0;
              points(i,lineLength(j,1):lineLength(i,1)+lineLength(j,1)-1)=points(i,1:lineLength(i,1));
              points(i,1:lineLength(j,1)-1)=points(j,1:lineLength(j,1)-1);
              points(j,:)=0;
              lineLength(i,1)=lineLength(i,1)+lineLength(j,1)-1;
              lineLength(j,1)=0;
            end
          end
        end
      end
    end

    points=sortrows(points,-1);
    nLines=size(find(points(:,1)~=0),1);
    points=points(1:nLines,1:max(lineLength));
    lineLength=0;

    for i=1:nLines
      lineLength=size(find(points(i,:)~=0),2);
      xplot(nLinesTotal+i,1:lineLength)=v(points(i,1:lineLength),1);
      yplot(nLinesTotal+i,1:lineLength)=v(points(i,1:lineLength),2);
      typeplot(nLinesTotal+i,1)=iLevel;
      lineLengthTotal(nLinesTotal+i,1)=lineLength;
    end
    nLinesTotal=nLinesTotal+nLines;

  end
  clear f v points lineEnd lineLength;

end

function plotIsolines(xplot,yplot,typeplot,lineLengthTotal)

  nLinesTotal=size(xplot,1);

  for i=1:nLinesTotal
    switch typeplot(i,1)
      case 1
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),'-c');
      case 6
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),'-m');
      case 11
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),'-r');
      case 16
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),'-g');
      case 21
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),'-b');
      otherwise
        plot(xplot(i,1:lineLengthTotal(i,1)),yplot(i,1:lineLengthTotal(i,1)),':k');
    end      
    hold on;
  end
  hold off;

end


%%%
% Overwrites the built-in plot functions and gives out
% a ViPLab graphic format file (.vgf).
%
% Usage: Paste this file in the same file below your program. Be
%        aware of using "end" for every of your functions.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010 - 2011)
%
% Copyright: All rights reserved C. Grüninger 2010 - 2011
%            This functions are licenced under the terms
%            of GNU GPL 3 or higher.
% Version: 2011-07-13
%%%


%%%
% It behaves similar to built-in plot function except
% that complex values are forbitten and X values must
% be provided for every plot.
% 
% The arguments are X, Y and an optional LineSpec. These
% two or three arguments can be appended multiple times.
% X contains the x-values of the points, Y the y-values.
% Consecutive points are drawn connected by a line.
% X and Y must have one matching dimension if at least
% one is a vector and must have the exact same dimension
% if both are matrices.
function plot(X, Y, varargin)
	% ensure valid arguments
	assert(not(isempty(X)), 'X must not be empty.');
	assert(not(isempty(Y)), 'Y must not be empty.');
	assert(isnumeric(X), 'X must be numeric.');
	assert(isnumeric(Y), 'Y must be numeric.');
	assert(not(isscalar(X)) || isvector(Y), 'If X is scalar Y must be a vector.');
	assert(not(isvector(X) && not(isscalar(X)) && isvector(Y)) || (length(X) == length(Y)), 'Vectors X and Y must have same dimensions.');
	assert(not(isvector(X) && not(isscalar(X)) && size(Y, 1) > 1 && size(Y, 2) > 1) || (length(X) == size(Y, 1) || length(X) == size(Y, 2)), 'Vector X and matrix Y must have one dimension in common.');
	assert(not(size(X, 1) > 1 && size(X, 2) > 1 && isvector(Y)) || (size(X, 1) == length(Y) || size(X, 2) == length(Y)), 'Matrix X and vector Y must have one dimension in common.');
	assert(not(size(X, 1) > 1 && size(X, 2) > 1 && size(Y, 1) > 1 && size(Y, 2) > 1) || isequal(size(X),size(Y)), 'Matrices X and Y must have same dimensions.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% handle optional arguments
	LineSpec = 'b-';
	newArgIn = {};
	% if first optional argument is a string, it's the line specification
	if (size(varargin, 2) == 1) && ischar(varargin{1})
		LineSpec = varargin{1};
	% pass remaining optional arguments to next plot call
	elseif (size(varargin, 2) > 1) && ischar(varargin{1})
		LineSpec = varargin{1};
		newArgIn = varargin(2:size(varargin, 2));
	elseif (size(varargin, 2) > 0)
		newArgIn = varargin;
	end; %if

	%%%
	% write symbol, linestyle and color data
	if not(isempty(LineSpec))
		% write color data
		if not(isempty(strfind(LineSpec, 'r')))
			fprintf(plot_file, '# color 255 0 0\n');
		elseif not(isempty(strfind(LineSpec, 'b')))
			fprintf(plot_file, '# color 0 0 255\n');
		elseif not(isempty(strfind(LineSpec, 'g')))
			fprintf(plot_file, '# color 0 255 0\n');
		elseif not(isempty(strfind(LineSpec, 'c')))
			fprintf(plot_file, '# color 0 255 255\n');
		elseif not(isempty(strfind(LineSpec, 'm')))
			fprintf(plot_file, '# color 255 0 255\n');
		elseif not(isempty(strfind(LineSpec, 'y')))
			fprintf(plot_file, '# color 255 255 0\n');
		elseif not(isempty(strfind(LineSpec, 'k')))
			fprintf(plot_file, '# color 0 0 0\n');
		elseif not(isempty(strfind(LineSpec, 'w')))
			fprintf(plot_file, '# color 255 255 255\n');
		else
			fprintf(plot_file, '# color 0 0 0\n');
		end; %if
		
		% write symbol data
		noSymbolGiven = false;
		if not(isempty(strfind(LineSpec, 'x')))
			fprintf(plot_file, '# symbol x\n');
		elseif not(isempty(strfind(LineSpec, '*')))
			fprintf(plot_file, '# symbol *\n');
		elseif not(isempty(strfind(LineSpec, '.')))
			fprintf(plot_file, '# symbol .\n');
		elseif not(isempty(strfind(LineSpec, '+')))
			fprintf(plot_file, '# symbol +\n');
		elseif not(isempty(strfind(LineSpec, 'v')))
			fprintf(plot_file, '# symbol v\n');
		elseif not(isempty(strfind(LineSpec, '^')))
			fprintf(plot_file, '# symbol ^\n');
		elseif not(isempty(strfind(LineSpec, 'o')))
			fprintf(plot_file, '# symbol o\n');
		elseif not(isempty(strfind(LineSpec, 's')))
			fprintf(plot_file, '# symbol s\n');
		elseif not(isempty(strfind(LineSpec, 'd')))
			fprintf(plot_file, '# symbol d\n');
		elseif and(not(isempty(strfind(LineSpec, '.'))), isempty(strfind(LineSpec, '-.')))
			fprintf(plot_file, '# symbol .\n');
		else
			fprintf(plot_file, '# symbol none\n');
			noSymbolGiven = true;
		end; %if
		
		% write line style data
		if not(isempty(strfind(LineSpec, '--')))
			fprintf(plot_file, '# linestyle dashed\n');
		elseif not(isempty(strfind(LineSpec, '-.')))
			fprintf(plot_file, '# linestyle dash-dot\n');
		elseif not(isempty(strfind(LineSpec, ':')))
			fprintf(plot_file, '# linestyle dotted\n');
		elseif not(isempty(strfind(LineSpec, '-')))
			fprintf(plot_file, '# linestyle solid\n');
		else
			% if no symbol is given the line must be solid
			if noSymbolGiven
				fprintf(plot_file, '# linestyle solid\n');
			else
				fprintf(plot_file, '# linestyle none\n');
			end; %if
		end; %if
	end; %if
	
	%%%
	% write plot data
	
	% if X is a scalar => Y a vector
	if isscalar(X)
		for i=1:length(Y)
			fprintf(plot_file, '%f %f %f %f\n', X(1), Y(i), X(1), Y(i));
		end; %for
	% if both X and Y are vectors
	elseif isvector(X) && isvector(Y)
		for i=1:(length(X)-1)
			fprintf(plot_file, '%f %f %f %f\n', X(i), Y(i), X(i+1), Y(i+1));
		end; %for
	% if X is a vector and Y a matrix
	elseif isvector(X) && size(Y, 1) > 1 && size(Y, 2) > 1
		% rotate matrix Y to match dimensions
		if length(X) ~= size(Y, 2)
			Y = Y';
		end;% if
		for j=1:size(Y, 1)
			for i=1:(length(X)-1)
				fprintf(plot_file, '%f %f %f %f\n', X(i), Y(j, i), X(i+1), Y(j, i+1));
			end; %for
		end; %for
	% if X is a matrix and Y a vector
	elseif size(X, 1) > 1 && size(X, 2) > 1 && isvector(Y)
		% rotate matrix X to match dimensions
		if size(X, 2) ~= length(Y)
			X = X';
		end;% if
		for j=1:size(X, 1)
			for i=1:(length(Y)-1)
				fprintf(plot_file, '%f %f %f %f\n', X(j, i), Y(i), X(j, i+1), Y(i+1));
			end; %for
		end; %for
	% if both X and Y are matrices
	else % size(X, 1) > 1 && size(X, 2) > 1 && size(Y, 1) > 1 && size(Y, 2) > 1)
		for i=1:size(X, 2)
			for j=1:(size(X, 1)-1)
				fprintf(plot_file, '%f %f %f %f\n', X(j, i), Y(j, i), X(j+1, i), Y(j+1, i));
			end; %for
		end; %for
	end; %if
	
	% close file
	fclose(plot_file);
	
	%%%
	% recursivly call plot to work off remaining optional arguments
	if size(newArgIn, 2) == 0
		return;
	end; %if
	
	assert(size(newArgIn, 2) >= 2, 'Wrong number of arguments, expected more arguments.');
	
	plot(newArgIn{1:size(newArgIn, 2)});
end %function

%%%
% Plots with two logarithmic scales.
% Only positive numbers are allowed to be plotted.
%%%
function loglog(X, Y, varargin)
	% ensure valid arguments
	% no error but ignore complete loglog call if non-positive numbers found
	if (and(min(min(X)) > 0.0, min(min(Y)) > 0.0))
		plot(X, Y, varargin{:});
		
		% open file to append
		plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
		
		% write loglog mode
		fprintf(plot_file, '# scale log-log\n');
		
		% close file
		fclose(plot_file);
	end; %if
end %function

%%%
% Plots with logarithmic scale for x.
% Only positive arguments are allowed to be plotted for x-values.
%%%
function semilogx(X, Y, varargin)
	% ensure valid arguments
	% no error but ignore complet loglog call if non-positive numbers found
	if (min(min(X)) > 0.0)
		plot(X, Y, varargin{:});
		% open file to append
		plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
		
		% write loglog mode
		fprintf(plot_file, '# scale log-lin\n');
		
		% close file
		fclose(plot_file);
	end; %if
end %functions

%%%
% Plots with logarithmic scale for y.
% Only positive arguments are allowed to be plotted for y-values.
%%%
function semilogy(X, Y, varargin)
	% ensure valid arguments
	% no error but ignore complet loglog call if non-positive numbers found
	if (min(min(Y)) > 0.0)
		plot(X, Y, varargin{:});
		% open file to append
		plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
		
		% write loglog mode
		fprintf(plot_file, '# scale lin-log\n');
		
		% close file
		fclose(plot_file);
	end; %if
end %function

%%%
% Surpress built-in hold funtion.
%%%
function hold(varargin)
	% do nothing
end %function

%%%
% Set plot legend. To stay compatible write all legends 
% after plotting.
% 
% The arguments must be strings. It does not support
% handles or orientation.
%%%
function legend(varargin)
	% ensure valid arguments
	for k = 1:size(varargin, 2);
		assert(ischar(varargin{k}), sprintf('%i All arguments in legend must be strings.', k));
	end; %for
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write legend data
	fprintf(plot_file, '# legend ');
	for k = 1:(size(varargin, 2) - 1);
		fprintf(plot_file, '%s,', varargin{k});
	end; %for
	fprintf(plot_file, '%s\n', varargin{size(varargin, 2)});
	
	% close file
	fclose(plot_file);
end %function

%%%
% Adds the title to the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%%%
function title(PlotTitle, varargin)
	% ensure valid arguments
	assert(ischar(PlotTitle), 'First argument in title must be a string.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write title data
	fprintf(plot_file, '# title %s\n', PlotTitle);
	
	% close file
	fclose(plot_file);
end %function

%%%
% Set x-range of visible part of the plot.
%%%
function xlim(xmin, xmax, varargin)
	% ensure valid arguments
	assert(isreal(xmin) && isreal(xmax), 'All arguments must be real numbers.');
	assert(isscalar(xmin) && isscalar(xmax), 'All arguments must be scalars.');
	assert(xmin < xmax, 'xmin must be smaller than xmax.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write axis data
	fprintf(plot_file, '# x-range %f %f\n', xmin, xmax);
	
	% close file
	fclose(plot_file);
end %function

%%%
% Set y-range of visible part of the plot.
%%%
function ylim(ymin, ymax, varargin)
	% ensure valid arguments
	assert(isreal(ymin) && isreal(ymax), 'All arguments must be real numbers.');
	assert(isscalar(ymin) && isscalar(ymax), 'All arguments must be scalars.');
	assert(ymin < ymax, 'ymin must be smaller than ymax.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write axis data
	fprintf(plot_file, '# y-range %f %f\n', ymin, ymax);
	
	% close file
	fclose(plot_file);
end %function

%%%
% Adds a new plot frame.
%%%
function figure(varargin)
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write command
	fprintf(plot_file, '# newframe\n');
	
	% close file
	fclose(plot_file);
end %function

%%%
% Add a label to the X-axis of the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%%%
function xlabel(AxisTitle, varargin)
	% ensure valid arguments
	assert(ischar(AxisTitle), 'First argument in title must be a string.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write title data
	fprintf(plot_file, '# x-label %s\n', AxisTitle);
	
	% close file
	fclose(plot_file);
end %function

%%%
% Add a label to the Y-axis of the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%%%
function ylabel(AxisTitle, varargin)
	% ensure valid arguments
	assert(ischar(AxisTitle), 'First argument in title must be a string.');
	
	% open file to append
	plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');
	
	% write title data
	fprintf(plot_file, '# y-label %s\n', AxisTitle);
	
	% close file
	fclose(plot_file);
end %function
