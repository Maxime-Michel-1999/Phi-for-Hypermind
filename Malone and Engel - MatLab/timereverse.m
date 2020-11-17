function Y=timereverse(X);

d=size(X);
n=d(2);

for i=1:n
    Y(:,i)=X(:,n+1-i);
end

end