import numpy as np

from models.base_model import BaseModel

class LogisticRegression(BaseModel):
    def __init__(self, alpha=0, eta0=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_type = 'logistic_regression'
        self.model_architecture["layer1"]=self.dataX.shape[1]
        self.alpha = alpha
        self.eta0 = eta0

        # Training parameters
        self.x_train, self.x_test, self.y_train, self.y_test = self._create_split(scaled=True)
        self.w, self.b = self.__init_weights(self.x_train[0])
        self.N = len(self.x_train)

        self.log_loss_train = []
        self.log_loss_test = []

    def train_step(self):
        for j in range(self.N):
            grad_dw = self.__gradient_dw(self.x_train[j], self.y_train[j], self.w, self.b, self.alpha, self.N)
            grad_db = self.__gradient_db(self.x_train[j], self.y_train[j], self.w, self.b)
            self.w = np.array(self.w) + (self.eta0 * np.array(grad_dw))
            self.b = self.b + (self.eta0 * grad_db)

        predict_train = []
        for m in range(len(self.y_train)):
            z = np.dot(self.w, self.x_train[m]) + self.b
            predict_train.append(self.__sigmoid(z))

        train_loss = self.__logloss(self.y_train, predict_train)

        predict_test = []
        for m in range(len(self.y_test)):
            z = np.dot(self.w, self.x_test[m]) + self.b
            predict_test.append(self.__sigmoid(z))

        test_loss = self.__logloss(self.y_test, predict_test)

        if self.log_loss_train and train_loss > self.log_loss_train[-1]:
            return self.w, self.b, self.log_loss_train, self.log_loss_test

        self.log_loss_train.append(train_loss)
        self.log_loss_test.append(test_loss)

        return self.w, self.b, self.log_loss_train, self.log_loss_test

    def get_train_progress(self):
        return self.w, self.b, self.log_loss_train, self.log_loss_test

    def __logloss(self, y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        return -1 * np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    def __gradient_dw(self, x, y, w ,b, alpha, N):
        dw = x * (y - self.__sigmoid(np.dot(w.T, x) + b)) - ((alpha * w * w) / N)
        return dw

    def __gradient_db(self, x, y, w, b):
        db = y - self.__sigmoid(np.dot(w.T, x) + b)
        return db

    def __init_weights(self, n_features):
        return np.zeros_like(n_features), 0

    def __sigmoid(self, z):
        return 1 / (1 + np.exp(-z))