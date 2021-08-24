% morphology_processing.m

%{Summary:

It performs a preliminary analysis of the morphology databases used by VOLCANS:
Pike and Clow (1981) and Grosse et al. (2014), and derives the data required to
calculate the single-criterion analogy matrix for volcano morphology.
It requires to import the data in the files: `PC81_GR2014_data.csv`, and
`VOTW467_8May18_volcano_data.csv` to carry out the aforementioned tasks.

%}

clear all
close all

%import the data
a=importdata('../VOLCANS_csv_files/PC81_GR2014_data.csv');

%final "discretised" matrix
%%datmat=zeros(length(a.data(:,1)),12);
datmat=nan(length(a.data(:,1)),12);

%filling in true data (reminder! columns 1-6: d, H, H/W*, T, sv, ave_ei)
HWall=a.data(:,8)./a.data(:,9); %H/W* data

datmat(:,1)=a.data(:,6); datmat(781,1)=1.37; %Quetrupillan crater
datmat(:,2)=a.data(:,8);
datmat(:,3)=HWall;
datmat(:,4)=a.data(:,12);
datmat(:,5)=a.data(:,13);
datmat(:,6)=a.data(:,11);

%filling in group/percentile data (columns 7-12 same order as before)

%creating a matrix to store the percentile values for the 6 variables
%NB. The NaN values in datmat(:,1:6) are not considered when calling the
%function "prctile". However, they appear as percentile group = 0 in
%datmat(:,7:12), if the initial matrix is of zeros! (see above)
percs=zeros(6,9);

for ii=1:length(percs(:,1))
    for jj=1:length(percs(1,:))
        percs(ii,jj)=prctile(datmat(:,ii),jj*10);
    end
end

%creating a matrix with the central measures of the percentiles
centrper=zeros(6,10);

%filling in that matrix plus the group indices
for ii=1:length(centrper(:,1))
    for jj=1:length(centrper(1,:))
        if jj==1
            ids=find(datmat(:,ii)<=percs(ii,jj));
            datmat(ids,ii+6)=jj;
            centrper(ii,jj)=(min(datmat(:,ii))+percs(ii,jj))./2;
        elseif jj==10
            ids=find(datmat(:,ii)>percs(ii,jj-1));
            datmat(ids,ii+6)=jj;
            centrper(ii,jj)=(percs(ii,jj-1)+max(datmat(:,ii)))./2;
        else
            ids=find(datmat(:,ii)>percs(ii,jj-1)&datmat(:,ii)<=percs(ii,jj));
            datmat(ids,ii+6)=jj;
            centrper(ii,jj)=(percs(ii,jj-1)+percs(ii,jj))./2;
        end
    end
end


%try to do a double-loop to plot everything
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

for ii=1:length(centrper(:,1))
    for jj=1:length(centrper(:,1))
            if ii~=jj
                subplot(length(centrper(:,1)),length(centrper(:,1)),...
                    ((ii-1).*length(centrper(:,1)))+jj);
                for kk=1:length(centrper(1,:))
                    scatter(centrper(ii,kk),...
                        nanmean(datmat(find(datmat(:,ii+...
                        length(centrper(:,1)))==kk),jj)),'b.'); hold on;
                end
            end
    end
end

%print -f1 -dpng -r300 discr_mean_patterns.png

figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

for ii=1:length(centrper(:,1))
    for jj=1:length(centrper(:,1))
            if ii~=jj
                subplot(length(centrper(:,1)),length(centrper(:,1)),...
                    ((ii-1).*length(centrper(:,1)))+jj);
                for kk=1:length(centrper(1,:))
                    scatter(centrper(ii,kk),...
                        nanvar(datmat(find(datmat(:,ii+...
                        length(centrper(:,1)))==kk),jj)),'b.'); hold on;
                end
            end
    end
end

%print -f2 -dpng -r300 discr_var_patterns.png


%cleaning datmat a bit to help processing
%findind non-NaN values (H, H/W* and T have no NaN values)
% dnonan=find(datmat(:,7));
% svnonan=find(datmat(:,11));
% einonan=find(datmat(:,12));
% dsvnonan=intersect(dnonan,svnonan);
% deinonan=intersect(dnonan,einonan);
% sveinonan=intersect(svnonan,einonan);
% allnonan=intersect(dnonan,sveinonan);

%means by percentile
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

