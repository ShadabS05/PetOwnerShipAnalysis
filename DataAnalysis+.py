import pandas as pd
import math
#from sklearn.metrics import accuracy_score

data_path  = '/Users/viomeuser/Documents/Viome Project/Data/'
genus_data = pd.read_csv(data_path + "genus_data.csv")
results_sample_data = pd.read_csv(data_path + "result_samples.csv")
results_genus_data = genus_data.merge(results_sample_data, how="inner", on=["external_id"])
first_split = results_genus_data.iloc[:int(len(results_genus_data)/5)]
second_split = results_genus_data.iloc[int(len(results_genus_data)/5):int((len(results_genus_data)/5) * 2)]
third_split = results_genus_data.iloc[int((len(results_genus_data)/5) * 2): int((len(results_genus_data)/5) * 3)]
fourth_split = results_genus_data.iloc[int((len(results_genus_data)/5) * 3): int((len(results_genus_data)/5) * 4)]
fifth_split = results_genus_data.iloc[int((len(results_genus_data)/5) * 4): int(len(results_genus_data))]

def log_fold_change(gdf):
    # Input : external_id, taxonomy_name, relative_activity, pet
    #These lines are algorithim/steps
    #For each genus, compute average relative activity for pet_owners(arap) and non_pet_owners(aranp)
    #return log2(arap / aranp )
    #need to remove aranp = 0 to avoid divison by 0
    fold_change = []
    print("printing: Length of Dataframe")
    print(len(gdf))
    print("printing amount of exeternal_ids for")
    print(len(gdf["external_id"].unique()))
    unique_pet = gdf[(gdf['pet'] == "Yes")]["external_id"].unique()
    unique_no_pet = gdf[(gdf['pet'] == "No")]["external_id"].unique()
    print("printing amount of people with a pet for")
    print(len(unique_pet))
    print("printing amount of people without a pet for")
    print(len(unique_no_pet))

    for x in gdf["taxonomy_name"].unique():
    #   aran = gdf["taxonomy_id"]
    #   arap = get all pet owners and taxonomy_id = x and compute average relative activity
    #   aranp = get all non_pet_owners and taxonomy id  = x and compute average relative activity
        unique_taxonomy_pet = gdf[(gdf['taxonomy_name'] == x) & (gdf['pet'] == "Yes")]
        pet_means = unique_taxonomy_pet['relative_activity'].sum(axis='index')/len(unique_pet)
        unique_taxonomy_no_pet = gdf[(gdf['taxonomy_name'] == x) & (gdf['pet'] == "No")]
        no_pet_means = unique_taxonomy_no_pet['relative_activity'].sum(axis='index')/len(unique_no_pet)
        if no_pet_means != 0 and pet_means != 0:
            lfc = math.log2(pet_means / no_pet_means)
            fold_change.append([x, lfc])
    fold_change_df = pd.DataFrame(fold_change, columns=['genus', 'log2fold_change'])
    return fold_change_df
# log_fold_change_young = log_fold_change(results_genus_data[results_genus_data["age"] < 18])
# log_fold_change_medium = log_fold_change(results_genus_data[(results_genus_data["age"] > 18) & (results_genus_data["age"] < 27 )])
# log_fold_change_old = log_fold_change(results_genus_data[(results_genus_data["age"] > 27) & (results_genus_data["age"] < 55)])
# log_fold_change_oldest = log_fold_change(results_genus_data[results_genus_data["age"] > 55])
# log_fold_change_young.to_csv(data_path + "log_fold_change_under_eighteen.csv")
# log_fold_change_medium.to_csv(data_path + "log_fold_change_between_eighteen_and_twenty-seven.csv")
# log_fold_change_old.to_csv(data_path + "log_fold_change_between_twenty-seven_and_fifty-five.csv")
# log_fold_change_oldest.to_csv(data_path + "log_fold_change_over_fifty-five.csv")
log_fold_change_first_split = log_fold_change(first_split)
log_fold_change_second_split = log_fold_change(second_split)
log_fold_change_third_split = log_fold_change(third_split)
log_fold_change_fourth_split = log_fold_change(fourth_split)
log_fold_change_fifth_split = log_fold_change(fifth_split)
log_fold_change_first_split["split_number"] = 1
log_fold_change_second_split["split_number"] = 2
log_fold_change_third_split["split_number"] = 3
log_fold_change_fourth_split["split_number"] = 4
log_fold_change_fifth_split["split_number"] = 5

