import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import glob
import matplotlib.dates as mdates
import matplotlib.ticker as plticker

## Lin_Flux[2] is N2O flux

#----------------------------------------------- NON ISO ----------------------------------------------- 
noniso = pd.read_csv('/Volumes/WSU/1. PYTHON Code/Concat iso + noniso & PST to STD/noniso_STD_20190515_20200121.csv', engine='python', header = 0)
noniso.index = pd.to_datetime(noniso.Date_IV)
noniso = noniso.sort_index()


noniso.loc[~(noniso['Lin_Flux[2]'] > 0), 'Lin_Flux[2]'] = np.nan            # Clip negative FLUX values to NaN
#noniso.loc[~(noniso['Lin_Flux[2]'] > 0.000056), 'Lin_Flux[2]'] = 0         # Value < lower detection lim = 0
#noniso.loc[~(noniso['Lin_Flux[2]'] < 0.0005), 'Lin_Flux[2]'] = np.nan      # Clip FLUX values > 0.002 to NaN
noniso.loc[~(noniso['Lin_R2[2]'] > 0.70), 'Lin_Flux[2]'] = 0                # Clip N2O R2 values < 0.7 to 0



# New df with extracted columns
#noniso_new = noniso.filter(['Port#','Lin_Flux[2]','Lin_R2[2]','Lin_SE[2]','Lin_SSN[2]','Lin_Flux','Lin_R2','Lin_SE','Lin_SSN','Pressure_IV','RH_IV','Tcham_IV', 'AmbT_C_IV' ], axis=1)
#noniso_new.rename(columns={'Lin_Flux[2]':'N2O_Lin_Flux','Lin_R2[2]':'N2O_Lin_R2', 'Lin_SE[2]':'N2O_Lin_SE', 'Lin_SSN[2]':'N2O_Lin_SSN', 'Lin_Flux':'CO2_Lin_Flux', 'Lin_R2':'CO2_Lin_R2','Lin_SE':'CO2_Lin_SE','Lin_SSN':'CO2_Lin_SSN', 'AmbT_C_IV':'Amb_Temp_C'}, inplace=True)

noniso = noniso[pd.notnull(noniso['Lin_Flux[2]'])]                          # Delete rows with NaN in N2O_Lin_Flux column
noniso = noniso[pd.notnull(noniso['Lin_R2[2]'])]                            # Delete rows with NaN in N2O_Lin_R2 column

#  Eric's adds; might need a little adjusting ##############################
LinExp = noniso['Lin_R2[2]'] >= noniso['Exp_R2[2]']
N2O_Flux = []; N2O_Flux = pd.DataFrame(N2O_Flux)
N2O_Flux = noniso['Exp_Flux[2]']; N2O_Flux = noniso['Lin_Flux[2]'][LinExp]
print(sum(LinExp))
########################################################


gr_chambers = noniso.groupby('Port#')
#ch1 = gr_chambers.get_group(1)

noniso['N2O_Flux_g/m2/h_NONISO'] = noniso['Lin_Flux[2]']*0.1584468
noniso['N2O_Flux_g/ha/d_NONISO'] = noniso['Lin_Flux[2]']*38027.232
noniso['N2O_Flux_kg/ha/d_NONISO'] = noniso['Lin_Flux[2]']*38.027232
noniso['N2O_Flux_kg/ha/y_NONISO'] = noniso['Lin_Flux[2]']*13879.9397

#      N2O-N FLUXES 
noniso['N2O_N_Flux_g/m2/h_NONISO'] = noniso['N2O_Flux_g/m2/h_NONISO']*(28/44)
noniso['N2O_N_Flux_g/ha/d_NONISO'] = noniso['N2O_Flux_g/ha/d_NONISO']*(28/44)
noniso['N2O_N_Flux_kg/ha/d_NONISO'] = noniso['N2O_Flux_kg/ha/d_NONISO']*(28/44)
noniso['N2O_N_Flux_kg/ha/y_NONISO'] = noniso['N2O_Flux_kg/ha/y_NONISO']*(28/44)
   
noniso.to_csv('noniso_processed.csv', index=False)

daily_noniso = pd.DataFrame()
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_mean'] = noniso['N2O_N_Flux_g/ha/d_NONISO'].resample('B').mean()
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_median'] = noniso['N2O_N_Flux_g/ha/d_NONISO'].resample('B').median()
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'] = noniso['N2O_N_Flux_g/ha/d_NONISO'].resample('B').max()
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'] = noniso['N2O_N_Flux_g/ha/d_NONISO'].resample('B').min()

