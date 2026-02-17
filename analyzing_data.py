from datetime import datetime



def filtering_dump():
    sub_dump_filtered = {}
    with open(f"../../Downloads/OneDrive_1_9-2-2026/CVM_mViva_BASE_20240109.csv", "r") as myfile:
        for line in myfile:
            record = line.strip().split(",")
            acc_num = record[0]
            last_subs_date = record[16]
            last_plan_valid = record[17]
            actvtn_date = record[22]
            last_recharge_date = record[27]
            last_voice_ex_cf_date = record[28]
            last_data_date = record[29]
            last_activation_date = record[30]
            

            cols_array = [
                    last_subs_date,
                    last_plan_valid,
                    actvtn_date,
                    last_recharge_date,
                    last_voice_ex_cf_date,
                    last_data_date,
                    last_activation_date
            ]
            sub_dump_filtered[acc_num] = {}
            for i in range(0,7):
                sub_dump_filtered[acc_num][i] = cols_array[i]
            
    with open("./filtered_dump.csv","w") as myfile:
        print("accountnum,Last_subscription_date,Last_plan_validity,Activationdate,Last_recharge_date ,Last_voice_ex_cf_date ,Last_data_date ,Last_activity_date",file = myfile)
        for acc_num in sub_dump_filtered:
            print(f"{acc_num},{sub_dump_filtered[acc_num][0]},{sub_dump_filtered[acc_num][1]},{sub_dump_filtered[acc_num][2]},{sub_dump_filtered[acc_num][3]},{sub_dump_filtered[acc_num][4]},{sub_dump_filtered[acc_num][5]},{sub_dump_filtered[acc_num][6]}",file = myfile)


def view_data_types(file, cols):
    with open(f"../../Downloads/OneDrive_1_9-2-2026/{file}", "r") as myfile:
        numrecords = 0

        for line in myfile:
            if numrecords == 5:
                break

            record = line.strip().split(",")

            for indx in range(len(record)):
                print(f"{cols[indx]} =====>> {record[indx]}\n")
            numrecords += 1
            print(".............*****.............")





def different_types_columns_voice():
    dates = set()
    call_types = set()
    service_groups = set()
    service_subtypes = set()
    traffics_national_international = set()
    traffics_onnet_offnet = set()
    traffics_country = set()

    with open(
        f"../../Downloads/OneDrive_1_9-2-2026/CVM_mViva_Calls_2023_Q3_Q4.csv", "r"
    ) as myfile:
        for line in myfile:
            record = line.strip().split(",")
            dates.add(record[2])
            call_types.add(record[3])
            service_groups.add(record[4])
            service_subtypes.add(record[5])
            traffics_national_international.add(record[6])
            traffics_onnet_offnet.add(record[7])
            traffics_country.add(record[8])
    print(call_types)
    print(dates)
    print(service_groups)
    print(service_subtypes)
    print(traffics_national_international)
    print(traffics_onnet_offnet)
    print(traffics_country)


def diff_type_cols_sms():
    ad_calltypes = set()                    
    service_groups = set()
    service_subtypes = set()                
    traffics_national_international = set()
    traffics_onnet_offnet = set() 
    traffics_country = set()             
    
    with open(f"../../Downloads/OneDrive_1_9-2-2026/CVM_mViva_SMS_2023_Q3_Q4.csv", "r") as myfile:
        for line in myfile:
            record = line.strip().split(",")
            ad_calltypes.add(record[3])
            service_groups.add(record[4])
            service_subtypes.add(record[5])
            traffics_national_international.add(record[6])
            traffics_onnet_offnet.add(record[7])
            traffics_country.add(record[8])

    print(ad_calltypes)
    print(service_groups)
    print(service_subtypes)
    print(traffics_national_international)
    print(traffics_onnet_offnet)
    print(traffics_country)

def diff_type_cols_data():
                       
    service_groups = set()
    service_subtypes = set()                
    traffics_national_international = set()
    traffics_onnet_offnet = set() 
    traffics_country = set()             
    
    with open(f"../../Downloads/OneDrive_1_9-2-2026/CVM_mViva_DATA_2023_Q3_Q4.csv", "r") as myfile:
        for line in myfile:
            record = line.strip().split(",")
            
            service_groups.add(record[3])
            service_subtypes.add(record[4])
            traffics_national_international.add(record[5])
            traffics_onnet_offnet.add(record[6])
            traffics_country.add(record[7])

   
    print(service_groups)
    print(service_subtypes)
    print(traffics_national_international)
    print(traffics_onnet_offnet)
    print(traffics_country)


def diff_type_cols_recharges():
    dsu_subscription_type_names = set()
    brands = set()
    adjustmentreasonnames = set()   
    categories_2 = set()

    with open(f"../../Downloads/OneDrive_1_9-2-2026/CVM_mViva_Recharges_Q3_Q4.csv", "r") as myfile:
        for line in myfile:
            record = line.strip().split(",")
            
            dsu_subscription_type_names.add(record[3])
            brands.add(record[4])
            adjustmentreasonnames.add(record[5])
            categories_2.add(record[6])
            

   
    print(dsu_subscription_type_names)
    print(brands)
    print(adjustmentreasonnames)
    print(categories_2)
   


    

if __name__ == "__main__":
    #filtering_dump()
    #different_types_columns_voice()
    #diff_type_cols_sms()
    #diff_type_cols_data()
    diff_type_cols_recharges()