log_fold_change_all_splits = pd.concat([log_fold_change_first_split, log_fold_change_second_split, log_fold_change_third_split, log_fold_change_fourth_split, log_fold_change_fifth_split], axis = 0)
print(len(log_fold_change_all_splits))
log_fold_change_all_splits.to_csv(data_path + "log_fold_change_all_splits.csv")

# log_fold_change_first_split.to_csv(data_path + "log_fold_change_first_split.csv")
# log_fold_change_second_split.to_csv(data_path + "log_fold_change_second_split.csv")
# log_fold_change_third_split.to_csv(data_path + "log_fold_change_third_split.csv")
# log_fold_change_fourth_split.to_csv(data_path + "log_fold_change_fourth_split.csv")
# log_fold_change_fifth_split.to_csv(data_path + "log_fold_change_fifth_split.csv")



print(log_fold_change_first_split)
# print(log_fold_change_second_split)




 # log_fold_change_twentyfive.to_csv(data_path + "log_fold_change_twentyfive.csv")
 #0-17, 18-26, 27-54, 55+, split the genus data into 5, do a loop for the 5, and everytime i run, report the pet and no pet, copy from screen to document
#log_fold_change_all = log_fold_change(results_genus_data)
#print(log_fold_change_all)
# log_fold_change_all.to_csv(data_path + "log_fold_change_all.csv")
# def log_fold_change_old(gdf):
#     #Code Sketch
#     #Start a blank list
#     fold_change = []
#     young_fold_change = []
#     middle_fold_change = []
#     old_fold_change = []
#     young_age_filter = 18
#     middle_age_filter = 27
#     old_age_filter = 55
#     young_age = gdf[(young_age_filter <= gdf['age']) & (gdf['age'] < middle_age_filter)]
#     middle_age = gdf[(middle_age_filter <= gdf['age']) & (gdf['age'] < old_age_filter)]
#     old_age = gdf[(old_age_filter <= gdf['age'])]
#     for x in gdf["taxonomy_name"].unique():
#     #   aran = gdf["taxonomy_id"]
#     #   arap = get all pet owners and taxonomy_id = x and compute average relative activity
#     #   aranp = get all non_pet_owners and taxonomy id  = x and compute average relative activity
#         unique_taxonomy = gdf.loc[gdf['taxonomy_name'] == x]
#         fold_change.append([x , unique_taxonomy['relative_activity'].mean(axis='index')])
#     for x in young_age["taxonomy_name"].unique():
#     #   aran = gdf["taxonomy_id"]
#     #   arap = get all pet owners and taxonomy_id = x and compute average relative activity
#     #   aranp = get all non_pet_owners and taxonomy id  = x and compute average relative activity
#         unique_taxonomy = young_age.loc[young_age['taxonomy_name'] == x]
#         young_fold_change.append([x , unique_taxonomy['relative_activity'].mean(axis='index')])
#     for x in middle_age["taxonomy_name"].unique():
#     #   aran = gdf["taxonomy_id"]
#     #   arap = get all pet owners and taxonomy_id = x and compute average relative activity
#     #   aranp = get all non_pet_owners and taxonomy id  = x and compute average relative activity
#         unique_taxonomy = middle_age.loc[middle_age['taxonomy_name'] == x]
#         middle_fold_change.append([x , unique_taxonomy['relative_activity'].mean(axis='index')])
#     for x in old_age["taxonomy_name"].unique():
#     #   aran = gdf["taxonomy_id"]
#     #   arap = get all pet owners and taxonomy_id = x and compute average relative activity
#     #   aranp = get all non_pet_owners and taxonomy id  = x and compute average relative activity
#         unique_taxonomy = old_age.loc[old_age['taxonomy_name'] == x]
#         old_fold_change.append([x , unique_taxonomy['relative_activity'].mean(axis='index')])
#
#     # for x in young_age["external_id"].unique():
#     #     unique_id = gdf.loc[gdf['external_id'] == x]
#     #     if ((gdf.query("external_id=='x'")["age"] >= 18) and (gdf.query("external_id=='x'")["age"] < 27)):
#     #         young_age_filter.append([x, unique_id])
#     #     if ((gdf.query("external_id=='x'")["age"] >= 27) and (gdf.query("external_id=='x'")["age"] < 55)):
#     #         middle_age_filter.append([x, unique_id])
#     #     if (gdf.query("external_id=='x'")["age"] >= 55):
#     #         old_age_filter.append([x, unique_id])
#     return fold_change, young_fold_change, middle_fold_change, old_fold_change
#         #,young_age_filter, middle_age_filter, old_age_filter
# #fold_change_df = pd.DataFrame(log_fold_change(results_genus_data), columns=['genus', 'average_relative_activity'])
#
# fold_change, young_fold_change, middle_fold_change, old_fold_change = log_fold_change(results_genus_data)
# fold_change_df = pd.DataFrame(fold_change, columns=['genus', 'average_relative_activity'])
# young_fold_change_df = pd.DataFrame(young_fold_change, columns=['genus', 'average_relative_activity'])
# middle_fold_change_df = pd.DataFrame(middle_fold_change, columns=['genus', 'average_relative_activity'])
# old_fold_change_df = pd.DataFrame(old_fold_change, columns=['genus', 'average_relative_activity'])
#
# print(old_fold_change_df)
#possible problem with relativty activity within genus_data (alot of 1.0s, doesn't look too similar to your spreadsheet)



    #   if aranp != 0:
    #       list.append([taxonomy_id, log2(arap/aranp])
    #return list