for ii=1:length(centrper(:,1))
    for jj=1:length(centrper(:,1))
            if ii~=jj
                subplot(length(centrper(:,1)),length(centrper(:,1)),...
                    ((ii-1).*length(centrper(:,1)))+jj);
                hold on; title(''); hold on; ylabel(''); hold on;
                
                for kk=1:length(centrper(1,:))
                    scatter(kk,...
                        nanmean(datmat(find(datmat(:,ii+...
                        length(centrper(:,1)))==kk),jj+...
                        length(centrper(:,1)))),'b.');
                        axis([0 10 0 10]); hold on;
                        
                end
            end
    end
end

print -f3 -dpng -r300 discr_meanperc_patterns_ALL_good.png

%only with H, H/W*, T
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

for ii=[2,3,4]
    for jj=[2,3,4]
            if ii~=jj
                subplot(3,3,...
                    ((ii-1-1).*3)+jj-1);
                for kk=1:length(centrper(1,:))
                    scatter(kk,...
                        nanmean(datmat(find(datmat(:,ii+...
                        length(centrper(:,1)))==kk),jj+...
                        length(centrper(:,1)))),'b.');
                        axis([0 10 0 10]); hold on;
                        
                end
            end
    end
end

%print -f4 -dpng -r300 discr_meanperc_patterns_H_HW_T.png

%preliminary test of summing/substracting the values of the percentile
%groups according how the variables are correlated between volcanoes (the
%final goal is obtaining unique values for each volcano, if possible)

%first we take back the NaN values to zero values, so they do not affect
%the sum of percentile-group values
for ii=7:1:length(datmat(1,:))
    zeroing=find(isnan(datmat(:,ii)));
    datmat(zeroing,ii)=0;
end

%then we perform the sum
%choose the AM metric to include sv and ave_ei (svei=1) or not (svei=0)

svei=0;

if svei
    AM=datmat(:,7)+datmat(:,10)+datmat(:,11)+datmat(:,12)-...
        (datmat(:,8)+datmat(:,9));
    toph=150;
else
    AM=datmat(:,7)+datmat(:,10)-...
        (datmat(:,8)+datmat(:,9));
    toph=200;
end

%sort the vector in ascending order (but keeping the ids)
%AMsorted=zeros(length(AM),2);
%AMsorted(:,1)=1:1:length(AM);
%AMsorted(:,2)=AM;
%AMsorted=sortrows(AMsorted,2);
AMsorted=sort(AM);

%plot and see if values are unique (or how unique they are)
figure(); plot(AMsorted,'-o');
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('Volcano Index');
ylabel('non-normalised AM [dimless]','fontsize',14);
print -f5 -dpng -r300 zero_test_AM_scale.png

% %exploring some "volcano examples"
% shld=[594,702,35,73,471];
% cald=[65,187,273,657,837];
% stvolc1=[625,5,228,795,858];
% stvolc2=[329,561,611,813,140];
% 
% for ii=1:length(shld)
%     hold on; plot([0 900],[AM(shld(ii)) AM(shld(ii))],...
%         'k','LineWidth',1.5);
%     hold on; plot([0 900],[AM(cald(ii)) AM(cald(ii))],...
%         'm','LineWidth',1.5);
%     hold on; plot([0 900],[AM(stvolc1(ii)) AM(stvolc1(ii))],...
%         'r','LineWidth',1.5);
%     hold on; plot([0 900],[AM(stvolc2(ii)) AM(stvolc2(ii))],...
%         'r','LineWidth',1.5);
% end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% IMPORTING THE VOTW DATA AT THIS POINT!! %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

b=importdata('../VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv');

%fill the VOTW "volcano type" associated with each of the volcanoes in the
%morphology database (note that there might be stratovolcanoes that have
%grown inside a previous caldera-collapse area)

AM2=zeros(length(AM),2); %expanding the AM vector to include the info
AM2(:,1)=AM;             %1st column stores AM data

%2nd column stores volcano-type data as in the VOTW database
for ii=1:length(AM2(:,1))
    volcid=find(b.data(:,1)==a.data(ii,1));
    AM2(ii,2)=b.data(volcid,4); %assigning the "volcano type" number
end

%domain of AM variable
xx=-25:5:40;

%info on how many volcanoes are not present in the volcano morphology DB
fprintf('%d volcanoes are not in the volcmorph database\n',...
    length(b.data(:,1))-length(intersect(b.data(:,1),a.data(:,1)))); pause(2);

