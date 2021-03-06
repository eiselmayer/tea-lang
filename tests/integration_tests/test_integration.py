import tea
import os

base_url = 'https://homes.cs.washington.edu/~emjun/tea-lang/datasets/'
# uscrime_data_path = None
# states_path = None
# cats_path = None
# cholesterol_path = None
# soya_path = None
# co2_path = None
# exam_path = None
# liar_path = None 
# pbcorr_path = None
# spider_path = None
# drug_path = None
# alcohol_path = None
# ecstasy_path = None
# goggles_path = None
# goggles_dummy_path = None
# data_paths = [uscrime_data_path, states_path, cats_path, cholesterol_path, soya_path, co2_path, exam_path, liar_path, pbcorr_path, spider_path, drug_path, alcohol_path, ecstasy_path, goggles_path, goggles_dummy_path]
file_names = ['UScrime.csv', 'statex77.csv', 'catsData.csv', 'cholesterol.csv', 'soya.csv', 'co2.csv', 'exam.csv', 'liar.csv', 'pbcorr.csv','spiderLong_within.csv', 'drug.csv', 'alcohol.csv', 'ecstasy.csv', 'gogglesData.csv', 'gogglesData_dummy.csv']
data_paths = [None] * len(file_names)

def load_data():
    global base_url, data_paths, file_names
    global drug_path 

    for i in range(len(data_paths)):
        csv_name = file_names[i]

        csv_url = os.path.join(base_url, csv_name)
        # import pdb; pdb.set_trace()
        data_paths[i] = tea.download_data(csv_url, csv_name)

def get_data_path(filename):
    load_data()
    try: 
        data_idx = file_names.index(filename)
    except: 
        raise ValueError(f"File is not found!:{filename}")
    data_path = data_paths[data_idx]
    
    return data_path

