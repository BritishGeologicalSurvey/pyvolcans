% votw_analysis.m

%{Summary:

It performs a preliminary analysis of the volcano data in the GVP database (v4.6.7),
and derives the data required to calculate the single-criterion analogy matrices for
tectonic setting and rock geochemistry. It requires to import the data in the file
`VOTW467_8May18_volcano_data.csv` to carry out the aforementioned tasks.

%}

clear all
close all

%importing the data
a=importdata('../VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv');

%coarse separation of tectonic settings
intpt=find(a.data(:,13)==1 | a.data(:,13)==2 | a.data(:,13)==3);
rift=find(a.data(:,13)==4 | a.data(:,13)==5 | a.data(:,13)==6);
subd=find(a.data(:,13)==7 | a.data(:,13)==8 | a.data(:,13)==9 | ...
    a.data(:,13)==10);

alltect=[intpt;rift;subd];  %concatenating tectonic settings

%plotting volcanoes by tectonic setting
load coast
figure(); plot(long,lat,'k');
hold on; scatter(a.data(:,10),a.data(:,9),'r^','filled');
hold on; scatter(a.data(rift,10),a.data(rift,9),'g^','filled');
hold on; scatter(a.data(subd,10),a.data(subd,9),'b^','filled');
legend({'coastline','intraplate','rift','subduction'},'FontSize',10,...
    'location','best');
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('Longitude [deg]','fontsize',14);
ylabel('Latitude [deg]','fontsize',14);
print -f1 -dpng -r300 volcanoes_by_tectosett.png

%histogram of simple tectonic types: intrapt, rift, subduction
figure(); hist(a.data([intpt;rift;subd],13),[2 5 8.5]);

%plotting volcanoes by primary rock type
ande=find(a.data(:,12)==1);
bas=find(a.data(:,12)==2);
dac=find(a.data(:,12)==3);
rhy=find(a.data(:,12)==8);
alk=find(a.data(:,12)==4 | a.data(:,12)==6 | a.data(:,12)==7 | ...
    a.data(:,12)==9 | a.data(:,12)==10 | a.data(:,12)==11);

allrock=[bas;ande;dac;rhy;alk]; %concatenating all (dominant) rock types

%let's deal with all rock types here as well
%we start with finding out the volcanoes that lack each major and minor
%rock types (max. 5 types per category)
noMR1=find(a.data(:,14)==-9999);    nomR1=find(a.data(:,19)==-9999);
noMR2=find(a.data(:,15)==-9999);    nomR2=find(a.data(:,20)==-9999);
noMR3=find(a.data(:,16)==-9999);    nomR3=find(a.data(:,21)==-9999);
noMR4=find(a.data(:,17)==-9999);    nomR4=find(a.data(:,22)==-9999);
noMR5=find(a.data(:,18)==-9999);    nomR5=find(a.data(:,23)==-9999);


figure(); plot(long,lat,'k');
hold on; scatter(a.data(bas,10),a.data(bas,9),'k^','filled');
hold on; scatter(a.data(ande,10),a.data(ande,9),'b^','filled');
hold on; scatter(a.data(dac,10),a.data(dac,9),'c^','filled');
hold on; scatter(a.data(rhy,10),a.data(rhy,9),'r^','filled');
hold on; scatter(a.data(alk,10),a.data(alk,9),'g^','filled');

legend({'coastline','basalt','andesite','dacite','rhyolite',...
    'other'},'FontSize',10,'location','best');
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('Longitude [deg]','fontsize',14);
ylabel('Latitude [deg]','fontsize',14);
print -f3 -dpng -r300 volcanoes_by_rocktype.png

%histogram of simple rock types: ande, bas, dac, rhy, other
figure(); hist(a.data(allrock,12),1:1:11);
set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D',...
                        'F','','P','Z','R','Y','X','T'});

%getting the indexes for volcanoes with both tectonic setting and rock type
%assigned
alltectrock=intersect(alltect,allrock);

%plot their zero-order relationship (hist3)
figure();
hist3([a.data(alltectrock,13) a.data(alltectrock,12)],'Ctrs',{1:1:11 1:1:11});
xlabel('tectonic setting'); ylabel('rock type');

