import pandas as pd
import time

# reading CSV file
fields_s1 = ["Endpoint Name", "Site", "Last Logged In User", "Domain", "Last Active", "Device Type", "OS"]
fields_ad = ["Name", "DNSHostName", "Enabled", "ModifiedLastLogonDate"]
fields_exclude = ["Name"]

# create pandas dataframe
df_s1 = pd.read_csv("s1export.csv", usecols=fields_s1)

# rename column for better understanding and avoid duplicate columns
df_s1 = df_s1.rename(columns={'Endpoint Name': 'Name_S1', 'Site': 'Site_S1', 'Last Logged In User': 'LastUser_S1', 'Domain': 'Domain_S1', 'Last Active': 'LastActive_S1', 'Device Type': 'Device_S1', 'OS': 'OS_S1'})

# change name to upper cause join is case sensitive
df_s1['Name_S1'] = df_s1['Name_S1'].str.upper()

# export of AD via. powershell (please see readme)
df_ad = pd.read_csv("ad-computers.csv", usecols=fields_ad)
df_ad = df_ad.rename(columns={'Name': 'Name_AD', 'DNSHostName': 'DNS_AD', 'Enabled': 'Enabled_AD', 'ModifiedLastLogonDate': 'LastLogon_AD'})
df_ad['Name_AD'] = df_ad['Name_AD'].str.upper()

# read excludes
df_exclude = pd.read_csv("exclude.csv", usecols=fields_exclude)
df_exclude['Name'] = df_exclude['Name'].str.upper()

# merge dataframes together as outer join
df_merge = pd.merge(df_ad, df_s1, left_on="Name_AD", right_on="Name_S1", how="outer")

# drop excluded rows
df_merge = df_merge.drop(df_merge[df_merge.Name_AD.isin(df_exclude.Name)].index.tolist())

# create new result csv
result_file = "s1-ad-diff_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
df_merge.to_csv(result_file, sep=";", encoding="utf-8")