daily_noniso['Tcham_mean'] = noniso['Tcham_IV'].resample('B').mean()
daily_noniso['Tcham_max'] = noniso['Tcham_IV'].resample('B').max()
daily_noniso['Tcham_min'] = noniso['Tcham_IV'].resample('B').min()


gr = noniso.groupby('Port#')        # CONDENSE THIS CODE ?????            
a = gr.get_group(1)
b = gr.get_group(2)
c = gr.get_group(3)
d = gr.get_group(4)
e = gr.get_group(5)
f = gr.get_group(6)
g = gr.get_group(7)
h = gr.get_group(8)
                              
#noniso['N2O_Flux_mg/m2/h'] = df['Lin_Flux[2]'].apply(negativevalues)
#OLD: Volumes/WSU/ALL DATA FILES/ISO/(3) Combined SFP Files/all_iso_data.csv


#-----------------------------------------------  ISO  -----------------------------------------------

isodata = pd.read_csv('/Volumes/WSU/1. PYTHON Code/Concat iso + noniso & PST to STD/iso_STD_20190515_20191125.csv', engine='python', header = 0)
isodata.index = pd.to_datetime(isodata.DateNew)
isodata = isodata.sort_index()
isodata.loc[~(isodata['Lin_Flux[2]'] > 0), 'Lin_Flux[2]'] = np.nan          # Clip negative FLUX values to NaN

isodata.loc[~(isodata['Lin_Flux[2]'] > 0), 'Lin_Flux[2]'] = np.nan           # Clip negative FLUX values to NaN
#isodata.loc[~(isodata['Lin_Flux[2]'] > 0.000056), 'Lin_Flux[2]'] = 0        # Value < lower detection lim = 0
#isodata.loc[~(isodata['Lin_Flux[2]'] < 0.0008), 'Lin_Flux[2]'] = np.nan     # Clip FLUX values > 0.002 to NaN
isodata.loc[~(isodata['Lin_R2[2]'] > 0.70), 'Lin_Flux[2]'] = 0                 # Clip N2O R2 values < 0.7 to 0

isodata['N2O_Flux_g/m2/h_ISO'] = isodata['Lin_Flux[2]']*0.1584468
isodata['N2O_Flux_g/ha/d_ISO'] = isodata['Lin_Flux[2]']*38027.232
isodata['N2O_Flux_kg/ha/d_ISO'] = isodata['Lin_Flux[2]']*38.027232 
isodata['N2O_Flux_kg/ha/y_ISO'] = isodata['Lin_Flux[2]']*13879.9397


#     N2O-N FLUXES 
isodata['N2O_N_Flux_g/m2/h_ISO'] = isodata['N2O_Flux_g/m2/h_ISO']*(28/44)
isodata['N2O_N_Flux_g/ha/d_ISO'] = isodata['N2O_Flux_g/ha/d_ISO']*(28/44)
isodata['N2O_N_Flux_kg/ha/d_ISO'] = isodata['N2O_Flux_kg/ha/d_ISO']*(28/44)
isodata['N2O_N_Flux_kg/ha/y_ISO'] = isodata['N2O_Flux_kg/ha/y_ISO']*(28/44)

daily_isodata = pd.DataFrame()
daily_isodata['N2O_N_Flux_g/ha/d_ISO_mean'] = isodata['N2O_N_Flux_g/ha/d_ISO'].resample('B').mean()
daily_isodata['N2O_N_Flux_g/ha/d_ISO_median'] = isodata['N2O_N_Flux_g/ha/d_ISO'].resample('B').median()
daily_isodata['N2O_N_Flux_g/ha/d_ISO_max'] = isodata['N2O_N_Flux_g/ha/d_ISO'].resample('B').max()
daily_isodata['N2O_N_Flux_g/ha/d_ISO_min'] = isodata['N2O_N_Flux_g/ha/d_ISO'].resample('B').min()

daily_isodata['Tcham_mean'] = isodata['Tcham_IV'].resample('B').mean()
daily_isodata['Tcham_max'] = isodata['Tcham_IV'].resample('B').max()
daily_isodata['Tcham_min'] = isodata['Tcham_IV'].resample('B').min()

gr2 = isodata.groupby('Port#')        # CONDENSE THIS CODE                  
i = gr.get_group(1)
j = gr.get_group(2)
k = gr.get_group(3)
l = gr.get_group(4)
m = gr.get_group(5)
n = gr.get_group(6)
o = gr.get_group(7)
p = gr.get_group(8)


