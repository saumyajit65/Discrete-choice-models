
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable, bioDraws, \
    PanelLikelihoodTrajectory, MonteCarlo, log

# Read the data
df = pd.read_csv('outside.dat', '\t')
database = db.Database('outside', df)
database.panel("ID")
# They are organized as panel data. The variable ID identifies each individual.
globals().update(database.variables)

# Parameters to be estimated
ASC_1 = Beta('ASC_1',0,None, None,1)
ASC_11 = Beta('ASC_11',0,None, None,0)
ASC_2 = Beta('ASC_2',0,None, None,0)
ASC_21 = Beta('ASC_21',0,None, None,0)
ASC_3 = Beta('ASC_3',0,None, None,0)
ASC_31 = Beta('ASC_31',0,None, None,0)
ASC_4 = Beta('ASC_4',0,None, None,0)
# Shared error parameters, fix the mean-parameter to 0
SIGMA_SH_MAAS_M = Beta('SIGMA_SH_MAAS_M', 0,None, None,1)
SIGMA_SH_MAAS_STD = Beta('SIGMA_SH_MAAS_STD', 0,None, None,0)
SIGMA_SH_MAASRND = SIGMA_SH_MAAS_M + SIGMA_SH_MAAS_STD * bioDraws('SIGMA_SH_MAASRND','NORMAL')

beta_fam_package = Beta('beta_fam_package',0,None, None,0)
beta_fam_private = Beta('beta_fam_private',0,None, None,0)
beta_age_package = Beta('beta_age_package',0,None, None,0)
beta_edu2_package = Beta('beta_edu2_package',0,None, None,0)
beta_edu2_private = Beta('beta_edu2_private',0,None, None,0)
beta_inc2_package = Beta('beta_inc2_package',0,None, None,0)
beta_inc2_private = Beta('beta_inc2_private',0,None, None,0)
beta_age_private = Beta('beta_age_private',0,None, None,0)

beta_enthu = Beta('beta_enthu',0,None, None,0)
beta_fru = Beta('beta_fru',0,None, None,0)
beta_constructive = Beta('beta_constructive',0,None, None,0)
beta_travelzeal = Beta('beta_travelzeal',0,None, None,0)
beta_age = Beta('beta_age',0,None, None,0)

beta_shtime = Beta('beta_shtime',0,None, None,0)
beta_WTP_shtime = Beta('beta_WTP_shtime',0,None, None,0)
beta_shcostperdist1= Beta('beta_shcostperdist1',0,None, None,0)
beta_shcostdist2= Beta('beta_shcostdist2',0,None, None,0)
beta_dist = Beta('beta_dist',0,None, None,0)
beta_maascost = Beta('beta_maascost',0,None, None,0)
beta_maascostperdist2 = Beta('beta_maascostperdist2',0,None, None,0)
beta_nonebike_accesstime = Beta('beta_nonebike_accesstime',0,None, None,0)
beta_ebike_accesstime = Beta('beta_ebike_accesstime',0,None, None,0)
beta_WTP_nonebike_accesstime = Beta('beta_WTP_nonebike_accesstime',0,None, None,0)
beta_WTP_ebike_accesstime = Beta('beta_WTP_ebike_accesstime',0,None, None,0)
beta_maasdist = Beta('beta_maasdist',0,None, None,0)
beta_extra = Beta('beta_extra',0,None, None,0)
beta_freq = Beta('beta_freq',0,None,None,0)
beta_maasdiscarsh = Beta('beta_distcarsh',0,None, None,0)
beta_maasdisbike = Beta('beta_distbike',0,None, None,0)
beta_fuel3 = Beta('beta_fuel3',0,None, None,0)
beta_totcost31 = Beta('beta_totcost31',0,None, None,0)
beta_totcostperdist = Beta('beta_totcostperdist',0,None, None,0)
# Definition of the utility functions

#Shared_vehicle =  ASC_1  + beta_shcostdist1 *(sharecost/distance) + beta_shtime * sharetime + SIGMA_SH_MAASRND
#MaaS = ASC_2 +  beta_maascost2dist1 *(maascost/distance) + beta_maastime1*maastime1 + beta_maastime2*maastime2  + beta_extra*(extra) + SIGMA_SH_MAASRND
#Continue_following_existing_way = ASC_3 + beta_totcost31 * (currcost/distance)
Shared_vehicle =   ASC_1  + beta_shcostperdist1 *(sharecost*10/distance) + beta_shtime * sharetime + SIGMA_SH_MAASRND

MaaS = ASC_2 +  beta_maascostperdist2 *(maascost*10/distance)+ beta_nonebike_accesstime*(maastime1) + beta_ebike_accesstime* maastime2 +\
       beta_extra*(extra) *extra +\
       beta_enthu * factor1 + beta_fru * factor2  + beta_constructive * factor3 + beta_travelzeal * factor4 + beta_age_package * age_10_60 +\
       beta_edu2_package * edu_WO +beta_edu2_package * edu_HBO + beta_inc2_package*inc_mid  + SIGMA_SH_MAASRND + beta_freq * highfreq + beta_freq * mediumfreq

Continue_following_existing_way = ASC_3 + beta_totcostperdist * (currcost*10/distance) + beta_age_private * age_60_abv + \
                                  beta_edu2_private * edu_WO + beta_edu2_private * edu_HBO + beta_inc2_private*inc_mid

# Associate utility functions with the numbering of alternatives
choiceset = {1: Shared_vehicle,2: MaaS,3: Continue_following_existing_way}
availability = {1: availability1,2: availability2,3: availability3}


# Definition of the model. This is the contribution of each
# observation to the log likelihood function.
# The choice model is a nested logit, with availability conditions
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
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=50)
biogeme.modelName = 'Mixed logit outside'

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasCorrelations)
print(pandasGeneralStat)
print(pandasResults)