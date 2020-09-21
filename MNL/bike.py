

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *
  
# [Choice]
choice

#[Beta]
#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_1 = Beta('ASC_1',0,-100,100,0)
ASC_11 = Beta('ASC_11',0,-100,100,0)
ASC_2 = Beta('ASC_2',0,-100,100,0)
ASC_21 = Beta('ASC_21',0,-100,100,0)
ASC_3 = Beta('ASC_3',0,-100,100,1)
ASC_31 = Beta('ASC_31',0,-100,100,0)
ASC_4 = Beta('ASC_4',0,-100,100,0)
ASC_41 = Beta('ASC_41',0,-100,100,0)

beta_fam = Beta('beta_fam',0,-100,100,0)
beta_gender = Beta('beta_gender',0,-100,100,0)
beta_edu = Beta('beta_edu',0,-100,100,0)
beta_occ = Beta('beta_occ',0,-100,100,0)
beta_inc = Beta('beta_inc',0,-100,100,0)
beta_age = Beta('beta_age',0,-100,100,0)
beta_vehkm = Beta('beta_vehkm',0,-100,100,0)
beta_fuel = Beta('beta_fuel',0,-100,100,0)
beta_parkcost = Beta('beta_parkcost',0,-100,100,0)
beta_totcost = Beta('beta_totcost',0,-100,100,0)
beta_parktime = Beta('beta_parktime',0,-100,100,0)
beta_sharedist = Beta('beta_sharedist',0,-100,100,0)
beta_shareprice1 = Beta('beta_shareprice1',0,-100,100,0)
beta_shtime1 = Beta('beta_shtime1',0,-100,100,0)
beta_shtime2 = Beta('beta_shtime2',0,-100,100,0)

beta_fam2 = Beta('beta_fam2',0,-100,100,0)
beta_gender2 = Beta('beta_gender2',0,-100,100,0)
beta_edu2 = Beta('beta_edu2',0,-100,100,0)
beta_occ2 = Beta('beta_occ2',0,-100,100,0)
beta_inc2 = Beta('beta_inc2',0,-100,100,0)
beta_age2 = Beta('beta_age2',0,-100,100,0)
beta_sharedist = Beta('beta_sharedist',0,-100,100,0)
beta_fuel2 = Beta('beta_fuel2',0,-100,100,0)
beta_parkcost2 = Beta('beta_parkcost2',0,-100,100,0)
beta_totcost2 = Beta('beta_totcost2',0,-100,100,0)
beta_parktime2 = Beta('beta_parktime2',0,-100,100,0)
beta_shcost2 = Beta('beta_shcost2',0,-100,100,0)
beta_shtime2 = Beta('beta_shtime2',0,-100,100,0)
beta_maascost = Beta('beta_maascost',0,-100,100,0)
beta_maascost2perprice2 = Beta('beta_maascost2perprice2',0,-100,100,0)
beta_maas_nonebike_accessibilitytime = Beta('beta_maas_nonebike_accessibilitytime',0,-100,100,0)
beta_maas_ebike_accessibilitytime = Beta('beta_maas_ebike_accessibilitytime',0,-100,100,0)
beta_maastime11 = Beta('beta_maastm11',0,-100,100,0)
beta_maastime22 = Beta('beta_maastm22',0,-100,100,0)
beta_MaaSdist = Beta('beta_MaaSdist',0,-100,100,0)
beta_distebike = Beta('beta_distebike',0,-100,100,0)
beta_distnormalbike = Beta('beta_distnormalbike',0,-100,100,0)
beta_extra = Beta('beta_extra',0,-100,100,0)

beta_totcost = Beta('beta_totcost',0,-100,100,0)
beta_totcost3perprice2 = Beta('beta_totcost3perprice2',0,-100,100,0)
beta_dist3 = Beta('beta_dist3',0,-100,100,0)

#[Utilities]

Shared_vehicle =  ASC_1 + beta_shtime1 *sharetime +  beta_shareprice1 * (sharecost) + beta_sharedist* vehkm/10

MaaS = ASC_2 +  beta_maascost *(maascost) + beta_maas_nonebike_accessibilitytime * (maastime1) + beta_maas_ebike_accessibilitytime *(maastime2) + beta_extra * extra + beta_distnormalbike * maaskm1/10 + beta_MaaSdist * vehkm/10

Private_vehicle = ASC_3  +  beta_totcost * (Total_cost) + beta_dist3 * vehkm/10

Others = ASC_4 



#[Choice set and availability]
choiceset = {1: Shared_vehicle,2: MaaS,3: Private_vehicle,4: Others}
availability = {1: availability1,2: availability2,3: availability3,4: availability4}

#Exclude [if you want to exclude observations]


#[Model]
# MNL  // Logit Model
# The choice model is a logit, with availability conditions
prob = bioLogit(choiceset,availability,choice)
l = log(prob)

# Defines an itertor on the data [in this case each row is a separate individual]
rowIterator('obsIter')

# Define the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(l,'obsIter')

# you can define which optimization algorithm to use, BIO is standard and is ok for MNL or PSL
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"
BIOGEME_OBJECT.PARAMETERS['shareOfProcessors'] = "60"

#Print some statistics
BIOGEME_OBJECT.FORMULAS['Shared_vehicle'] = Shared_vehicle
BIOGEME_OBJECT.FORMULAS['MaaS'] = MaaS
BIOGEME_OBJECT.FORMULAS['Private_vehicle'] = Private_vehicle
BIOGEME_OBJECT.FORMULAS['Others'] = Others


nullLoglikelihood(availability,'obsIter')
choiceSet = [1,2,3,4]
cteLoglikelihood(choiceSet,choice,'obsIter')
availabilityStatistics(availability,'obsIter')

