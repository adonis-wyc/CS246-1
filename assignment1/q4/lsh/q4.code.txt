load patches;
T1=lsh('lsh',10,24,size(patches,1),patches,'range',255);

tic;
for index = 100 : 100 : 1000
    lshlookup(patches(:,index),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
end
t1 = toc;
display(t1 / 10);

tic;
for index = 100 : 100 : 1000
    d=sum(abs(bsxfun(@minus,patches(:,index),patches)));sort(d);
end
t2 = toc;
display(t2 / 10);

% original
figure(1);imagesc(reshape(patches(:,100),20,20));colormap gray;axis image
nnlsh = [];
while length(nnlsh) < 11
    [nnlsh,numcand]=lshlookup(patches(:,100),patches,T1,'k',11,'distfun','lpnorm','distargs',{1});
end
d=sum(abs(bsxfun(@minus,patches(:,100),patches)));[ignore,ind]=sort(d);

% expect
figure(2);clf;
for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,nnlsh(k+1)),20,20)); colormap gray;axis image; end
% true
figure(3);clf;
for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,ind(k+1)),20,20));colormap gray;axis image; end


x_axis = 10 : 2 : 20;
y_axis = zeros(1, length(x_axis));
for ii = 1 : 1 : length(x_axis)
    L = x_axis(ii);
    T1=lsh('lsh',L,24,size(patches,1),patches,'range',255);
    error_vector = zeros(1, 10);
    for index = 100 : 100 : 1000
        nnlsh = [];
        while length(nnlsh) < 4
            [nnlsh,numcand]=lshlookup(patches(:,index),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
        end
        lsh_vectors = patches(:, nnlsh(2:4));
        d=sum(abs(bsxfun(@minus,patches(:,index),patches)));[ignore,ind]=sort(d);
        linear_vectors = patches(:, ind(2:4));
        
        z = patches(:, index);
        z_rep = repmat(z, 1, 3);
        numinator = sum(sum(abs(lsh_vectors - z_rep)));
        denominator = sum(sum(abs(linear_vectors - z_rep)));
        error_ratio = numinator / denominator;
        error_vector(index / 100) = error_ratio;
    end
    error_average = mean(error_vector);
    y_axis(ii) = error_average;
end
figure(4);clf;
plot(x_axis, y_axis);
xlabel('L');
ylabel('error')


x_axis = 16 : 2 : 24;
y_axis = zeros(1, length(x_axis));
for jj = 1 : 1 : length(x_axis)
    K = x_axis(jj);
    T1=lsh('lsh',10,K,size(patches,1),patches,'range',255);
    error_vector = zeros(1, 10);
    for index = 100 : 100 : 1000
        nnlsh = [];
        while length(nnlsh) < 4
            [nnlsh,numcand]=lshlookup(patches(:,index),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
        end
        lsh_vectors = patches(:, nnlsh(2:4));
        d=sum(abs(bsxfun(@minus,patches(:,index),patches)));[ignore,ind]=sort(d);
        linear_vectors = patches(:, ind(2:4));
        
        z = patches(:, index);
        z_rep = repmat(z, 1, 3);
        numinator = sum(sum(abs(lsh_vectors - z_rep)));
        denominator = sum(sum(abs(linear_vectors - z_rep)));
        error_ratio = numinator / denominator;
        error_vector(index / 100) = error_ratio;
    end
    error_average = mean(error_vector);
    y_axis(jj) = error_average;
end
figure(5);clf;
plot(x_axis, y_axis);
xlabel('K');
ylabel('error')