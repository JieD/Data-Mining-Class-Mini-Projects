# declare global variables
file_size = 0
dics = {}
categorical_dics = []
continuous_dics = []
histogram_dics = []
Max_k = 20
Ks = [8, 14, 20]
num_categorical = 8
num_coutinuous = 6

# init variables
def init():
    global dics, categorical_dics, continuous_dics
    workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic, \
    sex_dic, native_country_dic = {}, {}, {}, {}, {}, {}, {}, {}
    age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic \
        = {}, {}, {}, {}, {}, {}
    dics = { 0: age_dic,            1: workclass_dic,    2: fnlwgt_dic,       3: education_dic, 4: education_num_dic,
             5: marital_status_dic, 6: occupation_dic,   7: relationship_dic, 8: race_dic,      9: sex_dic,
            10: capital_gain_dic,  11: capital_loss_dic, 12: hours_per_week_dic, 13: native_country_dic}
    categorical_dics = [workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic,
                        sex_dic, native_country_dic]
    continuous_dics = [age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic]


def main():
    init()


if __name__ == "__main__":
    main()
