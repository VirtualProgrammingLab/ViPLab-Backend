file = fopen('bar.txt', 'r');
if file == -1
  error('file not found');
  quit force;
end
fprintf(file, 'some content');
fclose(file);
disp 'opening and closing file has happened';
