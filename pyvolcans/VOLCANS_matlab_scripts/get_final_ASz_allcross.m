% get_final_ASz_allcross.m

%{Summary:

It calculates the final single-criterion analogy matrix for eruption size.
It requires to load the file `ASzmatrices_SINA.mat`, which is derived from
the script `eruption_size_processing.m`

%}

clear all
close all

%load the ASz matrices
load ../VOLCANS_mat_files/data_mats/ASzmatrices_SINA.mat

%%% next step with all analogy scales is going to calculate the %%%
%%% cross-volcano analogies for all the analogies!!             %%%

%matrices of areas between ecdfs (all volcanoes, including itself)
AA_allcross=zeros(length(ASzecdfmat(:,1)),length(ASzecdfmat(:,1)));
AA_allcrossUR=zeros(length(ASzecdfmat(:,1)),length(ASzecdfmat(:,1)));

%matrices of final measure of analogy (1-area)
ASz_allcross=zeros(length(ASzecdfmat(:,1)),length(ASzecdfmat(:,1)));
ASz_allcrossUR=zeros(length(ASzecdfmat(:,1)),length(ASzecdfmat(:,1)));

%there is no case of single-eruption-size=VEI8 but, just to ensure the
%domain of the ASz_last(UR) variable is in between 0 and 1, we will
%normalise the difference in area between the ECDFs by the area that would
%result in the case of one single-size=VEI8 volcano compared to another
%single-size volcano but equal to VEI<=2
normAA=1-trapz(xveinorm,[zeros(1,6) 1]);

%here we introduce a loop to calculate all cross-volcano analogy
%measures for eruption size
for ii=1:length(ASz_allcross(:,1))
    for jj=1:length(ASz_allcross(1,:))
        if nansum(ASznorm_ALL(jj,:))>0
            for kk=1:length(xveinorm)-1
                %this method should work alright
                AA_allcross(ii,jj)=AA_allcross(ii,jj)+...
                    abs((xveinorm(kk+1)-xveinorm(kk)).*...
                    (abs(ASzecdfmat(jj,kk)-ASzecdfmat(ii,kk))+...
                    (abs(ASzecdfmat(jj,kk+1)-ASzecdfmat(ii,kk+1)))))/2;
            end
            %CRUCIAL!! We normalise the area, not the final measure of analogy!
            AA_allcross(ii,jj)=AA_allcross(ii,jj)./normAA;
            ASz_allcross(ii,jj)=1-AA_allcross(ii,jj);
        else
            ASz_allcross(ii,jj)=0;
        end
    end
    
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the ASz_allcross with zero values
    if nansum(ASznorm_ALL(ii,:))==0
        ASz_allcross(ii,:)=zeros(1,length(ASz_allcross(1,:)));
    end   
end

%we do another loop because there is one case that is nan in the UR matrix
%but not in the "normal" one (the one upon which the under-recording
%correction has been implemented)

%here we introduce an above loop to calculate all cross-volcano analogy
%measures for eruption size
for ii=1:length(ASz_allcrossUR(:,1))
    for jj=1:length(ASz_allcrossUR(1,:))
        if nansum(ASznorm_ALLund(jj,:))>0
            for kk=1:length(xveinorm)-1
                %this method should work alright
                AA_allcrossUR(ii,jj)=AA_allcrossUR(ii,jj)+...
                    abs((xveinorm(kk+1)-xveinorm(kk)).*...
                    (abs(ASzecdfmat_UR(jj,kk)-ASzecdfmat_UR(ii,kk))+...
                    (abs(ASzecdfmat_UR(jj,kk+1)-ASzecdfmat_UR(ii,kk+1)))))/2;
            end
            %CRUCIAL!! We normalise the area, not the final measure of analogy!
            AA_allcrossUR(ii,jj)=AA_allcrossUR(ii,jj)./normAA;
            ASz_allcrossUR(ii,jj)=1-AA_allcrossUR(ii,jj);
        else
            ASz_allcrossUR(ii,jj)=0;
        end
    end
    
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the ASz_allcross with zero values
    if nansum(ASznorm_ALLund(ii,:))==0
        ASz_allcrossUR(ii,:)=zeros(1,length(ASz_allcrossUR(1,:)));
    end
    
end

%save the final matrix
save ASzfinal_allvolcs_SINA.mat VNUM ASz_allcross ASz_allcrossUR -v7.3
