x = [0:.2:20]

% here comes the error
y := sin(x)./sqrt(x+1);

y(2,:) = sin(x/2)./sqrt(x+1);
y(3,:) = sin(x/3)./sqrt(x+1);
plot(x,y);

print -dpng /tmp/picture_1
x;
y;