#-----------------------------------------------  WEATHER DATA   -----------------------------------------------
## PCFS Weather file from Bob. Code to convert PST to STD.
weather1 = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(4) PCFS Weather Data/PCFS_Data_30minute_20190101_20191025.csv',index_col=None, header = 0)
weather1['TimeStamp_orig'] = pd.to_datetime(weather1['TimeStamp'])
weather1['TimeStamp'] = pd.to_datetime(weather1['TimeStamp']) - timedelta(hours=1)
weather1.index = pd.to_datetime(weather1.TimeStamp)
# daylight savings (STD to PST) starts 3/10/2019 & ends 11/3/2019. I -1h from all data bc I deleted the data from Jan - May 2019 anyways (flux data starts in May)
weather1 = weather1[weather1['TimeStamp'] > '2019-05-15 08:00:00']
weather1 = weather1.sort_index()
# weather.loc[~(weather['T_Avg_C'] > 0), 'T_Avg_C'] = np.nan
weather1['Precipitation_Tot_mm'] = (weather1['Precipitation_Tot']*25.4)
weather1 = weather1.replace(-6999, np.NaN)

## PCFS Weather files from Bob. Currently only have Oct - Dec 2019
weather2 = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(4) PCFS Weather Data/editted data (new logger)/PCFSMET_20191008_20200201.csv',index_col=None, header = 0)
weather2.index = pd.to_datetime(weather2.timestamp)


## Data from Trailer 3 instruments Patrick installed.
Trailer_weather = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(4) PCFS Weather Data/n2o_trailer_weather.dat', engine='python', header=1, skiprows=(2,3))
Trailer_weather.rename(columns={'WindDir_min':'WindDir_min_deg', 'WindDir_avg':'WindDir_avg_deg', 'WindDir_max':'WindDir_max_deg', 'WindSpeed_avg':'WindSpeed_avg_m/s', 'WindSpeed_min':'WindSpeed_min_m/s', 'WindSpeed_max':'WindSpeed_max_m/s', 'Tmpr':'Temp_degC', 'RH':'RH_percent', 'Press':'Press_hPa', 'Rain_amt':'Precip_mm', 'Rain_dur':'Precip_dur_sec', 'Rain_int':'Precip_int_mm/hr', 'Hail_amt':'Hail_amt_hits/cm2', 'Hail_dur':'Hail_dur_sec', 'Hail_int':'Hail_int_hits/cm2/hr', 'HeaterTmpr':'Heater_Temp_degC', 'HeaterVolts':'HeaterVolts_Vdc', 'PAR_density':'PAR_density_umol/s_m2', 'LoggerTmpr':'LoggerTmpr_degC', 'PowerIn':'PowerIn_Vdc', 'ClockError':'ClockError_msec', 'UTC_OFFSET':'UTC_OFFSET_hrs', 'WXT_AZIMUTH':'WXT_AZIMUTH_Deg', 'PAR_MULT':'PAR_MULT_umol/mV*s*m2'}, inplace=True)
Trailer_weather.index = pd.to_datetime(Trailer_weather.TIMESTAMP)
Trailer_weather = Trailer_weather.drop(columns="RECORD")
Trailer_weather = Trailer_weather.replace('NAN', np.NaN)
Trailer_weather["Precip_mm"] = pd.to_numeric(Trailer_weather["Precip_mm"])             # such low values bc not v accurate w/ snow
#Trailer_weather = Trailer_weather['Precip_mm'].astype(float)
#Trailer_weather['Precip_mm'] = Trailer_weather['Precip_mm'].fillna(0)

# SNOW DATA
snowdata = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(4) PCFS Weather Data/ACISweather_20191201_20200122.txt', engine='python',delimiter = '\t', header = 0)
snowdata.index = pd.to_datetime(snowdata.Date)
snowdata = snowdata.sort_index()



#-----------------------------------------------  SOIL DATA   -----------------------------------------------
def soilfunc(filename,cl):
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, header = 0, index_col=cl, skiprows=(1,2))
        li.append(df)
    
    df = pd.concat(li, axis=0, sort=False)                  
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[~df.index.duplicated(keep='first')]  #delete overlapping datetimes
    idx = pd.date_range(df.index[0].floor('D'), df.index[len(df.index)-1].ceil('D'), freq='5T')
    df = df.reindex(idx, fill_value=np.NaN)
    df = df[(df.index > '2019-05-15 08:27:14') & (df.index <= str(datetime.date.today()))]
    df['mean_moisture_'+cl] = df[['Port 1', 'Port 2', 'Port 3']].mean(axis=1)    #removed Port 4 bc faulty
    df['mean_temp_'+cl] = df[['Port 1.1', 'Port 2.1', 'Port 3.1']].mean(axis=1)  #removed Port 4.1 bc faulty
    return df


