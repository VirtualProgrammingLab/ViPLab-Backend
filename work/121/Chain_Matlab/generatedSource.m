% =====================================
function interpolation();
% =====================================
fprintf('PROGRAMM START...\n');
clear global;
% interpolates a function g(x) using in C=[-1;1]
% with polynomial degree N using
Nin=5;
% mode=1 regular grid points
% mode=2 GLL grid points
% mode=3 Gauss grid points
% mode=4 'bad' grid points inside C
% mode=5 'bad' grid points one -sided
% mode=6 Chebyshev nodes
% mode=7 Chebyshev Lobatto nodes
mode=1;
% plotmode=1 plots function and its interpolant
% plotmode=2 additionally plots the Lagrange functions
plotmode=1;

% Print chosen parameters
fprintf('Nin      = %d\n',Nin);
fprintf('mode     = %d\n',mode);
fprintf('plotmode = %d\n\n',plotmode);

global wBary; % Barycentric weights for Lagrange interpolation 
global GPPos1D; % Interpolation points
global N; % Polynomial degree of interpolation

N=Nin; % Polynomial degree for the interpolation
% For visualization and to determine Linf and Lebesgue constant
NVisu=1000; % Number of sample points,
  
% Initialize Linf error and Lebesgue constant
Linf=0;
Lebesgue=0;

% Choose the type of interpolation points
if (mode==1)      % Regular
  GPPos1D = linspace(-1,1,N+1)';
elseif (mode==2)  % Gauss Lobatto
  [GPPos1D,GPWeight1D]=lglnodes(N);
elseif (mode==3)  % Gauss points
  [GPPos1D,GPWeight1D]=JacobiGQ(0,0,N);
elseif (mode==4)  % 'bad points' inside C
  GPPos1D = linspace(-0.5,0.5,N+1)';
elseif (mode==5)  % 'bad points' one -sided
  GPPos1D = linspace(-1.,0.7,N+1)';
  GPPos1D(N+1)=1;
elseif (mode==6)  % Chebyshev nodes
  for j=1:N+1
    GPPos1D(j,1) = cos((2*j-1)*pi/2/(N+1));
  end
elseif (mode==7)  % Chebyshev Lobatto nodes
  for j=1:N+1
    GPPos1D(j,1) = cos((j-1)*pi/(N));
  end 
end

% Compute barycentric weights for lagrange interpolation
% Kopriva, Algorithm 30, pg. 75
wBary=ones(N+1,1);
for j = 2:N+1
 for k = 1:j-1
   wBary(k) = wBary(k)*(GPPos1D(k)-GPPos1D(j));
   wBary(j) = wBary(j)*(GPPos1D(j)-GPPos1D(k));
 end
end
wBary = 1 ./ wBary;

% Determine the position of the regular sample points
VisuPos1D=linspace(-1,1,NVisu);
% Evaluate all Lagrange functions at each sample point
VisuMat=LagrangeInterpolatingPolynomials(VisuPos1D).';

% Determine the nodal values of the function g(x) at the interpolation
% points x_j
g_j = exactfunction(GPPos1D);
% Determine the function g(x) at the sample points 
g_exa_j=exactfunction(VisuPos1D)'; 
% Interpolate the polynomial approximation to the sample points
g_int_j = VisuMat*g_j;

% Determine the maximum value of the interpolation (for visualization)
g_max=ceil(max(abs(g_int_j)));

% Linf = max | g_exact - g_int|
Linf = max(abs(g_int_j-g_exa_j));
% Determine the Lebesgue constant 
for j=1:NVisu
    % = \sum\limits_j=1^(N+1) | \psi_j(x_visu) |
    Lebesgue_j = sum(abs(VisuMat(j,:)));
    % Determine the maximum for all sample points
    Lebesgue = max(Lebesgue,Lebesgue_j);
end

% Visualization of the interpolation, the exact function and the
% interpolation grid
if (plotmode>=1)
  figure;
  plot(VisuPos1D,g_int_j,'b',VisuPos1D,g_exa_j,'r',[GPPos1D';GPPos1D'],[-g_max;g_max]*ones(1,N+1),'k');
  title('Darstellung der exakten Funktion und ihrer Interpolierenden','FontSize',14);
  axis([-1 1 -g_max g_max])
end
% Plot the Lagrange functions
if (plotmode>=2)
    figure;
  for j=1:N+1
      f_j=zeros(N+1,1);
      f_j(j)=1;
      % Interpolate the polynomial approximation to the sample points
      f_int_j = VisuMat*f_j;
      g_max=ceil(max(g_max,max(abs(f_int_j))));
      plot(VisuPos1D,f_int_j);
      hold on;
  end
  % plot position of interpolation points
  plot([GPPos1D';GPPos1D'],[-g_max;g_max]*ones(1,N+1),'k');
  title('Darstellung der Lagrange Polynome','FontSize',14);
  axis([-1 1 -g_max g_max])
  hold off;  
