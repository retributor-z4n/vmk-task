import pandas as pd
from datetime import datetime





def merge_all():
    files = [
        "./features/voice_features.csv",
        "./features/sms_features.csv",
        "./features/data_features.csv",
        "./features/subscriptions_features.csv",
        "./features/recharge_features.csv"
    ]


    with open("./features/voice_features.csv", "r") as myvoice, open("./features/sms_features.csv", "r") as mysms, open("./features/data_features.csv", "r") as mydatause, open("./features/subscriptions_features.csv", "r") as mysubscriptions, open("./features/recharge_features.csv", "r") as myrecharge, open("./features/all_features_final.csv", "w") as myfinalfeatures:
        count = 0
                    

        while True:
            count += 1
            if count % 1000000 == 0:
                print(f"Processed {count // 1000000} million rows...")


            line1 = myvoice.readline()
            line2 = mysms.readline()
            line3 = mydatause.readline()
            line4 = mysubscriptions.readline()
            line5 = myrecharge.readline()

            if not line1:
                break


            r1 = line1.strip().split(",")
            r2 = line2.strip().split(",")
            r3 = line3.strip().split(",")
            r4 = line4.strip().split(",")
            r5 = line5.strip().split(",")

            
            combined_record = r1 + r2[2:] + r3[2:] + r4[2:] + r5[2:]

            print(",".join(combined_record),file = myfinalfeatures)
            



            



            
       


if __name__ == "__main__":
    print(datetime.now())
    merge_all()
    print(datetime.now())