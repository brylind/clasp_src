function [y,z] = process_delta_t(x)
    y = x - x(1);
    z = zeros(length(y)-1,1);
    for i = 1:length(y)-2
        z(i) = y(i+1)-y(i);
    end
    mu = mean(z)
    sigma = std(z)
    normplot(z);    