path = '/Volumes/WSU/2. ALL DATA FILES/(3) Soil Data/1Pcsv'
all_files = glob.glob(path + "/*.csv")                                              
soil1P = soilfunc(all_files, '1P10')

path = '/Volumes/WSU/2. ALL DATA FILES/(3) Soil Data/2Pcsv'
all_files = glob.glob(path + "/*.csv")                                              
soil2P = soilfunc(all_files, '2P10')

path = '/Volumes/WSU/2. ALL DATA FILES/(3) Soil Data/3Pcsv'
all_files = glob.glob(path + "/*.csv") 
soil3P = soilfunc(all_files, '3P10')

path = '/Volumes/WSU/2. ALL DATA FILES/(3) Soil Data/4Pcsv'
all_files = glob.glob(path + "/*.csv") 
soil4P = soilfunc(all_files, '4P10')

df_soil = pd.concat([soil1P['mean_moisture_1P10'],soil2P['mean_moisture_2P10'],soil3P['mean_moisture_3P10'],soil4P['mean_moisture_4P10'], soil1P['mean_temp_1P10'],soil2P['mean_temp_2P10'],soil3P['mean_temp_3P10'],soil4P['mean_temp_4P10']],axis=1, sort=False)
df_soil['soil_avg_temp'] = df_soil[['mean_temp_1P10', 'mean_temp_2P10', 'mean_temp_3P10']].mean(axis=1)
df_soil['soil_avg_VWC'] = df_soil[['mean_moisture_1P10', 'mean_moisture_2P10', 'mean_moisture_3P10']].mean(axis=1)
df_soil = df_soil.sort_index()

df_soil_daily = pd.DataFrame()
df_soil_daily['soil_temp_mean'] = df_soil['soil_avg_temp'].resample('B').mean()
df_soil_daily['soil_temp_max'] = df_soil['soil_avg_temp'].resample('B').max()
df_soil_daily['soil_temp_min'] = df_soil['soil_avg_temp'].resample('B').min()



# ----------------------------------------------- FIGURE 1 (cover crop + winter wheat)  -----------------------------------------------
fig, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))

daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'].plot(ax = axes[0], subplots=True, c='grey', ms=1, alpha=0.5, lw=1.5, label='Max Flux')
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'].plot(ax = axes[0], subplots=True, c='darkgrey', alpha=0.5, lw=1.5, label='Min Flux')
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_mean'].plot(ax = axes[0], subplots=True, marker='o', ms = 2, linestyle=':', color = 'red', lw=0.5, label='Mean Flux')
axes[0].fill_between(daily_noniso.index, daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'], daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'], alpha=0.1)
fig.subplots_adjust(left=0.09,bottom=0.16, right=0.94,top=0.90, wspace=0.2, hspace=0)

weather1['Precipitation_Tot_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')
weather2['TB_Avg_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')
#Trailer_weather['Precip_mm'].astype(float).plot(ax = axes[1], subplots=True, color = 'orange')

#extra_ax = axes[1].twinx()
#extra_ax.plot(weather2.index, snowdata['Snowdepth_cm'], marker='.')
#extra_ax.set_ylim([0,300])

df_soil['soil_avg_VWC'].plot(ax=axes[2], subplots=True, color='darkblue', linewidth=2)
daily_noniso['Tcham_mean'].plot(ax = axes[3],subplots=True, color='red', linewidth=2, label='Ambient Air')
df_soil_daily['soil_temp_mean'].plot(ax=axes[3], subplots=True, color='black', linewidth=2, label='Surface Soil')

# Y-Axis Titles
#axes[0].set_title('Daily $N_2$O Fluxes', size=11)
axes[0].set_ylabel(r'$\frac{g-N_{2}O-N}{ha-day}$', size=12)
axes[1].set_ylabel('mm', size=10)
axes[2].set_ylabel('$m^{3}$/$m^{3}$', size=10)
axes[3].set_ylabel('$^\circ$C', size=10)
axes[1].get_yaxis().set_label_coords(-0.04,0.5)

# X -Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time (STD)', size=13)

axes[0].set_xticklabels([])
axes[1].set_xticklabels([])
axes[2].set_xticklabels([])

# Tick Font Size (x,y)
#axes[0].tick_params(axis='x', labelsize=7)    #, rotation=60
#axes[1].tick_params(axis='x', labelsize=7)
#axes[2].tick_params(axis='x', labelsize=7)
axes[3].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=10)
axes[1].tick_params(axis='y', labelsize=10)
axes[2].tick_params(axis='y', labelsize=10)
axes[3].tick_params(axis='y', labelsize=10)

