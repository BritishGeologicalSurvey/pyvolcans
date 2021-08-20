% get_final_AM_allcross.m

%{Summary:

It calculates the final single-criterion analogy matrix for volcano morphology.
It requires to load the file `AMmatrices_QUET.mat`, which is derived from the
script `morphology_processing.m`

%}

clear all
close all

%load the AM matrices
load ../VOLCANS_mat_files/data_mats/AMmatrices_QUET.mat

%%% next step with all analogy scales is going to calculate the %%%
%%% cross-volcano analogies for all the analogies!!             %%%

%there are no areas now but another parameter, measuring the dissimilarity
AM_allcross=zeros(length(AMlast(:,1)),length(AMlast(:,1)));
%here the matrix of final measure of analogy (1-DM)
%[similar to the other criteria for analogy]
DAM_allcross=zeros(length(AMlast(:,1)),length(AMlast(:,1)));

%here we introduce a loop to calculate all cross-volcano analogy
%measures for volcano morphology
for ii=1:length(AM_allcross(:,1))
    %here the content of the loop will be slightly different to the other cases
    for jj=1:length(AM_allcross(1,:))
        %we check the systems that do not have morphology analogy
        if AMlast(jj)==-9999
            %AM_all(jj)=0;
            AM_allcross(ii,jj)=0;
        else
            %first absolute difference in AM value
            DAM_allcross(ii,jj)=abs(AMlast(jj)-AMlast(ii));
            %second, 1 minus the dissimilary index
            AM_allcross(ii,jj)=1-DAM_allcross(ii,jj);
        end
    end
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the AM_allcross with zero values
    if AMlast(ii)==-9999
        AM_allcross(ii,:)=zeros(1,length(AM_allcross(1,:)));
    end
end

%save the final matrix
save AMfinal_allvolcs_QUET.mat VNUM AM_allcross -v7.3
