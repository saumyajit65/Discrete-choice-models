
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable, bioDraws, \
    PanelLikelihoodTrajectory, MonteCarlo, log

# Read the data
df = pd.read_csv('comboall.dat', '\t')
database = db.Database('comboall', df)
database.panel("ID")
# They are organized as panel data. The variable ID identifies each individual.
globals().update(database.variables)

# Shared error parameters, fix the mean-parameter to 0
SIGMA_SH_MAAS_M = Beta('SIGMA_SH_MAAS_M', 0,None, None,1)
SIGMA_SH_MAAS_STD = Beta('SIGMA_SH_MAAS_STD', 0,None, None,0) # assumed a normal distribution with mean as 0 and standard deviation as anything and starting from 0, if it is 1 then the null log likelihood shall change
SIGMA_SH_MAASRND = SIGMA_SH_MAAS_M + SIGMA_SH_MAAS_STD * bioDraws('SIGMA_SH_MAASRND','NORMAL')

# Parameters to be estimated
ASC_1 = Beta('ASC_1',0,None,None,0)
ASC_11 = Beta('ASC_11',0,None,None,0)
ASC_2 = Beta('ASC_2',0,None,None,0)
ASC_21 = Beta('ASC_21',0,None,None,0)
ASC_3 = Beta('ASC_3',0,None,None,0)
ASC_31 = Beta('ASC_31',0,None,None,0)
ASC_4 = Beta('ASC_4',0,None,None,1)

beta_fam_package = Beta('beta_fam_package',0,None, None,0)
beta_fam_private = Beta('beta_fam_private',0,None, None,0)
beta_age_package = Beta('beta_age_package',0,None, None,0)
beta_edu2_package = Beta('beta_edu2_package',0,None, None,0)
beta_edu2_private = Beta('beta_edu2_private',0,None, None,0)
beta_occ = Beta('beta_occ',0,None, None,0)
beta_inc2_package = Beta('beta_inc2_package',0,None, None,0)
beta_inc2_private = Beta('beta_inc2_private',0,None, None,0)
beta_age_private = Beta('beta_age_private',0,None, None,0)

beta_enthu = Beta('beta_enthu',0,None, None,0)
beta_fru = Beta('beta_fru',0,None, None,0)
beta_constructive = Beta('beta_constructive',0,None, None,0)
beta_travelzeal = Beta('beta_travelzeal',0,None, None,0)


beta_shtaxi_sub_price = Beta('beta_shtaxi_sub_price',0,None,None,0)
beta_sh_sub_price = Beta('beta_sh_sub_price',0,None,None,0)
beta_shtime = Beta('beta_shtime',0,None,None,0)
beta_dist = Beta('beta_dist',0,None,None,0)
beta_dist1 = Beta('beta_dist1',0,None,None,0)

beta_maasunitcosttaxi = Beta('beta_maasunitcosttaxi',0,None,None,0)
beta_maascosttaxi = Beta('beta_maascosttaxi',0,None,None,0)
beta_maascosttaxi2 = Beta('beta_maascosttaxi2',0,None,None,0)
beta_maascostshare = Beta('beta_maascostshare',0,None,None,0)
beta_maascostshare2 = Beta('beta_maascostshare2',0,None,None,0)
beta_maastime12taxi = Beta('beta_maastime12taxi',0,None,None,0)
beta_maastime22taxi = Beta('beta_maastime22taxi',0,None,None,0)
beta_maastime12taxi1 = Beta('beta_maastime12taxi1',0,None,None,0)
beta_maastime22taxi1 = Beta('beta_maastime22taxi1',0,None,None,0)
beta_maastime12shared = Beta('beta_maastime12shared',0,None,None,0)
beta_maastime12shared1 = Beta('beta_maastime12shared1',0,None,None,0)
beta_maastime22shared = Beta('beta_maastime22shared',0,None,None,0)
beta_maastime22shared1 = Beta('beta_maastime22shared1',0,None,None,0)
beta_extra = Beta('beta_extra',0,None,None,0)
beta_freq = Beta('beta_freq',0,None,None,0)
beta_extra1 = Beta('beta_extra1',0,None,None,0)
beta_maasdist = Beta('beta_maasdist',0,None,None,0)
beta_maasdiscarsh = Beta('beta_distcarsh',0,None,None,0)
beta_maasdisbike = Beta('beta_maasdisbike',0,None,None,0)

