% eruption_size_processing.m

%{Summary:

It derives the data required to calculate the single-criterion analogy matrix for eruption size.
It requires to import the data in the files: `VOTW467_8May18_eruption_data.csv`,
`VOTW467_8May18_volcano_data.csv`, and `MeadMagill2014_June2018.csv` to carry out
the aforementioned task.

%}

clear all
close all

%loading the eruption data
a=importdata('../VOLCANS_csv_files/VOTW467_8May18_eruption_data.csv');

%loading the volcano data as well because we will need them to assign the
%date of completeness according to the country or region of interest
b=importdata('../VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv');

%define a scale for VEI sizes
xvei=2:1:8;
xveinorm=(xvei-2)./(8-2);   %normalised

%start with getting the weights for each eruption, according to the
%eruption category and the VEI modifier (6 possible categories)
conf_erup=find(a.data(:,4)==1);
unc_erup=find(a.data(:,4)==3);

modi_null=find(a.data(:,7)==-9999 | a.data(:,7)==3 |...
    a.data(:,7)==4 | a.data(:,7)==5);
modi_hat=find(a.data(:,7)==2);
modi_quest=find(a.data(:,7)==1);
%we will call w1 to w6, in increasing order of weight given to the datum,
%to the indices of the combination of eruption category and VEI modifier
w1=intersect(unc_erup,modi_quest);
w2=intersect(unc_erup,modi_hat);
w3=intersect(unc_erup,modi_null);
w4=intersect(conf_erup,modi_quest);
w5=intersect(conf_erup,modi_hat);
w6=intersect(conf_erup,modi_null);

%what below: no needed in principle
% w_erupt=zeros(length(a.data(:,1)),1);   %vector where weights are stored
% w_erupt(w1)=0.250;   w_erupt(w2)=0.375;     w_erupt(w3)=0.500;
% w_erupt(w4)=0.667;   w_erupt(w5)=0.833;     w_erupt(w6)=1.000;

