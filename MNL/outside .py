

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
ASC_1 = Beta('ASC_1',0,-1000,1000,1)
ASC_11 = Beta('ASC_11',0,-1000,1000,0)
ASC_2 = Beta('ASC_2',0,-1000,1000,0)
ASC_3 = Beta('ASC_3',0,-1000,1000,0)
ASC_31 = Beta('ASC_31',0,-1000,1000,0)

beta_fam = Beta('beta_fam',0,-1000,1000,0)
beta_gender = Beta('beta_gender',0,-1000,1000,0)
beta_edu = Beta('beta_edu',0,-1000,1000,0)
beta_occ = Beta('beta_occ',0,-1000,1000,0)
beta_inc = Beta('beta_inc',0,-1000,1000,0)
beta_age = Beta('beta_age',0,-1000,1000,0)
beta_vehkm = Beta('beta_vehkm',0,-1000,1000,0)


beta_shcost = Beta('beta_shcost',0,-1000,1000,0)
beta_shcostperdist1 = Beta('beta_shcostperdist1',0,-1000,1000,0)
beta_shcostdist2 = Beta('beta_shcostdist2',0,-1000,1000,0)
beta_shcost1 = Beta('beta_shcost1',0,-1000,1000,0)
beta_shtime = Beta('beta_shtime',0,-1000,1000,0)
beta_WTP_shtime = Beta('beta_WTP_shtime',0,-1000,1000,0)
beta_sharedist = Beta('beta_sharedist',0,-1000,1000,0)

beta_fam2 = Beta('beta_fam2',0,-1000,1000,0)
beta_gender2 = Beta('beta_gender2',0,-1000,1000,0)
beta_edu2 = Beta('beta_edu2',0,-1000,1000,0)
beta_occ2 = Beta('beta_occ2',0,-1000,1000,0)
beta_inc2 = Beta('beta_inc2',0,-1000,1000,0)
beta_age2 = Beta('beta_age2',0,-1000,1000,0)
beta_fuel2 = Beta('beta_fuel2',0,-1000,1000,0)
beta_maascost = Beta('beta_maascost',0,-1000,1000,0)
beta_maascost2dist1 = Beta('beta_maascost2dist1',0,-1000,1000,0)
beta_maascostperdist2 = Beta('beta_maascostperdist2',0,-1000,1000,0)
beta_maascost22 = Beta('beta_maascost22',0,-1000,1000,0)
beta_nonebike_accesstime = Beta('beta_nonebike_accesstime',0,-1000,1000,0)
beta_ebike_accesstime = Beta('beta_ebike_accesstime',0,-1000,1000,0)
beta_WTP_nonebike_accesstime = Beta('beta_WTP_nonebike_accesstime',0,-1000,1000,0)
beta_WTP_ebike_accesstime = Beta('beta_WTP_ebike_accesstime',0,-1000,1000,0)
beta_Maasdist = Beta('beta_Maasdist',0,-1000,1000,0)
beta_distnormalbike = Beta('beta_distnormalbike',0,-1000,1000,0)
beta_extra = Beta('beta_extra',0,-1000,1000,0)

beta_totcost31 = Beta('beta_totcost31',0,-1000,1000,0)
beta_totcost32 = Beta('beta_totcost32',0,-1000,1000,0)
beta_totcostperdist = Beta('beta_totcostperdist',0,-1000,1000,0)
beta_dist3 = Beta('beta_dist3',0,-1000,1000,0)

#[Expressions]
#this is the place to specify the interaction variables

#[Utilities]
Shared_vehicle =  ASC_1  + beta_shcostperdist1 *(sharecost*10/distance) + beta_shtime * sharetime 

MaaS = ASC_2 +  beta_maascostperdist2 *(maascost*10/distance)+ beta_nonebike_accesstime*(maastime1) + beta_ebike_accesstime* maastime2  + beta_extra*(extra) *extra 

Continue_following_existing_way = ASC_3 + beta_totcostperdist * (currcost*10/distance) 


#[Choice set and availability]
choiceset = {1: Shared_vehicle,2: MaaS,3: Continue_following_existing_way}
availability = {1: availability1,2: availability2,3: availability3}

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
BIOGEME_OBJECT.FORMULAS['Continue_following_existing_way'] = Continue_following_existing_way

nullLoglikelihood(availability,'obsIter')
choiceSet = [1,2,3]
cteLoglikelihood(choiceSet,choice,'obsIter')
availabilityStatistics(availability,'obsIter')