# Edit Date Format
#axes[3].xaxis.set_major_locator(mdates.WeekdayLocator())
#axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

# Legend for fluxes
lgnd = axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize = 10)
#lgnd.get_texts()[0].set_text('Max Flux')
#lgnd.get_texts()[1].set_text('Min Flux')
#lgnd.get_texts()[2].set_text('Mean Flux')

# Legend for temps
lgnd = axes[3].legend(fontsize = 10, ncol=2)
#lgnd.get_texts()[0].set_text('Ambient Air')
#lgnd.get_texts()[1].set_text('Surface Soil')

# Add Graph Titles
axes[0].text('2019-05-02', 66, "Daily $N_2$O Fluxes", size=13, color='black',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.4))
axes[1].text('2019-05-02', 9.2, "Precipitation", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2.2))
axes[2].text('2019-05-02', 0.27, "Soil Moisture", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2, alpha=0.5))
axes[3].text('2019-05-02', 31, "Air & Soil Temp (Daily Avg)", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2.4))

# Add Event Lines & Desc
axes[0].axvline('2019-05-22', color='b', linestyle=':', lw=2)
axes[0].text('2019-06-06', 40, "Water Application\n(~5.3L/microplot)", size=8, color='b', ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))

axes[0].axvline('2019-07-10', color='b', linestyle=':', lw=2)
axes[0].text('2019-07-11', 40, "Harvest", size=8, color='b',  ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))

axes[0].axvline('2019-10-16', color='b', linestyle=':', lw=2)
axes[0].text('2019-10-17', 40, "Seeding &\nFertilization", size=8, color='b', ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))

axes[0].axvline('2020-01-13', color='b', linestyle=':', lw=2)
axes[0].text('2020-01-09', 89, "30cm\nsnow", size=8, color='b', ha='center', va='center')

axes[0].axvline('2020-01-23', color='b', linestyle=':', lw=2)
axes[0].text('2020-01-25', 89, "snow\nmelted", size=8, color='b', ha='center', va='center')

axes[1].axvline('2019-10-09', color='lightgray', lw=10, alpha=0.5)
axes[1].text('2019-10-08', 8, "light\nsnow cover", size=8.5, color='black', ha='center', va='center')

axes[1].axvline('2020-01-17', color='lightgray', lw=30, alpha=0.5)
axes[1].text('2020-01-17', 8, "snow\ncover", size=8.5, color='black', ha='center', va='center')

axes[3].axhline(0, color="gray", alpha=0.7, lw=1.5, linestyle=':')

# Date limit
axes[0].set_xlim(['2019-05-01', '2020-01-24'])
axes[1].set_xlim(['2019-05-01', '2020-01-24'])
axes[2].set_xlim(['2019-05-01', '2020-01-24'])
axes[3].set_xlim(['2019-05-01', '2020-01-24'])

axes[0].set_ylim([-3,80])
axes[1].set_ylim([-0.7,11])
#axes[2].set_ylim([0,0.35])
axes[3].set_ylim([-7,38])

loc = plticker.MultipleLocator(base=20.0) # this locator puts ticks at regular intervals
axes[0].yaxis.set_major_locator(loc)
loc2 = plticker.MultipleLocator(base=0.1) # this locator puts ticks at regular intervals
axes[2].yaxis.set_major_locator(loc2)
loc3 = plticker.MultipleLocator(base=10) # this locator puts ticks at regular intervals
axes[3].yaxis.set_major_locator(loc3)



# ----------------------------------------------- FIGURE 2 (COVERCROP)  -----------------------------------------------
fig2, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))

daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'].plot(ax = axes[0], subplots=True, c='grey', ms=1, alpha=0.7, lw=1)
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'].plot(ax = axes[0], subplots=True, c='darkgrey', alpha=0.7, lw=1)
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_mean'].plot(ax = axes[0], subplots=True, marker='o', ms = 2, linestyle=':', color = 'red', lw=0.5)
axes[0].fill_between(daily_noniso.index, daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'], daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'], alpha=0.1)
fig2.subplots_adjust(left=0.09,bottom=0.16, right=0.94,top=0.90, wspace=0.2, hspace=0)

weather1['Precipitation_Tot_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue', linewidth=2)
weather2['TB_Avg_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue', linewidth=2)
#Trailer_weather['Precip_mm'].astype(float).plot(ax = axes[1], subplots=True, color = 'orange')

df_soil['soil_avg_VWC'].plot(ax=axes[2], subplots=True, color='darkblue', linewidth=2)

daily_noniso['Tcham_mean'].plot(ax = axes[3],subplots=True, color='red', linewidth=2)
df_soil_daily['soil_temp_mean'].plot(ax=axes[3], subplots=True, color='black', linewidth=2)