%probably better as "slices" through tectonic setting
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

N=zeros(10,11); %here we will store the counts for each rock type (cols)
                %and taking into account each tectonic setting (rows)
rockratios=zeros(10,4); %here some rock-type ratios of interest
                        %e.g. basalt/andesite; andesite/dacite;
                        %basalt/rhyolite; subalk/alk

for ii=1:10
    subplot(2,5,ii);
    idx=find(a.data(:,13)==ii);
    idx2=intersect(idx,allrock);
    N(ii,:)=hist(a.data(idx2,12),1:1:11);
    hist(a.data(idx2,12),1:1:11);
    axis([0 12 0 max(N(ii,:))+10])
    xlabel('rock type'); ylabel('counts');
    
    
    rockratios(ii,1)=N(ii,2)./N(ii,1);
    rockratios(ii,2)=N(ii,1)./N(ii,3);
    rockratios(ii,3)=N(ii,2)./N(ii,8);
    %NB.rocktype=5 --> no data
    rockratios(ii,4)=sum(N(ii,[1,2,3,8]))./sum(N(ii,[4,6,7,9:11]));  
end

%%print -f6 -dpng -r300 rocktypes_by_tectosett1.png

%plot also grouped tectonic settings (intrapt, rift, subduction)
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

subplot(1,3,1); hist(a.data(intersect(intpt,allrock),12),...
                    1:1:11);
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D',...
                        'F','','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 600]);
                title('Intraplate');
subplot(1,3,2); hist(a.data(intersect(rift,allrock),12),...
                    1:1:11);
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D',...
                        'F','','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 600]);
                title('Rift zone');
subplot(1,3,3); hist(a.data(intersect(subd,allrock),12),...
                    1:1:11);
                    set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D',...
                        'F','','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 600]);
                title('Subduction zone');

print -f7 -dpng -r300 rocktypes_by_tectosett2.png
                
%plotting the rock ratios
figure();
scatter(1:1:10,rockratios(:,1),'k','filled'); hold on;
scatter(1:1:10,rockratios(:,2),'c','filled'); hold on;
scatter(1:1:10,rockratios(:,3),'r','filled'); hold on;
scatter(1:1:10,rockratios(:,4),'g','filled'); hold on;
legend({'basalt/andesite','andesite/dacite','basalt/rhyolite',...
    'subalkaline/alkaline'},'FontSize',10,'location','best');
xlim([0 11]);
set(gca,'FontSize',15,'LineWidth',1.5,'XTick',1:1:10,...
    'XTickLabel',{'IpC','IpI','IpO','RC','RI','RO','SC','SUnk','SI','SO'});
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('Tectonic setting','fontsize',14);
ylabel('Rock-type ratio','fontsize',14);
print -f8 -dpng -r300 rockratios_by_tectosett1.png

%create and plot a more general rock-ratios by intraplate, rift, subduction
rockratios2=zeros(3,4);

for ii=1:3
    switch ii
        case 1
            rng=1:3;
        case 2
            rng=4:6;
        case 3
            rng=7:10;
    end
    rockratios2(ii,1)=sum(N(rng,2))./sum(N(rng,1));
    rockratios2(ii,2)=sum(N(rng,1))./sum(N(rng,3));
    rockratios2(ii,3)=sum(N(rng,2))./sum(N(rng,8));
    rockratios2(ii,4)=sum(sum(N(rng,[1,2,3,8])))./...
        sum(sum(N(rng,[4,6,7,9:11])));
end

figure();
scatter(1:1:3,rockratios2(:,1),'k','filled'); hold on;
scatter(1:1:3,rockratios2(:,2),'c','filled'); hold on;
scatter(1:1:3,rockratios2(:,3),'r','filled'); hold on;
scatter(1:1:3,rockratios2(:,4),'g','filled'); hold on;
legend({'basalt/andesite','andesite/dacite','basalt/rhyolite',...
    'subalkaline/alkaline'},'FontSize',10,'location','best');
xlim([0 4]);
set(gca,'FontSize',15,'LineWidth',1.5,'XTick',1:1:3,...
    'XTickLabel',{'IntPt','Rift','Subd'});
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('Tectonic setting','fontsize',14);
ylabel('Rock-type ratio','fontsize',14);
print -f9 -dpng -r300 rockratios_by_tectosett2.png

