from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

# [Choice]
choice

#[Beta]
ASC_1 = Beta('ASC_1',-1.01,-1000,1000,0)
ASC_2 = Beta('ASC_2',-0.542,-1000,1000,0)
ASC_3 = Beta('ASC_3',0,-1000,1000,1)
ASC_4 = Beta('ASC_4',-1.34,-1000,1000,0)

beta_fam_package = Beta('beta_fam_package',-0.0618,-1000, 1000,0)
beta_fam_private = Beta('beta_fam_private',0.617,-1000, 1000,0)
beta_age_package = Beta('beta_age_package',0.649,-1000, 1000,0)
beta_edu2_package = Beta('beta_edu2_package',-0.0157,-1000, 1000,0)
beta_edu2_private = Beta('beta_edu2_private',0.981,-1000, 1000,0)
beta_inc2_package = Beta('beta_inc2_package',-0.535,-1000, 1000,0)
beta_inc2_private = Beta('beta_inc2_private',0.268,-1000, 1000,0)
beta_age_private = Beta('beta_age_private',-1.12,-1000, 1000,0)

beta_enthu = Beta('beta_enthu',0.306,-1000, 1000,0)
beta_fru = Beta('beta_fru',-0.221,-1000,1000,0)
beta_constructive = Beta('beta_constructive',0.033,-1000,1000,0)
beta_travelzeal = Beta('beta_travelzeal',0.231,-1000, 1000,0)

beta_sharedprice1 = Beta('beta_sharedprice1',-0.108,-1000,1000,0)
beta_shtime1 = Beta('beta_shtime1',-0.127,-1000,1000,0)
beta_sharedist = Beta('beta_sharedist',	0.0335,-1000,1000,0)

beta_maascost = Beta('beta_maascost',-0.306,-1000,1000,0)
beta_maas_nonebike_accessibilitytime = Beta('beta_maas_nonebike_accessibilitytime',-0.16,-1000,1000,0)
beta_maas_ebike_accessibilitytime = Beta('beta_maas_ebike_accessibilitytime',-0.14,-1000,1000,0)
beta_extra = Beta('beta_extra',-0.354,-1000,1000,0)
beta_maasdist = Beta('beta_maasdist',0.203,-1000,1000,0)
beta_distnormalbike = Beta('beta_distnormalbike',-0.0984,-1000,1000,0)
beta_freq = Beta('beta_freq',-0.895,-1000,1000,0)

beta_totcost = Beta('beta_totcost',-0.0058,-1000,1000,0)
beta_dist3 = Beta('beta_dist3',-0.00567,-1000,1000,0)

#for every random draw the probability shall be calculated
SIGMA_SH_MAAS_M = Beta('SIGMA_SH_MAAS_M', 0,-1000,1000,1)
SIGMA_SH_MAAS_STD = Beta('SIGMA_SH_MAAS_STD', -5.73,-1000,1000,0) # random normal distribution with mean as 0 and standard deviation as anything and starting from 1
SIGMA_SH_MAASRND = SIGMA_SH_MAAS_M + SIGMA_SH_MAAS_STD * bioDraws('SIGMA_SH_MAASRND')

#Utility
Shared_vehicle =  ASC_1 + beta_shtime1 * sharetime + beta_sharedprice1 * (sharecost) + beta_sharedist * vehkm / 10  + SIGMA_SH_MAASRND

MaaS = ASC_2 + beta_maascost * (maascost) + beta_maas_nonebike_accessibilitytime * (maastime1) + beta_maas_ebike_accessibilitytime * (maastime2) + beta_extra * extra + beta_distnormalbike * maaskm1 / 10 + beta_maasdist * vehkm / 10 + beta_fam_package * fam_1 + beta_fam_package * fam_2 + beta_edu2_package * edu_WO + beta_edu2_package * edu_HBO + beta_enthu * factor1 + beta_constructive * factor3 + beta_travelzeal * factor4 + beta_fru * factor2+ beta_age_package * age_10_60 + beta_inc2_package*inc_mid + SIGMA_SH_MAASRND + beta_freq * highfreq + beta_freq * mediumfreq

Private_vehicle = ASC_3 + beta_totcost * (Total_cost) + beta_dist3 * vehkm / 10 + beta_fam_private * fam_1 + beta_fam_private * fam_2 + beta_edu2_private * edu_WO + beta_edu2_private * edu_HBO +  beta_age_private * age_60_abv + beta_inc2_private*inc_mid

Others = ASC_4

#[Choice set and availability]
choiceset = {1: Shared_vehicle,2: MaaS,3: Private_vehicle,4: Others}
availability = {1: availability1,2: availability2,3: availability3,4: availability4}

rowIterator('obsIter') 
# The choice model is a logit, with availability conditions
prob1 = MonteCarlo(bioLogit(choiceset, availability, 1))
prob2 = MonteCarlo(bioLogit(choiceset, availability, 2))
prob3 = MonteCarlo(bioLogit(choiceset, availability, 3))
prob4 = MonteCarlo(bioLogit(choiceset, availability, 4))
#Pro=MonteCarlo(bioLogit(choiceset, availability,choice))

simulate = {'Prob. 1': prob1,
'Prob. 2': prob2,
'Prob. 3': prob3,
'Prob. 4': prob4}
#,'ProbTotal': Pro
BIOGEME_OBJECT.SIMULATE = Enumerate(simulate,'obsIter')

BIOGEME_OBJECT.PARAMETERS['NbrOfDraws'] = "1000"
#BIOGEME_OBJECT.PARAMETERS['RandomDistribution'] = "HALTON"
BIOGEME_OBJECT.DRAWS = {'SIGMA_SH_MAASRND': 'NORMAL'}