# Date limit
axes[0].set_xlim(['2019-05-01', '2019-08-23'])
axes[1].set_xlim(['2019-05-01', '2019-08-23'])
axes[2].set_xlim(['2019-05-01', '2019-08-23'])
axes[3].set_xlim(['2019-05-01', '2019-08-23'])

axes[0].set_ylim([-1,22])

# Y-Axis Titles
#axes[0].set_title('Daily $N_2$O Fluxes from Unertilized Cover Crop (Oct 2018 - July 2019)', size=11)
axes[0].set_ylabel(r'$\frac{g-N_{2}O-N}{ha-day}$', size=12)
axes[1].set_ylabel('mm', size=10)
axes[2].set_ylabel('$m^{3}$/$m^{3}$', size=10)
axes[3].set_ylabel('$^\circ$C', size=10)
axes[1].get_yaxis().set_label_coords(-0.04,0.5)

# X -Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time (STD)', size=13)

axes[0].set_xticklabels([])
axes[1].set_xticklabels([])
axes[2].set_xticklabels([])

# Tick Font Size (x,y)
#axes[0].tick_params(axis='x', labelsize=7)    #, rotation=60
#axes[1].tick_params(axis='x', labelsize=7)
#axes[2].tick_params(axis='x', labelsize=7)
axes[3].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=10)
axes[1].tick_params(axis='y', labelsize=10)
axes[2].tick_params(axis='y', labelsize=10)
axes[3].tick_params(axis='y', labelsize=10)

# Legend for fluxes
lgnd = axes[0].legend(loc="top left", bbox_to_anchor=(0.7, 1.35), ncol=3, fontsize = 11)
lgnd.get_texts()[0].set_text('Max Flux')
lgnd.get_texts()[1].set_text('Min Flux')
lgnd.get_texts()[2].set_text('Mean Flux')

# Legend for temps
lgnd = axes[3].legend(loc="bottom right", bbox_to_anchor=(1, 0.35), fontsize = 10, ncol=2)
lgnd.get_texts()[0].set_text('Ambient Air')
lgnd.get_texts()[1].set_text('Surface Soil')

# Add Graph Titles
axes[0].text('2019-05-02', 20, "Daily $N_2$O Fluxes", size=13, color='black',
    bbox=dict(facecolor='white', edgecolor='white', pad=2))
axes[1].text('2019-05-02', 9, "Precipitation", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2))
axes[2].text('2019-05-02', 0.25, "Soil Moisture", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2))
axes[3].text('2019-05-02', 29, "Air & Soil Temp (Daily Avg)", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=2))

# Add Event Lines & Desc
axes[0].axvline('2019-05-22', color='b', linestyle=':', lw=2)
axes[0].text('2019-05-16', 13, "Water Application\n(~5.3L/microplot)", size=9, color='b', ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))

axes[0].axvline('2019-07-10', color='b', linestyle=':', lw=2)
axes[0].text('2019-07-10', 15, "Harvest", size=9, color='b',  ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))


axes[0].set_ylim([-3,25])
axes[1].set_ylim([-0.7,11])
#axes[2].set_ylim([0,0.35])
axes[3].set_ylim([-7,38])

loc = plticker.MultipleLocator(base=10.0) # this locator puts ticks at regular intervals
axes[0].yaxis.set_major_locator(loc)
loc2 = plticker.MultipleLocator(base=0.1) # this locator puts ticks at regular intervals
axes[2].yaxis.set_major_locator(loc2)
loc3 = plticker.MultipleLocator(base=10) # this locator puts ticks at regular intervals
axes[3].yaxis.set_major_locator(loc3)



# ----------------------------------------------- FIGURE 3 (WINTER WHEAT)  -----------------------------------------------
fig3, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))

daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'].plot(ax = axes[0], subplots=True, c='grey', ms=1, alpha=0.5, lw=1)
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'].plot(ax = axes[0], subplots=True, c='darkgrey', alpha=0.5, lw=1)
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_mean'].plot(ax = axes[0], subplots=True, marker='o', ms = 2, linestyle=':', color = 'red', lw=0.5)
axes[0].fill_between(daily_noniso.index, daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'], daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'], alpha=0.1)
fig3.subplots_adjust(left=0.09,bottom=0.16, right=0.94,top=0.90, wspace=0.2, hspace=0)

weather1['Precipitation_Tot_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')
weather2['TB_Avg_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')
#Trailer_weather['Precip_mm'].astype(float).plot(ax = axes[1], subplots=True, color = 'orange')

