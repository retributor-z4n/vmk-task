from datetime import datetime, timedelta


def voice_data(account_nums):
    voice_dailydata = {}
    voice_accounts_recorddates = {}
    with open("./aggregation/aggregated_voice.csv", "r") as myvoice:
        _ = next(myvoice)
        for line in myvoice:
            record = line.strip().split(",")

            accountnum = record[0]
            recorddate = (datetime.strptime(record[1], "%Y-%b-%d")).date()

            if accountnum not in voice_accounts_recorddates:
                voice_accounts_recorddates[accountnum] = set()
            voice_accounts_recorddates[accountnum].add(recorddate)

            traffic_national_international = record[2]
            traffic_onnet_offnet = record[3].lower()

            ad_total_duration_actual = float(record[4])
            ad_total_duration = float(record[5])
            ad_total_quantity = int(float(record[6]))
            ad_total_duration_counter = float(record[7])
            ad_total_duration_payg = float(record[8])
            ad_total_revenue_received = float(record[9])

            if accountnum not in voice_dailydata:
                voice_dailydata[accountnum] = {}
            if recorddate not in voice_dailydata[accountnum]:
                voice_dailydata[accountnum][recorddate] = [0] * 21

            voice_dailydata[accountnum][recorddate][0] += ad_total_duration_actual
            voice_dailydata[accountnum][recorddate][1] += ad_total_duration
            voice_dailydata[accountnum][recorddate][2] += ad_total_quantity
            voice_dailydata[accountnum][recorddate][3] += ad_total_duration_counter
            voice_dailydata[accountnum][recorddate][4] += ad_total_duration_payg
            voice_dailydata[accountnum][recorddate][5] += ad_total_revenue_received

            # array_of_form = [        
            # ad_total_duration_actual => (0),
            # ad_total_duration => (1),
            # ad_total_quantity => (2),
            # ad_total_duration_counter => (3),
            # ad_total_duration_payg => (4),
            # ad_total_revenue_received => (5),
            # total_num_international_calls => (6),
            # total_international_drtn => (7),
            # total_international_revenue => (8),
            # total_num_national_calls => (9),
            # total_national_drtn => (10),
            # total_national_revenue => (11),
            # total_roaming_calls => (12),
            # total_roaming_drtn => (13),
            # total_roaming_revenue => (14),
            # total_num_offnet_calls => (15),
            # total_offnet_drtn => (16),
            # total_offnet_revenue => (17),
            # total_num_onnet_calls => (18),
            # total_onnet_drtn => (19),
            # total_onnet_revenue => (20),
            # ]

            if traffic_national_international == "International":
                voice_dailydata[accountnum][recorddate][6] += ad_total_quantity
                voice_dailydata[accountnum][recorddate][7] += ad_total_duration
                voice_dailydata[accountnum][recorddate][8] += ad_total_revenue_received

            elif traffic_national_international == "National":
                voice_dailydata[accountnum][recorddate][9] += ad_total_quantity
                voice_dailydata[accountnum][recorddate][10] += ad_total_duration
                voice_dailydata[accountnum][recorddate][11] += ad_total_revenue_received

            elif traffic_national_international == "Roaming":
                voice_dailydata[accountnum][recorddate][12] += ad_total_quantity
                voice_dailydata[accountnum][recorddate][13] += ad_total_duration
                voice_dailydata[accountnum][recorddate][14] += ad_total_revenue_received

            if "off-net" in traffic_onnet_offnet:
                voice_dailydata[accountnum][recorddate][15] += ad_total_quantity
                voice_dailydata[accountnum][recorddate][16] += ad_total_duration
                voice_dailydata[accountnum][recorddate][17] += ad_total_revenue_received

            elif "on-net" in traffic_onnet_offnet:
                voice_dailydata[accountnum][recorddate][18] += ad_total_quantity
                voice_dailydata[accountnum][recorddate][19] += ad_total_duration
                voice_dailydata[accountnum][recorddate][20] += ad_total_revenue_received

    return (voice_dailydata, voice_accounts_recorddates)


def generating_features(
    account_nums, voice_dailydata, voice_accounts_recorddates, num_days_lookback
):
    context_date_first = datetime(2023, 7, 31).date()
    context_date_last = datetime(2023, 12, 1).date()

    dateincrementer = context_date_first

    with open("./features/voice_features.csv", "w") as myfile:
        print(
            "account_num,context_date,total_duration_actual,total_duration,total_quantity,total_duration_counter,total_duration_payg,total_revenue_received,total_num_international_calls,total_international_duration,total_international_revenue,total_num_national_calls,total_national_duration,total_national_revenue,total_roaming_calls,total_roaming_duration,total_roaming_revenue,total_num_offnet_calls,total_offnet_duration,total_offnet_revenue,total_num_onnet_calls,total_onnet_duration,total_onnet_revenue",
            file=myfile,
        )

        while dateincrementer <= context_date_last:
            lookback_start = dateincrementer - timedelta(
                num_days_lookback 
            )  # inclusive
            lookback_end = dateincrementer - timedelta(1)
            for account_num in account_nums:
                # --*added*--later--down
                if account_num not in voice_dailydata:
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(21):
                        output_str += ""
                        if i != 20:
                            output_str += ","

                    print(output_str, file=myfile)
                # --*added*--later--up


                elif account_num in voice_dailydata:
                    concentrated_features_for_lookback = [0] * 21
                    for record_date in voice_accounts_recorddates[account_num]:
                        if lookback_start <= record_date <= lookback_end:
                            for i in range(21):
                                concentrated_features_for_lookback[
                                    i
                                ] += voice_dailydata[account_num][record_date][i]
                    output_str = f"{account_num},{dateincrementer},"
                    for i in range(21):
                        output_str += f"{concentrated_features_for_lookback[i]}"
                        if i != 20:
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

    voice_dailydata, voice_accounts_recorddates = voice_data(account_nums)

    generating_features(account_nums, voice_dailydata, voice_accounts_recorddates, 30)
    print(f"end: {datetime.now()}")
