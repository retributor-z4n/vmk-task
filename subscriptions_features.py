from datetime import datetime, timedelta


def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except (Exception ):
        return None  
def subscriptions_data():
    #{ account_num: [(start, end, MONTHLY_price), (start, end, mONTHly_price)] }
    subscriptions_dailydata = {}
    subscriptions_accounts_recorddates = {} #their_start_dates
    with open("./aggregation/trimmed_subscriptions.csv", "r") as mysubscriptions:
        _ = next(mysubscriptions)

        for line in mysubscriptions:
            record = line.strip().split(",")

            accountnum = record[0]
            sub_start_date = parse_date(record[5])
            sub_end_date = parse_date(record[6])
            
            recorddate = sub_start_date
            plan_commitment = int(float(record[11]))
            if sub_end_date is None:
                sub_end_date = sub_start_date + timedelta(days=plan_commitment*30)


            if accountnum not in subscriptions_accounts_recorddates:
                subscriptions_accounts_recorddates[accountnum] = set()
            subscriptions_accounts_recorddates[accountnum].add(sub_start_date)

            monthly_price = float(record[8])
            # plan_valdty = int(float(record[10]))

            if accountnum not in subscriptions_dailydata:
                subscriptions_dailydata[accountnum] = []
            subscriptions_dailydata[accountnum].append((sub_start_date, sub_end_date, monthly_price,plan_commitment))
            
            
    return (subscriptions_dailydata, subscriptions_accounts_recorddates)

def generating_features(
    account_nums, subscriptions_dailydata, subscriptions_accounts_recorddates, num_days_lookback
):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first

    with open("./features/subscriptions_features.csv", "w") as myfile:
        print(
            "account_num,context_date,total_monthly_price_active",
            file=myfile,
        )

        while dateincrementer <= context_date_last:
            lookback_start = dateincrementer - timedelta(
                num_days_lookback 
            )  # inclusive
            lookback_end = dateincrementer - timedelta(1)

            for account_num in account_nums:
                # --*added*--later--down
                if account_num not in subscriptions_dailydata:
                    output_str = f"{account_num},{dateincrementer},"

                    print(output_str, file=myfile)
                # --*added*--later--up


                elif account_num in subscriptions_dailydata:
                    total_active_price = 0

                    for sub_plans in subscriptions_dailydata[account_num]:
                        start, end, price, plan_commitment = sub_plans
                        # if end is None:
                            # end = start + timedelta(days=plan_commitment*30)
                            #if start <= lookback_end:
                            #    total_active_price += price


                        if start <= lookback_end and end >= lookback_start:
                            total_active_price += price
                    
                    
                    output_str = f"{account_num},{dateincrementer},{total_active_price}"
                    print(output_str, file=myfile)
            dateincrementer += timedelta(days=1)


def accountnum_subscriptions_details(account_nums,subscriptions_dailydata):
    with open("./features/subscription_details.csv","w") as mysub:
        print(
            "accountnum,subscription_start,subscription_end,MONTHLY_price,plan_commitment_months",
            file=mysub
        )
        for account_num in account_nums:
            if account_num in subscriptions_dailydata:
                for record in subscriptions_dailydata[account_num]:
                    print(f"{account_num},{record[0]},{record[1]},{record[2]},{record[3]}",file = mysub)

    





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
    subscriptions_dailydata, subscriptions_accounts_recorddates = subscriptions_data()

    generating_features(account_nums, subscriptions_dailydata, subscriptions_accounts_recorddates, 30)
    accountnum_subscriptions_details(account_nums,subscriptions_dailydata)
    print(f"end: {datetime.now()}")