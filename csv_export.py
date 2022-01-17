

import csv
import os
import pandas as pd
from pandas import DataFrame

# def save_to_file(jobs,text):
#     file = open(f"{text}.csv", mode="w", encoding='utf-8-sig')
#     writer = csv.writer(file)
#     writer.writerow(["제목", "기업명", "위치", "link"])
    
#     for job in jobs:
#         print(list(job.values()))
#         writer.writerow(list(job.values()))

#     return

def save_to_csv(df_result):
    
    df_tag = pd.DataFrame(df_result)
    if not os.path.exists('tag_list_.csv'):
        df_tag.to_csv('tag_list_.csv', index=False, mode='w', encoding='utf-8-sig')
        print("*" * 100)
        print("없는CSV 저장")
        print(df_tag)
        print("*" * 100)
    else:
        df_tag.to_csv('tag_list_.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
        print("*" * 100)
        print("있는CSV 저장")
        print(df_tag)
        print("*" * 100)



