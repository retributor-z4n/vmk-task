from datetime import datetime, timedelta


def sms_data(account_nums):
    sms_dailydata = {}
    sms_accounts_recorddates = {}
    with open("./aggregation/aggregated_sms.csv", "r") as mysms:
        _ = next(mysms)
        for line in mysms:
            record = line.strip().split(",")

            accountnum = record[0]
            recorddate = (datetime.strptime(record[1], "%Y-%b-%d")).date()

            if accountnum not in sms_accounts_recorddates:
                sms_accounts_recorddates[accountnum] = set()
            sms_accounts_recorddates[accountnum].add(recorddate)

            traffic_national_international = record[2]
            traffic_onnet_offnet = record[3].lower()

            total_sms = int(float(record[4]))
            total_sms_counter = float(record[5])
            total_sms_payg = int(float(record[6]))
            total_revenue_gross_payg = float(record[7])

            if accountnum not in sms_dailydata:
                sms_dailydata[accountnum] = {}
            if recorddate not in sms_dailydata[accountnum]:
                sms_dailydata[accountnum][recorddate] = [0] * 14

            sms_dailydata[accountnum][recorddate][0] += total_sms
            sms_dailydata[accountnum][recorddate][1] += total_sms_counter
            sms_dailydata[accountnum][recorddate][2] += total_sms_payg
            sms_dailydata[accountnum][recorddate][3] += total_revenue_gross_payg

            # array_of_form = [
            # total_sms => (0),
            # total_sms_counter => (1),
            # total_sms_payg => (2),
            # total_revenue_gross_payg => (3),
            # total_num_international_sms => (4),
            # total_num_national_sms => (5),
            # total_num_roaming_sms => (6),
            # total_num_offnet_sms=> (7),
            # total_num_onnet_sms => (8),
            # ]

            if traffic_national_international == "International":
                sms_dailydata[accountnum][recorddate][4] += total_sms

            elif traffic_national_international == "National":
                sms_dailydata[accountnum][recorddate][5] += total_sms

            elif traffic_national_international == "Roaming":
                sms_dailydata[accountnum][recorddate][6] += total_sms

            if "off-net" in traffic_onnet_offnet:
                sms_dailydata[accountnum][recorddate][7] += total_sms

            elif "on-net" in traffic_onnet_offnet:
                sms_dailydata[accountnum][recorddate][8] += total_sms

    return (sms_dailydata, sms_accounts_recorddates)


def generating_features(
    account_nums, sms_dailydata, sms_accounts_recorddates, num_days_lookback
):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first

    with open("./features/sms_features.csv", "w") as myfile:
        print(
            "account_num,context_date,total_sms,total_sms_counter,total_sms_payg,total_revenue_gross_payg,total_num_international_sms,total_num_national_sms,total_num_roaming_sms,total_num_offnet_sms,total_num_onnet_sms",
            file=myfile,
        )

        while dateincrementer <= context_date_last:
            lookback_start = dateincrementer - timedelta(
                num_days_lookback 
            )  # inclusive
            lookback_end = dateincrementer - timedelta(1)
            for account_num in account_nums:

                # --*added*--later--down
                if account_num not in sms_dailydata:
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(9):
                        output_str += ""
                        if i != 8:
                            output_str += ","

                    print(output_str, file=myfile)
                # --*added*--later--up

                
                elif account_num in sms_dailydata:
                    concentrated_features_for_lookback = [0] * 9
                    for record_date in sms_accounts_recorddates[account_num]:
                        if lookback_start <= record_date <= lookback_end:
                            for i in range(9):
                                concentrated_features_for_lookback[i] += sms_dailydata[
                                    account_num
                                ][record_date][i]
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(9):
                        output_str += f"{concentrated_features_for_lookback[i]}"
                        if i != 8:
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

    sms_dailydata, sms_accounts_recorddates = sms_data(account_nums)

    generating_features(account_nums, sms_dailydata, sms_accounts_recorddates, 30)
    print(f"end: {datetime.now()}")
