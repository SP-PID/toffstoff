clear all, close all, clc

%The Voltage values from the data sheet
x = [2.55 2 1.5 1.25 1.05 0.85 0.8 0.75 0.7 0.6 0.55 0.5 0.47 0.45];
%The voltage values from the calibration
x1 = [2.52 1.97 1.52 1.22 1.01 0.87 0.78 0.70 0.63 0.565 0.53 0.47 0.44 0.395];
%Disdances the measurements were taken
y = [20 30 40 50 60 70 80 90 100 110 120 130 140 150];

P1 = polyfit(x1,y,4) %Fitting a 4th degree polynomial to the data from the datasheet
P2 = polyfit(x,y,4) %Fitting a 4th degree polynomial to the data from the calibration

X2 = linspace(0,3); %Create array of evenly spaced numbers from 0 to 3
                    %Used to plot the polynomial

Y2 = polyval(P1,X2);%Create the an array of data from the polynomial
Y3 = polyval(P2,X2);%Create the an array of data from the polynomial

hold on
plot(x,y,'LineWidth',1) %Line from the datasheet.
plot(X2,Y2,".",'LineWidth',2) %Fitted line to the datasheet data

plot(x1,y,"g",'LineWidth',1)   %Line of calibration data
plot(X2,Y3,".",'LineWidth',2)   %Fit to calibration data
 

title("Distance as a function of voltage")%Set title 
xlabel("Voltage [V]")%Set x-axis label
ylabel("Distance [Cm]")%set y-axis label
xlim([0.25 2.6])%limit the x-axis
ylim([15 160])%limit the y-axis
grid on %turn on the grid
Text1 = ["Datashet data" "Fitted Lline to datasheet data"]; %define legend text
Text2 = ["Calibration data" "Fitted line to calibration data"];%define legend text
legend([Text1 Text2])%Show legend text