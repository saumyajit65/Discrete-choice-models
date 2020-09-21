from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

# [Choice]
choice

#[Beta]
ASC_1 = Beta('ASC_1',-0.89,-1000,1000,0)
ASC_11 = Beta('ASC_11',-0.266,-1000,1000,0)
ASC_2 = Beta('ASC_2',1.36,-1000,1000,0)
ASC_21 = Beta('ASC_21',2.05,-1000,1000,0)
ASC_3 = Beta('ASC_3',1.2,-1000,1000,0)
ASC_4 = Beta('ASC_4',0,-1000,1000,1)

beta_fam_package = Beta('beta_fam_package',0.592,-1000, 1000,0)
beta_fam_private = Beta('beta_fam_private',-0.512,-1000, 1000,0)
beta_age_package = Beta('beta_age_package',0.69,-1000, 1000,0)
beta_edu2_package = Beta('beta_edu2_package',0.507,-1000, 1000,0)
beta_edu2_private = Beta('beta_edu2_private',0.0198,-1000, 1000,0)
beta_occ = Beta('beta_occ',0,-1000, 1000,0)
beta_inc2_package = Beta('beta_inc2_package',0.131,-1000, 1000,0)
beta_inc2_private = Beta('beta_inc2_private',0.0659,-1000, 1000,0)
beta_age_private = Beta('beta_age_private',-0.0679,-1000, 1000,0)

beta_enthu = Beta('beta_enthu',0.516,-1000, 1000,0)
beta_fru = Beta('beta_fru',-0.246,-1000,1000,0)
beta_constructive = Beta('beta_constructive',0.295,-1000,1000,0)
beta_travelzeal = Beta('beta_travelzeal',0.401,-1000, 1000,0)

beta_shcosttaxi1 = Beta('beta_shcosttaxi1',-0.196,-1000,1000,0)
beta_shcostsharedcar = Beta('beta_shcostsharedcar',-0.223,-1000,1000,0)
beta_shtime_taxi = Beta('beta_shtime_taxi',-0.023,-1000,1000,0)
beta_dist = Beta('beta_dist',0.0356,-1000,1000,0)

beta_maascosttaxi = Beta('beta_maascosttaxi',-0.764,-1000,1000,0)
beta_maascostshare = Beta('beta_maascostshare',-0.765,-1000,1000,0)
beta_maastime12taxi = Beta('beta_maastime12taxi',-0.569,-1000,1000,0)
beta_maastime22taxi = Beta('beta_maastime22taxi',-0.491,-1000,1000,0)
beta_extra = Beta('beta_extra',-0.52,-1000,1000,0)
beta_maasdist = Beta('beta_maasdist',0.233,-1000,1000,0)
beta_maasdisbike = Beta('beta_maasdisbike',-0.196,-1000,1000,0)
beta_freq = Beta('beta_freq',0.195,-1000,1000,0)
beta_parkcost3 = Beta('beta_parkcost3',-0.0279,-1000,1000,0)
beta_dist3 = Beta('beta_dist3',-0.00996,-1000,1000,0)
beta_parktime3 = Beta('beta_parktime3',-0.00456,-1000,1000,0)

#for every random draw the probability shall be calculated
SIGMA_SH_MAAS_M = Beta('SIGMA_SH_MAAS_M', 0,-1000,1000,1)
SIGMA_SH_MAAS_STD = Beta('SIGMA_SH_MAAS_STD', -2.69,-1000,1000,0) # random normal distribution with mean as 0 and standard deviation as anything and starting from 1
SIGMA_SH_MAASRND = SIGMA_SH_MAAS_M + SIGMA_SH_MAAS_STD * bioDraws('SIGMA_SH_MAASRND')

Shared_vehicle =  ASC_1* dtaxi + ASC_11*dshare + beta_shcosttaxi1 *(sharecost)*dtaxi/10 + beta_shcostsharedcar * sharecost *dshare/10 + beta_shtime_taxi * (sharetime)  + beta_dist * sharedist/10 + SIGMA_SH_MAASRND

MaaS = ASC_2* dtaxi +ASC_21* dshare + beta_maascosttaxi *(maascost)*dtaxi/10 + beta_maascostshare * maascost * dshare/10 +beta_maastime12taxi * (maastime1) + beta_maastime22taxi * (maastime2) + beta_extra * extra  + beta_maasdisbike * maaskm2/10 + beta_maasdist * sharedist /10 +beta_inc2_package*inc_mid + beta_edu2_package * edu_WO + beta_edu2_package * edu_HBO + beta_fam_package * fam_1 + beta_fam_package * fam_2 + beta_enthu * factor1  + beta_constructive * factor3 + beta_travelzeal * factor4 + beta_fru * factor2 + beta_age_package * age_10_60  + SIGMA_SH_MAASRND + beta_freq * highfreq + beta_freq * mediumfreq

Private_vehicle = ASC_3 + beta_parktime3 * (parktime) + beta_parkcost3 * (parkcost)/10 + beta_dist3 * sharedist/10 + beta_edu2_private * edu_HBO + beta_edu2_private * edu_WO + beta_inc2_private*inc_mid + beta_fam_private * fam_1 + beta_fam_private * fam_2 + beta_age_private * age_60_abv

Others = ASC_4
 
# Associate utility functions with the numbering of alternatives
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
