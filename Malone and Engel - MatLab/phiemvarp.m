function [ret] = phiemvarp(A,Omega,tau)

% -----------------------------------------------------------------------
%   FUNCTION: phiemvarp.m
%   PURPOSE:  compute phi_e analytically for a stationary Gaussian mvar(p)
%             process: X_t=A_1*X_{t-1}+A_2*X_{t-2}+...+A_p*X_{t-p}+E_t
%
%   INPUT:  A          -    generalized connectivity matrix. 
%                           A=(A_1 A_2 ... A_p)
%           Omega      -    covariance matrix for E_t
%           tau        -    number of lags over which to compute Phi_e
%
%   OUTPUT: Phi        -    Phi_stat
%           Partition1 -    MIB (component 1)
%           Partition2 -    MIB (component 2)
%
%   Adam Barrett May 2010.
% -----------------------------------------------------------------------


nvar = size(A,1); %number of elements in system
p=floor(size(A,2)/nvar); %number of lags in MVAR model

%Variables contained in bipartitions
Partition1=zeros(nvar);
Partition2=zeros(nvar);

PhiNorm=1000000; %Will be current minimum for normalized effective information

Nblocks=max(tau+1,p); % Number of blocks in each dimension of big matrix F, Eq. (B.4).

%Obtain F and V, Eq. (B.3)
F=zeros(nvar*Nblocks,nvar*Nblocks);
ident=eye(nvar);
V=zeros(nvar*Nblocks,nvar*Nblocks);
for i=1:p
    F(1:nvar,nvar*(i-1)+1:nvar*i)=A(:,nvar*(i-1)+1:nvar*i);
end
for i=1:Nblocks-1
    F(nvar*i+1:nvar*(i+1),nvar*(i-1)+1:nvar*i)=ident(:,:);
end
V(1:nvar,1:nvar)=Omega(:,:);

%Stationary distribution
BigSigma=dlyap(F,V);
Sigma=zeros(nvar,nvar);
Sigma(:,:)=BigSigma(1:nvar,1:nvar); %Stationary covariance
s=nvar*tau+1;
Gamma=zeros(nvar,nvar);
Gamma(:,:)=BigSigma(s:s+nvar-1,1:nvar); %Stationary tau lags auto-covariance

entxstat=0.5*log(det(Sigma)); %Entropy of X_{t-tau}
PartialX=Sigma-Gamma*inv(Sigma)*Gamma';
entx=0.5*log(det(PartialX)); %Entropy of X_{t-tau} after knowing X_t

%   find the bipartitions
for nrestvars=1:floor(nvar/2)
    vvars=nchoosek(1:nvar,nrestvars);
    nrestvars2=nvar-nrestvars;
    for q=1:nchoosek(nvar,nrestvars)

        %Do everything for a specific bipartition
        clear MM;
        clear NN;

        %Subsets M and N
        MM=vvars(q,:);
        NN=setdiff(1:nvar,vvars(q,:));

        %Entropies for part M
        Gammamm=zeros(nrestvars,nrestvars);
        PartialM=zeros(nrestvars,nrestvars);
        Sigmamm=zeros(nrestvars,nrestvars);
        for i=1:nrestvars
            for j=1:nrestvars
                Gammamm(i,j)=Gamma(MM(i),MM(j));
                Sigmamm(i,j)=Sigma(MM(i),MM(j));
            end
        end
        PartialM=Sigmamm-Gammamm*inv(Sigmamm)*Gammamm';
        entm=0.5*log(det(PartialM));  %A posteriori entropy
        entmstat=0.5*log(det(Sigmamm)); %A priori entropy

        %Entropies for part N
        Gammann=zeros(nrestvars2,nrestvars2);
        PartialN=zeros(nrestvars2,nrestvars2);
        Sigmann=zeros(nrestvars2,nrestvars2);
        for i=1:nrestvars2
            for j=1:nrestvars2
                Gammann(i,j)=Gamma(NN(i),NN(j));
                Sigmann(i,j)=Sigma(NN(i),NN(j));
            end
        end
        PartialN=Sigmann-Gammann*inv(Sigmann)*Gammann';
        entn=0.5*log(det(PartialN)); %A posteriori entropy
        entnstat=0.5*log(det(Sigmann)); %A priori entropy

        %Effective information for specific bipartition
        phi=entm+entn-entx+entxstat-entmstat-entnstat;

        %normalisation factor for specific bipartition
        normm=0.5*log((2*pi*exp(1))^nrestvars*det(Sigmamm));
        normn=0.5*log((2*pi*exp(1))^nrestvars2*det(Sigmann));
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
