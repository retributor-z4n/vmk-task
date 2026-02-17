from datetime import datetime
import pandas as pd



def load_df(file, columnlist):
    loaded_df = pd.read_csv(
        f"../../Downloads/OneDrive_1_9-2-2026/{file}", header=None, names=columnlist
    )
    return loaded_df

def trim_recharge():
    recharge_cols = [
        "fad_accountnum",
        "fad_msisdn",
        "fad_time_stamp",
        "dsu_subscription_type_name",
        "brand",
        "dad_adjustmentreasonname",    
        "dad_category_2",              
        "fad_amount",                  
        "fad_postbalance" 
    ]

    recharge_df = load_df("CVM_mViva_Recharges_Q3_Q4.csv", recharge_cols)

    cols_to_trim = [
        "fad_accountnum",
        "fad_time_stamp",
        "brand",    
        "dad_category_2",              
        "fad_amount",                  
        "fad_postbalance" 
    ]

    trimmed_recharge_df = recharge_df[cols_to_trim]
    return trimmed_recharge_df


def trim_subscriptions():
     
    subscriptions_cols = [
        "ad_accountnum",
        "brand",
        "msisdn",
        "productcode",
        "packname",
        "commitmentstartdate",
        "subscriptionstartdate",
        "subscriptionenddate",
        "nextpaymentdate",
        "monthlyprice",
        "plantype",
        "planvalidityindays",
        "Plancommitmentinmonth"
    ]

    subscriptions_df = load_df("CVM_mViva_Subscription_Q3_Q4_new.csv", subscriptions_cols)

    cols_to_trim = [
        "ad_accountnum",
        "brand",
        "productcode",
        "packname",
        "commitmentstartdate",
        "subscriptionstartdate",
        "subscriptionenddate",
        "nextpaymentdate",
        "monthlyprice",
        "plantype",
        "planvalidityindays",
        "Plancommitmentinmonth" 
    ]

    trimmed_subscriptions_df = subscriptions_df[cols_to_trim]
    return trimmed_subscriptions_df



if __name__ == "__main__":
    #trimmed_recharge_df = trim_recharge()
    #trimmed_recharge_df.to_csv("./aggregation/trimmed_recharges.csv",index = False)

    trimmed_subscriptions_df = trim_subscriptions()
    trimmed_subscriptions_df.to_csv("./aggregation/trimmed_subscriptions.csv",index = False)