%getting the indices by 3 main groups: calderas, shields, stratovolcanoes
idcald=find(AM2(:,2)==1 | AM2(:,2)==2);
idshld=find(AM2(:,2)==20 | AM2(:,2)==21);
idstvolc1=find(AM2(:,2)==22 | AM2(:,2)==23 | AM2(:,2)==24);
idstvolc2=find(AM2(:,2)==3 | AM2(:,2)==4 | AM2(:,2)==5 | AM2(:,2)==6);

%manually moving some calderas to stratovolcanoes (or vice versa)
%Sibayak (described as cone), Singkut (ID), moved from
%calderas to stratovolcanoes
idcald=setxor(idcald,184);  idstvolc1=union(idstvolc1,184);
%Semuning, Ranau (ID), moved from calderas to stratovolcanoes
idcald=setxor(idcald,202);  idstvolc1=union(idstvolc1,202); 
%treating Taal volcano inside Taal Lake (PH) as a complex stratovolcano 
idcald=setxor(idcald,325);  idstvolc2=union(idstvolc2,325);
%Sakurajima, Aira (JP), moved from calderas to stratovolcanoes
idcald=setxor(idcald,341);  idstvolc1=union(idstvolc1,341);
%Kamuinupuri, Mashu (JP), moved from calderas to stratovolcanoes
idcald=setxor(idcald,406);  idstvolc1=union(idstvolc1,406);
%Nemo Peak (RU), moved from calderas to stratovolcanoes
idcald=setxor(idcald,438);  idstvolc1=union(idstvolc1,438);
%Gorely (RU), moved from calderas to stratovolcanoes
idcald=setxor(idcald,456);  idstvolc1=union(idstvolc1,456);
%Opala (RU), moved from calderas to stratovolcanoes
idcald=setxor(idcald,457);  idstvolc1=union(idstvolc1,457);
%Krasheninnikov (RU), moved from calderas to stratovolcanoes
idcald=setxor(idcald,467);  idstvolc1=union(idstvolc1,467);
%Mt Emmons, Lake Emmons (US), moved from calderas to stratovolcanoes
idcald=setxor(idcald,532);  idstvolc1=union(idstvolc1,532);
%Vent Mount (described as a cone), Aniakchak (US), moved from calderas to
%stratovolcanoes
idcald=setxor(idcald,540);  idstvolc1=union(idstvolc1,540);
%Timber Crater as a shield volcano of Crater Lake (US)
idcald=setxor(idcald,571);  idshld=union(idshld,571);
%Hatchery and Ripley Butte in Yellowstone (US) left unassigned 
idcald=setxor(idcald,[584,586]);    AM2([584,586],2)=-9999;
%Maipo (CL), moved from calderas to stratovolcanoes
idcald=setxor(idcald,761);  idstvolc1=union(idstvolc1,761);

