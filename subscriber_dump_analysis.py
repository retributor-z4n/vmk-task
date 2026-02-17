from datetime import datetime


def nummsisdns(file, msisdncol):
    linecount = 0

    accountnums = set()
    msisdns = set()
    with open(f"../../Downloads/OneDrive_1_9-2-2026/{file}", "r") as myfile:
        for line in myfile:
            record = line.strip().split(",")
            linecount += 1

            if record[0] in accountnums:
                print(record[0])
            accountnums.add(record[0])
            msisdns.add(record[msisdncol])

    print(f"Total Line Count {linecount}")
    print(f"Total accountnums count {len(accountnums)}")
    print(f"Total msisdns count {len(msisdns)}")


if __name__ == "__main__":

    #files = [
    #    "CVM_mViva_BASE_20240109.csv",
    #    "CVM_mViva_DATA_2023_Q3_Q4.csv",
    #    "CVM_mViva_SMS_2023_Q3_Q4.csv",
    #    "CVM_mViva_Calls_2023_Q3_Q4.csv",
    #    "CVM_mViva_Recharges_Q3_Q4.csv",
    #]

    files = [
        "CVM_mViva_BASE_20240109.csv"
    ]
    for file in files:
        nummsisdns(file, 1)
        print("----*----")
    #nummsisdns("CVM_mViva_Subscription_Q3_Q4_new.csv", 2)
