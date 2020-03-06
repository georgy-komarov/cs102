import math

import pymorphy2


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.morph = pymorphy2.MorphAnalyzer()

        self.alpha = alpha
        self.words = {}
        self.words_proba = {}
        self.counters = {"good": 0, "maybe": 0, "never": 0}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        for i, title in enumerate(X):
            for word in title.lower().split():
                nominal_form = self.morph.parse(word)[0].normal_form

                if not nominal_form in self.words:
                    self.words[nominal_form] = dict.fromkeys(self.counters.keys(), 0)

                if not nominal_form in self.words_proba:
                    self.words_proba[nominal_form] = dict.fromkeys(self.counters.keys(), 0)

                self.words[nominal_form][y[i]] += 1
            self.counters[y[i]] += 1

        for word in self.words:
            for label in self.counters.keys():
                nc = sum([self.words[word][label] for word in self.words])
                nic = self.words[word][label]
                self.words_proba[word][label] = (nic + self.alpha) / (nc + len(self.words.keys()) * self.alpha)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        results = []

        for i, title in enumerate(X):
            probabilities = dict.fromkeys(self.counters.keys(), 0)

            for label in probabilities:
                proba = self.counters[label] / sum(self.counters.values())
                probabilities[label] = math.log(proba) if proba != 0 else -100000

            for word in title.lower().split():
                nominal_form = self.morph.parse(word)[0].normal_form

                for label in self.counters.keys():
                    if nominal_form in self.words_proba:
                        probabilities[label] += math.log(self.words_proba[nominal_form][label])

            max_proba = max(probabilities, key=lambda label: probabilities[label])
            results.append(max_proba)

        return results

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y_predicted = self.predict(X_test)
        results = [predicted == real for predicted, real in zip(y_predicted, y_test)]
        accuracy = results.count(True) / len(results)

        return accuracy
