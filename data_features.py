from datetime import datetime, timedelta


def datause_data(account_nums):
    datause_dailydata = {}
    datause_accounts_recorddates = {}
    with open("./aggregation/aggregated_data.csv", "r") as mydatause:
        _ = next(mydatause)
        for line in mydatause:
            record = line.strip().split(",")

            accountnum = record[0]
            recorddate = (datetime.strptime(record[1], "%Y-%b-%d")).date()

            if accountnum not in datause_accounts_recorddates:
                datause_accounts_recorddates[accountnum] = set()
            datause_accounts_recorddates[accountnum].add(recorddate)

            traffic_national_international = record[2]
            traffic_onnet_offnet = record[3].lower()

            total_data_volume_mb = float(record[4])
            total_data_volume_counter_mb = float(record[5])
            total_revenue_gross_payg = float(record[6])

            if accountnum not in datause_dailydata:
                datause_dailydata[accountnum] = {}

            if recorddate not in datause_dailydata[accountnum]:
                datause_dailydata[accountnum][recorddate] = [0] * 13

            datause_dailydata[accountnum][recorddate][0] += total_data_volume_mb 
            datause_dailydata[accountnum][recorddate][1] += total_data_volume_counter_mb
            datause_dailydata[accountnum][recorddate][2] += total_revenue_gross_payg
            
            if traffic_national_international == "International":
                datause_dailydata[accountnum][recorddate][3] += total_data_volume_mb
                datause_dailydata[accountnum][recorddate][4] += total_data_volume_counter_mb
            elif traffic_national_international == "National":
                datause_dailydata[accountnum][recorddate][5] += total_data_volume_mb
                datause_dailydata[accountnum][recorddate][6] += total_data_volume_counter_mb

            elif traffic_national_international == "Roaming":
                datause_dailydata[accountnum][recorddate][7] += total_data_volume_mb
                datause_dailydata[accountnum][recorddate][8] += total_data_volume_counter_mb


            if "off-net" in traffic_onnet_offnet:
                datause_dailydata[accountnum][recorddate][9] += total_data_volume_mb
                datause_dailydata[accountnum][recorddate][10] += total_data_volume_counter_mb

            elif "on-net" in traffic_onnet_offnet:
                datause_dailydata[accountnum][recorddate][11] += total_data_volume_mb
                datause_dailydata[accountnum][recorddate][12] += total_data_volume_counter_mb
    
    return (datause_dailydata, datause_accounts_recorddates)

def generating_features(
    account_nums, datause_dailydata, datause_accounts_recorddates, num_days_lookback
):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first

    with open("./features/data_features.csv", "w") as myfile:
        print(
            "account_num,context_date,total_data_volume_mb,total_data_volume_counter_mb,total_revenue_gross_payg,total_data_volume_mb_international,total_data_volume_counter_mb_international,total_data_volume_mb_national,total_data_volume_counter_mb_national,total_data_volume_mb_roaming,total_data_volume_counter_mb_roaming,total_data_volume_mb_offnet,total_data_volume_counter_mb_offnet,total_data_volume_mb_onnet,total_data_volume_counter_mb_onnet",
            file=myfile,
        )

        while dateincrementer <= context_date_last:
            lookback_start = dateincrementer - timedelta(
                num_days_lookback 
            )  # inclusive
            lookback_end = dateincrementer - timedelta(1)
            for account_num in account_nums:
                # --*added*--later--down
                if account_num not in datause_dailydata:
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(13):
                        output_str += ""
                        if i != 12:
                            output_str += ","

                    print(output_str, file=myfile)
                # --*added*--later--up


                elif account_num in datause_dailydata:
                    concentrated_features_for_lookback = [0] * 13
                    for record_date in datause_accounts_recorddates[account_num]:
                        if lookback_start <= record_date <= lookback_end:
                            for i in range(13):
                                concentrated_features_for_lookback[i] += datause_dailydata[
                                    account_num
                                ][record_date][i]
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(13):
                        output_str += f"{concentrated_features_for_lookback[i]}"
                        if i != 12:
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

    datause_dailydata, datause_accounts_recorddates = datause_data(account_nums)

    generating_features(account_nums, datause_dailydata, datause_accounts_recorddates, 30)
    print(f"end: {datetime.now()}")


