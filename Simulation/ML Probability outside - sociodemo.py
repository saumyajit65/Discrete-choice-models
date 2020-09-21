from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

# [Choice]
choice

#[Beta]
ASC_1 = Beta('ASC_1',0,-1000,1000,1)
ASC_2 = Beta('ASC_2',1.34,-1000,1000,0)
ASC_3 = Beta('ASC_3',0.483,-1000,1000,0)

beta_fam_package = Beta('beta_fam_package',-0.538,-1000, 1000,0)
beta_fam_private = Beta('beta_fam_private',0.742,-1000, 1000,0)
beta_age_package = Beta('beta_age_package',0.273,-1000, 1000,0)
beta_edu2_package = Beta('beta_edu2_package',-0.127,-1000, 1000,0)
beta_edu2_private = Beta('beta_edu2_private',0.857,-1000, 1000,0)
beta_inc2_package = Beta('beta_inc2_package',-0.326,-1000, 1000,0)
beta_inc2_private = Beta('beta_inc2_private',0.223,-1000, 1000,0)
beta_age_private = Beta('beta_age_private',0.64,-1000, 1000,0)

beta_enthu = Beta('beta_enthu',0.256,-1000, 1000,0)
beta_fru = Beta('beta_fru',0.255,-1000,1000,0)
beta_constructive = Beta('beta_constructive',0.188,-1000,1000,0)
beta_travelzeal = Beta('beta_travelzeal',0.333,-1000, 1000,0)

beta_shcostperdist1 = Beta('beta_shcostperdist1',-0.752,-1000,1000,0)
beta_shtime = Beta('beta_shtime',-0.18,-1000,1000,0)
beta_WTP_shtime = Beta('beta_WTP_shtime',0.807,-1000, 1000,0)

beta_maascostperdist2 = Beta('beta_maascostperdist2',-0.823,-1000,1000,0)
beta_nonebike_accesstime = Beta('beta_nonebike_accesstime',-0.298,-1000, 1000,0)
beta_ebike_accesstime = Beta('beta_ebike_accesstime',-0.277,-1000, 1000,0)
beta_WTP_nonebike_accesstime = Beta('beta_WTP_nonebike_accesstime',-0.0458,-1000, 1000,0)
beta_WTP_ebike_accesstime = Beta('beta_WTP_ebike_accesstime',0.0359,-1000, 1000,0)
beta_freq = Beta('beta_freq',-0.563,-1000, 1000,0)
beta_extra = Beta('beta_extra',-0.356,-1000,1000,0)

beta_totcostperdist = Beta('beta_totcostperdist',-0.429,-1000,1000,0)

#for every random draw the probability shall be calculated
SIGMA_SH_MAAS_M = Beta('SIGMA_SH_MAAS_M', 0,-1000,1000,1)
SIGMA_SH_MAAS_STD = Beta('SIGMA_SH_MAAS_STD', 4.04,-1000,1000,0) # random normal distribution with mean as 0 and standard deviation as anything and starting from 1
SIGMA_SH_MAASRND = SIGMA_SH_MAAS_M + SIGMA_SH_MAAS_STD * bioDraws('SIGMA_SH_MAASRND')


#Utility
Shared_vehicle =   ASC_1  + beta_shcostperdist1 *(sharecost*10/distance) + beta_shtime * sharetime + SIGMA_SH_MAASRND

MaaS = ASC_2 +  beta_maascostperdist2 *(maascost*10/distance)+ beta_nonebike_accesstime*(maastime1) + beta_ebike_accesstime* maastime2 + beta_extra*(extra) *extra + beta_enthu * factor1 + beta_fru * factor2  + beta_constructive * factor3 + beta_travelzeal * factor4 + beta_age_package * age_10_60 + beta_edu2_package * edu_WO +beta_edu2_package * edu_HBO + beta_inc2_package*inc_mid  + SIGMA_SH_MAASRND + beta_freq * highfreq + beta_freq * mediumfreq

Continue_following_existing_way = ASC_3 + beta_totcostperdist * (currcost*10/distance) + beta_age_private * age_60_abv + beta_edu2_private * edu_WO + beta_edu2_private * edu_HBO + beta_inc2_private*inc_mid

# Associate utility functions with the numbering of alternatives
choiceset = {1: Shared_vehicle,2: MaaS,3: Continue_following_existing_way}
availability = {1: availability1,2: availability2,3: availability3}

rowIterator('obsIter') 
# The choice model is a logit, with availability conditions
prob1 = MonteCarlo(bioLogit(choiceset, availability, 1))
prob2 = MonteCarlo(bioLogit(choiceset, availability, 2))
prob3 = MonteCarlo(bioLogit(choiceset, availability, 3))
#Pro=MonteCarlo(bioLogit(choiceset, availability,choice))

simulate = {'Prob. 1': prob1,
'Prob. 2': prob2,
'Prob. 3': prob3}
#,'ProbTotal': Pro
BIOGEME_OBJECT.SIMULATE = Enumerate(simulate,'obsIter')

BIOGEME_OBJECT.PARAMETERS['NbrOfDraws'] = "1000"
#BIOGEME_OBJECT.PARAMETERS['RandomDistribution'] = "HALTON"
BIOGEME_OBJECT.DRAWS = {'SIGMA_SH_MAASRND': 'NORMAL'}
