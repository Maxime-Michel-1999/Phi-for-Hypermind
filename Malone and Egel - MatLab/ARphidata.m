function [ret] = ARphidata(X,tau)

% -----------------------------------------------------------------------
%   FUNCTION: ARPhidata.m
%   PURPOSE:  Compute Phi_AR from time-series data.
%
%   INPUT:  X          -    data matrix, rows correspond to elements,
%                           columns to observations.
%           tau        -    number of lags over which to compute ARPhi
%
%   OUTPUT: Phi        -    Phi_AR
%           Partition1 -    MIB (component 1)
%           Partition2 -    MIB (component 2)
%
%   Adam Barrett May 2010.
%   Uses material from Granger Causality Toolbox Written by Anil K Seth,
%   Ref: Seth, A.K. (2005) Network: Comp. Neural. Sys. 16(1):35-5
% -----------------------------------------------------------------------

% Obtain number of elements in system, and number of observations
nobs = size(X,2);
nvar = size(X,1);
if(nvar>nobs) error('error in ARphidata: nvar>nobs, check input matrix'); end

%Time-reverse the data
X=timereverse(X);

%Variables contained in bipartitions
Partition1=zeros(nvar);
Partition2=zeros(nvar);

% remove sample means if present (not interested in constant terms in regressions)
m = mean(X');
if(abs(sum(m)) > 0.0001)
    mall = repmat(m',1,nobs);
    X = X-mall;
end

PhiNorm=1000000; %Will be current minimum for normalized effective information

%  regression of present of X to predict past of X.
regressors = zeros(nobs-tau,nvar);
for i=1:nvar,
    regressors(:,i) = X(i,1:nobs-tau);
end
for i=1:nvar
    xvec = X(i,:)';
    xdep = xvec(tau+1:end);
    beta(:,i) = regressors\xdep;
    xpred(:,i) = regressors*beta(:,i);
    u(:,i) = xdep-xpred(:,i); %residuals for X
end

Cu=cov(u); %residual covariance matrix for X regression
EuT=det(Cu); % Determinant of residual for full regression
        
covx=cov(X'); %stationary covariance matrix for X
detcovx=det(covx); %Determinant of stationary covariance matrix

%   find the bipartitions
for nrestvars=1:floor(nvar/2)
    vvars=nchoosek(1:nvar,nrestvars);
    nrestvars2=nvar-nrestvars;
    for q=1:nchoosek(nvar,nrestvars)
        
        %Do everything for a specific bipartition
        clear regressors;
        clear regressors2;
        clear beta;
        clear beta2;
        clear u;
        clear v;
        clear MM;
        clear NN;
        clear mvec;
        clear mdep;
        clear mpred;
        clear nvec;
        clear ndep;
        clear npred;
        clear C1;
        clear C2;
        clear covm;
        clear covn;
        
        %Subsets M and N
        MM=vvars(q,:);
        NN=setdiff(1:nvar,vvars(q,:));
        M=zeros(nrestvars,nobs);
        N=zeros(nrestvars2,nobs);
        for k=1:nrestvars
            M(k,:)=X(MM(k),:); % restricted data for set M
        end
        for k=1:nrestvars2
            N(k,:)=X(NN(k),:); % restricted data for set N
        end
        
        %Regression for system M
        regressors = zeros(nobs-tau,nrestvars);
        for i=1:nrestvars,
            regressors(:,i) = M(i,1:nobs-tau);
        end
        for i=1:nrestvars
            mvec = M(i,:)';
            mdep = mvec(tau+1:end);
            beta(:,i) = regressors\mdep;
            mpred(:,i) = regressors*beta(:,i);  
            u(:,i) = mdep-mpred(:,i); %residuals for M
        end
        
        % Regression for system N
        regressors2 = zeros(nobs-tau,nrestvars2);
        for i=1:nrestvars2,
            regressors2(:,i) = N(i,1:nobs-tau);
        end
        for i=1:nrestvars2
            nvec = N(i,:)';
            ndep = nvec(tau+1:end);
            beta2(:,i) = regressors2\ndep;
            npred(:,i) = regressors2*beta2(:,i);  
            v(:,i) = ndep-npred(:,i); %residuals for N
        end
        
        %Residual covariance matrices for parts
        C1=cov(u);
        C2=cov(v);
        %Determinants
        Er1=det(C1);
        Er2=det(C2);
        
        %Stationary covariance matrices, and their determinants for parts
        covm=cov(M');
        covn=cov(N');
        detcovm=det(covm);
        detcovn=det(covn);
        
        %Effective information for specific bipartition (Eq. (7.9))
        phi=0.5*log(detcovx*Er1*Er2/(detcovm*detcovn*EuT));
        
        %normalisation factor for specific bipartition
        normm=0.5*log(((2*pi*exp(1))^nrestvars)*detcovm);
        normn=0.5*log(((2*pi*exp(1))^nrestvars2)*detcovn);
        if normm<normn
            Normalise=normm;
        else
            Normalise=normn;
        end
        
        %normalised effective information
        phinorm=phi/Normalise;
        
        % record as Phi if minimum
        if phinorm<PhiNorm
            PhiNorm=phinorm;
            Phi=phi;
            Partition1=MM;
            Partition2=NN;
        end
    end
end

%  organize output structure
ret.Partition1=Partition1;
ret.Partition2=Partition2;
ret.Phi=Phi;
ret.type = 'td_normal';
