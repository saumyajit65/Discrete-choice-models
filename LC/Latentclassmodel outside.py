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

# They are organized as panel data. The variable ID identifies each individual.
database.panel("ID")
globals().update(database.variables)

# Parameters to be estimated. One version for each latent class.
numberOfClasses = 2
ASC_1 = [Beta(f'ASC_1{i}', 0.1, None, None, 1) for i in range(numberOfClasses)]
ASC_2 = [Beta(f'ASC_2{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_3 = [Beta(f'ASC_3{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

beta_shcostperdist1 = [Beta(f'beta_shcostperdist1{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_shtime = [Beta(f'beta_shtime{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_sharedist = [Beta(f'beta_sharedist{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

beta_maascostperdist2 = [Beta(f'beta_maascostperdist2{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maastime1 = [Beta(f'beta_maastime1{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maastime2 = [Beta(f'beta_maastime2{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_extra = [Beta(f'beta_extra{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maasdist = [Beta(f'beta_maasdist{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maasdisbike = [Beta(f'beta_maasdisbike{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

beta_totcostperdist = [Beta(f'beta_totcostperdist{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

# Parameters for the class membership model
beta_enthu_class1 = Beta('beta_enthu_class1', 0.1, None, None, 0)
beta_fru_class1 = Beta('beta_fru_class1', 0.1, None, None, 0)
CLASS_MAAS_1 = Beta('CLASS_MAAS_1', 0.1, None, None, 0)
beta_fam_1 = Beta('beta_fam_1', 0.1, None, None, 0)
beta_edu2_1 = Beta('beta_edu2_1', 0.1, None, None, 0)
beta_inc2_1 = Beta('beta_inc2_1', 0.1, None, None, 0)
beta_enthu_class2 = Beta('beta_enthu_class2', 0.1, None, None, 0)
beta_fru_class2 = Beta('beta_fru_class2', 0.1, None, None, 0)
CLASS_MAAS_2 = Beta('CLASS_MAAS_2', 0.1, None, None, 0)
beta_fam_2 = Beta('beta_fam_2', 0.1, None, None, 0)
beta_edu2_2 = Beta('beta_edu2_2', 0.1, None, None, 0)
beta_inc2_1 = Beta('beta_inc2_1', 0.1, None, None, 0)
beta_age = Beta('beta_age',0.1,None, None,0)
beta_freq = Beta('beta_freq',0.1,None,None,0)
SIGMA_SH_MAAS_M = [Beta(f'SIGMA_SH_MAAS_M{i}', 0, None, None, 1) for i in range(numberOfClasses)]
SIGMA_SH_MAAS_STD = [Beta(f'SIGMA_SH_MAAS_STD{i}', 0, None, None, 0) for i in range(numberOfClasses)]
SIGMA_SH_MAASRND = [SIGMA_SH_MAAS_M[i] + SIGMA_SH_MAAS_STD[i] * bioDraws(f'SIGMA_SH_MAASRND{i}', 'NORMAL_HALTON5') for i in range(numberOfClasses)]

# Utility functions
V1 = [ASC_1[i]  + beta_shcostperdist1[i] *(sharecost/distance) + beta_shtime[i] * sharetime  + SIGMA_SH_MAASRND[i]  for i in range(numberOfClasses)]

V2 = [ASC_2[i] +  beta_maascostperdist2[i] *(maascost/distance)+ beta_maastime1[i]*(maastime1) + beta_maastime2[i]* maastime2  +\
beta_extra[i]*(extra) *extra + SIGMA_SH_MAASRND[i]  for i in range(numberOfClasses)]

V3 = [ASC_3[i] + beta_totcostperdist[i] * (currcost/distance) for i in range(numberOfClasses)]

V = [{1: V1[i],
      2: V2[i],
      3: V3[i]} for i in range(numberOfClasses)]

# Associate the availability conditions with the alternatives
av = {1: availability1,2: availability2,3: availability3}
# The choice model is a discrete mixture of logit, with availability conditions
# We calculate the conditional probability for each class
prob = [PanelLikelihoodTrajectory(models.logit(V[i], av, choice)) for i in range(numberOfClasses)]

# Class membership model
W = CLASS_MAAS_1 + beta_enthu_class1 * factor1  + beta_fru_class1 * factor2  + beta_edu2_1 * edu_HBO + \
    beta_inc2_1*inc_mid + beta_age * age_10_60 + beta_freq * mediumfreq
PROB_class0 = models.logit({0: W, 1: 0}, None, 0)
PROB_class1 = models.logit({0: W, 1: 0}, None, 1)

# Conditional to the random variables, likelihood for the individual.
probIndiv = PROB_class0 * prob[0] + PROB_class1 * prob[1]
# We integrate over the random variables using Monte-Carlo
logprob = log(MonteCarlo(probIndiv))

# Define level of verbosity
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
logger.setGeneral()
logger.setDetailed()

# Create the Biogeme object
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=20)
biogeme.modelName = 'Latent model for outside'

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasGeneralStat)
print(pandasResults)