end
% Print results
fprintf('Linf     = %e\n',Linf);
fprintf('Lebesgue = %e\n',Lebesgue);
fprintf('=======================\n');
end

% =====================================


% =====================================
% SUBFUNCTIONS
% =====================================


% =====================================
function [g]=exactfunction(x);
% =====================================
% L_2([-1;1]) function g(x)

% C_inf Function: 'leicht'
g=sin(pi*x)+cos(pi*x);

% Runge Function: 'schwer'
%g=1./(1+(x*5).^2);

% Large scale + small scale
%g=sin(pi*x)+cos(4*pi*x)*0.01;
end
% =====================================


% =====================================
function [x,w]=lglnodes(N);
% =====================================
% Truncation + 1
N1=N+1;
% Use the Chebyshev-Gauss-Lobatto nodes as the first guess
x=cos(pi*(0:N)/N)';
% The Legendre Vandermonde Matrix
P=zeros(N1,N1);
% Compute P_(N) using the recursion relation
% Compute its first and second derivatives and 
% update x using the Newton-Raphson method.
xold=2;
while max(abs(x-xold))>eps
    xold=x;        
    P(:,1)=1;    P(:,2)=x;    
    for k=2:N
        P(:,k+1)=( (2*k-1)*x.*P(:,k)-(k-1)*P(:,k-1) )/k;
    end     
    x=xold-( x.*P(:,N1)-P(:,N) )./( N1*P(:,N1) );             
end
w=2./(N*N1*P(:,N1).^2);
end
% =====================================


% =====================================
function [x,w] = JacobiGQ(alpha,beta,N);
% =====================================
% Purpose: Compute the N'th order Gauss quadrature points, x, 
%          and weights, w, associated with the Jacobi 
%          polynomial, of type (alpha,beta) > -1 ( <> -0.5).

if (N==0) x(1)=(alpha-beta)/(alpha+beta+2); w(1) = 2; return; end;
% Form symmetric matrix from recurrence.
J = zeros(N+1);
h1 = 2*(0:N)+alpha+beta;
J = diag(-1/2*(alpha^2-beta^2)./(h1+2)./h1) + ...
    diag(2./(h1(1:N)+2).*sqrt((1:N).*((1:N)+alpha+beta).*...
    ((1:N)+alpha).*((1:N)+beta)./(h1(1:N)+1)./(h1(1:N)+3)),1);
if (alpha+beta<10*eps) J(1,1)=0.0;end;
J = J + J';

