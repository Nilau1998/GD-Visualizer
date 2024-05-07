if "__main__" == __name__:
    logistic_regression = LogisticRegression(alpha=0.0001, eta0=0.0001)
    w, b, log_loss_train, log_loss_test = logistic_regression.train(1)

    # Plotting log_loss_train
    plt.subplot(1, 2, 1)
    plt.plot(log_loss_train)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    # Plotting log_loss_test
    plt.subplot(1, 2, 2)
    plt.plot(log_loss_test)
    plt.title('Testing Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    # Adjusting the layout
    plt.tight_layout()

    # Displaying the plot
    plt.savefig('logistic_regression.png', dpi=300)