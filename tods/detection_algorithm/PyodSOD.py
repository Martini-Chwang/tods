from typing import Any, Callable, List, Dict, Union, Optional, Sequence, Tuple
from numpy import ndarray
from collections import OrderedDict
from scipy import sparse
import os
import sklearn
import numpy
import typing

# Custom import commands if any
import warnings
import numpy as np
from sklearn.utils import check_array
from sklearn.exceptions import NotFittedError
# from numba import njit
from pyod.utils.utility import argmaxn

from d3m.container.numpy import ndarray as d3m_ndarray
from d3m.container import DataFrame as d3m_dataframe
from d3m.metadata import hyperparams, params, base as metadata_base
from d3m import utils
from d3m.base import utils as base_utils
from d3m.exceptions import PrimitiveNotFittedError
from d3m.primitive_interfaces.base import CallResult, DockerContainer

# from d3m.primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase
from d3m.primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from d3m.primitive_interfaces.transformer import TransformerPrimitiveBase

from d3m.primitive_interfaces.base import ProbabilisticCompositionalityMixin, ContinueFitMixin
from d3m import exceptions
import pandas
import uuid

from d3m import container, utils as d3m_utils

from .UODBasePrimitive import Params_ODBase, Hyperparams_ODBase, UnsupervisedOutlierDetectorBase
from pyod.models.sod import SOD
# from typing import Union

Inputs = d3m_dataframe
Outputs = d3m_dataframe

from tods.utils import construct_primitive_metadata

class Params(Params_ODBase):
	######## Add more Attributes #######

	pass


class Hyperparams(Hyperparams_ODBase):
	######## Add more Hyperparamters #######

	n_neighbors = hyperparams.Hyperparameter[int](
		default=20,
		semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
		description="Number of neighbors to use by default for k neighbors queries.",
	)

	ref_set = hyperparams.Hyperparameter[int](
		default=10,
		semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
		description="specifies the number of shared nearest neighbors to create the reference set. Note that ref_set must be smaller than n_neighbors.",
	)

	alpha = hyperparams.Hyperparameter[float](
		default=0.8,
		semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
		description="specifies the lower limit for selecting subspace. 0.8 is set as default as suggested in the original paper.",
	)


class SODPrimitive(UnsupervisedOutlierDetectorBase[Inputs, Outputs, Params, Hyperparams]):
	"""	
	Subspace outlier detection (SOD) schema aims to detect outlier in
	varying subspaces of a high dimensional feature space. For each data
	object, SOD explores the axis-parallel subspace spanned by the data
	object's neighbors and determines how much the object deviates from the
	neighbors in this subspace.
	See :cite:`kriegel2009outlier` for details.

Parameters
----------
	n_neighbors : int, optional (default=20)
		Number of neighbors to use by default for k neighbors queries.
	ref_set: int, optional (default=10)
		specifies the number of shared nearest neighbors to create the
		reference set. Note that ref_set must be smaller than n_neighbors.
	alpha: float in (0., 1.), optional (default=0.8)
		   specifies the lower limit for selecting subspace.
		   0.8 is set as default as suggested in the original paper.
	contamination : float in (0., 0.5), optional (default=0.1)
		The amount of contamination of the data set, i.e.
		the proportion of outliers in the data set. Used when fitting to
		define the threshold on the decision function.

.. dropdown:: Attributes
	
	decision_scores_ : numpy array of shape (n_samples,)
		The outlier scores of the training data.
		The higher, the more abnormal. Outliers tend to have higher
		scores. This value is available once the detector is
		fitted.
	threshold_ : float
		The threshold is based on ``contamination``. It is the
		``n_samples * contamination`` most abnormal samples in
		``decision_scores_``. The threshold is calculated for generating
		binary outlier labels.
	labels_ : int, either 0 or 1
		The binary labels of the training data. 0 stands for inliers
		and 1 for outliers/anomalies. It is generated by applying
		``threshold_`` on ``decision_scores_``.
	"""

	metadata = construct_primitive_metadata(module='detection_algorithm', name='pyod_sod', id='SODPrimitive', primitive_family='anomaly_detect', hyperparams=['contamination', 'n_neighbors', 'ref_set', 'alpha'], description='Subspace Outlier Detection Primitive')


	def __init__(self, *,
				 hyperparams: Hyperparams, #
				 random_seed: int = 0,
				 docker_containers: Dict[str, DockerContainer] = None) -> None:
		super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)

		self._clf = SOD(contamination=hyperparams['contamination'],
						n_neighbors=hyperparams['n_neighbors'],
						ref_set=hyperparams['ref_set'],
						alpha=hyperparams['alpha'],
						)

	def set_training_data(self, *, inputs: Inputs) -> None:
		"""
		Set training data for outlier detection.
		Args:
			inputs: Container DataFrame
		Returns:
			None
		"""
		super().set_training_data(inputs=inputs)

	def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
		"""
		Fit model with training data.
		Args:
			*: Container DataFrame. Time series data up to fit.
		Returns:
			None
		"""
		return super().fit()

	def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
		"""
		Process the testing data.
		Args:
			inputs: Container DataFrame. Time series data up to outlier detection.
		Returns:
			Container DataFrame
			1 marks Outliers, 0 marks normal.
		"""
		return super().produce(inputs=inputs, timeout=timeout, iterations=iterations)

	def get_params(self) -> Params: # pragma: no cover
		"""
		Return parameters.
		Args:
			None
		Returns:
			class Params
		"""
		return super().get_params()

	def set_params(self, *, params: Params) -> None: # pragma: no cover
		"""
		Set parameters for outlier detection.
		Args:
			params: class Params
		Returns:
			None
		"""
		super().set_params(params=params)



