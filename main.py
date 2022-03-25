########################################################################
#This code was written by Ben Wilson with the supervison of Paul Ledger
#at the ZCCE, Swansea University
#Powered by NETGEN/NGSolve
########################################################################


#User Inputs

#Geometry
#Geometry = "cone_steel.geo"#"cone_d1z.geo"# "cone_alan.geo"
#nb cone_copper.geo = cone_alan.geo used for comparing with Toykan's Copper cone
#nb cone_brass.geo  used for comparing with Toykan's Brass cone
#(string) Name of the .geo file to be used in the frequency sweep i.e.
# "sphere.geo"
Geometry = "output.geo"


#Scaling to be used in the sweep in meters
alpha = 0.001
#(float) scaling to be applied to the .geo file i.e. if you have defined
#a sphere of unit radius in a .geo file   alpha = 0.01   would simulate a
#sphere with a radius of 0.01m ( or 1cm)


#About the mesh
#How fine should the mesh be
MeshSize = 1
#(int 1-5) this defines how fine the mesh should be for regions that do
#not have maxh values defined for them in the .geo file (1=verycoarse,
#5=veryfine)

#The order of the elements in the mesh
Order = 0
#(int) this defines the order of each of the elements in the mesh


#About the Frequency sweep (frequencies are in radians per second)
#Minimum frequency (Powers of 10 i.e Start = 2 => 10**2)
Start = 1
#(float)
#Maximum frequency (Powers of 10 i.e Start = 8 => 10**8)
Finish = 6
#(float)
#Number of points in the freqeuncy sweep
Points = 10
#(int) the number of logarithmically spaced points in the sweep

#I only require a single frequency
Single = False
#(boolean) True if single frequency is required
Omega = 4.8e4 #133.5
#(float) the frequency to be solved if Single = True


#POD
#I want to use POD in the frequency sweep
Pod = True
#(boolean) True if POD is to be used, the number of snapshots can be
#edited in in the Settings.py file


#MultiProcessing
MultiProcessing = True
#(boolean) #I have multiple cores at my disposal and have enough spare RAM
# to run the frequency sweep in parrallel (Edit the number of cores to be
#used in the Settings.py file)








########################################################################


#Main script


#Importing
import sys
import numpy as np
sys.path.insert(0,"Functions")
sys.path.insert(0,"Settings")
from MeshCreation import *
from Settings import *
from SingleSolve import SingleFrequency
from SingleSolveGMPT import SingleFrequencyGMPT
from FullSolvers import *
from PODSolvers import *
from ResultsFunctions import *
from Checkvalid import *

