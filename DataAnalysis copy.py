import os
import numpy as np
import pandas as pd
#from sklearn.metrics import accuracy_score

data_path  = '/Users/viomeuser/Documents/Viome Project/Data/'
genus_data = pd.read_csv(data_path + "genus_data.csv")
results_sample_data = pd.read_csv(data_path + "result_samples.csv")
results_genus_data = genus_data.merge(results_sample_data, how="inner", on=["external_id"])
print(len(genus_data))
print(len(results_sample_data))

def summarize_genus(gdf):
    count_uniques = len(pd.unique(gdf["external_id"]))
    genus_value_counts = gdf.value_counts(["external_id", "taxonomy_name"])
    genus_data_value_counts = pd.DataFrame(genus_value_counts)
    genus_data_value_counts_reset = genus_data_value_counts.reset_index()
    genus_data_value_counts_reset.columns = ['external_id','taxonomy_name', 'counts'] # change column names
    #print(genus_data_value_counts_reset)
    common_genus = genus_data_value_counts_reset["taxonomy_name"].value_counts(normalize = True).rename_axis('taxonomy_id').reset_index(name='proportion')
    #common_genus.insert(count_uniques)
    #common_genus_dataframe = common_genus.to_frame()
    #common_genus_dataframe["taxonomy_name"] = common_genus_dataframe.index.values
    return common_genus, count_uniques
genus_no, genus_no_counts = summarize_genus(results_genus_data[results_genus_data['pet'] == "No"])
genus_yes, genus_yes_counts = summarize_genus(results_genus_data[results_genus_data['pet'] == "Yes"])
genus_all, genus_all_counts = summarize_genus(results_genus_data)
low_filter = .1
print(low_filter)
high_filter = .9
print(high_filter)
def middle_quartile(dataframe, h_filter, l_filter):
    middle_quartile_genus = dataframe[(dataframe.proportion > dataframe.proportion.quantile(l_filter)) & (dataframe.proportion < dataframe.proportion.quantile(h_filter))]
    return middle_quartile_genus
genus_yes_middle_quartile = middle_quartile(genus_yes, high_filter, low_filter)
genus_no_middle_quartile = middle_quartile(genus_no, high_filter, low_filter)
genus_all_middle_quartile = middle_quartile(genus_all, high_filter, low_filter)
print(genus_yes_middle_quartile)
print(genus_no_middle_quartile)
print(genus_all_middle_quartile)
genus_all_middle_quartile.to_csv(data_path + "genus_all_middle_quartile.csv")
genus_no_middle_quartile.to_csv(data_path + "genus_no_middle_quartile.csv")
genus_yes_middle_quartile.to_csv(data_path + "genus_yes_middle_quartile.csv")
results_genus_data.to_csv(data_path + "results_genus_data.csv")

#middle_quartile_yes_genus =  genus_yes[(low_filter <= genus_yes['proportion'])]
#middle_quartile_no_genus = genus_no[(low_filter <= genus_no['proportion']) & (genus_no['proportion'] < high_filter)]
#chop 2nd and 3rd quartile
#print(summarize_genus(genus_data))

#load data
#quick summary of genomic data to test how data structure works
#first counts
#split into top pets/top non pets genus
#take bottom taxonomy_name appearances and take the external id of those bottom ones and check to see if they have a pet or not