df_soil['soil_avg_VWC'].plot(ax=axes[2], subplots=True, color='darkblue', linewidth=2)

daily_noniso['Tcham_mean'].plot(ax = axes[3],subplots=True, color='mediumvioletred', linewidth=2)
df_soil_daily['soil_temp_mean'].plot(ax=axes[3], subplots=True, color='black', linewidth=2)

#axes[0].set_ylim([-1,22])

# Y-Axis Titles
#axes[0].set_title('Daily $N_2$O Fluxes from Fertilized Winter Wheat (Oct 2019 - Present)', size=9)
axes[0].set_ylabel(r'$\frac{g-N_{2}O-N}{ha-day}$', size=12)
axes[1].set_ylabel('mm', size=10)
axes[2].set_ylabel('$m^{3}$/$m^{3}$', size=10)
axes[3].set_ylabel('$^\circ$C', size=10)
axes[1].get_yaxis().set_label_coords(-0.04,0.5)

# X -Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time (STD)', size=13)

axes[0].set_xticklabels([])
axes[1].set_xticklabels([])
axes[2].set_xticklabels([])

# Tick Font Size (x,y)
axes[3].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=10)
axes[1].tick_params(axis='y', labelsize=10)
axes[2].tick_params(axis='y', labelsize=10)
axes[3].tick_params(axis='y', labelsize=10)

# Legend for fluxes
lgnd = axes[0].legend(loc="top left", bbox_to_anchor=(0.7, 1.35), ncol=3, fontsize = 11)
lgnd.get_texts()[0].set_text('Max Flux')
lgnd.get_texts()[1].set_text('Min Flux')
lgnd.get_texts()[2].set_text('Mean Flux')

# Legend for temps
lgnd = axes[3].legend(loc="top right", fontsize = 10, ncol=2)
lgnd.get_texts()[0].set_text('Ambient Air')
lgnd.get_texts()[1].set_text('Surface Soil')

# Add Graph Titles
axes[0].text('2019-10-11', 65, "Daily $N_2$O Fluxes", size=13, color='black',
    bbox=dict(facecolor='white', edgecolor='white', pad=1))
axes[1].text('2019-10-11', 9.2, "Precipitation", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=1))
axes[2].text('2019-10-11', 0.35, "Soil Moisture", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=1))
axes[3].text('2019-10-11', 18, "Air & Soil Temp (Daily Avg)", size=13, color='black',
         bbox=dict(facecolor='white', edgecolor='white', pad=1))

# Add Event Lines & Desc
axes[0].axvline('2019-10-16', color='b', linestyle=':', lw=2)
axes[0].text('2019-10-18', 35, "Seeding &\nFertilization", size=9, color='b', ha='center', va='center',
    bbox=dict(facecolor='white', edgecolor='white', pad=2.8))

axes[0].axvline('2020-01-15', color='b', linestyle=':', lw=2)
axes[0].text('2020-01-15', 89, "30cm\nsnow", size=9, color='b', ha='center', va='center')

axes[0].axvline('2020-01-23', color='b', linestyle=':', lw=2)
axes[0].text('2020-01-23', 89, "snow\nmelted", size=9, color='b', ha='center', va='center')

axes[1].axvline('2020-01-18', color='lightgray', lw=60, alpha=0.5)
axes[1].text('2020-01-18', 8, "snow\ncover", size=9, color='black', ha='center', va='center')

axes[3].axhline(0, color="gray", alpha=0.7, lw=1.5, linestyle=':')

# Date limit
axes[0].set_xlim(['2019-10-10', '2020-01-24'])
axes[1].set_xlim(['2019-10-10', '2020-01-24'])
axes[2].set_xlim(['2019-10-10', '2020-01-24'])
axes[3].set_xlim(['2019-10-10', '2020-01-24'])

axes[0].set_ylim([-4,80])
axes[1].set_ylim([-2,11])
axes[2].set_ylim([0,0.45])
axes[3].set_ylim([-10,25])

loc = plticker.MultipleLocator(base=20.0) # this locator puts ticks at regular intervals
axes[0].yaxis.set_major_locator(loc)
loc2 = plticker.MultipleLocator(base=0.1) # this locator puts ticks at regular intervals
axes[2].yaxis.set_major_locator(loc2)
loc3 = plticker.MultipleLocator(base=10) # this locator puts ticks at regular intervals
axes[3].yaxis.set_major_locator(loc3)


# TEST ----------------------------------------------- FIGURE 4 (cover crop + winter wheat)  -----------------------------------------------
fig4, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6), sharey = True)

