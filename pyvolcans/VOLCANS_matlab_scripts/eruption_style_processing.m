% eruption_style_processing.m

%{Summary:

It derives the data required to calculate the single-criterion analogy matrix for eruption style.
It requires to import the data in the files: `VOTW467_8May18_event_data.csv`,
`VOTW467_8May18_eruption_data.csv`, and `VOTW467_8May18_volcano_data.csv` to
carry out the aforementioned task.

%}

clear all
close all

%load the events data
a=importdata('../VOLCANS_csv_files/VOTW467_8May18_event_data.csv');

%we load the eruption data as well, to exclude caldera formation linked
%with VEI<4 eruptions
b=importdata('../VOLCANS_csv_files/VOTW467_8May18_eruption_data.csv');

%import the volcano data as well, we will need to work with it too
c=importdata('../VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv');

%here we create the matrices that will store the main-group counts and the
%normalised values (by eruption). Note that we will not need any type of
%histogram this time
AStcountmat=zeros(length(c.data(:,1)),8);  %there are 8 main groups
AStnormmat=zeros(length(c.data(:,1)),8);

%here we include the analysis of phreatomagmatic eruptions only
phreatomag_norm=zeros(length(c.data(:,1)),1);

%we create the loop that we will use to populate the matrices
for ii=1:length(AStcountmat(:,1))
    vnum=c.data(ii,1);  %getting the VNUM of the volcano
        
    idsvolc=find(a.data(:,1)==vnum); %finding all entries (events) that are
                                     %linked with the specific volcano
    
    %finding the total number of unique eruptions from all the events
    %(i.e. length(ia_er))
    [Cer,ia_er,ic_er]=unique(a.data(idsvolc,3),'first');
    
    Ner=length(ia_er); %total number of eruptions
    
    %%%fprintf('VNUM=%d; Ner=%d\n',vnum,Ner);
    
    %explore the eruptions searching for the main groups of events
    for jj=1:Ner
        ernum=a.data(idsvolc(ia_er(jj)),3); %we deal with 1 eruption at a time
        idserupt=find(a.data(:,3)==ernum); %global indices for the eruption
        
        %get the counts (max. 1) per each main group and eruption (NB. We
        %must use find because knnsearch gives the nearest neighbour, hence
        %it will never return an empty matrix!
        lava=find(a.data(idserupt,7)==1);
        tephra=find(a.data(idserupt,7)==2);
        phreato=find(a.data(idserupt,7)==3);
        wsedflow=find(a.data(idserupt,7)==4);
        tsunami=find(a.data(idserupt,7)==5);
        pdc=find(a.data(idserupt,7)==6);
        edestru=find(a.data(idserupt,7)==7);
        caldera=find(a.data(idserupt,7)==8);
        
        %here we deal with the phreatomagmatic eruptions only
        phreatomag_only=find(a.data(idserupt,6)==17);
    
        %get the counts (if the vectors are not empty)
        if ~isempty(lava)
            AStcountmat(ii,1)=AStcountmat(ii,1)+1;
        end
        
        if ~isempty(tephra)
            AStcountmat(ii,2)=AStcountmat(ii,2)+1;
        end
        
        if ~isempty(phreato)
            AStcountmat(ii,3)=AStcountmat(ii,3)+1;
        end
        
        if ~isempty(wsedflow)
            AStcountmat(ii,4)=AStcountmat(ii,4)+1;
        end
        
        if ~isempty(tsunami)
            AStcountmat(ii,5)=AStcountmat(ii,5)+1;
        end
        
        if ~isempty(pdc)
            AStcountmat(ii,6)=AStcountmat(ii,6)+1;
        end
        
        if ~isempty(edestru)
            AStcountmat(ii,7)=AStcountmat(ii,7)+1;
        end
        
        if ~isempty(caldera)
            iderupt2=find(b.data(:,3)==ernum); %see if the eruption exists
                                               %in our list of VEI
                                               %eruptions
            %proceed only if the eruption has a VEI associated
            if ~isempty(iderupt2)
                caldvei=b.data(iderupt2,6); %get the VEI of the eruption
                %proceed with the count of the main group of event if only
                %if the eruption has a VEI>3
                if caldvei>3
                    AStcountmat(ii,8)=AStcountmat(ii,8)+1;
                end
            end
        end
    %end of exploring the main-group events for a given eruption
    
    %adding the phreatomagmatic eruptions only
        if ~isempty(phreatomag_only)
            phreatomag_norm(ii,1)=phreatomag_norm(ii,1)+1;
        end
    %end of exploring any type of events for a given eruption
    
    end
%end of exploring ALL different eruptions for a given volcano

%we get the normalised counts (by total number of eruptions) here, before
%the variable Ner gets re-defined/re-evaluated in the following step of the
%loop
AStnormmat(ii,:)=AStcountmat(ii,:)./Ner;

%here we get the normalised count for phreatomagmatic eruptions only
%(N.B. We use only one vector in this case)
phreatomag_norm(ii,1)=phreatomag_norm(ii,1)./Ner;

end
   
%testing some bar plots (and some discrete ecdfs)
toplot=unidrnd(length(c.data(:,1)),10,1);

for ii=1:length(toplot) %length(b.data(:,1))
    figure();
    %subplot(1,2,1);
    bar(1:1:8,AStnormmat(toplot(ii),:),'k');
    %bar(xvei,ASznorm_ALL(ii,:),'k');
    set(gca,'FontSize',15,'LineWidth',1.5,...
        'XTick',1:1:8,...
        'XTickLabel',{'LF','BT','PH','WSF','TSU','PDC','DST','CF'});
    set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
        'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
    %axis([-(1/6),1+(1/6),0,1]);
    axis([0 9 0 1])
    box on;
    %xlabel('ASz [dimless]');
    xlabel('Hazardous Phenomena'); ylabel('counts');
    title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+1,...
        c.data(toplot(ii),1)));
    %title(sprintf('Volcano #%d (VNUM=%d)',ii+2,...
     %   b.data(ii,1)));
    pause;
     
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
    
%     plot(xveinorm,ASzecdfmat(toplot(ii),:),'k','LineWidth',1.5);
%     set(gca,'FontSize',15,'LineWidth',1.5);
%     set(gcf,'PaperSize',[20 16],'PaperUnits','centimeters',...
%         'PaperPosition',[1 1 16 12],'PaperOrientation','portrait');
%     axis([0 1 0 1]);
%     box on;
%     xlabel('ASz [dimless]'); ylabel('ecdf');
%     title(sprintf('Volcano #%d (VNUM=%d)',toplot(ii)+2,...
%         a.data(toplot(ii),1)));
%    pause;
%    close all;
end
        
%we create a vector with the VNUM identifier as well
VNUM=c.data(:,1);   %c is the VOTW Holocene volcano list in this script!

%we save the ASz vectors alongside the VNUM
save AStmatrices.mat VNUM AStcountmat AStnormmat ...
        phreatomag_norm -v7.3 
