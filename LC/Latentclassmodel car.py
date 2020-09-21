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

# They are organized as panel data. The variable ID identifies each individual.
database.panel("ID")
globals().update(database.variables)

# Parameters to be estimated. One version for each latent class.
numberOfClasses = 2
ASC_1 = [Beta(f'ASC_1{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_11 = [Beta(f'ASC_11{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_2 = [Beta(f'ASC_2{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_21 = [Beta(f'ASC_21{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_3 = [Beta(f'ASC_3{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
ASC_4 = [Beta(f'ASC_4{i}', 0.1, None, None, 1) for i in range(numberOfClasses)]

beta_shcosttaxi1 = [Beta(f'beta_shcosttaxi1{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_shcostsharedcar = [Beta(f'beta_shcostsharedcar{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_shtime_taxi = [Beta(f'beta_shtime_taxi{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_dist = [Beta(f'beta_dist{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

beta_maascosttaxi = [Beta(f'beta_maascosttaxi{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maascostshare = [Beta(f'beta_maascostshare{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maastime12taxi = [Beta(f'beta_maastime12taxi{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maastime22taxi = [Beta(f'beta_maastime22taxi{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_extra = [Beta(f'beta_extra{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maasdist = [Beta(f'beta_maasdist{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_maasdisbike = [Beta(f'beta_maasdisbike{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

beta_parkcost3 = [Beta(f'beta_parkcost3{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_dist3 = [Beta(f'beta_dist3{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]
beta_parktime3 = [Beta(f'beta_parktime3{i}', 0.1, None, None, 0) for i in range(numberOfClasses)]

# Parameters for the class membership model
beta_enthu = Beta('beta_enthu', 0.1, None, None, 0)
beta_fru = Beta('beta_fru', 0.1, None, None, 0)
beta_constructive = Beta('beta_constructive', 0.1, None, None, 0)
beta_travelzeal = Beta('beta_travelzeal', 0.1, None, None, 0)
CLASS_MAAS = Beta('CLASS_MAAS', 0.1, None, None, 0)
beta_fam = Beta('beta_fam', 0.1, None, None, 0)
beta_gender = Beta('beta_gender', 0.1, None, None, 0)
beta_edu2 = Beta('beta_edu2', 0.1, None, None, 0)
beta_occ = Beta('beta_occ', 0.1, None, None, 0)
beta_inc2 = Beta('beta_inc2', 0.1, None, None, 0)
beta_age = Beta('beta_age', 0.1, None, None, 0)
beta_freq = Beta('beta_freq',0.1,None,None,0)
SIGMA_SH_MAAS_M = [Beta(f'SIGMA_SH_MAAS_M{i}', 0, None, None, 1) for i in range(numberOfClasses)]
SIGMA_SH_MAAS_STD = [Beta(f'SIGMA_SH_MAAS_STD{i}', 0, None, None, 0) for i in range(numberOfClasses)]
SIGMA_SH_MAASRND = [SIGMA_SH_MAAS_M[i] + SIGMA_SH_MAAS_STD[i] * bioDraws(f'SIGMA_SH_MAASRND{i}', 'NORMAL_HALTON5') for i in range(numberOfClasses)]

# Utility functions
V1 = [ASC_1[i]* dtaxi + ASC_11[i]*dshare + beta_shcosttaxi1[i] *(sharecost)*dtaxi/10 + beta_shcostsharedcar[i] * sharecost *dshare/10 +\
    beta_shtime_taxi[i] * (sharetime)  + beta_dist[i] * sharedist/10 + SIGMA_SH_MAASRND[i]  for i in range(numberOfClasses)]

V2 = [ASC_2[i]* dtaxi +ASC_21[i]* dshare + beta_maascosttaxi[i] *(maascost)*dtaxi/10 + beta_maascostshare[i] * maascost * dshare/10 +\
beta_maastime12taxi[i] * (maastime1) + beta_maastime22taxi[i] * (maastime2) + beta_extra[i] * extra  + \
beta_maasdisbike[i] * maaskm2/10 +beta_maasdist[i] * sharedist /10  + SIGMA_SH_MAASRND[i] for i in range(numberOfClasses)]

V3 = [ASC_3[i] + beta_parktime3[i] * (parktime) + beta_parkcost3[i] * (parkcost)/10 + beta_dist3[i] * sharedist/10 for i in range(numberOfClasses)]

V4 = [ASC_4[i] for i in range(numberOfClasses)]

V = [{1: V1[i],
      2: V2[i],
      3: V3[i],
      4: V4[i]} for i in range(numberOfClasses)]

# Associate the availability conditions with the alternatives
av = {1: availability1,2: availability2,3: availability3,4: availability4}
# The choice model is a discrete mixture of logit, with availability conditions
# We calculate the conditional probability for each class
prob = [PanelLikelihoodTrajectory(models.logit(V[i], av, choice)) for i in range(numberOfClasses)]

# Class membership model
W = CLASS_MAAS + beta_enthu * factor1  + beta_fru * factor2 + beta_inc2*inc_mid +\
beta_edu2 * edu_HBO + beta_fam * fam_1 + beta_fam * fam_2 + beta_age * age_10_60
PROB_class0 = models.logit({1: W, 0: 0}, None, 1)
PROB_class1 = models.logit({1: W, 0: 0}, None, 0)

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
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=5)
biogeme.modelName = 'Latent model for car'

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
pandasCorrelations = results.getCorrelationResults()
pandasGeneralStat = results.getGeneralStatistics()
print(pandasGeneralStat)
print(pandasResults)