%after having checked for repetitions...
%Laghi di Albano&Nemi (described as maars), Colli Albani (IT) left unassigned
idcald=setxor(idcald,[3,4]);    AM2([3,4],2)=-9999;
%Caldera del Piano and della Fossa (Vulcano, IT), moved to calderas
idstvolc1=setxor(idstvolc1,[11,12]);    idcald=union(idcald,[11,12]);
%Ngurdoto (described as a cone-crater of Meru, TZ) left unassigned
idstvolc1=setxor(idstvolc1,84);    AM2(84,2)=-9999;
%Tandikat-Singgalang (VU) considered as compound/complex (both edifices are
%considered)
idstvolc1=setxor(idstvolc1,195);  idstvolc2=union(idstvolc2,195);
%Danau Caldera, Karang (ID) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,209);  idcald=union(idcald,209);
%Sunda Caldera, Tangkubanparahu (ID) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,214);  idcald=union(idcald,214);
%Idjen Caldera, Ijen (ID) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,241);  idcald=union(idcald,241);
%Segera Caldera, Rinjani (ID) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,247);  idcald=union(idcald,247);
%Banahaw (San Cristobal; PH) moved from compound/complex to simple
idstvolc2=setxor(idstvolc2,321);  idstvolc1=union(idstvolc1,321);
%Toya Caldera, Toya (JP) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,397);  idcald=union(idcald,397);
%Tao-Rusyr (Caldera, RU) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,437);  idcald=union(idcald,437);
%Makushin Caldera (US) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,522);  idcald=union(idcald,522);
%Crater Ridge (described as a dome), in Edgecumbe (US) left unassigned
idstvolc1=setxor(idstvolc1,555);    AM2(555,2)=-9999;
%Prospect Peak as shield volcano of Lassen Volcanic Center (US)
idstvolc1=setxor(idstvolc1,575);  idshld=union(idshld,575);
%Lake Atitlan (Caldera), Atitlan (GT) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,616);  idcald=union(idcald,616);
%Viejo volcano, in Nevados de Chillan (CL), considered as compound/complex
%(e.g. two peaks in summit region)
idstvolc1=setxor(idstvolc1,772);  idstvolc2=union(idstvolc2,772);
%Cordillera Nevada caldera moved to calderas and Puyehue-Cordon Caulle
%(when delineation includes several peaks) is moved to complex/compound
%stratovolcanoes (both are in Puyehue-Cordon Caulle)
idstvolc1=setxor(idstvolc1,786);  idcald=union(idcald,786);
idstvolc1=setxor(idstvolc1,784);  idstvolc2=union(idstvolc2,784);
%Kollottadyngja as shield volcano of Askja (IS)
idstvolc1=setxor(idstvolc1,832);  idshld=union(idshld,832);
%Ketildyngja as shield volcano of Fremrinamar (IS)
idstvolc1=setxor(idstvolc1,833);  idshld=union(idshld,833);
%Cinco Picos caldera, Terceira (PT) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,842);  idcald=union(idcald,842);
%Furnas entry taken as a caldera and Povoacao caldera, Furnas (PT),
%both moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,[846,847]);  idcald=union(idcald,[846,847]);
%Tenerife Caldera, Tenerife (ES) moved from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,850);  idcald=union(idcald,850);
%Fogo, Cape Verde (whole-island entry, which includes the caldera) moved
%from stratovolcanoes to calderas
idstvolc1=setxor(idstvolc1,852);  idcald=union(idcald,852);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%spotting duplicate values in VNUM
[C,ia,ic]=unique(a.data(:,1),'first');
dups=setxor(1:1:length(a.data(:,1)),ia)';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

idcald=idcald';
idstvolc1=idstvolc1';

idstvolcN=vertcat(idstvolc1,idstvolc2);

%fprintfing some information
fprintf('Calderas mean, variance and [min,max] AM values: %.2f, %.2f, [%.2f,%.2f]\n',...
    mean(AM2(idcald,1)),var(AM2(idcald,1)),min(AM2(idcald,1)),max(AM2(idcald,1)));

pause(2);

fprintf('Shields mean, variance and [min,max] AM values: %.2f, %.2f, [%.2f,%.2f]\n',...
    mean(AM2(idshld,1)),var(AM2(idshld,1)),min(AM2(idshld,1)),max(AM2(idshld,1)));

pause(2);

fprintf('Stratovolcanoes mean, variance and [min,max] AM values: %.2f, %.2f, [%.2f,%.2f]\n',...
    mean(AM2(idstvolc1,1)),var(AM2(idstvolc1,1)),min(AM2(idstvolc1,1)),max(AM2(idstvolc1,1)));

pause(2);

fprintf('Complex/Compound Stratovolcanoes mean, variance and [min,max] AM values: %.2f, %.2f, [%.2f,%.2f]\n',...
    mean(AM2(idstvolc2,1)),var(AM2(idstvolc2,1)),min(AM2(idstvolc2,1)),max(AM2(idstvolc2,1)));

pause(2);

fprintf('Any Stratovolcano mean, variance and [min,max] AM values: %.2f, %.2f, [%.2f,%.2f]\n',...
    mean(AM2(idstvolcN,1)),var(AM2(idstvolcN,1)),min(AM2(idstvolcN,1)),max(AM2(idstvolcN,1)));

%plotting more complete information (histograms)

%stratovolcanoes grouped
figure();
subplot(2,2,1); hist(AM2(idcald,1),xx); hold on;
                plot([median(AM2(idcald,1)) median(AM2(idcald,1))],...
                    [0 150],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 150]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Calderas'); legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;

subplot(2,2,2); hist(AM2(idshld,1),xx); hold on;
                plot([median(AM2(idshld,1)) median(AM2(idshld,1))],...
                    [0 150],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 150]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Shields'); legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;
                
subplot(2,2,3); hist(AM2(idstvolcN,1),xx); hold on;
                plot([median(AM2(idstvolcN,1)) median(AM2(idstvolcN,1))],...
                    [0 toph],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 toph]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('ALL stratovolcanoes');
                legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;
                
