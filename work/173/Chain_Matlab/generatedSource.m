function syntacticallyNeeded()

a = 14/3;
b = 1.0;
[p,q] = rat((a-b)/b);
tmax = q*2*pi;

t = linspace(0,tmax,300);
x = (a-b)*cos(t) + b*cos((a-b)/b*t);
y = (a-b)*sin(t) - b*sin((a-b)/b*t);

title('zykloide mit b=1');
%legend('a=14/3');
plot(x,y,'g');

a = 3;
[p,q] = rat((a-b)/b);
tmax = q*2*pi;

t = linspace(0,tmax,300);
x = (a-b)*cos(t) + b*cos((a-b)/b*t);
y = (a-b)*sin(t) - b*sin((a-b)/b*t);

%legend('a=3');
plot(x,y,'c');

end %function syntacticallyNeeded()

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

function title(PlotTitle)
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
