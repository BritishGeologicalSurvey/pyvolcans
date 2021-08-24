% get_final_AT_allcross.m

%{Summary:

It calculates the final single-criterion analogy matrix for tectonic setting.
It requires to load the file `ATmatrices.mat`, which is derived from the script
`votw_analysis.m`.

%}

clear all
close all

%load the AT matrices
load ../VOLCANS_mat_files/data_mats/ATmatrices.mat

%%% next step with all analogy scales is going to calculate the %%%
%%% cross-volcano analogies for all the analogies!!             %%%

%there are no areas now but another parameter, measuring the dissimilarity
AT_allcross=zeros(length(ATlast(:,1)),length(ATlast(:,1)));
%here the matrix of final measure of analogy (1-DTs)
%[similar to the other criteria for analogy]
DAT_allcross=zeros(length(ATlast(:,1)),length(ATlast(:,1)));

%here we introduce a loop to calculate all cross-volcano analogy
%measures for tectonic setting
for ii=1:length(AT_allcross(:,1))
    %here the content of the loop will be slightly different to the other cases
    for jj=1:length(AT_allcross(1,:))
        %we check the systems that do not have tectonic-setting analogy
        if ATlast(jj)==-9999
            %AT_all(jj)=0;
            AT_allcross(ii,jj)=0;
        else
            %first absolute difference in AT value
            DAT_allcross(ii,jj)=abs(ATlast(jj)-ATlast(ii));
            %second, 1 minus the dissimilary index
            AT_allcross(ii,jj)=1-DAT_allcross(ii,jj);
        end
    end
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the AT_allcross with zero values
    if ATlast(ii)==-9999
        AT_allcross(ii,:)=zeros(1,length(AT_allcross(1,:)));
    end
end

%save the final matrix
save ATfinal_allvolcs.mat VNUM AT_allcross -v7.3
