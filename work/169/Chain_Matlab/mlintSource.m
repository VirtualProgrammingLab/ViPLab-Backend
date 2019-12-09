function get_EOC();
fprintf('=======================\n');
fprintf('Get EOC (experimental order of convergence) of \n');
fprintf('IVP (initial value problems) solver: \n');
fprintf('=======================\n');



% set initial data
x_0  = 0;
x_end = 2;
y_0 = 1;

E_1 = 0;
h_1 =0;
EOC = 0;
%Err_hist = zeros(1,5);
%h_hist = zeros(1,5);
counter = 1;

% loop over different step sizes
for n = 4:10
   n_steps = 2^n;
   h = (x_end-x_0)/n_steps;
   h_hist(counter) = h;

   y  = y_0;  
   x = 0;
   Err = 0;
   hist_y(counter,1) = y;
   hist_x(counter,1) = x;

   % time step loop
   for i_step = 1:n_steps
      %dy = Euler_Cauchy(y,h,x);
      %dy = Improved_Euler_Cauchy(y,h,x);
      %dy = Heun(y,h,x);
      dy = Runge_Kutta(y,h,x);
      y = y + dy;
      x = x + h;
      hist_y(counter,i_step+1) = y;
      hist_x(counter,i_step+1) = x;
      Err = Err + (y - y_exact(x))^2;
   end % i_step
   Err = sqrt(Err/n_steps);
   Err_hist(counter) = Err;
   fprintf('n_steps: %i\n',n_steps);
   fprintf('h: %f\n',h);
   fprintf('Error: %e\n',Err);
   if (EOC ~= 0)
     E_2 = Err;
     h_2 = h;
     EOC = log(E_1/E_2)/log(h_1/h_2);
     fprintf('EOC:  %f\n',EOC);
   else;
     EOC = 1;
     fprintf('First run. No EOC available.\n';
   end
   fprintf('=======================\n');
   E_1 = Err;
   h_1 = h;
   counter = counter + 1;

end % n

% plot step-size over error to see exponential convergence
% this requires double-logarithmic plots (not implemented yet)
%plot(h_hist,Err_hist,'k');


% plot results for differents step sizes
x_exact_hist = linspace(0,x_end,2^10);
for i =1:2^10
   y_exact_hist(i) = y_exact(x_exact_hist(i));
end
plot(hist_x(1,:),hist_y(1,:),'k');
%plot(hist_x(2,:),hist_y(2,:),'r');
%plot(hist_x(3,:),hist_y(3,:),'b');
plot(x_exact_hist,y_exact_hist,'c');

end % function get_EOC

%-------------------------------------------------------%
function [dy] = Euler_Cauchy(y,h,x);
    dy = h * f(x,y);
end % function Euler_Cauchy
%-------------------------------------------------------%
function [dy] = Improved_Euler_Cauchy(y,h,x);
     y_tilde = y + h/2 * f(x,y);
    dy = h * f(x+h/2,y_tilde);
end % function Improved_Euler_Cauchy
%-------------------------------------------------------%
function [dy] = Heun(y,h,x);
    y_tilde = y + h * f(x,y);
    dy = h/2 * ( f(x,y) + f(x+h,y_tilde) );
end % function Heun
%-------------------------------------------------------%
function [dy] = Runge_Kutta(y,h,x);
k1=f(x,y);
k2=f(x+h/2,y+h/2*k1);
k3=f(x+h/2,y+h/2*k2);
k4=f(x+h,y+h*k3);
dy=h/6*(k1+2*(k2+k3)+k4);
end  % function Runge_Kutta

