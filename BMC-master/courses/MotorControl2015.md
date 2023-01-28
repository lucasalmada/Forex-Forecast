# Motor Control (v. 2015)  
*Introduction to modeling and simulation of human movement*

### Instructor  
- Marcos Duarte 

### Time and place  
- Wednesdays, 16-18h, room 303-I; Fridays, 16-18h, room 503-I, block A, Santo André.

## Lecture Schedule

### Week 1   
- [Introduction](https://drive.google.com/open?id=0BxbW72zV7WmUTzdzWFgwelVMSW8&authuser=0)
 + Aspects of Biomechanics and Motor Control
 + Aspects of modeling and simulation of movement
 + [OpenSim software](https://simtk.org/home/opensim)

**Readings** (see the complete reference at the end of the page)
 + Zajac (1993)
 + Delp et al. (2007)
 + Pandy (2001)

**Assignments**   
 + Install [OpenSim](https://simtk.org/home/opensim) and complete the first three tutorials (in the Help menu).

### Week 2
- Concepts on modeling and simulation

**Readings**   
 + Chapter 4 (pages 501-534) of Nigg & Herzog (2006)
 + [Models in Science](http://plato.stanford.edu/entries/models-science/) (from [Stanford Encyclopedia of Philosophy](http://plato.stanford.edu/index.html))

**Assignments**   
 + Write a computer program to plot the results of Example 2 (page 537 of Nigg & Herzog (2006)). Your code should have as inputs the initial position, initial velocity, and acceleration (constant) and as outputs, plots of the position, velocity and acceleration of the particle.  
 + Write a computer program to perform inverse dynamics with the data in [Inverse dynamics benchmark data](http://isbweb.org/data/invdyn/index.html). See [this notebook](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/GaitAnalysis2D.ipynb) for a solution in Python.
 
### Week 3
- Muscle modeling and simulation   

**Readings**   
 + Chapter 4 of Oatis (2009), chapter 9 of Winter (2009)
 + Chapter 4 (pages 622-644) of Nigg & Herzog (2006)
 + Chapter 9 of Robertson et al. (2013)  

**Assignments**   
 + Study and run the muscle simulation from page 655 of Nigg & Herzog (2006).
 
### Week 4
- Muscle modeling and simulation
 + [Muscle modeling](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/MuscleModeling.ipynb)  
 + [Muscle simulation](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/MuscleSimulation.ipynb) 
 
**Readings**   
 + Zajac (1989)  
 + Anderson (2007), Thelen (2003), Millard et al. (2013), McLean et al. (2003)

**Assignments (due by March 6th)**
 + Add a function for the parallel elastic element (PEE) to the script from page 655 of Nigg & Herzog (2006).    
 + Write computer programs to plot each component of a Hill-type muscle model having parameters as inputs.
 
### Week 5
- [Ordinary differential equation and numerical integration](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/OrdinaryDifferentialEquation.ipynb)

**Readings**   
 + Chapter 8 of Downey (2011)
 
**Assignments (due by March 13th)**   
 + Write computer programs to solve the exercises 8.1 and 8.2 of Downey (2011).
 
### Week 6
- [Musculoskeletal modeling and simulation](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/MusculoskeletaModelingSimulation.ipynb)

**Readings**   
 + Chapter 4 of Nigg & Herzog (2006)  
 + Chapters 10 and 11 of Robertson et al. (2013)  
 + Zajac & Gordon (1989)
 + Pandy (2001)  
 + Erdemir et al. (2007)  
 
**Assignments**   
 + Study and run the script knee.m of chapter 4 from Nigg & Herzog (2006).   
 + Change knee.m to use another integrator (e.g., ode45) and add plots for muscle length and velocity.  
 
### Week 7
- [Optimization](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/Optimization.ipynb)

**Readings**   
 + Chapter 4 (page 609-621) of Nigg & Herzog (2006)  
 
**Assignments**   
 + Solve the example on the elbow forces using a different method
 
### Week 8
- [Multibody dynamics of simple biomechanical models](http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/MultibodyDynamics.ipynb)

**Readings**
 + Chapter 5 of Zatsiorsky (2002)
 + Zajac & Gordon (1989)
 + Zajac (1993)

### Weeks 9 - 10
- [OpenSim software](https://simtk.org/home/opensim)   

**Readings**   
 + Delp et al. (2007)
 + [OpenSim support site](http://opensim.stanford.edu/support/index.html)    
 + Hamner et al. (2010)

**Assignments** 
 * Study of [Muscle-actuated Simulation of Human Running](https://simtk.org/home/runningsim). Run Scale, Inverse Kinematics (IK), Reduced Residual Algorithm (RRA), and Computed Muscle Control (CMC) and interpret the results.
 
## Readings

- Anderson C (2007) [Equations for Modeling the Forces Generated by Muscles and Tendons](https://docs.google.com/viewer?url=https%3A%2F%2Fsimtk.org%2Fdocman%2Fview.php%2F124%2F604%2FMuscleAndTendonForcesClayAnderson20070521.doc) ([PDF](https://drive.google.com/open?id=0BxbW72zV7WmUVUh0MldGOGZ6aHc&authuser=0)). BioE215 Physics-based Simulation of Biological Structures.  
- Delp SL, Anderson FC, Arnold AS, Loan P, Habib A, John CT, Guendelman E, Thelen DG (2007) [OpenSim: open-source software to create and analyze dynamic simulations of movement](http://www.ncbi.nlm.nih.gov/pubmed/18018689). IEEE Trans Biomed Eng., 54, 1940-50.   
- Downey AB (2011) [Physical Modeling in MATLAB](http://greenteapress.com/matlab/). Green Tea Press. 
- Erdemir A, McLean S, Herzog W, van den Bogert AJ (2007) [Model-based estimation of muscle forces exerted during movements](http://www.ncbi.nlm.nih.gov/pubmed/17070969). Clinical Biomechanics, 22, 131–154.  
- Hamner SR, Seth A, Delp SL (2010) [Muscle contributions to propulsion and support during running](https://nmbl.stanford.edu/publications/pdf/Hamner2010.pdf). Journal of Biomechanics, 43, 2709–2716.
- McLean SG, Su A, van den Bogert AJ (2003) [Development and validation of a 3-D model to predict knee joint loading during dynamic movement](http://www.ncbi.nlm.nih.gov/pubmed/14986412). Journal of Biomechanical Engineering, 125, 864-74.  
- Nigg & Herzog (2006) [Biomechanics of the Musculo-skeletal System](https://books.google.com.br/books?id=hOIeAQAAIAAJ&dq=editions:ISBN0470017678). 3rd Edition. Wiley. [4](https://drive.google.com/open?id=0BxbW72zV7WmUVlhPYk9NNm5HbTQ&authuser=0)  
- Oatis CA (2009) [Kinesiology : the mechanics and pathomechanics of human movement](https://books.google.com.br/books?id=SqZZSAAACAAJ). Lippincott Williams &​ Wilkins. 2nd Edition. [4](http://downloads.lww.com/wolterskluwer_vitalstream_com/sample-content/9780781774222_Oatis/samples/Oatis_CH04_045-068.pdf)
- Pandy MG (2001) [Computer modeling and simulation](https://drive.google.com/open?id=0BxbW72zV7WmUbXZBR2VRMnF5UTA&authuser=0). Annu. Rev. Biomed. Eng., 3, 245–73.  
- Thelen DG (2003) [Adjustment of muscle mechanics model parameters to simulate dynamic contractions in older adults](http://homepages.cae.wisc.edu/~thelen/pubs/jbme03.pdf). Journal of Biomechanical Engineering, 125, 70–77.  
- Millard M, Uchida T, Seth A, Delp SL (2013) [Flexing computational muscle: modeling and simulation of musculotendon dynamics](http://www.ncbi.nlm.nih.gov/pubmed/23445050). Journal of Biomechanical Engineering, 135, 021005.  
- Robertson G, Caldwell G, Hamill J, Kamen G (2013) [Research Methods in Biomechanics](http://books.google.com.br/books?id=gRn8AAAAQBAJ). 2nd Edition. Human Kinetics.  
- Winter DA (2009) [Biomechanics and motor control of human movement](http://books.google.com.br/books?id=_bFHL08IWfwC). 4th Edition. Hoboken, EUA: Wiley.   
- Zajac FE (1989) [Muscle and tendon: properties, models, scaling and application to biomechanics and motor control](https://drive.google.com/open?id=0BxbW72zV7WmUclNNaTd2TGVndFE&authuser=0). Critical Reviews in Biomedical Engineering 17, 359-411.   
Zajac FE, Gordon ME (1989) [Determining muscle's force and action in multi-articular movement](https://drive.google.com/open?id=0BxbW72zV7WmUcC1zSGpEOUxhWXM&authuser=0). Exercise and Sport Sciences Reviews, 17, 187-230.
- Zajac FE (1993) [Muscle coordination of movement: a perspective](http://e.guigon.free.fr/rsc/article/Zajac93.pdf). J Biomech., 26, Suppl 1:109-24.  
- Zatsiorsky VM (2002) [Kinetics of human motion](http://books.google.com.br/books?id=wp3zt7oF8a0C). Human Kinetics.  