%calculate the indices of VEI<=2 eruptions (which we will group together)
veilt2=find(a.data(:,6)<=2);    %is it needed? (maybe with the histogram
                                %it is enough to get the VEI<=2 eruptions
                                %grouped

%load the data from Mead&Magill (2014) about dates of completeness
c=importdata('../VOLCANS_csv_files/MeadMagill2014_June2018.csv');

%create a vector to store the probability of recording an eruption of
%a given VEI size. This vector is the same for any volcano, only the
%date of completeness changes!! The vector has the same length as xvei
p_rec=zeros(length(xvei),1);
%first the parameters of the function
alp1=-4.595;
bet1=1.150;
%then the values of the function
p_recALL=1./(1+exp(-alp1-(bet1.*[0:1:8]))); %VEI sizes from 0 to 8

p_rec(1)=sum(p_recALL(1:3)); %probability of recording VEI<=2
p_rec(2:end)=p_recALL(4:end);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% just saving the probability of recording of eruptions of different %
% sizes here:                                                        %
save recording_prob.mat p_rec -v7.3                                  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%create a matrix where we will store the histograms of VEI eruptions for
%each volcano in the VOTW database
ASzcount_ALLund=zeros(length(b.data(:,1)),length(xvei)); %under-recording
ASzcount_ALL=zeros(length(b.data(:,1)),length(xvei)); %corrected for UR

ASznorm_ALLund=zeros(length(b.data(:,1)),length(xvei)); %normalised (UR)
ASznorm_ALL=zeros(length(b.data(:,1)),length(xvei)); %normalised and
                                                     %corrected for UR

%we will need as many different histograms as combined categories of
%eruption category and VEI modifier we have in our analysis (6)
%TIMES the pre-date-of-completeness and post-date-of-completeness histograms (2)7
%we could create multi-sheet matrices but it may lead to confusion in
%matrix assignments (we leave it the 'ugly way')
subASzcount_w1pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w2pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w3pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w4pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w5pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w6pre=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims

subASzcount_w1post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w2post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w3post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w4post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w5post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims
subASzcount_w6post=nan(length(b.data(:,1)),length(xvei)); %VNUM x NVEI dims

%and now we go through a single loop that will work on every volcano in the
%VOTW database. Several intermediate steps will be required to account for:
%different weights given to each eruption, date-of-completeness correction, etc.

for ii=1:length(ASzcount_ALL(:,1))
    vnum=b.data(ii,1);  %getting the VNUM of the volcano
    vreg=b.data(ii,7);  %getting the region of the volcano
    vcountry=b.data(ii,3);  %getting the country of the volcano
    k_country=intersect(c.data(20:end,2),vcountry); %checking whether there
                                                    %is information on the
                                                    %date of completeness by
                                                    %country
    %if there's not: get the region (there should be a k date for any
    %region!)
        if isempty(k_country)
            k_reg=intersect(c.data(1:19,2),vreg);
            kid=find(c.data(:,2)==k_reg&c.data(:,1)==0); %getting the index
        else
            kid=find(c.data(:,2)==k_country&c.data(:,1)==1); %getting the index
        end
        
    k=c.data(kid,3); %getting the date of completeness
    
    idsvolc=find(a.data(:,1)==vnum); %finding all eruptions for the volcano
    
    idspre=find(a.data(:,9)<=k); %finding any eruption pre/syn-
                                 %date-of-completeness
    idspost=find(a.data(:,9)>k); %finding any eruption post-date-of-completeness
     
    %getting the pre/syn/post-complete eruption for this specific volcano
    volcpre=intersect(idsvolc,idspre);
    volcpost=intersect(idsvolc,idspost);
    
    %%%fprintf('VNUM=%d, region=%d, country=%d, k=%d\n',vnum,vreg,...
       %%% vcountry,k);
    
    %getting the w1:w6 (pre&post) indices for this volcano
    %NB: each count will be multiplied by the corresponding w1:w6 values.
    %Moreover, those pre-date-of-completeness will be divided by the
    %corresponding recording probability associated with that particular
    %eruption size (as stored in the p_rec vector)
    volcw1pre=intersect(volcpre,w1);
    volcw2pre=intersect(volcpre,w2);
    volcw3pre=intersect(volcpre,w3);
    volcw4pre=intersect(volcpre,w4);
    volcw5pre=intersect(volcpre,w5);
    volcw6pre=intersect(volcpre,w6);
    
    volcw1post=intersect(volcpost,w1);
    volcw2post=intersect(volcpost,w2);
    volcw3post=intersect(volcpost,w3);
    volcw4post=intersect(volcpost,w4);
    volcw5post=intersect(volcpost,w5);
    volcw6post=intersect(volcpost,w6);
     
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    % histogram filling part %
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    
    subASzcount_w1pre(ii,:)=hist(a.data(volcw1pre,6),xvei);
    subASzcount_w2pre(ii,:)=hist(a.data(volcw2pre,6),xvei);
    subASzcount_w3pre(ii,:)=hist(a.data(volcw3pre,6),xvei);
    subASzcount_w4pre(ii,:)=hist(a.data(volcw4pre,6),xvei);
    subASzcount_w5pre(ii,:)=hist(a.data(volcw5pre,6),xvei);
    subASzcount_w6pre(ii,:)=hist(a.data(volcw6pre,6),xvei);
    
    subASzcount_w1post(ii,:)=hist(a.data(volcw1post,6),xvei);
    subASzcount_w2post(ii,:)=hist(a.data(volcw2post,6),xvei);
    subASzcount_w3post(ii,:)=hist(a.data(volcw3post,6),xvei);
    subASzcount_w4post(ii,:)=hist(a.data(volcw4post,6),xvei);
    subASzcount_w5post(ii,:)=hist(a.data(volcw5post,6),xvei);
    subASzcount_w6post(ii,:)=hist(a.data(volcw6post,6),xvei);
    
    %%%%%%%%%%%%%%%%%%%
    % correction part %
    %%%%%%%%%%%%%%%%%%%
    
    % uncertain eruptions count less
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subASzcount_w1pre(ii,:)=subASzcount_w1pre(ii,:).*0.250;
    subASzcount_w2pre(ii,:)=subASzcount_w2pre(ii,:).*0.375;
    subASzcount_w3pre(ii,:)=subASzcount_w3pre(ii,:).*0.500;
    subASzcount_w4pre(ii,:)=subASzcount_w4pre(ii,:).*0.667;
    subASzcount_w5pre(ii,:)=subASzcount_w5pre(ii,:).*0.833;
    %w6 is not required because it would be multiplying by 1
    
    subASzcount_w1post(ii,:)=subASzcount_w1post(ii,:).*0.250;
    subASzcount_w2post(ii,:)=subASzcount_w2post(ii,:).*0.375;
    subASzcount_w3post(ii,:)=subASzcount_w3post(ii,:).*0.500;
    subASzcount_w4post(ii,:)=subASzcount_w4post(ii,:).*0.667;
    subASzcount_w5post(ii,:)=subASzcount_w5post(ii,:).*0.833;
    %w6 is not required because it would be multiplying by 1
    
    %filling in the histograms with under-recording
    ASzcount_ALLund(ii,:)=round(subASzcount_w1pre(ii,:)+...
        subASzcount_w2pre(ii,:)+subASzcount_w3pre(ii,:)+...
        subASzcount_w4pre(ii,:)+subASzcount_w5pre(ii,:)+...
        subASzcount_w6pre(ii,:)+...
        subASzcount_w1post(ii,:)+subASzcount_w2post(ii,:)+...
        subASzcount_w3post(ii,:)+subASzcount_w4post(ii,:)+...
        subASzcount_w5post(ii,:)+subASzcount_w6post(ii,:));
    
    % old and small eruptions are more likely to have been missed
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for jj=1:length(p_rec)
        %it applies to all w1:w6!!
        subASzcount_w1pre(ii,jj)=subASzcount_w1pre(ii,jj)./p_rec(jj);
        subASzcount_w2pre(ii,jj)=subASzcount_w2pre(ii,jj)./p_rec(jj);
        subASzcount_w3pre(ii,jj)=subASzcount_w3pre(ii,jj)./p_rec(jj);
        subASzcount_w4pre(ii,jj)=subASzcount_w4pre(ii,jj)./p_rec(jj);
        subASzcount_w5pre(ii,jj)=subASzcount_w5pre(ii,jj)./p_rec(jj);
        subASzcount_w6pre(ii,jj)=subASzcount_w6pre(ii,jj)./p_rec(jj);
    end

    %filling the histogram for which under-recording has been addressed
    ASzcount_ALL(ii,:)=round(subASzcount_w1pre(ii,:)+...
        subASzcount_w2pre(ii,:)+subASzcount_w3pre(ii,:)+...
        subASzcount_w4pre(ii,:)+subASzcount_w5pre(ii,:)+...
        subASzcount_w6pre(ii,:)+...
        subASzcount_w1post(ii,:)+subASzcount_w2post(ii,:)+...
        subASzcount_w3post(ii,:)+subASzcount_w4post(ii,:)+...
        subASzcount_w5post(ii,:)+subASzcount_w6post(ii,:));  
    
