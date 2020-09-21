import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable

# Read the data
df = pd.read_csv('outside.dat', '\t')
database = db.Database('outside', df)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

# The following statement allows you to use the names of the variable
# as Python variable.
globals().update(database.variables)

MU = Beta('MU', 1, 1, 10, 0)
# Parameters to be estimated
ASC_1 = Beta('ASC_1',0,None, None,1)
ASC_11 = Beta('ASC_11',0,None, None,0)
ASC_2 = Beta('ASC_2',0,None, None,0)
ASC_21 = Beta('ASC_21',0,None, None,0)
ASC_3 = Beta('ASC_3',0,None, None,0)
ASC_31 = Beta('ASC_31',0,None, None,0)
ASC_4 = Beta('ASC_4',0,None, None,0)

beta_shtime = Beta('beta_shtime',0,None, None,0)
beta_shtime1 = Beta('beta_shtime1',0,None, None,0)
beta_shcostperdist1= Beta('beta_shcostperdist1',0,None, None,0)
beta_WTP_shtime = Beta('beta_WTP_shtime',0,None, None,0)
beta_dist = Beta('beta_dist',0,None, None,0)

beta_maascost = Beta('beta_maascost',0,None, None,0)
beta_maascostperdist2 = Beta('beta_maascostperdist2',0,None, None,0)
beta_nonebike_accesstime = Beta('beta_nonebike_accesstime',0,None, None,0)
beta_ebike_accesstime = Beta('beta_ebike_accesstime',0,None, None,0)
beta_WTP_nonebike_accesstime = Beta('beta_WTP_nonebike_accesstime',0,None, None,0)
beta_WTP_ebike_accesstime = Beta('beta_WTP_ebike_accesstime',0,None, None,0)
beta_maasdist = Beta('beta_maasdist',0,None, None,0)
beta_extra = Beta('beta_extra',0,None, None,0)
beta_maasdiscarsh = Beta('beta_distcarsh',0,None, None,0)
beta_maasdisbike = Beta('beta_distbike',0,None, None,0)
beta_fuel3 = Beta('beta_fuel3',0,None, None,0)
beta_totcost31 = Beta('beta_totcost31',0,None, None,0)
beta_totcostperdist = Beta('beta_totcostperdist',0,None, None,0)
# Definition of the utility functions

#Shared_vehicle =  ASC_1  + beta_shcostdist1 *(sharecost/distance) + beta_shtime * sharetime + SIGMA_SH_MAASRND
#MaaS = ASC_2 +  beta_maascost2dist1 *(maascost/distance) + beta_maastime1*maastime1 + beta_maastime2*maastime2  + beta_extra*(extra) + SIGMA_SH_MAASRND
#Continue_following_existing_way = ASC_3 + beta_totcost31 * (currcost/distance)
Shared_vehicle =   ASC_1  + beta_shcostperdist1 *(sharecost*10/distance) + beta_shtime * sharetime

MaaS = ASC_2 +  beta_maascostperdist2 *(maascost*10/distance)+ beta_nonebike_accesstime*(maastime1) + beta_ebike_accesstime* maastime2 +\
       beta_extra*(extra) *extra

Continue_following_existing_way = ASC_3 + beta_totcostperdist * (currcost*10/distance)

# Associate utility functions with the numbering of alternatives
choiceset = {1: Shared_vehicle,2: MaaS,3: Continue_following_existing_way}
availability = {1: availability1,2: availability2,3: availability3}

#Definition of nests:
# 1: nests parameter
# 2: list of alternatives
existing = MU, [1, 2]
future1 = 1.0, [3]
nests = existing, future1

# Definition of the model. This is the contribution of each
# observation to the log likelihood function.
# The choice model is a nested logit, with availability conditions
logprob = models.lognested(choiceset, availability, nests, choice)

# Define level of verbosity
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
logger.setGeneral()
#logger.setDetailed()

# Create the Biogeme object
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = "nested outside"

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasCorrelations)
print(pandasGeneralStat)
print(pandasResults)