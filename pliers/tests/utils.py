from os.path import dirname, join
from pliers.stimuli import ImageStim
from pliers.extractors.base import Extractor, ExtractorResult
from pliers.transformers import BatchTransformerMixin
import numpy as np
from copy import deepcopy


def get_test_data_path():
    """Returns the path to test datasets """
    return join(dirname(__file__), 'data')


class DummyExtractor(Extractor):

    ''' A dummy Extractor class that always returns random values when
    extract() is called. Can set the extractor name inside _extract() to
    facilitate testing of results merging etc. '''
    _input_type = ImageStim
    _log_attributes = ('param_A', 'param_B')

    def __init__(self, param_A=None, param_B='pie', name=None, n_rows=100,
                 n_cols=3, max_time=1000):
        super(DummyExtractor, self).__init__()
        self.param_A = param_A
        self.param_B = param_B
        if name is not None:
            self.name = name
        self.n_rows = n_rows
        self.n_cols = n_cols

    def _extract(self, stim):
        data = np.random.randint(0, 1000, (self.n_rows, self.n_cols))
        onsets = np.random.choice(self.n_rows*2, self.n_rows, False)
        return ExtractorResult(data, stim, deepcopy(self), onsets=onsets)

class DummyExactExtractor(Extractor):
    ''' A dummy Extractor that returns the value you give it on init '''
    _input_type = ImageStim
    _log_attributes = ('value', )

    def __init__(self, value):
        super(DummyExactExtractor, self).__init__()
        self.value = value

    def _extract(self, stim):
        return ExtractorResult([self.value], stim, deepcopy(self), features=['dummy'])

class DummyBatchExtractor(BatchTransformerMixin, Extractor):

    _input_type = ImageStim
    _batch_size = 3

    def __init__(self, *args, **kwargs):
        self.num_calls = 0
        super(DummyBatchExtractor, self).__init__(*args, **kwargs)

    def _extract(self, stims):
        self.num_calls += 1
        results = []
        for s in stims:
            results.append(ExtractorResult([[len(s.name)]], s, self))
        return results