ax[0].plot(daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'], )

daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'].plot(ax = axes[0], subplots=True, c='grey', ms=1, alpha=0.5, lw=1.5, label='Max Flux')
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'].plot(ax = axes[0], subplots=True, c='darkgrey', alpha=0.5, lw=1.5, label='Min Flux')
daily_noniso['N2O_N_Flux_g/ha/d_NONISO_mean'].plot(ax = axes[0], subplots=True, marker='o', ms = 2, linestyle=':', color = 'red', lw=0.5, label='Mean Flux')
axes[0].fill_between(daily_noniso.index, daily_noniso['N2O_N_Flux_g/ha/d_NONISO_min'], daily_noniso['N2O_N_Flux_g/ha/d_NONISO_max'], alpha=0.1)
fig.subplots_adjust(left=0.09,bottom=0.16, right=0.94,top=0.90, wspace=0.2, hspace=0)

weather1['Precipitation_Tot_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')
weather2['TB_Avg_mm'].plot(ax = axes[1], subplots=True, color = 'darkblue')


extra_ax = axes[1].twinx()
extra_ax.plot(snowdata['Snowdepth_mm'])
extra_ax.set_ylim([0,300])

#snowdata['Snowdepth_mm'].plot(ax = axes[4], subplots=True, color = 'blue')
#axes[4] = axes[1].twinx()
#axes[4].set_ylim([0,300])

df_soil['soil_avg_VWC'].plot(ax=axes[2], subplots=True, color='darkblue', linewidth=2)
daily_noniso['Tcham_mean'].plot(ax = axes[3],subplots=True, color='red', linewidth=2, label='Ambient Air')
df_soil_daily['soil_temp_mean'].plot(ax=axes[3], subplots=True, color='black', linewidth=2, label='Surface Soil')

# Y-Axis Titles
#axes[0].set_title('Daily $N_2$O Fluxes', size=11)
axes[0].set_ylabel(r'$\frac{g-N_{2}O-N}{ha-day}$', size=12)
axes[1].set_ylabel('mm', size=10)
axes[2].set_ylabel('$m^{3}$/$m^{3}$', size=10)
axes[3].set_ylabel('$^\circ$C', size=10)
axes[1].get_yaxis().set_label_coords(-0.04,0.5)

# X -Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time (STD)', size=13)

axes[0].set_xticklabels([])
axes[1].set_xticklabels([])
axes[2].set_xticklabels([])

# Tick Font Size (x,y)

axes[3].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=10)
axes[1].tick_params(axis='y', labelsize=10)
axes[2].tick_params(axis='y', labelsize=10)
axes[3].tick_params(axis='y', labelsize=10)



# Legend for fluxes
lgnd = axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize = 10)

# Legend for temps
lgnd = axes[3].legend(fontsize = 10, ncol=2)

# Add Graph Titles
axes[0].text('2019-05-02', 59, "Daily $N_2$O Fluxes", size=11, color='black',
    bbox=dict(facecolor='white', edgecolor='black', pad=3.2))
axes[1].text('2019-05-02', 3.9, "Precipitation", size=11, color='black',
         bbox=dict(facecolor='white', edgecolor='black', pad=3.0))
axes[2].text('2019-05-02', 0.05, "Soil Moisture", size=11, color='black',
         bbox=dict(facecolor='white', edgecolor='black', pad=3.0))
axes[3].text('2019-05-02', -5, "Air & Soil Temp", size=11, color='black',
         bbox=dict(facecolor='white', edgecolor='black', pad=3.0))

# Add Event Lines & Desc
axes[0].axvline('2019-05-22', color='g', linestyle=':', lw=2)
axes[0].text('2019-05-23', 26, "Water Application \n(~5.3L/microplot)", size=9, color='g')

axes[0].axvline('2019-07-10', color='g', linestyle=':', lw=2)
axes[0].text('2019-07-11', 26, "Harvest", size=9, color='g')

axes[0].axvline('2019-10-16', color='g', linestyle=':', lw=2)
axes[0].text('2019-10-17', 26, "Seeding &\nFertilization", size=9, color='g')

axes[0].axvline('2020-01-15', color='g', linestyle=':', lw=2)
axes[0].text('2020-01-06', 50, "30cm \nsnow", size=9, color='g')

axes[0].axvline('2020-01-20', color='g', linestyle=':', lw=2)
axes[0].text('2020-01-26', 50, "snow \nmelted", size=9, color='g')

# Date limit
axes[0].set_xlim(['2019-05-01', '2020-01-24'])
axes[1].set_xlim(['2019-05-01', '2020-01-24'])
axes[2].set_xlim(['2019-05-01', '2020-01-24'])
axes[3].set_xlim(['2019-05-01', '2020-01-24'])