%     fprintf('VNUM=%d, region=%d, country=%d, k=%d\n',vnum,vreg,...
%         vcountry,k);
%     fprintf('This is ASzcount_UR:%d\n',ASzcount_ALLund(ii,:));
%     fprintf('And ASzcount (no UR):%d\n',ASzcount_ALL(ii,:));
%     pause;
    
end


%normalising
%rowsum=nansum(AGcountmat,2); %calculating the sum of each row
rowsumALL=sum(ASzcount_ALL,2); %calculating the sum of each row
                               %(nansum should not be required anymore)
rowsumALLund=sum(ASzcount_ALLund,2); %calculating the sum of each row
                               %(nansum should not be required anymore)
                               

for ii=1:length(ASznorm_ALL(:,1))
    ASznorm_ALL(ii,:)=ASzcount_ALL(ii,:)./rowsumALL(ii);
    ASznorm_ALLund(ii,:)=ASzcount_ALLund(ii,:)./rowsumALLund(ii);
end

%calculating the ecdfs
ASzecdfmat=cumsum(ASznorm_ALL,2);
ASzecdfmat_UR=cumsum(ASznorm_ALLund,2);

%testing some bar plots (and some discrete ecdfs)
toplot=unidrnd(length(b.data(:,1)),10,1);

% for ii=1:length(b.data(:,1))%length(toplot)
%     figure();
%     subplot(1,2,1);
%     %bar(xvei,ASznorm_ALL(toplot(ii),:),'k');
%     bar(xvei,ASznorm_ALL(ii,:),'k');
%     set(gca,'FontSize',15,'LineWidth',1.5);
%     set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
%         'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
%     %axis([-(1/6),1+(1/6),0,1]);
%     axis([1 9 0 1])
%     box on;
%     %xlabel('ASz [dimless]');
%     xlabel('VEI'); ylabel('counts');
%     %title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+2,...
%      %   b.data(toplot(ii),1)));
%     title(sprintf('Volcano #%d (VNUM=%d)',ii+2,...
%         b.data(ii,1))); 
%      
%     subplot(1,2,2);
%     %bar(xvei,ASznorm_ALLund(toplot(ii),:),'k');
%     bar(xvei,ASznorm_ALLund(ii,:),'k');
%     set(gca,'FontSize',15,'LineWidth',1.5);
%     set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
%         'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
%     %axis([-(1/6),1+(1/6),0,1]);
%     axis([1 9 0 1])
%     box on;
%     %xlabel('ASz [dimless]');
%     xlabel('VEI'); ylabel('counts');
%     %title(sprintf('UR: Volcano #%d (VNUM=%d)',toplot(ii)+2,...
%      %   b.data(toplot(ii),1)));
%     title(sprintf('UR: Volcano #%d (VNUM=%d)',ii+2,...
%         b.data(ii,1)));
%     
% %     plot(xveinorm,ASzecdfmat(toplot(ii),:),'k','LineWidth',1.5);
% %     set(gca,'FontSize',15,'LineWidth',1.5);
% %     set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
% %         'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
% %     axis([0 1 0 1]);
% %     box on;
% %     xlabel('ASz [dimless]'); ylabel('ecdf');
% %     title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+2,...
% %         a.data(toplot(ii),1)));
% %    pause;
% %    close all;
% end

%%%NB. We will store two ASz matrices: one with UR (i.e. no correction
%%%applied) and another with UR partially corrected
%we create a vector with the VNUM identifier as well
VNUM=b.data(:,1);   %b is the VOTW Holocene volcano list in this script!

%we save the ASz vectors alongside the VNUM
save ASzmatrices.mat VNUM ASzcount_ALL ASzcount_ALLund...
    rowsumALL rowsumALLund ASznorm_ALL ASznorm_ALLund...
        ASzecdfmat ASzecdfmat_UR xvei xveinorm -v7.3