print -f6 -dpng -r300 AM_3_volcano_types.png
                
%stratovolcanoes separated between simple and compound/complex
figure();
subplot(2,2,1); hist(AM2(idcald,1),xx); hold on;
                plot([median(AM2(idcald,1)) median(AM2(idcald,1))],...
                    [0 150],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 150]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Calderas'); legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;

subplot(2,2,2); hist(AM2(idshld,1),xx); hold on;
                plot([median(AM2(idshld,1)) median(AM2(idshld,1))],...
                    [0 150],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 150]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Shields'); legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;
                
subplot(2,2,3); hist(AM2(idstvolc1,1),xx); hold on;
                plot([median(AM2(idstvolc1,1)) median(AM2(idstvolc1,1))],...
                    [0 toph],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 toph]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Simple stratovolcanoes');
                legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;

subplot(2,2,4); hist(AM2(idstvolc2,1),xx); hold on;
                plot([median(AM2(idstvolc2,1)) median(AM2(idstvolc2,1))],...
                    [0 toph],'c','LineWidth',1.5,'LineStyle','--');
                axis([-20 40 0 toph]);
                xlabel('non-normalised AM [dimless]'); ylabel('counts');
                title('Compound/Complex stratovolcanoes');
                legend({'data','median'},'FontSize',10);
                set(gca,'FontSize',15,'LineWidth',1.5,...
                    'XTick',-20:10:40); box on;

print -f7 -dpng -r300 AM_4_volcano_types.png

%testing if any of the 5 groups (in 10 combinations of 2 groups) passes a
%2-sample Kolmogorov-Smirnov test (5% significance level) that their AM
%values might have been sampled from a common underlying distribution
%%%group ordering (rows or cols independently) is: calderas, shields,
%%%simple stratovolcanoes (st1), complex/compound stratovolcanoes (st2),
%%%all stratovolcanoes (stN)
hAM=nan(5,5); pAM=nan(5,5);

[hAM(1,2) pAM(1,2)]=kstest2(AM2(idcald,1),AM2(idshld,1));
[hAM(1,3) pAM(1,3)]=kstest2(AM2(idcald,1),AM2(idstvolc1,1));
[hAM(1,4) pAM(1,4)]=kstest2(AM2(idcald,1),AM2(idstvolc2,1));
[hAM(1,5) pAM(1,5)]=kstest2(AM2(idcald,1),AM2(idstvolcN,1));
[hAM(2,3) pAM(2,3)]=kstest2(AM2(idshld,1),AM2(idstvolc1,1));
[hAM(2,4) pAM(2,4)]=kstest2(AM2(idshld,1),AM2(idstvolc2,1));
[hAM(2,5) pAM(2,5)]=kstest2(AM2(idshld,1),AM2(idstvolcN,1));
[hAM(3,4) pAM(3,4)]=kstest2(AM2(idstvolc1,1),AM2(idstvolc2,1));
[hAM(3,5) pAM(3,5)]=kstest2(AM2(idstvolc1,1),AM2(idstvolcN,1));
[hAM(4,5) pAM(4,5)]=kstest2(AM2(idstvolc2,1),AM2(idstvolcN,1));

%let's plot the histograms normalised (sort of pdfs)
Ncald=hist(AM2(idcald,1),xx);   Ncald=Ncald./length(idcald);
Nshld=hist(AM2(idshld,1),xx);   Nshld=Nshld./length(idshld);
Nst1=hist(AM2(idstvolc1,1),xx); Nst1=Nst1./length(idstvolc1);
Nst2=hist(AM2(idstvolc2,1),xx); Nst2=Nst2./length(idstvolc2);
NstN=hist(AM2(idstvolcN,1),xx); NstN=NstN./length(idstvolcN);

figure();
plot(xx,Ncald,'r','Linewidth',1.5,'LineStyle','--'); hold on;
plot(xx,Nshld,'k','Linewidth',1.5,'LineStyle','--'); hold on;
plot(xx,Nst1,'b','Linewidth',1.5,'LineStyle','--'); hold on;
plot(xx,Nst2,'c','Linewidth',1.5,'LineStyle','--'); hold on;
%stem(xx,Ncald,'r','filled'); hold on; 
%stem(xx,Nshld,'k','filled'); hold on; %set(get(b2,'Children'),'FaceAlpha',0.3);
%stem(xx,Nst1,'b','filled'); hold on;  %set(get(b3,'Children'),'FaceAlpha',0.5);
%stem(xx,Nst2,'c','filled'); hold on;
%%set(get(b3,'Children'),'FaceAlpha',0.7);
%%%%%%%xtickvar=[-19,-11.4,-3.8,3.8,11.4,19]; xticklabvar=(xtickvar+19)/.38;
legend({'Calderas','Shield volcanoes','Simple stratovolcanoes',...
    'Complex stratovolcanoes'},'location','nw','FontSize',10);
