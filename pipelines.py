from mapreduce import base_handler
from mapreduce.mapreduce_pipeline import MapreducePipeline
import logging
import re


class WordCountPipeline(base_handler.PipelineBase):
    """A pipeline to run word count"""

    def run(self, filekey, blobkey, with_combiner=False):
        logging.debug("Running word count without combiners")

        combiner = ''
        mapper = 'pipelines.word_count_map'
        reducer = 'pipelines.word_count_reduce'

        output = yield MapreducePipeline(
            'word_count',
            mapper,
            reducer,
            'mapreduce.input_readers.BlobstoreZipInputReader',
            'mapreduce.output_writers.BlobstoreOutputWriter',
            mapper_params={
                'blob_key': blobkey,
            },
            combiner_spec=combiner,
            reducer_params={
                'mime_type': 'text/plain',
            },
            shards=16
        )

# Mappers and Reducers


def word_count_map(data):
    (entry, text_fn) = data
    text = text_fn()

    for s in split_into_sentences(text):
        for w in split_into_words(s.lower()):
            yield (w, "")


def word_count_reduce(key, values):
    yield "%s: %d\n" % (key, len(values))


# Utility functions
def split_into_sentences(s):
    """Split text into list of sentences."""
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[\\.\\?\\!]", "\n", s)
    return s.split("\n")


def split_into_words(s):
    """Split a sentence into list of words."""
    s = re.sub(r"\W+", " ", s)
    s = re.sub(r"[_0-9]+", " ", s)
    return s.split()


def remove_whitespaces(s):
    s = re.sub(r"\s+", "", s)
    return s


