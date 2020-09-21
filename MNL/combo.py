

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
ASC_1 = Beta('ASC_1',0,-10000,10000,0)
ASC_11 = Beta('ASC_11',0,-10000,10000,0)
ASC_2 = Beta('ASC_2',0,-10000,10000,0)
ASC_21 = Beta('ASC_21',0,-10000,10000,0)
ASC_3 = Beta('ASC_3',0,-10000,10000,0)
ASC_31 = Beta('ASC_31',0,-10000,10000,0)
ASC_4 = Beta('ASC_4',0,-10000,10000,1)
ASC_41 = Beta('ASC_41',0,-10000,10000,0)

beta_shcosttaxi1 = Beta('beta_shcosttaxi1',0,-10000,10000,0)
beta_shcosttaxi2 = Beta('beta_shcosttaxi2',0,-10000,10000,0)
beta_shcostsharedcar = Beta('beta_shcostsharedcar',0,-10000,10000,0)
beta_shtime_taxi = Beta('beta_shtimetaxi',0,-10000,10000,0)
beta_shtime_taxi1 = Beta('beta_shtimetaxi1',0,-10000,10000,0)
beta_shtime_share = Beta('beta_shtimeshare',0,-10000,10000,0)
beta_shtime_share1 = Beta('beta_shtimeshare1',0,-10000,10000,0)
beta_dist = Beta('beta_dist',0,-10000,10000,0)
beta_dist1 = Beta('beta_dist1',0,-10000,10000,0)

beta_maascosttaxi = Beta('beta_maascosttaxi',0,-10000,10000,0)
beta_maascosttaxi2 = Beta('beta_maascosttaxi2',0,-10000,10000,0)
beta_maascostshare = Beta('beta_maascostshare',0,-10000,10000,0)
beta_maastime12taxi = Beta('beta_maastime12taxi',0,-10000,10000,0)
beta_maastime22taxi = Beta('beta_maastime22taxi',0,-10000,10000,0)
beta_maastime12taxi1 = Beta('beta_maastime12taxi1',0,-10000,10000,0)
beta_maastime22taxi1 = Beta('beta_maastime22taxi1',0,-10000,10000,0)
beta_maastime12shared = Beta('beta_maastime12shared',0,-10000,10000,0)
beta_maastime12shared1 = Beta('beta_maastime12shared1',0,-10000,10000,0)
beta_maastime22shared = Beta('beta_maastime22shared',0,-10000,10000,0)
beta_maastime22shared1 = Beta('beta_maastime22shared1',0,-10000,10000,0)
beta_extra = Beta('beta_extra',0,-10000,10000,0)
beta_maasdist = Beta('beta_maasdist',0,-10000,10000,0)
beta_maasdiscarsh = Beta('beta_distcarsh',0,-10000,10000,0)
beta_maasdisbike = Beta('beta_maasdisbike',0,-10000,10000,0)

beta_fuel3 = Beta('beta_fuel3',0,-10000,10000,0)
beta_parkcost3 = Beta('beta_parkcost3',0,-10000,10000,0)
beta_unitcost31 = Beta('beta_unitcost31',0,-10000,10000,0)
beta_totcost3 = Beta('beta_totcost3',0,-10000,10000,0)
beta_dist3 = Beta('beta_dist3',0,-10000,10000,0)
beta_dist31 = Beta('beta_dist31',0,-10000,10000,0)
beta_parktime3 = Beta('beta_parktime3',0,-10000,10000,0)
beta_parktime23 = Beta('beta_parktime23',0,-10000,10000,0)

#Utilities
Shared_vehicle =  ASC_1* dtaxi + ASC_11*dshare   + beta_shcosttaxi1 *(sharecost)*dtaxi/10 + beta_shcostsharedcar * sharecost *dshare/10 + beta_shtime_taxi * (sharetime)  + beta_dist * sharedist/10

MaaS =  ASC_2* dtaxi +ASC_21* dshare  + beta_maascosttaxi *(maascost)*dtaxi/10 + beta_maascostshare * maascost * dshare/10 + beta_maastime12taxi * (maastime1) + beta_maastime22taxi * (maastime2) + beta_extra * extra  + beta_maasdisbike * maaskm2/10 + beta_maasdist * sharedist/10


Private_vehicle = ASC_3  + beta_parktime3 * (parktime) + beta_parkcost3 * (parkcost)/10 + beta_dist3 * sharedist/10


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
BIOGEME_OBJECT.PARAMETERS['shareOfProcessors'] = "120"

#Print some statistics
BIOGEME_OBJECT.FORMULAS['Shared_vehicle utility'] = Shared_vehicle
BIOGEME_OBJECT.FORMULAS['MaaS utility'] = MaaS
BIOGEME_OBJECT.FORMULAS['Private_vehicle utility'] = Private_vehicle
BIOGEME_OBJECT.FORMULAS['Others utility'] = Others


nullLoglikelihood(availability,'obsIter')
choiceSet = [1,2,3,4]
cteLoglikelihood(choiceSet,choice,'obsIter')
availabilityStatistics(availability,'obsIter')