# outputs 1: all, by age groups (18, 27, 55). Analysis = Most prominent fold change genus in each group, difference between the subgroups
# outputs 2: robustness check, pick one subgroup from outputs 1 and run log_fold_change on 5 random subsets
#     count_uniques = len(pd.unique(gdf["external_id"]))
#     genus_value_counts = gdf.value_counts(["external_id", "taxonomy_name"])
#     genus_data_value_counts = pd.DataFrame(genus_value_counts)
#     genus_data_value_counts_reset = genus_data_value_counts.reset_index()
#     genus_data_value_counts_reset.columns = ['external_id','taxonomy_name', 'counts'] # change column names
#     #print(genus_data_value_counts_reset)
#     common_genus = genus_data_value_counts_reset["taxonomy_name"].value_counts(normalize = True).rename_axis('taxonomy_id').reset_index(name='proportion')
    #common_genus.insert(count_uniques)
    #common_genus_dataframe = common_genus.to_frame()
    #common_genus_dataframe["taxonomy_name"] = common_genus_dataframe.index.values
#     return common_genus, count_uniques
# genus_no, genus_no_counts = summarize_genus(results_genus_data[results_genus_data['pet'] == "No"])
# genus_yes, genus_yes_counts = summarize_genus(results_genus_data[results_genus_data['pet'] == "Yes"])
# genus_all, genus_all_counts = summarize_genus(results_genus_data)>>
# low_filter = .1
# print(low_filter)
# high_filter = .9
# print(high_filter)
# def middle_quartile(dataframe, h_filter, l_filter):
#     middle_quartile_genus = dataframe[(dataframe.proportion > dataframe.proportion.quantile(l_filter)) & (dataframe.proportion < dataframe.proportion.quantile(h_filter))]
#     return middle_quartile_genus
# genus_yes_middle_quartile = middle_quartile(genus_yes, high_filter, low_filter)
# genus_no_middle_quartile = middle_quartile(genus_no, high_filter, low_filter)
# genus_all_middle_quartile = middle_quartile(genus_all, high_filter, low_filter)
# print(genus_yes_middle_quartile)
# print(genus_no_middle_quartile)
# print(genus_all_middle_quartile)
# genus_all_middle_quartile.to_csv(data_path + "genus_all_middle_quartile.csv")
# genus_no_middle_quartile.to_csv(data_path + "genus_no_middle_quartile.csv")
# genus_yes_middle_quartile.to_csv(data_path + "genus_yes_middle_quartile.csv")
# results_genus_data.to_csv(data_path + "results_genus_data.csv")

#middle_quartile_yes_genus =  genus_yes[(low_filter <= genus_yes['proportion'])]
#middle_quartile_no_genus = genus_no[(low_filter <= genus_no['proportion']) & (genus_no['proportion'] < high_filter)]
#chop 2nd and 3rd quartile
#print(summarize_genus(genus_data))

#load data
#quick summary of genomic data to test how data structure works
#first counts
#split into top pets/top non pets genus
#take bottom taxonomy_name appearances and take the external id of those bottom ones and check to see if they have a pet or not