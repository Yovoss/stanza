"""
Processor that attaches a sentiment score to a sentence
"""

import stanza.models.classifier as classifier

from stanza.models.common import doc
from stanza.models.common.pretrain import Pretrain
from stanza.pipeline._constants import *
from stanza.pipeline.processor import UDProcessor

class SentimentProcessor(UDProcessor):
    # set of processor requirements this processor fulfills
    PROVIDES_DEFAULT = set([SENTIMENT])
    # set of processor requirements for this processor
    REQUIRES_DEFAULT = set([TOKENIZE])

    def _set_up_model(self, config, use_gpu):
        # get pretrained word vectors
        self._pretrain = Pretrain(config['pretrain_path'])
        # set up model
        self._model = classifier.load(filename=config['model_path'], pretrain=self._pretrain)

        # TODO: move this call to load()
        if use_gpu:
            self._model.cuda()

    def process(self, document):
        classifier.label_document(self._model, document)
        return document