if __name__ == '__main__':
    #Load the default settings
    CPUs,BigProblem,PODPoints,PODTol,OldMesh,Stepmesh = DefaultSettings()

    if OldMesh == False:
        #Create the mesh
        Meshmaker(Geometry,MeshSize)
    else:
        #Check whether to add the material information to the .vol file
        try:
            Materials,mur,sig,inorout = VolMatUpdater(Geometry,OldMesh)
            ngmesh = ngmeshing.Mesh(dim=3)
            ngmesh.Load("VolFiles/"+Geometry[:-4]+".vol")
            mesh = Mesh("VolFiles/"+Geometry[:-4]+".vol")
            mu_coef = [ mur[mat] for mat in mesh.GetMaterials() ]
        except:
            #Force update to the .vol file
            OldMesh = False

    #Update the .vol file and create the material dictionaries
    Materials,mur,sig,inorout = VolMatUpdater(Geometry,OldMesh)

    #create the array of points to be used in the sweep
    Array = np.logspace(Start,Finish,Points)
    #Define frequency sweep
    #Array=np.array([  7.4927e+02, 1.1239e+03,  1.4985e+03,  1.8732e+03,  2.2478e+03,  2.9971e+03,  3.7463e+03,  4.4956e+03,  5.99E+03, 7.49E+03, 8.99E+03, 1.20E+04, 1.50E+04, 1.80E+04, 2.40E+04, 3.00E+04, 3.60E+04, 4.80E+04, 5.99E+04, 7.79E+04, 1.02E+05, 1.32E+05, 1.68E+05, 2.16E+05, 2.76E+05, 3.60E+05, 4.62E+05, 5.99E+05])
    PlotPod, PODErrorBars, EddyCurrentTest, vtk_output, Refine = AdditionalOutputs()
    SavePOD = False
    if PODErrorBars!=True:
        ErrorTensors=False
    else:
        ErrorTensors=True
    PODArray = np.logspace(Start,Finish,PODPoints)

    #Create the folders which will be used to save everything
    sweepname = FolderMaker(Geometry, Single, Array, Omega, Pod, PlotPod, PODArray, PODTol, alpha, Order, MeshSize, mur, sig, ErrorTensors, vtk_output)


    #Run the sweep

    #Check the validity of the eddy-current model for the object
    if EddyCurrentTest == True:
        EddyCurrentTest = Checkvalid(Geometry,Order,alpha,inorout,mur,sig,Stepmesh)

    if Single==True:
        if MultiProcessing!=True:
            CPUs = 1
        #MPT, EigenValues, N0, elements = SingleFrequency(Geometry,Order,alpha,inorout,mur,sig,Omega,CPUs,vtk_output,Refine)
        #print(MPT)
        MPTR3, N0R3, elements = SingleFrequencyGMPT(Geometry,Order,alpha,inorout,mur,sig,Omega,CPUs,vtk_output,Refine,Stepmesh)
    else:
        if Pod==True:
            if MultiProcessing==True:
                if PlotPod==True:
                    if PODErrorBars==True:
                        TensorArrayR3, TensorArrayR4, EigenValues, N0, PODTensorsR3, PODTensorsR4, PODEigenValues, elements, ErrorTensors = PODSweepMultiR3(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,CPUs,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                    else:
                        TensorArrayR3, TensorArrayR4, EigenValues, N0, PODTensorsR3, PODTensorsR4, PODEigenValues, elements = PODSweepMultiR3(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,CPUs,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                else:
                    if PODErrorBars==True:
                        TensorArrayR3, TensorArrayR4, EigenValues, N0, elements, ErrorTensors = PODSweepMultiR3(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,CPUs,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                    else:
                        TensorArrayR3, TensorArrayR4, EigenValues, N0, elements = PODSweepMultiR3(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,CPUs,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
            else:
                if PlotPod==True:
                    if PODErrorBars==True:
                        TensorArray, EigenValues, N0, PODTensors, PODEigenValues, elements, ErrorTensors = PODSweep(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                    else:
                        TensorArray, EigenValues, N0, PODTensors, PODEigenValues, elements = PODSweep(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                else:
                    if PODErrorBars==True:
                        TensorArray, EigenValues, N0, elements, ErrorTensors = PODSweep(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
                    else:
                        TensorArray, EigenValues, N0, elements = PODSweep(Geometry,Order,alpha,inorout,mur,sig,Array,PODArray,PODTol,PlotPod,sweepname,SavePOD,PODErrorBars,BigProblem,Stepmesh)
        else:
            if MultiProcessing==True:
                #TensorArray, EigenValues, N0, elements = FullSweepMulti(Geometry,Order,alpha,inorout,mur,sig,Array,CPUs,BigProblem)
                TensorArray, EigenValues, N0, elements = FullSweepMultiR3(Geometry,Order,alpha,inorout,mur,sig,Array,CPUs,BigProblem,Stepmesh)
            else:
                TensorArray, EigenValues, N0, elements = FullSweepR3(Geometry,Order,alpha,inorout,mur,sig,Array,BigProblem,Stepmesh)


    #Plotting and saving
    if Single==True:
        SingleSave(Geometry, Omega, MPT, EigenValues, N0, elements, alpha, Order, MeshSize, mur, sig, EddyCurrentTest)
    elif PlotPod==True:
        if Pod==True:
            PODSave(Geometry, Array, TensorArrayR3, TensorArrayR4, EigenValues, N0, PODTensorsR3, PODTensorsR4, PODEigenValues, PODArray, PODTol, elements, alpha, Order, MeshSize, mur, sig, ErrorTensors,EddyCurrentTest)
        else:
            FullSave(Geometry, Array, TensorArray, EigenValues, N0, Pod, PODArray, PODTol, elements, alpha, Order, MeshSize, mur, sig, ErrorTensors,EddyCurrentTest)
    else:
        FullSave(Geometry, Array, TensorArray, EigenValues, N0, Pod, PODArray, PODTol, elements, alpha, Order, MeshSize, mur, sig, ErrorTensors,EddyCurrentTest)
