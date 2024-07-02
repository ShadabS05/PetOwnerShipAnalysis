import os
import numpy as np
import pandas as pd
#from sklearn.metrics import accuracy_score

data_path  = '/Users/viomeuser/Documents/Viome Project/Data/'
genus_no_middle_quartile = pd.read_csv(data_path + "genus_all_middle_quartile.csv")
genus_all_middle_quartile = pd.read_csv(data_path + "genus_no_middle_quartile.csv")
genus_yes_middle_quartile = pd.read_csv(data_path + "genus_yes_middle_quartile.csv")
genus_all_data = pd.read_csv(data_path + "results_genus_data.csv")
#print(len(genus_all_data["external_id"].unique()))
def fun_score(all_df, external_id, m_qle):
    specific_external_id = all_df[all_df["external_id"] == external_id]
    merged_m_qle = specific_external_id.merge(m_qle, how="inner", left_on = ["taxonomy_name"], right_on=["taxonomy_id"], suffixes=('', '0_x'))
    #print(specific_external_id)
    #print(merged_m_qle)
    return sum(merged_m_qle["proportion"] * merged_m_qle["relative_activity"])
total_score = []
for x in genus_all_data["external_id"].unique():
    total_score.append([x, (genus_all_data.query("external_id == '"+x+"'")["pet"].unique()[0]), fun_score(genus_all_data, x, genus_all_middle_quartile),
    fun_score(genus_all_data, x, genus_yes_middle_quartile),
    fun_score(genus_all_data, x, genus_no_middle_quartile)])
score_data = pd.DataFrame(total_score, columns=['external_id', 'pet', 'score_all', 'score_yes','score_no'])
print(score_data)
score_data.to_csv(data_path + "score_data.csv")


