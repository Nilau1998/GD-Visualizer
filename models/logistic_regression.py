import numpy as np

from models.base_model import BaseModel

class LogisticRegression(BaseModel):
    def __init__(self, alpha=0, eta0=0):
        self.model_type = 'logistic_regression'
        self.alpha = alpha
        self.eta0 = eta0
        super().__init__()

    def train(self, epochs):
        x_train, x_test, y_train, y_test = self.__create_split(scaled=True)
        w, b = self.__init_weights(x_train[0])
        N = len(x_train)
        log_loss_train = []
        log_loss_test = []

        for i in range(0, epochs):
            for j in range(N):
                grad_dw = self.__gradient_dw(x_train[j], y_train[j], w, b, self.alpha, N)
                grad_db = self.__gradient_db(x_train[j], y_train[j], w, b)
                w = np.array(w) + (self.eta0 * np.array(grad_dw))
                b = b + (self.eta0 * grad_db)

            predict_train = []
            for m in range(len(y_train)):
                z = np.dot(w, x_train[m]) + b
                predict_train.append(self.__sigmoid(z))

            train_loss = self.__logloss(y_train, predict_train)

            predict_test = []
            for m in range(len(y_test)):
                z = np.dot(w, x_test[m]) + b
                predict_test.append(self.__sigmoid(z))

            test_loss = self.__logloss(y_test, predict_test)

            if log_loss_train and train_loss > log_loss_train[-1]:
                return w, b, log_loss_train, log_loss_test

            log_loss_train.append(train_loss)
            log_loss_test.append(test_loss)

        return w, b, log_loss_train, log_loss_test

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