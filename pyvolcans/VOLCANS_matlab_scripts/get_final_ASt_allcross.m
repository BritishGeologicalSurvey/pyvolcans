% get_final_ASt_allcross.m

%{Summary:

It calculates the final single-criterion analogy matrix for eruption style.
It requires to load the file `AStmatrices_SINA.mat`, which is derived from
the script `eruption_style_processing.m`.

%}

clear all
close all

%load the ASt matrices
load ../VOLCANS_mat_files/data_mats/AStmatrices_SINA.mat

%%% next step with all analogy scales is going to calculate the %%%
%%% cross-volcano analogies for all the analogies!!             %%%

%there are no areas now but another parameter, measuring the dissimilarity
DSt_allcross=zeros(length(AStnormmat(:,1)),length(AStnormmat(:,1)));
%here the matrix of final measure of analogy (1-DSt)
%[similar to the other criteria for analogy]
ASt_allcross=zeros(length(AStnormmat(:,1)),length(AStnormmat(:,1)));

%number of categories is defined here
Hcat=length(AStnormmat(1,:));

%here we introduce a loop to calculate all cross-volcano analogy
%measures for eruption style
for ii=1:length(ASt_allcross(:,1))
    %here the content of the loop will be slightly different to the other cases
    for jj=1:length(ASt_allcross(1,:))
        if nansum(AStnormmat(jj,:))>0
            for kk=1:Hcat
                %we are now comparing the values for each category
                DSt_allcross(ii,jj)=DSt_allcross(ii,jj)+...
                    abs(AStnormmat(jj,kk)-AStnormmat(ii,kk));
            end
            %after having computed the sum of differences, we have to normalise
            %by the number of categories
            DSt_allcross(ii,jj)=DSt_allcross(ii,jj)/Hcat;    

            %final measure of analogy is 1-DSt
            ASt_allcross(ii,jj)=1-DSt_allcross(ii,jj);
        else
            ASt_allcross(ii,jj)=0;
        end
    end
    
    %if the volcano analysed is a no-data one, over-rule what happened
    %above and fill the ASt_allcross with zero values
    if nansum(AStnormmat(ii,:))==0
        ASt_allcross(ii,:)=zeros(1,length(ASt_allcross(1,:)));
    end   
end

%save the final matrix
save AStfinal_allvolcs_SINA.mat VNUM ASt_allcross -v7.3
