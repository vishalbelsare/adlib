# iterative_retraining_learner.py
# A learner that iteratively retrains and removes outliers based on loss.
# Matthew Sedam

from adlib.learners.learner import learner
from adlib.learners.simple_learner import SimpleLearner
from adlib.utils.common import logistic_loss
from data_reader.binary_input import Instance
from copy import deepcopy
from typing import Dict
import numpy as np


class IterativeRetrainingLearner(learner):
    """
    A learner that iteratively retrains and removes outliers based on loss.
    """

    def __init__(self, lnr: SimpleLearner, training_instances: Instance):
        learner.__init__(self)

        self.learner = lnr
        self.learner.set_training_instances(training_instances)
        self.learner.train()

        self.set_training_instances(training_instances)
        self.orig_training_instances = deepcopy(training_instances)
        self.loss_threshold = None

    def train(self):
        loss = logistic_loss(self.training_instances, self.learner)
        mean = np.mean(loss)
        std = np.std(loss)
        self.loss_threshold = mean + 1.5 * std

        old_training_instances = self.training_instances[:]
        while set(old_training_instances) != set(self.training_instances):
            for i, inst in enumerate(self.training_instances):
                if loss[i] >= self.loss_threshold:
                    del self.training_instances[i]

            loss = logistic_loss(self.training_instances, self.learner)
            mean = np.mean(loss)
            std = np.std(loss)
            self.loss_threshold = mean + 1.5 * std

            self.learner.set_training_instances(self.training_instances)
            self.learner.train()

        self.learner.set_training_instances(self.training_instances)
        self.learner.train()

    def predict(self, instances):
        return self.learner.predict(instances)

    def set_params(self, params: Dict):
        raise NotImplementedError

    def predict_proba(self, X):
        raise NotImplementedError

    def decision_function(self, X):
        raise NotImplementedError