beta_parkcost3 = Beta('beta_parkcost3',0,None,None,0)
beta_dist3 = Beta('beta_dist3',0,None,None,0)
beta_dist31 = Beta('beta_dist31',0,None,None,0)
beta_parktime3 = Beta('beta_parktime3',0,None,None,0)
beta_parktime23 = Beta('beta_parktime23',0,None,None,0)

# Definition of the utility functions
#Alt1 =  ASC_1_RND*dist_eff200 + ASC_11_RND*dist_eff300   + beta_shunitcosttaxi1_RND *(sharedist/sharecost)*dist_eff200 + beta_shunitcosttaxi2_RND *(sharedist/sharecost)*dist_eff300 + beta_shtime_taxi_RND * (eff_sh4)  + beta_shtime_taxi1_RND * (eff_sh6) + SIGMA_SH_MAASRND
#Alt2 =  ASC_2_RND*dist_eff200 +ASC_21_RND*dist_eff300  +  beta_maascosttaxi_RND *(vehkm/maascost)*dist_eff200 +  beta_maascosttaxi2RND *(vehkm/maascost)*dist_eff300  + beta_maastime12taxiRND * (eff_ma2) + beta_maastime22taxiRND * (eff_ma3) +beta_maastime12taxi1RND*(eff_ma1) +beta_maastime22taxi1RND*(eff_ma22) + beta_extraRND * extra + SIGMA_SH_MAASRND
#Alt3 = ASC_3_RND*dist_eff200+ASC_31_RND*dist_eff300 + beta_unitcost3_sRND * (vehkm / totcost)*dist_eff200 + beta_unitcost31RND * (vehkm / totcost)*dist_eff300 + beta_parktime3RND * (eff_own10)
#Alt4 = ASC_4_RND
#Shared_vehicle =  ASC_1 + beta_shunitcosttaxi1 *(vehkm/sharecost) + beta_shtime_taxi * (sharetime) + SIGMA_SH_MAASRND
#MaaS =  ASC_2+ beta_maascosttaxi *(vehkm/maascost) + beta_maastime22taxi * ( maastime1 + maastime2)  + beta_extra * extra  + SIGMA_SH_MAASRND
#Private_vehicle = ASC_3  + beta_parktime3 * (parktime) + beta_parkcost3 * (parkcost)
#Others = ASC_4

Shared_vehicle =  ASC_1* dtaxi + ASC_11*dshare + beta_shtaxi_sub_price *(sharecost)*dtaxi/10 + \
                  beta_sh_sub_price * sharecost *dshare/10 + beta_shtime * (sharetime)  + beta_dist * sharedist/10 +  SIGMA_SH_MAASRND

MaaS = ASC_2* dtaxi +ASC_21* dshare + beta_maascosttaxi *(maascost)*dtaxi/10 + beta_maascostshare * maascost * dshare/10 +\
       beta_maastime12taxi * (maastime1) + beta_maastime22taxi * (maastime2) + beta_extra * extra  + \
       beta_maasdisbike * maaskm2/10 + beta_maasdist * sharedist /10 +beta_inc2_package*inc_mid + beta_edu2_package * edu_WO +\
       beta_edu2_package * edu_HBO + beta_fam_package * fam_1 + beta_fam_package * fam_2 + beta_enthu * factor1  + beta_constructive * factor3 + \
       beta_travelzeal * factor4 + beta_fru * factor2 + beta_age_package * age_10_60  + SIGMA_SH_MAASRND + beta_freq * highfreq + beta_freq * mediumfreq

Private_vehicle = ASC_3 + beta_parktime3 * (parktime) + beta_parkcost3 * (parkcost)/10 + beta_dist3 * sharedist /10 + \
                  beta_edu2_private * edu_HBO + beta_edu2_private * edu_WO + beta_inc2_private*inc_mid + beta_fam_private * fam_1 + \
                  beta_fam_private * fam_2 + beta_age_private * age_60_abv
Others = ASC_4

#[Choice set and availability]
choiceset = {1: Shared_vehicle,2: MaaS,3: Private_vehicle,4: Others}
availability = {1: availability1,2: availability2,3: availability3,4: availability4}
obsprob = models.logit(choiceset, availability, choice)
condprobIndiv = PanelLikelihoodTrajectory(obsprob)

# We integrate over the random parameters using Monte-Carlo
logprob = log(MonteCarlo(condprobIndiv))
# Define level of verbosity
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
#logger.setGeneral()
logger.setDetailed()

# Create the Biogeme object
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=10)
biogeme.modelName = 'Mixed logit car'

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasCorrelations)
print(pandasGeneralStat)
print(pandasResults)