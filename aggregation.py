from datetime import datetime
import pandas as pd


def load_df(file, columnlist):
    loaded_df = pd.read_csv(
        f"../../Downloads/OneDrive_1_9-2-2026/{file}", header=None, names=columnlist
    )
    return loaded_df


def aggregate_df(df, to_grp_clmns, agg_cols, outputfile):
    aggregated_df = df.groupby(to_grp_clmns).agg(agg_cols)
    aggregated_df.to_csv(f"./aggregation/{outputfile}")


if __name__ == "__main__":
    voice_cols = [
        "accountnum",
        "Msisdn",
        "The_date",
        "Call_type",
        "Service_group",
        "Service_subtype",
        "Traffic_national_international",
        "Traffic_onnet_offnet",
        "Traffic_country",
        "Ad_total_duration_actual",
        "Ad_total_duration",
        "Ad_total_quantity",
        "Ad_total_duration_counter",
        "Ad_total_duration_payg",
        "Ad_total_revenue_received",
    ]

    # voice_df = load_df("CVM_mViva_Calls_2023_Q3_Q4.csv", voice_cols)
    to_grp_clmn_list_voice = [
        "accountnum",
        "The_date",
        "Traffic_national_international",
        "Traffic_onnet_offnet",
    ]
    agg_cols_voice = {
        "Ad_total_duration_actual": "sum",
        "Ad_total_duration": "sum",
        "Ad_total_quantity": "sum",
        "Ad_total_duration_counter": "sum",
        "Ad_total_duration_payg": "sum",
        "Ad_total_revenue_received": "sum",
    }
    # aggregate_df(voice_df, to_grp_clmn_list_voice, agg_cols_voice, "aggregated_voice.csv")

    sms_cols = [
        "ad_accountnum",
        "ad_msisdn",
        "ad_date",
        "ad_calltype",
        "service_group",
        "service_subtype",
        "traffic_national_international",
        "traffic_onnet_offnet",
        "traffic_country",
        "ad_total_sms",
        "ad_total_sms_counter",
        "ad_total_sms_payg",
        "ad_total_revenue_gross_payg",
    ]

    #sms_df = load_df("CVM_mViva_SMS_2023_Q3_Q4.csv", sms_cols)
    to_grp_clmn_list_sms = [
        "ad_accountnum",
        "ad_date",
        "traffic_national_international",
        "traffic_onnet_offnet",
    ]
    agg_cols_sms = {
        "ad_total_sms": "sum",
        "ad_total_sms_counter": "sum",
        "ad_total_sms_payg": "sum",
        "ad_total_revenue_gross_payg": "sum",
    }
    #aggregate_df(sms_df, to_grp_clmn_list_sms, agg_cols_sms, "aggregated_sms.csv")




    data_cols = [
        "ad_accountnum",                    
        "ad_msisdn",                        
        "ad_date",                          
        "service_group",                    
        "service_subtype",                  
        "traffic_national_international",   
        "traffic_onnet_offnet",             
        "traffic_country",                  
        "ad_total_data_volume_mb",          
        "ad_total_data_volume_counter_mb", 
        "ad_total_revenue_gross_payg" 
    ]
    data_df = load_df("CVM_mViva_DATA_2023_Q3_Q4.csv", data_cols)

    to_grp_clmn_list_data = [
        "ad_accountnum",
        "ad_date",
        "traffic_national_international",
        "traffic_onnet_offnet",
    ]
    agg_cols_data = {
        "ad_total_data_volume_mb": "sum",
        "ad_total_data_volume_counter_mb": "sum",
        "ad_total_revenue_gross_payg": "sum",
    }
    aggregate_df(data_df, to_grp_clmn_list_data, agg_cols_data, "aggregated_data.csv")


    