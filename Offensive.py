import os
import pickle
from Classifier.featx import bag_of_words

featx = lambda words: bag_of_words([word.lower() for word in words])

class Offensive():
    def __init__(self, clasi=None):
        try:
            if clasi == None:
                clasi = pickle.load(open(os.path.join("Classifier", "classifier.pickle")))

            self.clasi = clasi
        except:
            print "Failed to read clasifier"

    def is_offensive(self, text):
        return self.clasi.classify(featx(text.split())) == "neg"
