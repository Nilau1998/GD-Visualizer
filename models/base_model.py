from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class BaseModel:
    def __init__(self):
        self.model_type = None
        self.model_architecture = dict()
        self.dataX = None
        self.dataY = None
        self.__create_dataset()
        self.current_epoch = 0

    def train_step(self):
        pass

    def get_model_architecture(self):
        return self.model_architecture

    def _create_split(self, ratio=0.75, scaled=False):
        x_train, x_test, y_train, y_test = train_test_split(self.dataX, self.dataY, train_size=ratio, random_state=15)

        if scaled:
            scaler = StandardScaler()
            x_train = scaler.fit_transform(x_train)
            x_test = scaler.transform(x_test)

        return x_train, x_test, y_train, y_test

    def __create_dataset(self):
        self.dataX, self.dataY = make_classification(n_samples = 50000, n_features = 15,
                    n_informative = 10, n_redundant = 5,
                    n_classes = 2, weights = [0.7],
                    class_sep = 0.7, random_state=15)