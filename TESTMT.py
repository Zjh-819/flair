import torch

import flair
from flair.data import Corpus, Sentence
from flair.embeddings import DocumentRNNEmbeddings, StackedEmbeddings, TransformerWordEmbeddings, \
    TransformerDocumentEmbeddings
from flair.models.text_classification_model import RefactoredTARSClassifier
from flair.tokenization import SegtokTokenizer
from flair.trainers import ModelTrainer
from flair.datasets import TREC_50, CSVClassificationCorpus, SentenceDataset, CONLL_03
import random

def main():
    # ----- CORPORA -----
    trec50_label_name_map = {
        'ENTY:sport': 'question about entity sport',
        'ENTY:dismed': 'question about entity diseases medicine',
        'LOC:city': 'question about location city',
        'DESC:reason': 'question about description reasons',
        'NUM:other': 'question about number other',
        'LOC:state': 'question about location state',
        'NUM:speed': 'question about number speed',
        'NUM:ord': 'question about number order ranks',
        'ENTY:event': 'question about entity event',
        'ENTY:substance': 'question about entity element substance',
        'NUM:perc': 'question about number percentage fractions',
        'ENTY:product': 'question about entity product',
        'ENTY:animal': 'question about entity animal',
        'DESC:manner': 'question about description manner of action',
        'ENTY:cremat': 'question about entity creative pieces inventions books',
        'ENTY:color': 'question about entity color',
        'ENTY:techmeth': 'question about entity technique method',
        'NUM:dist': 'question about number distance measure',
        'NUM:weight': 'question about number weight',
        'LOC:mount': 'question about location mountains',
        'HUM:title': 'question about person title',
        'HUM:gr': 'question about person group organization of persons',
        'HUM:desc': 'question about person description',
        'ABBR:abb': 'question about abbreviation abbreviation',
        'ENTY:currency': 'question about entity currency',
        'DESC:def': 'question about description definition',
        'NUM:code': 'question about number code',
        'LOC:other': 'question about location other',
        'ENTY:other': 'question about entity other',
        'ENTY:body': 'question about entity body organ',
        'ENTY:instru': 'question about entity musical instrument',
        'ENTY:termeq': 'question about entity term equivalent',
        'NUM:money': 'question about number money prices',
        'NUM:temp': 'question about number temperature',
        'LOC:country': 'question about location country',
        'ABBR:exp': 'question about abbreviation expression',
        'ENTY:symbol': 'question about entity symbol signs',
        'ENTY:religion': 'question about entity religion',
        'HUM:ind': 'question about person individual',
        'ENTY:letter': 'question about entity letters characters',
        'NUM:date': 'question about number date',
        'ENTY:lang': 'question about entity language',
        'ENTY:veh': 'question about entity vehicle',
        'NUM:count': 'question about number count',
        'ENTY:word': 'question about entity word special property',
        'NUM:period': 'question about number period lasting time',
        'ENTY:plant': 'question about entity plant',
        'ENTY:food': 'question about entity food',
        'NUM:volsize': 'question about number volume size',
        'DESC:desc': 'question about description description'
    }
    trec: Corpus = TREC_50(label_name_map=trec50_label_name_map)

    # ----- TAG SPACES -----
    trec_dictionary = trec.make_label_dictionary()

    # ----- SHARED RNN LAYERS -----
    shared_rnn_layer_classification: TransformerDocumentEmbeddings= TransformerDocumentEmbeddings("distilbert-base-uncased",
                                                                                                  fine_tune=True,
                                                                                                  batch_size=16)

    tars = TARSClassifier(
        task_name="trec",
        label_dictionary=trec_dictionary,
        document_embeddings=shared_rnn_layer_classification
    )
    trainer = ModelTrainer(tars, trec)
    trainer.train(base_path="output",
                  learning_rate=0.02,
                  mini_batch_size=16,
                  max_epochs=10,
                  embeddings_storage_mode='none')


    # ----- MULTITASK CORPUS -----
    multi_corpus = MultitaskCorpus(
        {"corpus": trec6, "model": trec_classifier},
        {"corpus": subj, "model": subj_classifier},
        {"corpus": conll03, "model": ner_tagger},
        {"corpus": conll03, "model": pos_tagger}
    )

    # ----- MULTITASK MODEL -----
    multitask_model: MultitaskModel = MultitaskModel(multi_corpus.models)

    # ----- TRAINING ON MODEL AND CORPUS -----
    trainer: ModelTrainer = ModelTrainer(multitask_model, multi_corpus)
    trainer.train('results/multitask-1',
                  learning_rate=0.1,
                  mini_batch_size=64,
                  max_epochs=3)

if __name__ == "__main__":
    main()