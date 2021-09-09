# Sickle Cell vs Malaria Selection Pressure Simulator
A simulation modeling the relationship between sickle cell anemia and malaria. It is based upon real world data and phenotype
frequency calculations. Developed with Mesa Agent-Based Modeling library. 

# Reference
Mathematical Models and Equations in this simulation are based on the following paper:

C. Liddell, N. Owusu-Brackett, and D. Wallace, “A Mathematical Model of Sickle Cell Genome Frequency in Response to Selective Pressure from Malaria,” Bull Math Biol, vol. 76, no. 9, pp. 2292–2305, Sep. 2014, doi: 10.1007/s11538-014-9993-z.

# Installation
Make sure Python 3 is installed
Use `pip install mesa` to install the Mesa library. For more information about the library, 
visit https://mesa.readthedocs.io/en/master/

Use `python run.py` in the directory of the project to run the model on a localhost server. Visit http://127.0.0.1:8080. 

# Files

`model.py`: Contains the main structure of the model, including parameters, methods to delete agents.

`schedule.py`: Contains commands to remove/add agents. 

`agents.py`: Controls basic initialization of agents

`server.py`: Creates the visualization components, including the sliders, canvas, and the chart. 

# Author

Developed by Eric Chen