%plotting some in-country variability of dominant rock type
%namely: Japan (excluding Kuril Is), USA, Chile (including borders)
%and Indonesia
%getting the data first
idxJp=find(a.data(:,3)==52); idxJp2=intersect(idxJp,allrock);
idxUS=find(a.data(:,3)==92); idxUS2=intersect(idxUS,allrock);   
idxCl=find(a.data(:,3)==13 | a.data(:,3)==14 |...
    a.data(:,3)==15 | a.data(:,3)==16); idxCl2=intersect(idxCl,allrock);
idxId=find(a.data(:,3)==49); idxId2=intersect(idxId,allrock);
%also Ethiopia (including borders)
idxEt=find(a.data(:,3)==33 | a.data(:,3)==34 | a.data(:,3)==35 |...
    a.data(:,3)==36 | a.data(:,3)==37); idxEt2=intersect(idxEt,allrock);

%now plotting the bar plots (dominant rock type)
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

subplot(2,2,1); NJp=hist(a.data(idxJp2,12),1:1:11);
                for ii=1:length(NJp)
                    h=bar(ii,NJp(ii),'w'); hold on;
                    if ii==5 || ii==6 || ii==7
                        set(h,'FaceColor','r'); hold on;
                    end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
                title(sprintf('Japan (%d volcanoes)',sum(NJp)));
                
subplot(2,2,2); NUS=hist(a.data(idxUS2,12),1:1:11);
                for ii=1:length(NUS)
                    h=bar(ii,NUS(ii)); hold on;                    
                    if ii==3 || ii==6 || ii==9
                        set(h,'FaceColor','r'); hold on;
                    elseif ii==2 || ii==5 || ii==8 || ii==11
                        set(h,'FaceColor','w'); hold on;
                    end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
                title(sprintf('USA (%d volcanoes)',sum(NUS)));
                
subplot(2,2,3); NCl=hist(a.data(idxCl2,12),1:1:11);
                for ii=1:length(NCl)
                    h=bar(ii,NCl(ii)); hold on;
                    if ii==1 || ii==4 || ii==7 || ii==10
                        set(h,'FaceColor','r'); hold on;
                    elseif ii==2 || ii==5 || ii==8 || ii==11
                        set(h,'FaceColor','w'); hold on;
                    end  
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
                title(sprintf('Chile (%d volcanoes)',sum(NCl)));
                
subplot(2,2,4); NId=hist(a.data(idxId2,12),1:1:11);
                for ii=1:length(NId)
                    h=bar(ii,NId(ii),'r'); hold on;
                    if ii==6 || ii==7 || ii==8 || ii==9 || ii==10 || ii==11
                        set(h,'FaceColor','w'); hold on;
                   end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
                title(sprintf('Indonesia (%d volcanoes)',sum(NId)));
                
print -f10 -dpng -r300 rocktype_variability_countries_1rock.png

%plotting Ethiopia rock types (dominant)
figure();
NEt=hist(a.data(idxEt2,12),1:1:11);
for ii=1:length(NEt)
    h=bar(ii,NEt(ii),'r'); hold on;
    if ii==1 || ii==2 || ii==3 || ii==4
        set(h,'FaceColor','g'); hold on;
    elseif ii==5 || ii==6 || ii==7
        set(h,'FaceColor','y'); hold on;
    end
end
set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
    '','P','Z','R','Y','X','T'});
xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
title(sprintf('Ethiopia (%d volcanoes)',sum(NEt)));
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

print -f11 -dpng -r300 rocktype_variability_Ethiopia_1rock.png

%now plotting the bar plots (ALL rock types)
figure();
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

%NB. We have to count the minor rock types as half a datum compared to
%major rock types
%1. Getting the into single-column vectors
JpMR=reshape(a.data(idxJp2,14:18),[],1);
JpmR=reshape(a.data(idxJp2,19:23),[],1);

USMR=reshape(a.data(idxUS2,14:18),[],1);
USmR=reshape(a.data(idxUS2,19:23),[],1);

ClMR=reshape(a.data(idxCl2,14:18),[],1);
ClmR=reshape(a.data(idxCl2,19:23),[],1);

