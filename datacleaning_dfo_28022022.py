import pandas as pd
import sys
import re
from difflib import SequenceMatcher
from dateutil.parser import parse
from datetime import datetime
import datetime as dt
import glob
from functools import reduce
import string
import numpy as np
from pathlib import Path
def dane_logic(master):
    crash=0
    # excel_file_path_dfosheets = (Path(__file__).resolve().parent.joinpath(f"static/media/input_files/DFO_latest_sheets"))    
    files = glob.glob('static/media/input_files/DFO_latest_sheets/*.xlsx')
    with open("log.txt", "w") as f:
        f.truncate(0)
        # sys.stdout.close()
    with open('log.txt','a') as logfile:
        # print("I am in log file",file = logfile)
        now_files_upload = datetime.now()
        timestamp_files_upload = now_files_upload.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
        print(f"{timestamp_files_upload}-->total DFO sheets uploaded is"+" "+str(len(files)),file=logfile)
        dfo_list = [pd.read_excel(file) for file in files]

        excel_file_path = (Path(__file__).resolve().parent.joinpath(f"static/media/input_files/master_DFO/{master}"))
        # Load the two Excel files into pandas dataframes
        df1 = pd.read_excel(excel_file_path)

        integer_regex = re.compile(r'^\d{4,}$')
        integer_regex_district = re.compile(r'^\d{1,3}$')

        date_regex = re.compile(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}[/-][a-zA-Z]{3}[/-]\d{2,4}|\d{1,2}[/-][a-zA-Z]{3}[/-]\d{2,4}\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)|\d{4}[/-]\d{1,2}[/-]\d{1,2}\s\d{1,2}:\d{2}:\d{2}|[a-zA-Z]{3}\s\d{1,2},?\s\d{2,4}\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)?)')

        # Define the sets of keywords for date type columns
        keywords1 = ['participant_start', 'participantstart','license_participant_start','lic_participant_start','licenseparticipant_start','lic_participantstart','lic participantstart','licenseparticipant start','licparticipant start']
        keywords2 = ['participant_end', 'participantend','license_participant_end','lic_participant_end','licenseparticipant_end','lic_participantend','lic participantend','licenseparticipant end','licparticipant end']
        keywords3 = ['area_start', 'areastart','license_area_start','lic_area_start','licensearea_start','lic_areastart','lic areastart','licensearea start','licarea start']
        keywords4 = ['area_end', 'areaend','license_area_end','lic_area_end','licensearea_end','lic_areaend','lic areaend','licensearea end','licarea end']
        keywords5 = ['vessel_start', 'vesselstart','license_vessel_start','lic_vessel_start','licensevessel_start','lic_vesselstart','lic vesselstart','licensevessel start','licvessel start']
        keywords6 = ['vessel_end', 'vesselend','license_vessel_end','lic_vessel_end','licensevessel_end','lic_vesselend','lic vesselend','licensevessel end','licvessel end']
        keywords7 = ['gear_start', 'gearstart','license_gear_start','lic_gear_start','licensegear_start','lic_gearstart','lic gearstart','licensegear start','licgear start']
        keywords8 = ['gear_end', 'gearend','license_gear_end','lic_gear_end','licensegear_end','lic_gearend','lic gearend','licensegear end','licgear end']
        keyword_sets = [keywords1,keywords2,keywords3,keywords4,keywords5,keywords6,keywords7,keywords8]

        def classify_column_name(column_name, keyword_sets):
            # Predict the label for the input column name for each keyword set
            for i, keywords in enumerate(keyword_sets):
                # Return the name of the keyword set if any of the keywords is present in the column name
                if any(keyword in column_name.lower() for keyword in keywords):
                    return f'keywords{i+1}'
            return "column name not found"

        date_dict_name = {'keywords1': 'LICENCE_PARTICIPANT_START_DATE', 'keywords2': 'LICENCE_PARTICIPANT_END_DATE', 'keywords3': 'LICENCE_AREA_START_DATE', 'keywords4': 'LICENCE_AREA_END_DATE', 'keywords5': 'LICENCE_VESSEL_START_DATE', 'keywords6': 'LICENCE_VESSEL_END_DATE', 'keywords7': 'LICENCE_GEAR_START_DATE', 'keywords8': 'LICENCE_GEAR_END_DATE'}

        #Identify the column(s) & renaming them which contain the common data between the DFO master sheet & DFO files

        dfo_list1=[]
        df_final = pd.DataFrame()
        for df2 in dfo_list:
            common_columns = []    
            for col1 in df1.columns:
                for col2 in df2.columns:
                    df2[col2]=df2[col2].fillna("******")
                    if (df2[col2].isin(df1[col1])).any():
                        
                        if  all([bool(integer_regex.match(str(val))) for val in df2[col2]]):
                            s = SequenceMatcher(None,col2,col1)
                            similarity = s.ratio()
                            sim = round(similarity,2)
                            if similarity >= 0.40:
                                # print(f"The similarity between {col1} and {col2} is {similarity}")                      
                                common_columns.append((col1, col2))
                                
                        elif all([bool(date_regex.match(str(val))) for val in df2[col2]]): 
                            # s = SequenceMatcher(None,col2,col1)
                            # similarity = s.ratio()
                            # sim = round(similarity,2)
                            # if similarity >= 0.90:
                            #     print(f"The similarity between {col1} and {col2} for date is {similarity}")
                            keyword_set_name = classify_column_name(col2, keyword_sets)
                            if('keyword'in keyword_set_name):
                                common_columns.append((date_dict_name[keyword_set_name], col2))
                            else:
                                print(keyword_set_name) 

                        elif  all([bool(integer_regex_district.match(str(val))) for val in df2[col2]]):
                            s = SequenceMatcher(None,col2,col1)
                            similarity = s.ratio()
                            sim = round(similarity,2)
                            if similarity >= 0.70:
                                # print(f"The similarity between {col1} and {col2} is {similarity}")
                                common_columns.append((col1, col2))                        
                        else:
                            common_columns.append((col1, col2))            
                    
            
            # print("these are common_columns",common_columns,file=logfile)

            
            #To remove dummy pairs in common columns
            seen_pairs = set()
            unique_common_columns = []

            # Iterate over each tuple in the list and check if it has already been seen
            for pair in common_columns:
                if pair not in seen_pairs:
                    unique_common_columns.append(pair)
                    seen_pairs.add(pair)
            
            # print("these are unique_common_columns",unique_common_columns)

            #Renaming the sheets as per master sheet & sorting by License id
            for i, j in unique_common_columns:
                df2 = df2.rename(columns={j:i})
            try:
                df_sorted = df2.sort_values(by='LICENCE_ID', ascending=True)
                dfo_list1.append(df_sorted)
            except Exception as e:
                now_lid_excep = datetime.now()
                timestamp_lid_execp = now_lid_excep.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
                print(f"{timestamp_lid_execp}-->The LicenseID naming of the column is missing in this file: {e}",file=logfile)
                crash=1
            
        #Merging the sheets based on License ID
        if(len(dfo_list1)>1):
            try:
                merged_df = reduce(lambda left, right: pd.merge(left, right, on=['LICENCE_ID']), dfo_list1)
                print("these  are merged",merged_df.columns)
                waste_columns=list(merged_df.columns)
            except Exception as e:
                now_lid_excep_any = datetime.now()
                timestamp_lid_execp_any = now_lid_excep_any.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
                print(f"{timestamp_lid_execp_any}-->There is no named column LicenseID in one of the files: {e}",file=logfile)
                crash=1
        else:
            merged_df1 = df_sorted.copy()
            now_singlefile = datetime.now()
            timestamp_singlefile = now_singlefile.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
            print(f"{timestamp_singlefile}-->these  are renamed columns of single file",list(merged_df1.columns),file=logfile)
            waste_columns=list(merged_df1.columns)       
        # print("these  are waste",waste_columns)
        if(crash!=1):
            #Removing the duplicate columns in sheet ex: district_x,district_y,District
            underscore_strings = [string for string in waste_columns if re.search(r'_\w$', string)]
            useless_columns=[]
            if(len(underscore_strings)!=0):
                for l in underscore_strings:
                    if '_x' in l:
                        original_string = l
                        substring_to_remove = "_x"
                        modified_string = original_string[:original_string.index(substring_to_remove)] + original_string[original_string.index(substring_to_remove) + len(substring_to_remove):] if substring_to_remove in original_string else original_string
                        for k in waste_columns:
                            if modified_string == k:
                                useless_columns.append(l)
                            else:
                                merged_df1=merged_df.rename(columns={l:modified_string})
                    else:
                        useless_columns.append(l)
            else:            
                if(len(dfo_list1)>1):
                    merged_df1 = merged_df.copy()
                else:
                    merged_df1 = df_sorted.copy()

            merged_clean = merged_df1.drop(columns=useless_columns)
            #Check wether our master(dfo master) columns are present in slave(dfo sheets) columns or not 
            slave_list = list(merged_clean.columns)
            fixed_columns=["LIC_GEAR_DESC","GEAR_CODE","DISTRICT","PROVINCE","LIC_AREA_DESC","LIC_SPC_DESC","LIC_TYPE_DESC","DFO Region","Corporation",'Time stamp']
            master = df1.drop(fixed_columns,axis=1)
            master_list = list(master.columns)
            missing_columns_merged_clean = []
            new_columns_or_differentnamesofcolumns = []
            #for identifying data columns which are not in master sheet
            for newitem in slave_list:
                if newitem not in master_list:
                    new_columns_or_differentnamesofcolumns.append(newitem)

            if(len(new_columns_or_differentnamesofcolumns)!=0):
                alien_columns=[]
                for commonitem in new_columns_or_differentnamesofcolumns:
                    if commonitem not in fixed_columns:
                        alien_columns.append(commonitem)
                        now_newcol = datetime.now()
                        timestamp_newcol = now_newcol.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
                        print(f"{timestamp_newcol}-->These are new data columns or rename these columns as per our master sheet",alien_columns)
                merged_clean = merged_clean.drop(columns=new_columns_or_differentnamesofcolumns)
                slave_list = list(merged_clean.columns)

            #for identifying data columns which are important & are they present in master sheet
            for item in master_list:
                if item not in slave_list:
                    missing_columns_merged_clean.append(item)

            if(len(missing_columns_merged_clean)== 0):
                columns_to_drop_for_analysis = []
                # merged_clean["DFO Region"]='Maritimes'
            
                merged_clean['Time stamp']=datetime.now()
                columns_to_keep_for_analysis = ['LICENCE_ID',"LIC_GEAR_DESC","GEAR_CODE","DISTRICT","PROVINCE","LIC_AREA_DESC","LIC_SPC_DESC","LIC_TYPE_DESC","DFO Region","Corporation",'Time stamp']
                for keep in df1.columns:
                    if keep not in columns_to_keep_for_analysis:
                        columns_to_drop_for_analysis.append(keep)
                # df_dummy =(df1.head(35)).copy()
                df_dummy = df1.copy()        
                test_filling = df_dummy.drop(columns=columns_to_drop_for_analysis,axis=1)
                test_filling_sorting = test_filling.sort_values(by=['LICENCE_ID','Time stamp'], ascending=True)
                test_filling_latestrecords = test_filling_sorting.drop_duplicates(subset=['LICENCE_ID'],keep ='last')
                test_filling_notimestamp = test_filling_latestrecords.drop(columns=['Time stamp'],axis=1)
                merged_clean_with_fixedfields = test_filling_notimestamp.merge(merged_clean,on=['LICENCE_ID'])
                merged_clean["Corporation"] = merged_clean_with_fixedfields['FIRSTNAME'].apply(lambda x: "Yes" if pd.isna(x) else "No")
                # print(merged_clean_with_fixedfields)
                # merged_clean_with_fixedfields.to_excel("chudali.xlsx")
                test_final = pd.concat([df_dummy,merged_clean_with_fixedfields],axis=0,ignore_index=True)
                test_sorted = test_final.sort_values(by=['LICENCE_ID','Time stamp'], ascending=True)
                test_sorted = test_sorted.replace({'******': np.nan})
                test_final = test_sorted.drop_duplicates(subset=test_sorted.columns.difference(['Time stamp']).tolist(), keep='first')
                # print(test_final)
                now = datetime.now()
                timestamp = now.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
                # test_final['Time stamp'] = pd.to_datetime(test_final['Time stamp'])
                threshold = now - dt.timedelta(minutes=10)
                result_zoho = test_final[test_final['Time stamp'] >= threshold]
                result_zoho.to_excel(f"static/media/output_files/result_zoho_{timestamp}.xlsx",index=False)
                test_final.to_excel(f"static/media/output_files/DFOMaster_updated_{timestamp}.xlsx",index=False)
                message = "Programme is successfully executed"
                filename_generated_master =f"DFOMaster_updated_{timestamp}"
                filename_generated_zoho=f"result_zoho_{timestamp}"
            else:
                now_misscol = datetime.now()
                timestamp_misscol = now_misscol.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
                empty_df = pd.DataFrame()
                empty_df.to_excel(f"static/media/output_files/empty_{timestamp_misscol}.xlsx")
                print(f"{timestamp_misscol}-->These columns data is missing from DFO sheets",missing_columns_merged_clean,file=logfile)
                message = "Programme is hindered"
                filename_generated_master =f"empty_{timestamp_misscol}"
                filename_generated_zoho=f"result_zoho_{timestamp_misscol}"
        else:
            now_prgcrash = datetime.now()
            timestamp_prgcrash = now_prgcrash.strftime("%d-%b-%Y_%Hhrs-%Mms-%Ss")
            empty_df = pd.DataFrame()
            empty_df.to_excel(f"static/media/output_files/empty_{timestamp_prgcrash}.xlsx")           
            message = "Programme crashed"
            filename_generated_master =f"empty_{timestamp_prgcrash}"
            filename_generated_zoho =f"empty_{timestamp_prgcrash}"
            print(f"{timestamp_prgcrash}-->programme crashed",file=logfile)
        # sys.stdout.close() 
    return message,filename_generated_master,filename_generated_zoho