%Compute quadrature by eigenvalue solve
[V,D] = eig(J); x = diag(D);
w = (V(1,:)').^2*2^(alpha+beta+1)/(alpha+beta+1)*gamma(alpha+1)*...
    gamma(beta+1)/gamma(alpha+beta+1);
end
% =====================================


% =====================================
function [L]=LagrangeInterpolatingPolynomials(x)
% =====================================
%  evaluates the lagrange basis functions at x
%  algorithm 34, page 77

% load global variables
global wBary;
global GPPos1D;
global N;

% make sure x is a row vector
x=x(:).';
L=zeros(N+1,length(x));

% look if x is an interpolation point
Lindex=[];
for k=1:N+1
  index=find(x==GPPos1D(k));
  if (index)
    L(k,index)=1;
    Lindex=[Lindex,index];
  end
end

% else compute the interpolated value of the basis functions
Lindex=setdiff(1:length(x),Lindex);
if (Lindex)
  s=0;
  for k=1:N+1
    t=wBary(k)./(x(Lindex)-GPPos1D(k));
    L(k,Lindex)=t;
    s=s+t;
  end
  L(:,Lindex)=L(:,Lindex)./s(ones(N+1,1),:);
end
end
% =====================================

%%%
% Overwrites the built-in plot function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in plot function except
% that complex values are forbitten and X values must
% be provided for every plot.
% 
% The arguments are X, Y and an optional LineSpec. These
% two or three arguments can be appended multiple times.
% X contains the x values of the points, Y the y values.
% Consecutive points are drawn connected by a line.
% X and Y must have one matching dimension if at least
% one is a vector and must have the exact same dimension
% if moth are matrices.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-08
%%%

function plot(X, Y, varargin)
	
	%%%
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
    
  %%%
	% open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
	% handle optional arguments
	LineSpec = '';
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
  % write color data
  if length(LineSpec) > 0
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
		end; %if
	
	%%%
  % write symbol data
		if not(isempty(strfind(LineSpec, 'x')))
			fprintf(plot_file, '# symbol x\n');
		elseif not(isempty(strfind(LineSpec, '*')))
			fprintf(plot_file, '# symbol *\n');
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
		else
			fprintf(plot_file, '# symbol none\n');
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

  %%%
  % close file
  fclose(plot_file);
	
	%%%
	% recursivly call plot to work off remaining optional arguments
	if size(newArgIn, 2) == 0
		return;
	end; %if
	
	assert(size(newArgIn, 2) >= 2, 'Wrong number of arguments, expected more arguments.');
	
	X = newArgIn{1};
	Y = newArgIn{2};
	if size(newArgIn, 2) == 2
		plot(X, Y);
	else
		plot(X, Y, newArgIn{3:size(newArgIn, 2)});
	end; %if
	
end %function

%%%
% Overwrites the built-in legend function and gives out
% a ViPLab graphic format file (.vgf).
% It breaks with th built-in legend function because it
% can only handly one argument. If the legend is set all
% plots from now on will use the new legend. To stay
% compatible with the built-in legend use legend('')
% at the end of your program to prevent a legend.
% 
% The argument must be a string. It does not support
% handles, orientation or multiple legends.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-12
%%%

function legend(PlotLegend)
  % ensure valid arguments
  assert(ischar(PlotLegend), 'First argument in legend must be a string.');
    
	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write legend data
  fprintf(plot_file, '# legend %s\n', PlotLegend);

	%%%
  % close file
  fclose(plot_file);
end %function

%%%
% Overwrites the built-in title function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in legend function and adds
% a title to the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-09
%%%

function title(PlotTitle, varargin)
  % ensure valid arguments
  assert(ischar(PlotTitle), 'First argument in title must be a string.');
    
	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write title data
  fprintf(plot_file, '# title %s\n', PlotTitle);

	%%%
  % close file
  fclose(plot_file);
end %function

%%%
% Overwrites the built-in plot function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in plot function except
% that complex values are forbitten and X values must
% be provided for every plot.
% 
% The arguments are X, Y and an optional LineSpec. These
% two or three arguments can be appended multiple times.
% X contains the x values of the points, Y the y values.
% Consecutive points are drawn connected by a line.
% X and Y must have one matching dimension if at least
% one is a vector and must have the exact same dimension
% if moth are matrices.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-01
%%%

function axis(Range)
  xmin = Range(1);
  xmax = Range(2);
  ymin = Range(3);
  ymax = Range(4);
	%%%
  % ensure valid arguments
  assert(isreal(xmin) && isreal(xmax) && isreal(ymin) && isreal(ymax), 'All arguments must be real numbers.');
  assert(isscalar(xmin) && isscalar(xmax) && isscalar(ymin) && isscalar(ymax), 'All arguments must be scalars.');
  assert(xmin < xmax, 'xmin must be smaller than xmax.');
	assert(ymin < ymax, 'ymin must be smaller than ymax.');

	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write axis data
  fprintf(plot_file, '# x-range %f %f\n', xmin, xmax);
  fprintf(plot_file, '# y-range %f %f\n', ymin, ymax);

	%%%
  % close file
  fclose(plot_file);
end %function

%%%
% Overwrites the built-in figure function.
% The function does nothing but surpresses the built-in
% figure function which opens a new plot window.
%
% It does not accept any arguments and has no return values.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-01
%%%

function figure()
  % nothing todo just prevent buit-in function to open a plot window
end %function

%%%
% Overwrites the built-in xlabel function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in xlabel function and adds
% a label to the X-axis of the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-09
%%%

function xlabel(AxisTitle)
  % ensure valid arguments
  assert(ischar(AxisTitle), 'First argument in title must be a string.');
    
	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write title data
  fprintf(plot_file, '# x-label %s\n', AxisTitle);

	%%%
  % close file
  fclose(plot_file);
end %function

%%%
% Overwrites the built-in ylabel function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in ylabel function and adds
% a label to the Y-axis of the plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-09
%%%

function ylabel(AxisTitle)
  % ensure valid arguments
  assert(ischar(AxisTitle), 'First argument in title must be a string.');
    
	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write title data
  fprintf(plot_file, '# y-label %s\n', AxisTitle);

	%%%
  % close file
  fclose(plot_file);
end %function

%%%
% Overwrites the built-in zlabel function and gives out
% a ViPLab graphic format file (.vgf).
% It behaves similar to built-in zlabel function and adds
% a label to the Z-axis of the 3d-plot.
% 
% The arguments must be a string. No handles or properties are
% supported.
%
% Usage: Put file in the same directory containing your programm.
%        Matlab will warn you that it may conflict with built-in
%        functions but that is intended.
%
% Author: C. Grüninger (2010)
%
% Copyright: All rights reserved C. Grüninger 2010
%            This function is licenced under the 
%            terms of GNU GPL 3 or higher.
% Version: 2010-11-09
%%%

function zlabel(AxisTitle)
  % ensure valid arguments
  assert(ischar(AxisTitle), 'First argument in title must be a string.');
    
	%%%
  % open file to append, use UTF-8 encoding
  plot_file = fopen('vipplot.vgf', 'a');%, 'n', 'UTF-8');

	%%%
  % write title data
  fprintf(plot_file, '# z-label %s\n', AxisTitle);

	%%%
  % close file
  fclose(plot_file);
end %function
function hold(varargin)
end

