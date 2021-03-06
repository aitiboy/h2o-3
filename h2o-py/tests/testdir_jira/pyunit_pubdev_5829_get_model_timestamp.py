from builtins import range
import sys, os
sys.path.insert(1, os.path.join("..","..",".."))
import h2o
from tests import pyunit_utils
import numpy as np
from h2o.estimators.gbm import H2OGradientBoostingEstimator


def test_api_returns_the_same_timestamp():
    prostate_train = h2o.import_file(path=pyunit_utils.locate("smalldata/logreg/prostate_train.csv"))

    #Log.info("Converting CAPSULE and RACE columns to factors...\n")
    prostate_train["CAPSULE"] = prostate_train["CAPSULE"].asfactor()

    # Import prostate_train.csv as numpy array for scikit comparison
    trainData = np.loadtxt(pyunit_utils.locate("smalldata/logreg/prostate_train.csv"), delimiter=',', skiprows=1)

    ntrees = 1
    learning_rate = 0.1
    depth = 5
    min_rows = 10

    # Build H2O GBM classification model:
    gbm_h2o = H2OGradientBoostingEstimator(ntrees=ntrees, learn_rate=learning_rate,
                                           max_depth=depth,
                                           min_rows=min_rows,
                                           distribution="bernoulli",
                                           model_id="test_timestamp")
    gbm_h2o.train(x=list(range(1,prostate_train.ncol)),y="CAPSULE", training_frame=prostate_train)

    model = h2o.get_model(model_id="test_timestamp")
    models = h2o.api("GET /3/Models")
    assert model._model_json['timestamp'] == models["models"][0]["timestamp"], "Timestamp should be the same."

if __name__ == "__main__":
    pyunit_utils.standalone_test(test_api_returns_the_same_timestamp)
else:
    test_api_returns_the_same_timestamp()