IdMR=reshape(a.data(idxId2,14:18),[],1);
IdmR=reshape(a.data(idxId2,19:23),[],1);

EtMR=reshape(a.data(idxEt2,14:18),[],1);
EtmR=reshape(a.data(idxEt2,19:23),[],1);

%2. Calculating the histograms
NJpMR=hist(JpMR,-1:1:11);   %the -1 bin is needed to get rid of "empty"
                            %(i.e. -9999) rock types
NJpMR=NJpMR.*2;             %Major rocks count double the minor rocks                            
NJpmR=hist(JpmR,-1:1:11);   %same for minor rocks (no correction applied)

NUSMR=hist(USMR,-1:1:11);   %the -1 bin is needed to get rid of "empty"
                            %(i.e. -9999) rock types
NUSMR=NUSMR.*2;             %Major rocks count double the minor rocks                            
NUSmR=hist(USmR,-1:1:11);   %same for minor rocks (no correction applied)

NClMR=hist(ClMR,-1:1:11);   %the -1 bin is needed to get rid of "empty"
                            %(i.e. -9999) rock types
NClMR=NClMR.*2;             %Major rocks count double the minor rocks                            
NClmR=hist(ClmR,-1:1:11);   %same for minor rocks (no correction applied)

NIdMR=hist(IdMR,-1:1:11);   %the -1 bin is needed to get rid of "empty"
                            %(i.e. -9999) rock types
NIdMR=NIdMR.*2;             %Major rocks count double the minor rocks                            
NIdmR=hist(IdmR,-1:1:11);   %same for minor rocks (no correction applied)

NEtMR=hist(EtMR,-1:1:11);   %the -1 bin is needed to get rid of "empty"
                            %(i.e. -9999) rock types
NEtMR=NEtMR.*2;             %Major rocks count double the minor rocks                            
NEtmR=hist(EtmR,-1:1:11);   %same for minor rocks (no correction applied)


%3. Merging the histograms actually
NJpAll=NJpMR+NJpmR;
NJpAll=NJpAll(3:end);   %getting rid of the -9999 and 0 bins

NUSAll=NUSMR+NUSmR;
NUSAll=NUSAll(3:end);   %getting rid of the -9999 and 0 bins

NClAll=NClMR+NClmR;
NClAll=NClAll(3:end);   %getting rid of the -9999 and 0 bins

NIdAll=NIdMR+NIdmR;
NIdAll=NIdAll(3:end);   %getting rid of the -9999 and 0 bins

NEtAll=NEtMR+NEtmR;
NEtAll=NEtAll(3:end);   %getting rid of the -9999 and 0 bins

%3. Plotting the histogram as a bar
subplot(2,2,1); for ii=1:length(NJpAll)
                    h=bar(ii,NJpAll(ii),'w'); hold on;
                    if ii==5 || ii==6 || ii==7
                        set(h,'FaceColor','r'); hold on;
                    end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); xlim([0 12]);
                title(sprintf('Japan (%d volcanoes)',length(JpMR)./5));            
                                
subplot(2,2,2); for ii=1:length(NUSAll)
                    h=bar(ii,NUSAll(ii)); hold on;                    
                    if ii==3 || ii==6 || ii==9
                        set(h,'FaceColor','r'); hold on;
                    elseif ii==2 || ii==5 || ii==8 || ii==11
                        set(h,'FaceColor','w'); hold on;
                    end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); xlim([0 12]);
                title(sprintf('USA (%d volcanoes)',length(USMR)./5));
                                
subplot(2,2,3); for ii=1:length(NClAll)
                    h=bar(ii,NClAll(ii)); hold on;
                    if ii==1 || ii==4 || ii==7 || ii==10
                        set(h,'FaceColor','r'); hold on;
                    elseif ii==2 || ii==5 || ii==8 || ii==11
                        set(h,'FaceColor','w'); hold on;
                    end  
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); xlim([0 12]);
                title(sprintf('Chile (%d volcanoes)',length(ClMR)./5));
                                
