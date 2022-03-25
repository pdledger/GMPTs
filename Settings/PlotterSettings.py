#This file contains the function which allows the user to edit plotting settings
#Importing
import numpy as np
from ngsolve import *


#Function definition of the plotter settings
def PlotterSettings():

    #Line settings
    EigsToPlot = [1,2,3]
    #(list) Which Eigenvalues should be plotted smallest to largest (this is
    #used for both the main lines and snapshots)
    TensorsToPlot = [1,4,6,2,3,5]
    #(list) Which Tensor coefficients to plot leading diagonals are [1,4,6]
    #and tensor layout can be seen below (this is used for both the main
    #lines and the snapshots)
    #
    #             (1,2,3)
    # Tensor ref =(_,4,5)
    #             (_,_,6)

    #specify the indices of tensors to plot (i,j,k)
    TensorsToPlotR3I=[1]
    TensorsToPlotR3J=[1]
    TensorsToPlotR3K=[1]
    #specify the indices of tensors to plot (i,j,k)
    TensorsToPlotR4I=[1,2,1]
    TensorsToPlotR4J=[1,2,1]
    TensorsToPlotR4K=[1,2,2]
    TensorsToPlotR4L=[1,2,2]

    #(list) Which Tensor coefficients to plot leading diagonals are [1,4,6]
    #and tensor layout can be seen below (this is used for both the main
    #lines and the snapshots)
    #
    #             (1,2,3)
    # Tensor ref =(_,4,5)
    #             (_,_,6)


    #Line styles
    MainLineStyle = "-"
    #(string) Linestyle of the eigenvalue/Tensor plots (string, see
    #matplotlib for availible linestyles)
    MainMarkerSize = 4
    #(float) markersize of eigenvalue/Tensor plots (if applicable linestyle
    #is chosen)

    #Snapshot styles
    SnapshotLineStyle = "x"
    #(string) Linestyle of snapshots (if plotted)
    SnapshotMarkerSize = 8
    #(float) markersize of snapshots (if plotted)

    #ErrorBars
    ErrorBarLineStyle = "--"
    #(string) Linestyle of the error bars (string, see matplotlib for
    #availible linestyles)
    ErrorBarMarkerSize = 4
    #(float) markersize of the error bars (if applicable linestyle is chosen)

    #Eddy-current model breakdown
    EddyCurrentLine = True
    #(boolean) display where the eddy-current model breaks down (if value
    #has been calculated)

    #Title
    Title = False
    #(boolean)

    #Display graph?
    Show = True
    #(boolean) if false then graph is only saved


    return Title, Show, EigsToPlot, TensorsToPlot, MainLineStyle,\
     MainMarkerSize, SnapshotLineStyle, SnapshotMarkerSize,\
     ErrorBarLineStyle, ErrorBarMarkerSize, EddyCurrentLine,\
     TensorsToPlotR3I, TensorsToPlotR3J, TensorsToPlotR3K,\
     TensorsToPlotR4I, TensorsToPlotR4J, TensorsToPlotR4K,\
     TensorsToPlotR4L