% set(gca,'FontSize',15,'LineWidth',1.5,...
%     'XTick',[-19,-11.4,-3.8,3.8,11.4,19],'XTickLabel',0:0.2:1,...
%     'YTick',0:0.1:0.6,'YTickLabel',0:0.1:0.6);
set(gca,'FontSize',15,'LineWidth',1.5,...
    'YTick',0:0.1:0.6,'YTickLabel',0:0.1:0.6);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
axis([-30 30 0 0.6]); %axis([-19 19 0 0.6])
%xlabel('non-normalised AM [dimless]'); ylabel('pdf');
xlabel('M [dimensionless]'); ylabel('probability distribution');
print -f8 -dpng -r300 AM_pdfs_volctypes_4.png

figure();
plot(xx,Ncald,'r','Linewidth',1.5,'LineStyle','--'); hold on;
plot(xx,Nshld,'k','Linewidth',1.5,'LineStyle','--'); hold on;
plot(xx,NstN,'b','Linewidth',1.5,'LineStyle','--'); hold on;
legend({'Calderas','Shields','All stvolcs'},...
    'location','nw','FontSize',12);
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('non-normalised AM [dimless]'); ylabel('pdf');
print -f9 -dpng -r300 AM_pdfs_volctypes_3.png

%ECDFs with true, final AM scale
%analogy-in-morphology scale, after normalisation
wdth=max(AM2(:,1))-min(AM2(:,1));   %domain of non-normalised AM variable
nonze=abs(min(AM2(:,1))); %shift in the AM scale to ensure positive values

%let's also plot the ecdfs
[f1 x1]=ecdf((AM2(idcald,1)+nonze)./wdth);
[f2 x2]=ecdf((AM2(idshld,1)+nonze)./wdth);
[f3 x3]=ecdf((AM2(idstvolcN,1)+nonze)./wdth);

figure();
plot(x1,f1,'r','LineWidth',1.5); hold on;
plot(x2,f2,'k','LineWidth',1.5); hold on;
plot(x3,f3,'b','LineWidth',1.5); hold on;
legend({'Calderas','Shields','All stratovolcanoes'},...
    'location','nw','FontSize',12);
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('AM [dimless]');
ylabel('P(X<=x)','fontsize',14);
print -f10 -dpng -r300 AM_volctypes_3_ECDF.png

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WE CREATE THE MORPHOLOGY-ANALOGY SCALE IN HERE %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
%here we calculate the new domain of the AM variable to be AM=[0,1-jumpsp]
[C2,ia2,ic2]=unique(AM2(:,1));  %ia2 is the total number of AM "classes",
                                %without taking into account Volc. Fields
jumpsp=1./length(ia2);  %we do not need to do length(ia2)-1 because we have
                        %to take VFs in the categories. That is, what we
                        %should actually do is: (length(ia2)+1)-1
wdth2=wdth./(1-jumpsp);
AM2toscale=(AM2(:,1)+nonze)./wdth2;
 
%vector where the values of AM will be stored
AMlast=nan(length(b.data(:,1)),1);
 
%let's calculate the mean value of each of the main groups (calderas,
%shields, simple stvolcs, complex/compound stvolcs, any stvolc)
meancald=mean(AM2toscale(idcald));
meanshld=mean(AM2toscale(idshld));
meanstvolc1=mean(AM2toscale(idstvolc1));
meanstvolc2=mean(AM2toscale(idstvolc2));
meanstvolcN=mean(AM2toscale(idstvolcN));
 
%let's try to automatically assign the correct morphological value to each
%volcano entry
 