subplot(2,2,4); for ii=1:length(NIdAll)
                    h=bar(ii,NIdAll(ii),'r'); hold on;
                    if ii==6 || ii==7 || ii==8 || ii==9 || ii==10 || ii==11
                        set(h,'FaceColor','w'); hold on;
                   end
                end
                set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
                    '','P','Z','R','Y','X','T'});
                xlabel('rock type'); ylabel('counts'); xlim([0 12]);
                title(sprintf('Indonesia (%d volcanoes)',length(IdMR)./5));
                                
print -f12 -dpng -r300 rocktype_variability_countries_allrocks.png

%same for Ethiopia (all rock types)
figure();
for ii=1:length(NEtAll)
    h=bar(ii,NEtAll(ii),'r'); hold on;
    if ii==1 || ii==2 || ii==3 || ii==4
        set(h,'FaceColor','g'); hold on;
    elseif ii==5 || ii==6 || ii==7
        set(h,'FaceColor','y'); hold on;
    end
end
set(gca,'XTick',1:1:11,'XTickLabel',{'A','B','D','F',...
    '','P','Z','R','Y','X','T'});
xlabel('rock type'); ylabel('counts'); axis([0 12 0 100]);
title(sprintf('Ethiopia (%d volcanoes)',length(EtMR)./5));
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;

print -f13 -dpng -r300 rocktype_variability_Ethiopia_allrocks.png


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GETTING THE ANALOGY SCALE FOR TECTONIC SETTING %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

AT=nan(length(a.data(:,1)),1);

tecsp=1./8; %given that there are 9 different classes, there are 8 spaces
            %between them

AT(find(a.data(:,13)==-9999 | a.data(:,13)==11))=-9999; %no_data=-9999         
            
AT(find(a.data(:,13)==6))=0;        %rift oceanic equal to 0
AT(find(a.data(:,13)==3))=tecsp.*1; %intraplate oceanic equal to 0.125
AT(find(a.data(:,13)==5))=tecsp.*2; %rift intermediate equal to 0.250
AT(find(a.data(:,13)==2))=tecsp.*3; %intraplate intermediate equal to 0.375
AT(find(a.data(:,13)==4))=tecsp.*4; %rift continental equal to 0.5
AT(find(a.data(:,13)==1))=tecsp.*5; %intraplate continental equal to 0.625
AT(find(a.data(:,13)==10))=tecsp.*6; %subduction oceanic equal to 0.750
AT(find(a.data(:,13)==8 |...
    a.data(:,13)==9))=tecsp.*7; %subduction intermediate or unknown
                                %equal to 0.875
AT(find(a.data(:,13)==7))=tecsp.*8; %subduction continental equal to 1

%plotting histograms of the variable AT
figure()
hist(AT,-0.125:0.125:1); xlim([-0.05 1.05])
set(gca,'FontSize',15,'LineWidth',1.5);
set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
box on;
xlabel('AT [dimless]'); ylabel('counts');
print -f14 -dpng -r300 AT_final_hist_9bins.png

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GETTING THE ANALOGY SCALE FOR GEOCHEMISTRY %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%we first create a matrix Nvolcs X Nrocktypes to store the analogy values
AGmat=nan(length(a.data(:,1)),10);

geochsp=1/9;   %there are 10 rock types, then 9 spaces between types

%filling in the matrix
for ii=1:length(AGmat(1,:))
    ag0=find(a.data(:,ii+13)==4);   AGmat(ag0,ii)=0.*geochsp;
    ag1=find(a.data(:,ii+13)==6);   AGmat(ag1,ii)=1.*geochsp;
    ag2=find(a.data(:,ii+13)==11);  AGmat(ag2,ii)=2.*geochsp;
    ag3=find(a.data(:,ii+13)==9);   AGmat(ag3,ii)=3.*geochsp;
    ag4=find(a.data(:,ii+13)==7);   AGmat(ag4,ii)=4.*geochsp;
    ag5=find(a.data(:,ii+13)==10);  AGmat(ag5,ii)=5.*geochsp;
    ag6=find(a.data(:,ii+13)==2);   AGmat(ag6,ii)=6.*geochsp;
    ag7=find(a.data(:,ii+13)==1);   AGmat(ag7,ii)=7.*geochsp;
    ag8=find(a.data(:,ii+13)==3);   AGmat(ag8,ii)=8.*geochsp;
    ag9=find(a.data(:,ii+13)==8);   AGmat(ag9,ii)=9.*geochsp;
