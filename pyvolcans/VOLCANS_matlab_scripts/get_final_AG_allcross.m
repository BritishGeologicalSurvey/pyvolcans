% get_final_AG_allcross.m

%{Summary:

It calculates the final single-criterion analogy matrix for rock geochemistry.
It requires to load the file `AGmatrices_ALU_QUET.mat`, which is derived from
the script `votw_analysis.m`.

%}

clear all
close all

%load the AG matrices
load ../VOLCANS_mat_files/data_mats/AGmatrices_ALU_QUET.mat

%%% next step with all analogy scales is going to calculate the %%%
%%% cross-volcano analogies for all the analogies!!             %%%

%matrix of areas between ecdfs (all volcanoes, including itself)
AA_allcross=zeros(length(AGecdfmat(:,1)),length(AGecdfmat(:,1)));
%matrix of final measure of analogy (1-area)
AG_allcross=zeros(length(AGecdfmat(:,1)),length(AGecdfmat(:,1)));

%volcano #24 (Yali, Greece) is an example of single-rock-type=rhyolite
%considering the way we compute the area in between ecdfs, such a volcano
%type does not yield an area of 0. However, a volcano with
%single-rock-type=foidite, will generate an area of 1. Therefore, in order
%to ensure that such two volcanoes are given a 0 in analogy, we normalise
%the areas by 1 minus the area under the ecdf of a single-rock-type=rhyolite
normAA=1-trapz(xgeoch,AGecdfmat(24,:));

%here we introduce a loop to calculate all cross-volcano analogy
%measures for rock geochemistry
for ii=1:length(AG_allcross(:,1))
    for jj=1:length(AG_allcross(1,:))
        if nansum(AGnormmat(jj,:))>0
            for kk=1:length(xgeoch)-1
                %this method should work alright
                AA_allcross(ii,jj)=AA_allcross(ii,jj)+...
                    abs((xgeoch(kk+1)-xgeoch(kk)).*...
                    (abs(AGecdfmat(jj,kk)-AGecdfmat(ii,kk))+...
                    (abs(AGecdfmat(jj,kk+1)-AGecdfmat(ii,kk+1)))))/2;
            end
            %CRUCIAL!! We normalise the area, not the final measure of analogy!
            AA_allcross(ii,jj)=AA_allcross(ii,jj)./normAA;
            AG_allcross(ii,jj)=1-AA_allcross(ii,jj);
        else
            AG_allcross(ii,jj)=0;
        end
    end
    
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the AG_allcross with zero values
    if nansum(AGnormmat(ii,:))==0
        AG_allcross(ii,:)=zeros(1,length(AG_allcross(1,:)));
    end
    
end

%save the final matrix
save AGfinal_allvolcs_ALU_QUET.mat VNUM AG_allcross -v7.3
