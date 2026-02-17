from datetime import datetime, timedelta


def recharge_data(account_nums):
    recharge_dailydata = {}
    recharge_accounts_recorddates = {}
    with open("./aggregation/trimmed_recharges.csv", "r") as myrecharge:
        _ = next(myrecharge)
        for line in myrecharge:
            record = line.strip().split(",")
            accountnum = record[0]
            record_date = datetime.strptime(record[1],"%Y-%m-%d").date()
            if accountnum not in recharge_accounts_recorddates:
                recharge_accounts_recorddates[accountnum] = set()
            recharge_accounts_recorddates[accountnum].add(record_date)
        
            brand = record[2]
            category_2 = record[3]        
            amount = float(record[4])                 
            postbalance = float(record[5])
            prevbalance = postbalance - amount

            if accountnum not in recharge_dailydata:
                recharge_dailydata[accountnum] = {}

            if record_date not in recharge_dailydata[accountnum]:
                recharge_dailydata[accountnum][record_date] = [0] * 4
            recharge_dailydata[accountnum][record_date][0] += amount
            recharge_dailydata[accountnum][record_date][1] += postbalance
            recharge_dailydata[accountnum][record_date][2] += prevbalance
       
            recharge_dailydata[accountnum][record_date][3] += 1 #num_recharges

    return (recharge_dailydata, recharge_accounts_recorddates)
        
    

def writting_features(
    account_nums, recharge_dailydata, recharge_accounts_recorddates, num_days_lookback
):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first

    with open("./features/recharge_features.csv", "w") as myfile:
        print(
            "account_num,context_date,totalamount,postbalance,prevbalance,number_ofrecharges,average_postbalance,average_recharge_amount",
            file=myfile,
        )

        while dateincrementer <= context_date_last:
            lookback_start = dateincrementer - timedelta(
                num_days_lookback 
            )  # inclusive
            lookback_end = dateincrementer - timedelta(1)
            for account_num in account_nums:
                # --*added*--later--down
                if account_num not in recharge_dailydata:
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(4):
                        output_str += ","
                        
                    output_str += ",,"

                    print(output_str, file=myfile)
                # --*added*--later--up

                elif account_num in recharge_dailydata:
                    concentrated_features_for_lookback = [0] * 4
                    for record_date in recharge_accounts_recorddates[account_num]:
                        if lookback_start <= record_date <= lookback_end:
                            for i in range(4):
                                concentrated_features_for_lookback[i] += recharge_dailydata[
                                    account_num
                                ][record_date][i]
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(4):
                        output_str += f"{concentrated_features_for_lookback[i]}"
                                           
                        output_str += ","
                    if(concentrated_features_for_lookback[3] != 0):
                        output_str += f"{concentrated_features_for_lookback[1]/concentrated_features_for_lookback[3]},"
                        output_str += f"{concentrated_features_for_lookback[0]/concentrated_features_for_lookback[3]}"
                    else:
                        output_str += ","



                    print(output_str, file=myfile)
            dateincrementer += timedelta(days=1)


if __name__ == "__main__":
    print(f"Start: {datetime.now()}")
    # account_nums = set()

    # with open("./reports/account_nums.csv") as acc_nums:
    #     for line in acc_nums:
    #         account_nums.add(line.strip())

    account_nums = {}

    with open("./reports/account_nums.csv") as acc_nums:
        for line in acc_nums:
            account_nums[line.strip()] = ""

    recharge_dailydata, recharge_accounts_recorddates = recharge_data(account_nums)

    writting_features(account_nums, recharge_dailydata, recharge_accounts_recorddates, 30)
    print(f"end: {datetime.now()}")




