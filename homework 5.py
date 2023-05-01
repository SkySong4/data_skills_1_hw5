# PPHA 30537
# Spring 2023
# Homework 5

# YOUR NAME HERE
# YOUR GITHUB USER NAME HERE

# Due date: Sunday April 30th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work. Using functions for organization will be rewarded.

##################

# To answer these questions, you will continue from where you left off in
# homework 4, by using the included file named hw4_data.csv.

import os
import pandas as pd

BASE_DIR = r"D:\\data_skills_1_hw5"
def load_df(csv_filename):
    abs_path = os.path.join(BASE_DIR, csv_filename)
    return pd.read_csv(abs_path)
if __name__ == '__main__':
    csv_filename = "hw4_data.csv"
    df = load_df(csv_filename)
    df.reset_index(drop=True, inplace=True)
   
  
# Question 1a: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
df_long = pd.wide_to_long(df,
                          stubnames=["POPESTIMATE"],
                          i="STATE", j="Year", sep="").reset_index()
df_long=df_long.drop(columns=['POPCHANGE'])
df_long=df_long.sort_values(by=['STATE', 'Year']).reset_index(drop=True)
print(df_long)


# Question 1b: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 1a (without the POPCHANGE column).
melted_df = pd.melt(df, id_vars=['STATE'], value_vars=['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022'], var_name='Year', value_name='Population')
melted_df['Year'] = melted_df['Year'].str[-4:]
melted_df = melted_df.sort_values(by=['STATE', 'Year']).reset_index(drop=True)
print(melted_df)


# Question 2: Open the state-visits.xlsx file, and fill in the VISITED column
# with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original long-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.
state_visits = pd.read_excel('state-visits.xlsx')
merged_df = pd.merge(melted_df, state_visits[['STATE', 'VISITED']], on='STATE', how='inner')
print(merged_df)
# Check if any observations are dropped
merged_obs = len(merged_df)
original_obs = len(melted_df)
print(f"Original number of observations: {original_obs}")
print(f"Merged number of observations: {merged_obs}")

if original_obs == merged_obs:
    print("No observations were dropped.")
else:
    print(f"{original_obs - merged_obs} observations were dropped.")
# Display any observations that weren't in both dataframes
dropped_obs = melted_df[~melted_df['STATE'].isin(merged_df['STATE'])]
print("Observations that were not in both dataframes:")
print(dropped_obs)


# Question 3a: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.
epu_df = pd.read_excel('policy_uncertainty.xlsx')
epu_grouped = epu_df.groupby(['state', 'year'])['EPU_Composite'].mean().reset_index()
print("Mean EPU-C value for each state/year:")
print(epu_grouped)


# Question 3b: Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. Reshape the EPU data into wide format
epu_wide = epu_grouped.pivot(index='state', columns='year', values='EPU_Composite').reset_index()
epu_wide =epu_wide[['state', 2020, 2021, 2022]]
print("EPU data in wide format:")
print(epu_wide)


# Question 3c: Finally, merge this data into your merged data from question 2, 
# making sure the merge does what you expect.
# Merge the wide EPU data into the merged data from question 2
final_df = pd.merge(merged_df, epu_wide, left_on='STATE', right_on='state', how='inner')
# Drop the duplicate 'state' column
print(final_df) 
final_df.drop(columns=['state'], inplace=True)
print("Final merged DataFrame:")
print(final_df)


# Question 4: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: 
#（a) what is the single smallest state by 2022 population that you have 
# visited, and not visited?
visited_smallest = final_df[(final_df['VISITED'] == 1 )&( final_df['Year'] == "2022")].nsmallest(1, 'Population') # 1 for visited states
not_visited_smallest = final_df[(final_df['VISITED'] == 0)&( final_df['Year'] == "2022")].nsmallest(1, 'Population') # 0 for not visited states
print("Smallest visited state:", visited_smallest["STATE"])
print("Smallest not visited state:", not_visited_smallest['STATE'])


#（b) what are the three largest states by 2022 population you have visited, 
# and the three largest states by 2022 population you have not visited? 
visited_largest = final_df[(final_df['VISITED'] == 1 )&( final_df['Year'] == "2022")].nlargest(3, 'Population')
not_visited_largest = final_df[(final_df['VISITED'] == 0 )&( final_df['Year'] == "2022")].nlargest(3, 'Population')
print("Three largest visited states:")
print(visited_largest['STATE'])
print("\nThree largest not visited states:")
print(not_visited_largest['STATE'])


# c) do states you have visited or states you have not visited have a 
# higher average EPU-C value in 2022?
print(final_df)
average_epu_c = final_df.groupby('VISITED')[2022].mean()
print("Average EPU-C value for visited states:", average_epu_c[1])
print("Average EPU-C value for not visited states:", average_epu_c[0])
if average_epu_c[1] > average_epu_c[0]:
    print("Visited states have a higher average EPU-C value in 2022.")
else:
    print("Not visited states have a higher average EPU-C value in 2022.")
    
    
# Question 5: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 3a and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore. 
def standardize(series):
    mean = series.mean()
    std = series.std()
    return (series - mean) / std
print(epu_grouped)
epu_c_zscore = epu_grouped.groupby('state')['EPU_Composite'].transform(standardize)
epu_grouped['EPU_C_zscore'] = epu_c_zscore
print(epu_grouped) 
