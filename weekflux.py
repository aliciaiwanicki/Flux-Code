import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as plticker

#%%
noniso = pd.read_csv(r'C:\Users\Eric\Desktop\Students\Alicia_I\noniso_20200127_20200203.txt', engine='python', delimiter='\t', header = 0)
noniso.index = pd.to_datetime(noniso.Date_IV)

noniso.loc[~(noniso['Lin_Flux[2]'] > 0), 'Lin_Flux[2]'] = np.nan            # Clip negative FLUX values to NaN
noniso.loc[~(noniso['Exp_Flux[2]'] > 0), 'Exp_Flux[2]'] = np.nan
#noniso.loc[~(noniso['Lin_Flux[2]'] = 1), 'Lin_Flux[2]'] = np.nan
noniso.loc[~(noniso['Lin_R2[2]'] > 0.70), 'Lin_Flux[2]'] = 0                # Change N2O fluxes with R2 values < 0.7 to 0
noniso.loc[~(noniso['Exp_R2[2]'] > 0.70), 'Exp_Flux[2]'] = 0 

LinExp = noniso['Lin_R2[2]'] >= noniso['Exp_R2[2]']
N2O_Flux = []; N2O_Flux = pd.DataFrame(N2O_Flux)

#New Stuff; creates a column called 'Flux' as part of this.
N2O_Flux['Flux'] = noniso['Exp_Flux[2]'] # Sets the entire column equal to Exp_Flux[2] data
N2O_Flux['Flux'][LinExp] = noniso['Lin_Flux[2]'] # Sets just the times when LinExp == True to the Lin_Flux[2] data; should just replace those few columns
# End of new stuff
print(sum(LinExp))
