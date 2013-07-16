#Code:  pd_front_end.py

#outline:

#1. Generate Grid
#2. Run SPS + CLOUDY
#3. Generate Hyperion Model
#4. Run Hyperion


#=========================================================
#IMPORT STATEMENTS
#=========================================================




import numpy as np
from hyperion.model import Model
import matplotlib as mpl
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput

import constants as const
import parameters as par

import random
import pfh_readsnap
from grid_construction import *


#=========================================================
#GRIDDING
#=========================================================


if par.Manual_TF: 
    print 'Grid is coming from a Manually Set T/F Octree'
    refined = np.genfromtxt(par.Manual_TF_file,dtype = 'str')
    dustdens = np.loadtxt(par.Manual_density_file,dtype='float')

    #change refined T's to Trues and F's to Falses
    
    refined2 = []

    for i in range(len(refined)):
        if refined[i] == 'T':refined2.append(True)
        if refined[i] == 'F':refined2.append(False)
        
    refined = refined2

    print 'Manual grid finished reading in '


else:
    print 'Grid is being generated from the Gadget Snapshot'
    
    refined = gadget_logical_generate(par.Gadget_dir,par.Gadget_snap_num)


    print 'pdb.set_trace() at end of pd_front_end'
    pdb.set_trace()







#end gridding








'''COMMENT STARTS HERE JUST TO NOT RUN THE REST OF CODE WHILE WE WORK ON GRIDDING 



#Make dustdens array as long as the refined array (with zero's where the Trues are)
dustdens2 = np.zeros(len(refined))
counter = 0
for i in range(len(refined)):
    if refined[i] == True: dustdens2[i] = 0
    if refined[i] == False: 
        dustdens2[i] = dustdens[counter]
        counter+=1
dustdens = dustdens2




m = Model()

par.dx *= 1e3*const.pc
par.dy *= 1e3*const.pc
par.dz *= 1e3*const.pc


m.set_octree_grid(par.x_cent,par.y_cent,par.z_cent,
                  par.dx,par.dy,par.dz,refined)






m.add_density_grid(dustdens,par.dustfile)




#=========================================================
#Add Sources
#=========================================================

m.add_spherical_source(luminosity = 1.e3*const.lsun,temperature = 6000., 
                       radius = 10.*const.rsun)


#debug 052313 - this only adds a few sources
for i in range(10):
    m.add_spherical_source(luminosity = 1e3*const.lsun,temperature = 6000.,
                           radius = 10.*const.rsun, 
                           position = [random.random()*par.dx,random.random()*par.dy,random.random()*par.dz])

for i in range(10):
     m.add_spherical_source(luminosity = 1e3*const.lsun,temperature = 6000.,
                           radius = 10.*const.rsun, 
                           position = [random.random()*-par.dx,random.random()*-par.dy,random.random()*-par.dz])
                           





#=========================================================
#Set RT Parameters
#=========================================================

m.set_raytracing(True)
m.set_n_photons(initial = 1.e5,imaging = 1.e5,
                raytracing_sources = 1.e5,raytracing_dust = 1.e5)


#DEBUG - need to make the number of iterations we run flexible
m.set_n_initial_iterations(5)



#=========================================================
#ADD THE SED INFORMATION YOU WANT
#=========================================================

if par.CALCULATE_SED == 1:
    
    image = m.add_peeled_images(sed = True,image = False)
    image.set_wavelength_range(par.n_wav,par.wav_min,par.wav_max)

    #DEBUG - the phi angles don't need to only be 0 degrees
    image.set_viewing_angles(np.linspace(0.,90.,par.N_viewing_angles),
                              np.repeat(0.,par.N_viewing_angles))

    image.set_track_origin('basic')


#=========================================================
#WRITE AND RUN THE MODEL
#=========================================================

m.write('dum.rtin')
m.run('dum.rtout',mpi=True,n_processes=3)




'''