# Example from Kabacoff
# Expected outcome: Pearson correlation 
def test_pearson_corr(): 
    data_path = get_data_path('statex77.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Illiteracy',
            'data type' : 'interval',
            'categories' : [0, 100]
        },
        {
            'name' : 'Life Exp',
            'data type' : 'ratio',
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Illiteracy', 'Life Exp'],
                            'outcome variables': ''
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    results = tea.hypothesize(['Illiteracy', 'Life Exp'], ['Illiteracy ~ Life Exp'])
    print("\nfrom Kabacoff")
    print("Expected outcome: Pearson")
    
def test_pearson_corr_2(): 
    data_path = get_data_path('exam.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Exam',
            'data type' : 'ratio',
            'range' : [0, 100]
        },
        {
            'name' : 'Anxiety',
            'data type' : 'interval',
            'range' : [0, 100]
        },
        {
            'name' : 'Gender',
            'data type' : 'nominal',
            'categories' : ['Male', 'Female']
        },
        {
            'name' : 'Revise',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Anxiety', 'Gender', 'Revise'],
                            'outcome variables': 'Exam'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    results = tea.hypothesize(['Anxiety', 'Exam'])
    results = tea.hypothesize(['Revise', 'Exam'])
    results = tea.hypothesize(['Anxiety', 'Revise'])
    print("\nfrom Field et al.")
    print("Expected outcome: Pearson")

def test_spearman_corr(): 
    data_path = get_data_path('liar.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Creativity',
            'data type' : 'interval'
        },
        {
            'name' : 'Position',
            'data type' : 'ordinal',
            'categories' : [6, 5, 4, 3, 2, 1] # ordered from lowest to highest
        },
        {
            'name' : 'Novice',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Novice', 'Creativity'],
                            'outcome variables': 'Position'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    results = tea.hypothesize(['Position', 'Creativity'], ['Position:1 > 6']) # TODO: allow for partial orders?
    print("\nfrom Field et al.")
    print("Expected outcome: Spearman")


# Same as test for Spearman rho
def test_kendall_tau_corr(): 
    data_path = get_data_path('liar.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Creativity',
            'data type' : 'interval'
        },
        {
            'name' : 'Position',
            'data type' : 'ordinal',
            'categories' : [6, 5, 4, 3, 2, 1] # ordered from lowest to highest
        },
        {
            'name' : 'Novice',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['Novice', 'Creativity'],
                            'outcome variables': 'Position'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    results = tea.hypothesize(['Position', 'Creativity'], ['Position:1 > 6', 'Position:1 > 2']) # I think this works!?
    print("\nfrom Field et al.")
    print("Expected outcome: Kendall Tau")
    

def test_pointbiserial_corr(): 
    data_path = get_data_path('pbcorr.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'time',
            'data type' : 'ratio'
        },
        {
            'name' : 'gender',
            'data type' : 'nominal',
            'categories' : [0, 1] # ordered from lowest to highest
        },
        {
            'name' : 'recode',
            'data type' : 'nominal',
            'categories' : [0, 1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': ['gender', 'recode'],
                            'outcome variables': 'time'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design)
    tea.assume(assumptions)

    tea.hypothesize(['time', 'gender'], ['gender:1 > 0']) # I think this works!?
    print("\nfrom Field et al.")
    print("Expected outcome: Pointbiserial")


def test_indep_t_test():
    data_path = get_data_path('UScrime.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'So',
            'data type' : 'nominal',
            'categories' : ['0', '1']
        },
        {
            'name' : 'Prob',
            'data type' : 'ratio',
            'range' : [0,1]
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': 'So',
                            'outcome variables': 'Prob',
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['So', 'Prob'], ['So:1 > 0'])  ## Southern is greater
    print("\nfrom Kabacoff")
    print("Expected outcome: Student's t-test")


def test_paired_t_test(): 
    data_path = get_data_path('spiderLong_within.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Group',
            'data type' : 'nominal',
            'categories' : ['Picture', 'Real Spider']
        },
        {
            'name' : 'Anxiety',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'Group',
                            'dependent variables': 'Anxiety',
                            'within subjects' : 'Group'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05
    }

    tea.data(data_path, key="id")
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Group', 'Anxiety'], ['Group:Real Spider > Picture'])

    print("\nfrom Field et al.")
    print("Expected outcome: Paired/Dependent t-test")
    

def test_wilcoxon_signed_rank(): 
    data_path = get_data_path('alcohol.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'drug',
            'data type' : 'nominal',
            'categories' : ['Alcohol']
        },
        {
            'name' : 'day',
            'data type' : 'nominal',
            'categories': ['sundayBDI', 'wedsBDI']
        },
        {
            'name' : 'value',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'day',
                            'dependent variables': 'value',
                            'within subjects' : 'day'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['day', 'value'], ['day:sundayBDI > wedsBDI'])

    print("\nfrom Field et al.")
    print("Expected outcome: Wilcoxon signed rank test")

def test_f_test(): 
    data_path = get_data_path('cholesterol.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'trt',
            'data type' : 'nominal',
            'categories' : ['1time', '2times', '4times', 'drugD', 'drugE']
        },
        {
            'name' : 'response',
            'data type' : 'ratio'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'trt',
                            'dependent variables': 'response',
                            'between subjects': 'trt'

                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['trt', 'response'])
    print("\nFrom Field et al.")
    print("Expected outcome: Oneway ANOVA (F) test")
        
def test_kruskall_wallis(): 
    data_path = get_data_path('soya.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Sperm',
            'data type' : 'interval'
        },
        {
            'name' : 'Soya',
            'data type' : 'ordinal',
            'categories': ['No Soya', '1 Soya Meal', '4 Soya Meals', '7 Soya Meals']
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': 'Soya',
                            'dependent variables': 'Sperm',
                            'between subjects': 'Soya'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Soya', 'Sperm'])

    print("\nFrom Field et al.")
    print("Expected outcome: Kruskall Wallis")

def test_rm_one_way_anova(): 
    data_path = get_data_path('co2.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'uptake',
            'data type' : 'interval'
        },
        {
            'name' : 'Type',
            'data type' : 'nominal',
            'categories': ['Quebec', 'Mississippi']
        },
        {
            'name' : 'conc',
            'data type' : 'ordinal',
            'categories': [95, 175, 250, 350, 500, 675, 1000]
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': ['Type', 'conc'],
                            'dependent variables': 'uptake',
                            'within subjects': 'conc',
                            'between subjects': 'Type'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path, key="Plant")
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['uptake', 'conc'])

    print("\nFrom Field et al.")
    print("Expected outcome: Repeated Measures One Way ANOVA")

def test_factorial_anova():
    data_path = get_data_path('gogglesData.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'gender',
            'data type' : 'nominal',
            'categories' : ['Female', 'Male']
        },
        {
            'name' : 'alcohol',
            'data type' : 'nominal',
            'categories': ['None', '2 Pints', '4 Pints']
        },
        {
            'name' : 'attractiveness',
            'data type' : 'interval'
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': ['gender', 'alcohol'],
                            'dependent variables': 'attractiveness',
                            'between subjects': ['gender', 'alcohol']
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['attractiveness', 'gender', 'alcohol']) 
    # alcohol main effect?
    print("\nFrom Field et al.")
    print("Expected outcome: Factorial ANOVA")

def test_two_way_anova(): 
    data_path = get_data_path('co2.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'uptake',
            'data type' : 'interval'
        },
        {
            'name' : 'Type',
            'data type' : 'nominal',
            'categories': ['Quebec', 'Mississippi']
        },
        {
            'name' : 'conc',
            'data type' : 'ordinal',
            'categories': [95, 175, 250, 350, 500, 675, 1000]
        }
    ]
    experimental_design = {
                            'study type': 'experiment',
                            'independent variables': ['Type', 'conc'],
                            'dependent variables': 'uptake',
                            'within subjects': 'conc',
                            'between subjects': 'Type'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['uptake', 'conc', 'Type']) # Fails: not all groups are normal
    #Type main effect?
    print('Supposed to be 2 way ANOVA')

def test_chi_square(): 
    data_path = get_data_path('catsData.csv')

    # Declare and annotate the variables of interest
    variables = [
        {
            'name' : 'Training',
            'data type' : 'nominal',
            'categories' : ['Food as Reward', 'Affection as Reward']
        },
        {
            'name' : 'Dance',
            'data type' : 'nominal',
            'categories' : ['Yes', 'No']
        }
    ]
    experimental_design = {
                            'study type': 'observational study',
                            'contributor variables': 'Training',
                            'outcome variables': 'Dance'
                        }
    assumptions = {
        'Type I (False Positive) Error Rate': 0.05,
    }

    tea.data(data_path)
    tea.define_variables(variables)
    tea.define_study_design(experimental_design) # Allows for using multiple study designs for the same dataset (could lead to phishing but also practical for saving analyses and reusing as many parts of analyses as possible)
    tea.assume(assumptions)

    tea.hypothesize(['Training', 'Dance'])
    print('Chi square')
