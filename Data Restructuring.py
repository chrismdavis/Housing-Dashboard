import pandas as pd

######################################################################################################
# Define Inputs
######################################################################################################

# Set year range and default selections
Min_Year = 2010
Max_Year = 2021

######################################################################################################
# Import and Prepare Data
######################################################################################################

# Import data
df_1br = pd.read_csv("1 Bedroom.csv")
df_2br = pd.read_csv("2 Bedroom.csv")
df_3br = pd.read_csv("3 Bedroom.csv")

# Define restructuring functions


def data_restructure_choro(dff, start_year, end_year, br_type):
    dff['CountyCode'] = dff['StateCodeFIPS'].apply(lambda x: str(x).zfill(2)) + dff['MunicipalCodeFIPS'].apply(
        lambda x: str(x).zfill(3))

    dff = dff.drop(['RegionID', 'SizeRank', 'RegionType', 'State', 'Metro', 'StateCodeFIPS', 'MunicipalCodeFIPS'],
                   axis=1)

    dff = dff.melt(id_vars=['CountyCode', 'RegionName', 'StateName'],
                   var_name="Year",
                   value_name="Home Value")

    dff['Year'] = dff['Year'].apply(lambda x: int(x[0:4]))

    dff = dff.groupby(['CountyCode', 'RegionName', 'StateName', 'Year'], axis=0, as_index=False).mean()

    dff = dff[(dff.Year >= start_year) & (dff.Year <= end_year)]

    dff["Home Value"] = dff["Home Value"].round(0)

    dff['Size'] = br_type

    return dff


def data_restructure_line(dff, start_year, end_year, br_type):
    dff['CountyCode'] = dff['StateCodeFIPS'].apply(lambda x: str(x).zfill(2)) + dff['MunicipalCodeFIPS'].apply(
        lambda x: str(x).zfill(3))

    dff = dff.drop(['RegionID', 'SizeRank', 'RegionType', 'State', 'Metro', 'StateCodeFIPS', 'MunicipalCodeFIPS'], axis=1)

    dff = dff.melt(id_vars=['CountyCode', 'RegionName', 'StateName'],
                   var_name="Date",
                   value_name="Home Value")

    dff['Year'] = dff['Date'].apply(lambda x: int(x[0:4]))
    dff = dff[(dff['Year'] >= start_year) & (dff['Year'] <= end_year)]
    dff = dff.drop(['Year'], axis=1)

    dff = dff.sort_values(by='Date', ascending=True)

    dff['Size'] = br_type

    return dff


# Restructure datasets
df_1br_cl = data_restructure_choro(df_1br, Min_Year, Max_Year, '1 Bedroom')
df_2br_cl = data_restructure_choro(df_2br, Min_Year, Max_Year, '2 Bedroom')
df_3br_cl = data_restructure_choro(df_3br, Min_Year, Max_Year, '3 Bedroom')
df_1br_lp = data_restructure_line(df_1br, Min_Year, Max_Year, '1 Bedroom')
df_2br_lp = data_restructure_line(df_2br, Min_Year, Max_Year, '2 Bedroom')
df_3br_lp = data_restructure_line(df_3br, Min_Year, Max_Year, '3 Bedroom')

# Merge files
df_choro = pd.concat([df_1br_cl, df_2br_cl, df_3br_cl])
df_line = pd.concat([df_1br_lp, df_2br_lp, df_3br_lp])

df_choro.reset_index(drop=True, inplace=True)
df_line.reset_index(drop=True, inplace=True)

# Save files
df_choro.to_csv("df_choro.csv", index=False)
df_line.to_csv("df_line.csv", index=False)
