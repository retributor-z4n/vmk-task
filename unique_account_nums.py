from datetime import datetime



def all_account_nums():
    account_nums = set()
    #"CVM_mViva_BASE_20240109.csv"
    files = [
        "CVM_mViva_DATA_2023_Q3_Q4.csv",
        "CVM_mViva_SMS_2023_Q3_Q4.csv",
        "CVM_mViva_Calls_2023_Q3_Q4.csv",
        "CVM_mViva_Recharges_Q3_Q4.csv",
        "CVM_mViva_Subscription_Q3_Q4_new.csv"
    ]
    for file in files:
        with open(f"../../Downloads/OneDrive_1_9-2-2026/{file}", "r") as myfile:
            for line in myfile:
                record = line.strip().split(",")            
                account_nums.add(record[0])

    with open(f"./reports/account_nums.csv","w") as myfile:
        for account_num in account_nums:
            print(account_num,file = myfile)
    

if __name__ == "__main__":

    all_account_nums()
