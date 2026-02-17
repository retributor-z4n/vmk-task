from datetime import datetime, timedelta


def loadall_accountnums():
    account_nums = {}
    with open("./reports/account_nums.csv") as myaccounts:
        for line in myaccounts:
            account_nums[line.strip()] = ""
    return account_nums


def load_subdetails():
    subscription_details = {}
    with open("./features/subscription_details.csv") as mysubdetails:
        _ = next(mysubdetails)
        for line in mysubdetails:

            record = line.strip().split(",")
            accountnum = record[0]
            subscription_start = datetime.strptime(record[1], "%Y-%m-%d").date()
            subscription_end = datetime.strptime(record[2], "%Y-%m-%d").date()
            monthly_price = float(record[3])
            plan_commitment = int(float(record[4]))

            if accountnum not in subscription_details:
                subscription_details[accountnum] = []
            subscription_details[accountnum].append(
                (subscription_start, subscription_end, monthly_price, plan_commitment)
            )
    return subscription_details


def generatingLabels(numdays_label_window, account_nums, subscription_details):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first
    with open(
        f"./labels/subscriptions_labels_{numdays_label_window}.csv", "w"
    ) as mylabels:
        print(
            f"account_num,context_date,label{numdays_label_window}_days",
            file=mylabels,
        )
        while dateincrementer <= context_date_last:

            label_window_start = dateincrementer + timedelta(days=1)  # inclusive
            label_window_end = dateincrementer + timedelta(
                days=numdays_label_window
            )  # inclusive

            for account_num in account_nums:
                if account_num not in subscription_details:
                    print(
                        f"{account_num},{dateincrementer},-3", file=mylabels
                    )  # -3 means not even present in the subscription data source...
                    continue

                # if he buys a plan in next 7 days and comparing that to the previous purchased plan
                planexpired_in_label_window = False
                for idx in range(len(subscription_details[account_num])):
                    if planexpired_in_label_window == True:
                        break
                    (
                        subscription_start,
                        subscription_end,
                        monthly_price,
                        plan_commitment,
                    ) = subscription_details[account_num][idx]
                    if label_window_start <= subscription_end <= label_window_end:
                        planexpired_in_label_window = True

                        if idx < len(subscription_details[account_num]) - 1:
                            monthly_price_previous = monthly_price
                            monthly_price_next = subscription_details[account_num][
                                idx + 1
                            ][2]
                            if monthly_price_previous > 0:
                                change_in_price = (
                                    monthly_price_previous - monthly_price_next
                                )
                                if (change_in_price / monthly_price_previous) > 0.10:
                                    print(
                                        f"{account_num},{dateincrementer},1",
                                        file=mylabels,
                                    )  # 1 means downgrade more than 10%
                                else:
                                    print(
                                        f"{account_num},{dateincrementer},0",
                                        file=mylabels,
                                    )  # 0 means no downgrade more than 10%
                            else:
                                print(
                                    f"{account_num},{dateincrementer},0", file=mylabels
                                )  # there can be no downgrade from 0
                        else:
                            print(
                                f"{account_num},{dateincrementer},-1", file=mylabels
                            )  # -1 means no plan bought after

                if not planexpired_in_label_window:
                    print(
                        f"{account_num},{dateincrementer},-2", file=mylabels
                    )  # -2 means no expiry of the  plans of this particular accountnum in this label window
            dateincrementer += timedelta(days=1)


if __name__ == "__main__":
    account_nums = loadall_accountnums()
    subscription_details = load_subdetails()
    print(datetime.now())
    generatingLabels(7, account_nums, subscription_details)
    print(datetime.now())
    generatingLabels(15, account_nums, subscription_details)
    print(datetime.now())
    generatingLabels(30, account_nums, subscription_details)
    
