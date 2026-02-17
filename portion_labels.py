from datetime import datetime,timedelta


def allthebuyers(): #who bought some plan in the entire data source
    account_nums = set()
    #"CVM_mViva_BASE_20240109.csv"
    files = [
        "CVM_mViva_Subscription_Q3_Q4_new.csv"
    ]
    for file in files:
        with open(f"../../Downloads/OneDrive_1_9-2-2026/{file}", "r") as myfile:
            for line in myfile:
                record = line.strip().split(",")            
                account_nums.add(record[0])

    print(len(account_nums)) 

def allthedowngraders7days():
    downgraders = set()
    with open("./labels/subscriptions_labels_7.csv") as myfile:
        _ = next(myfile)

        for line in myfile:
            record = line.strip().split(",")   
          
            if(int(float(record[2])) == 1):
                downgraders.add(record[0])
    print(len(downgraders))

def allthedowngraders15days():
    downgraders = set()
    with open("./labels/subscriptions_labels_15.csv") as myfile:
        _ = next(myfile)

        for line in myfile:
            record = line.strip().split(",")
            if(int(float(record[2])) == 1):
                downgraders.add(record[0])
    print(len(downgraders))

def allthedowngraders30days():
    downgraders = set()
    with open("./labels/subscriptions_labels_30.csv") as myfile:
        _ = next(myfile)

        for line in myfile:
            record = line.strip().split(",")
            if(int(float(record[2])) == 1):
                downgraders.add(record[0])

    print(len(downgraders))

if __name__ == "__main__":
    allthebuyers()
    allthedowngraders7days()
    allthedowngraders15days()
    allthedowngraders30days()
