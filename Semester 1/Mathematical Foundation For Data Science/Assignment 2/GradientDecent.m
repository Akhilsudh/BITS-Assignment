format long;
syms X1 X2;

% Function given in question:
f = (X1 - X2)^2 + 1 - X1;

% Tolerance Criterias
max_iterations = 50;
tol = 0.01;

% Preallocate for speed
x1 = zeros(1,max_iterations);
x2 = zeros(1,max_iterations);
obj = zeros(1,max_iterations);

% Initial Values for x1, x2:
x1(1) = 2;
x2(1) = -2;

i = 1;

% Gradient Computation:
df_dx1 = diff(f, X1);
df_dx2 = diff(f, X2);
G = [subs(df_dx1,[X1,X2], [x1(1),x2(1)]) subs(df_dx2, [X1,X2], [x1(1),x2(1)])]; % Gradient

% Iterative process
while (true)
    X = [x1(i),x2(i)]';
    syms r;
    
    % X_k+1 = X_k - r * Gradient
    f_new = subs(f, [X1,X2], [x1(i) - r * G(1) ,x2(i) - r * G(2)]);
    dg_dh = diff(f_new,r);
    r = solve(dg_dh, r);
    x1(i+1) = X(1) - r * G(1);
    x2(i+1) = X(2) - r * G(2);
    obj(i+1) = eval(f_new);
    i = i+1;
    
    % Checking for tolerance criteria
    % If max iterations are reached or 
    % if the difference between the previous values for x_1 and x_2
    % and the current values are less than the tolerance criteria
    if(i > max_iterations - 1 || ((abs(r * G(1)) <= tol) && (abs(r * G(2))<=tol)))
        fprintf('Tolerance criteria reached...\n');
        break
    end
    
    % Update Gradient
    G = [subs(df_dx1,[X1,X2], [x1(i),x2(i)]) subs(df_dx2, [X1,X2], [x1(i),x2(i)])];
end
% Result Table:
header = {'Iteration Number', 'X', 'Y', 'Function' };
T = table((1:i)', x1',x2',obj');
T.Properties.VariableNames = header;

% Contour Plot x1 and x2:
fcontour(f, 'Fill', 'On');
plot(x1,x2,'*-r');

% Final Output:
disp(T);
fprintf('Initial Objective Value: %d\n',subs(f,[X1,X2], [x1(1),x2(1)]));
fprintf('Number of Iterations for Convergence: %d\n', i);
fprintf('Point of Minima (x, y): (%d,%d)\n', x1(i), x2(i));