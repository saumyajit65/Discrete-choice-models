

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable

# Read the data
df = pd.read_csv('comboall.dat', '\t')
database = db.Database('comboall', df)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

# The following statement allows you to use the names of the variable
# as Python variable.
globals().update(database.variables)

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) &
#           (database.data.PURPOSE != 3)) |
#          (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)


# Parameters to be estimated
ASC_1 = Beta('ASC_1',0,None,None,0)
ASC_11 = Beta('ASC_11',0,None,None,0)
ASC_2 = Beta('ASC_2',0,None,None,0)
ASC_21 = Beta('ASC_21',0,None,None,0)
ASC_3 = Beta('ASC_3',0,None,None,0)
ASC_31 = Beta('ASC_31',0,None,None,0)
ASC_4 = Beta('ASC_4',0,None,None,1)
ASC_41 = Beta('ASC_41',0,None,None,1)

beta_shcosttaxi1 = Beta('beta_shcosttaxi1',0,None,None,0)
beta_shcosttaxi2 = Beta('beta_shcosttaxi2',0,None,None,0)
beta_shcostsharedcar = Beta('beta_shcostsharedcar',0,None,None,0)
beta_shcostsharedcar2=Beta('beta_shcostsharedcar2',0,None,None,0)
beta_shtime_taxi = Beta('beta_shtimetaxi',0,None,None,0)
beta_shtime_taxi1 = Beta('beta_shtimetaxi1',0,None,None,0)
beta_shtime_share = Beta('beta_shtimeshare',0,None,None,0)
beta_shtime_share1 = Beta('beta_shtimeshare1',0,None,None,0)
beta_dist = Beta('beta_dist',0,None,None,0)

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
beta_extra1 = Beta('beta_extra1',0,None,None,0)
beta_maasdiscartaxi = Beta('beta_distcartaxi',0,None,None,0)
beta_maasdiscarsh = Beta('beta_distcarsh',0,None,None,0)
beta_maasdisbike = Beta('beta_distbike',0,None,None,0)
beta_maasdist = Beta('beta_maasdist',0,None, None,0)

beta_fuel3 = Beta('beta_fuel3',0,None,None,0)
beta_parkcost3 = Beta('beta_parkcost3',0,None,None,0)
beta_unitcost31 = Beta('beta_unitcost31',0,None,None,0)
beta_unitcost39 = Beta('beta_unitcost39',0,None,None,0)
beta_unitcost319 = Beta('beta_unitcost319',0,None,None,0)
beta_totcost3 = Beta('beta_totcost3',0,None,None,0)
beta_dist3 = Beta('beta_dist3',0,None,None,0)
beta_parktime3 = Beta('beta_parktime3',0,None,None,0)
beta_parktime23 = Beta('beta_parktime23',0,None,None,0)

MU = Beta('MU', 1,None,None,0)

# Definition of the utility functions
Shared_vehicle =  ASC_1* dtaxi + ASC_11*dshare + beta_shcosttaxi1 *(sharecost)*dtaxi/10 + \
                  beta_shcostsharedcar * sharecost *dshare/10 + beta_shtime_taxi * (sharetime)  + beta_dist * sharedist/10
MaaS = ASC_2* dtaxi +ASC_21* dshare + beta_maascosttaxi *(maascost/10)*dtaxi + beta_maascostshare * maascost * dshare/10 +\
       beta_maastime12taxi * (maastime1) + beta_maastime22taxi * (maastime2) + beta_extra * extra  + beta_maasdisbike * maaskm2/10+\
       beta_maasdist*sharedist/10
Private_vehicle = ASC_3  + beta_parktime3 * (parktime) + beta_parkcost3 * (parkcost)/10 + beta_dist3 * sharedist /10
Others = ASC_4

#[Choice set and availability]
choiceset = {1: Shared_vehicle,2: MaaS,3: Private_vehicle,4: Others}
availability = {1: availability1,2: availability2,3: availability3,4: availability4}

#Definition of nests:
# 1: nests parameter
# 2: list of alternatives
existing = MU, [1, 2]
future1 = 1.0, [3]
future2 = 1.0, [4]
nests = existing, future1,future2

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
biogeme.modelName = "nested car"

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasCorrelations)
print(pandasGeneralStat)
print(pandasResults)