for ii=1:length(AMlast)
    %get the volcano type as in (adapted) VOTW
    volctype=b.data(ii,4);
    %check if there is an entry in the merged morphoDB corresponding to the
    %VNUM
    inmerged=find(a.data(:,1)==b.data(ii,1));
    
    %need to reset sametype at the beginning of each iteration!!
    sametype=[];
   
    %check for volcanic fields first
    if volctype==32 || volctype==33
        AMlast(ii)=1;
    %for the rest, if "inmerged" is empty, assign mean values of AM
    elseif isempty(inmerged)
            switch volctype
                case {1, 2}
                    AMlast(ii)=meancald;
                case {20, 21}
                    AMlast(ii)=meanshld;
                case {22, 23, 24}
                    AMlast(ii)=meanstvolc1;
                case {3, 4, 5, 6}
                    AMlast(ii)=meanstvolc2;
                otherwise
                    AMlast(ii)=-9999;
            end
    %if "inmerged" is not empty and has more than 1 value, assign the value
    %that corresponds with the volctype in the VOTW database
    elseif length(inmerged)>1
        switch volctype
                case {1, 2}
                    sametype=intersect(inmerged,idcald);
                case {20, 21}
                    sametype=intersect(inmerged,idshld);
                case {22, 23, 24}
                    sametype=intersect(inmerged,idstvolc1);
                case {3, 4, 5, 6}
                    sametype=intersect(inmerged,idstvolc2);             
        end
             
        if ~isempty(sametype)
            if length(sametype)>1
                %%disp(inmerged)
                %%fprintf('The above entries need to be checked in detail\n')
                %%pause(1)
            elseif length(sametype)==1  
                AMlast(ii)=AM2toscale(sametype);
            end
            
            %%sametype %display it if it's not empty
            
        else
                AMlast(ii)=-9999;
        end
    elseif length(inmerged)==1
        AMlast(ii)=AM2toscale(inmerged);
    end
    
    %%fprintf('AMlast=%.3f, loop #%d finished\n',AMlast(ii),ii);
    
    %%pause; %we display volctype, inmerged and sametype for each
               %volcano in the loop and see if there is something
               %unexpected
end

%%pause;

AMlast(91)=mean(AM2toscale([60,61],1)); %mean value of AM of Boset&Bericha
AMlast(338)=mean(AM2toscale([174,175],1)); %mean value of AM of 2 stratovolcs
                                           %in North Vate
AMlast(361)=mean(AM2toscale([193,194],1)); %mean value of AM of Tandikat&
                                           %Singgalang                                         
AMlast(486)=mean(AM2toscale([304,305],1)); %mean value of AM of 2 stratovolcs
                                           %of Camiguin
AMlast(493)=mean(AM2toscale([312,313],1)); %mean value of AM of 2 stratovolcs
                                           %of Biliran
AMlast(632)=mean(AM2toscale([389,390],1)); %mean value of AM of 2 stratovolcs
                                           %of Pagan
AMlast(760)=mean(AM2toscale([475,476],1)); %mean value of AM of 2 stratovolcs
                                           %of Udina
AMlast(960)=mean(AM2toscale([566,567],1)); %mean value of AM of 2 stratovolcs
                                           %of 3 Sisters
AMlast(984)=AM2toscale(587,1); %Yellowstone as the Caldera
AMlast(1196)=mean(AM2toscale([711,712],1)); %mean value of AM of 2 stratovolcs
					    %of Sabancaya (+Ampato)

AMlast(1257)=mean(AM2toscale([758,759],1)); %mean value of AM of 2 shields
                                            %of Easter Is

AMlast(1356)=mean(AM2toscale([824,825,828],1)); %mean value of AM of 3
                                                %shields volcanoes of
                                                %Langjokull

AMlast(1385)=AM2toscale(841,1); %Terceira as the Grosse et al. (2014) entry
				%(assumed to be "stratovolcano(es))"

AMlast(1398)=-9999;   %discard "La Caldera de la Alegranza" (Lanzarote)

%plotting histograms of the variable AM
figure()
hist(AMlast,-0.1:0.1:1); xlim([-0.05 1.05])
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('AM [dimless]'); ylabel('counts');
print -f11 -dpng -r300 AM_final_hist_10bins.png

figure();
hist(AMlast,-0.05:0.05:1); xlim([-0.025 1.025])
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('AM [dimless]'); ylabel('counts');
print -f12 -dpng -r300 AM_final_hist_20bins.png

%we create a vector with the VNUM identifier as well
VNUM=b.data(:,1);

%we save the VNUM and AMlast vectors
save AMmatrices_QUET.mat VNUM AMlast datmat AM2 idcald idshld...
    idstvolc1 idstvolc2 idstvolcN wdth2 nonze -v7.3                