end

%calculating the histograms then
xgeoch=0:geochsp:1;

%creating a matrix to store the histogram counts (then maybe normalised)
AGcountmat=zeros(length(a.data(:,1)),length(xgeoch));  %to store the counts
AGnormmat=zeros(length(a.data(:,1)),length(xgeoch)); %to store the normalised

%creating submatrices to store the counts of major and minor rock types
subAGcount_M=nan(length(AGmat(:,1)),10); %the matrix must have 10 columns
                                         %because it is storing the counts
                                         %of any type of rock (Major)
subAGcount_m=nan(length(AGmat(:,1)),10); %the matrix must have 10 columns
                                         %because it is storing the counts
                                         %of any type of rock (minor)

for ii=1:length(subAGcount_M(:,1))
    subAGcount_M(ii,:)=hist(AGmat(ii,1:5),xgeoch);  %here we consider
                                                    %major rocks only however
    %%subAGcount_M(ii,:)
    %%pause;
    subAGcount_M(ii,:)=subAGcount_M(ii,:).*2; %any major rock occurrence
                                              %counts double
    subAGcount_m(ii,:)=hist(AGmat(ii,6:10),xgeoch); %here we take each
                                                    %minor rock occurrence
end

%then, provided that the same rock never appears in both major and minor
%categories, we search the non-zero indices of both the Major and minor
%submatrices and fill the final AGcountmat matrices with those values
%[notice that being AGcountmat a zeros matrix, the zeros from the Major
%and minor submatrices should be kept anyway]
nozeroM=find(subAGcount_M);
nozerom=find(subAGcount_m);

AGcountmat(nozeroM)=subAGcount_M(nozeroM);
AGcountmat(nozerom)=subAGcount_m(nozerom);

% subAGnorm1=nan(length(AGmat(:,1)),5);
% subAGnorm2=nan(length(AGmat(:,1)),5);
% 
% %filling in
% majorR=find(AGmat(:,1:5)>=0);   minorR=find(AGmat(:,6:10)>=0);
% subAGnorm1(majorR)=2;           subAGnorm2(minorR)=1;
% AGcountmat(:,1:5)=subAGnorm1;   AGcountmat(:,6:10)=subAGnorm2;

% 
% %normalising through ecdf
% xgeoch=0:geochsp:1;


%normalising
%rowsum=nansum(AGcountmat,2); %calculating the sum of each row
rowsum=sum(AGcountmat,2); %calculating the sum of each row
                          %(nansum should not be required anymore)

for ii=1:length(AGnormmat(:,1))
    AGnormmat(ii,:)=AGcountmat(ii,:)./rowsum(ii);
end

%calculating the ecdfs
AGecdfmat=cumsum(AGnormmat,2);

%testing some bar plots (and some discrete ecdfs)
toplot=unidrnd(length(a.data(:,1)),10,1);

for ii=1:length(toplot)
    figure();
    subplot(1,2,1);
    bar(xgeoch,AGnormmat(toplot(ii),:),'k');
    set(gca,'FontSize',15,'LineWidth',1.5);
    set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
        'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
    axis([-geochsp 1+geochsp 0 1]);
    box on;
    xlabel('AG [dimless]'); ylabel('counts');
    title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+2,...
        a.data(toplot(ii),1)));
    subplot(1,2,2);
    plot(xgeoch,AGecdfmat(toplot(ii),:),'k','LineWidth',1.5);
    set(gca,'FontSize',15,'LineWidth',1.5);
    set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
        'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
    axis([0 1 0 1]);
    box on;
    xlabel('AG [dimless]'); ylabel('ecdf');
    title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+2,...
        a.data(toplot(ii),1)));
    pause;
end

%we create a vector with the VNUM identifier as well
VNUM=a.data(:,1);
ATlast=AT;

%we save the VNUM and AT vectors
save ATmatrices.mat VNUM ATlast -v7.3

%we save the AG vectors alongside the VNUM
save AGmatrices.mat VNUM AGmat AGcountmat rowsum AGnormmat ...
        AGecdfmat xgeoch -v7.3
