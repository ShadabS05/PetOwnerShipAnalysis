import os
import numpy as np
import pandas as pd
#from sklearn.metrics import accuracy_score

data_path  = '/Users/viomeuser/Documents/Viome Project/Data/'
cohort_data = pd.read_csv(data_path + "cohort.csv")
labels_data = pd.read_csv(data_path + "labels.csv")
samples_data = pd.read_csv(data_path + "samples.csv")
print("Labels_data has ", len(labels_data), "rows")
print("Cohort_data has ", len(cohort_data), "rows")
cohort_data = cohort_data.dropna(axis=0)
cohort_data = cohort_data.astype({'userId':'int'})
labels_duplicate = labels_data[labels_data.duplicated(['userId'])]
#cohort_duplicate = cohort_data[cohort_data.duplicated(['userId'])]
#samples_duplicate = samples_data[samples_data.duplicated(['userId'])]
#print(duplicate["userId"])
def filter_rows_by_values(df, col, values):
   return df[~df[col].isin(values)]

labels_filter = labels_duplicate["userId"].tolist()
#cohort_filter = cohort_duplicate["userId"].tolist()
#samples_filter = samples_duplicate["userId"].tolist()


#print(filter)
print("filtering out ", len(labels_filter), "rows")
labels_data_filtered = filter_rows_by_values(labels_data, "userId", labels_filter)
#cohort_data_filtered = filter_rows_by_values(cohort_data, "userId", cohort_filter)
#samples_data_filtered = filter_rows_by_values(samples_data, "userId", samples_filter)

print(len(labels_data_filtered))

result = cohort_data.merge(labels_data_filtered, how="inner", on=["userId"])
result = result.dropna(axis=0)

print(len(result))

#Next step : Add variables from dates from and date to May 1st, 2022, 4-25-2023
low_filter = "2022-05-01"
high_filter = "2023-04-25"
result_filtered = result[(low_filter <= result['recs_date']) & (result['recs_date'] < high_filter)]
samples_filtered = samples_data[(low_filter <= samples_data['recs_date']) & (samples_data['recs_date'] < high_filter)]
print(len(result_filtered))
print(len(samples_filtered))
print(result_filtered[result_filtered['pet'] == "No"])
result_filtered_samples = result_filtered.merge(samples_filtered, how="inner", on=["kitId", "recs_date", "userId", "rn"])
result_filtered_samples = result_filtered_samples.dropna(axis=0)
print(result_filtered_samples)
genus_data_list = []
for x in result_filtered_samples["external_id"]:
   title = "taxa_" + x + ".csv"
   genus = pd.read_csv(data_path + 'genus/' + title)
   genus["external_id"] = x
   genus_data_list.append(genus)
genus_data = pd.concat(genus_data_list)
genus_data.to_csv(data_path + "genus_data.csv")
result_filtered_samples.to_csv(data_path + "result_samples.csv")


#Filter results for kits between dates from and date to
#Count how many are pets Yes/Np
#Test for old bioinfromatics or new bioinformatics
#Next Step : Loop through all external ID
#Load all the microbiome data
#When Loading microbiome data, it will not have the sample id within it
# Need to add sample id when loading