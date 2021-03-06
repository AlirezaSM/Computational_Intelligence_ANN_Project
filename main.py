import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time


# A function to plot images
def show_image(img):
    image = img.reshape((28, 28))
    plt.imshow(image, 'gray')


# The sigmoid function
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))


# The sigmoid derivation function
def sigmoid_deriv(z):
    return sigmoid(z) * (1 - sigmoid(z))


# A function for feedforward calculation
def feedforward(x, w, a, b, z):
    z[0] = np.add(np.matmul(w[0], x), b[0])
    a[0] = sigmoid(z[0])
    for i in range(1, 3):
        z[i] = np.add(np.matmul(w[i], a[i - 1]), b[i])
        a[i] = sigmoid(z[i])
    return a, z


# Reading The Train Set
train_images_file = open('train-images.idx3-ubyte', 'rb')
train_images_file.seek(4)
num_of_train_images = int.from_bytes(train_images_file.read(4), 'big')
train_images_file.seek(16)

train_labels_file = open('train-labels.idx1-ubyte', 'rb')
train_labels_file.seek(8)

train_set = []
for n in range(num_of_train_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i, 0] = int.from_bytes(train_images_file.read(1), 'big') / 256

    label_value = int.from_bytes(train_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1

    train_set.append((image, label))
print("[STATUS] Train set loaded!")

# Reading The Test Set
test_images_file = open('t10k-images.idx3-ubyte', 'rb')
test_images_file.seek(4)

test_labels_file = open('t10k-labels.idx1-ubyte', 'rb')
test_labels_file.seek(8)

num_of_test_images = int.from_bytes(test_images_file.read(4), 'big')
test_images_file.seek(16)

test_set = []
for n in range(num_of_test_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i] = int.from_bytes(test_images_file.read(1), 'big') / 256

    label_value = int.from_bytes(test_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1

    test_set.append((image, label))
print("[STATUS] Test set loaded!")

# # Plotting an image
# show_image(train_set[0][0])
# plt.show()
# # Print label of image
# print(np.argmax(train_set[0][1]))
print("[STATUS] Learning started!")
start = time.time()
# Initialize weights with standard normal distribution
w = [np.random.standard_normal(size=(16, 784)), np.random.standard_normal(size=(16, 16)),
     np.random.standard_normal(size=(10, 16))]
# Initialize bias with zero matrix
b = [np.zeros((16, 1)), np.zeros((16, 1)), np.zeros((10, 1))]
# Initialize activations with zero matrix
a = [np.zeros((16, 1)), np.zeros((16, 1)), np.zeros((10, 1))]
# Initialize z with zero matrix
z = [np.zeros((16, 1)), np.zeros((16, 1)), np.zeros((10, 1))]
print("[STATUS] w, b, a, z matrix initialized!")

# Set learning_rate, number_of_epochs and batch_size
learning_rate = 1
number_of_epochs = 5
batch_size = 50

# Create a short train_set
short_train_set = train_set

cost = np.zeros((number_of_epochs, 1))
# For i from 0 to number_of_epochs
for i in range(number_of_epochs):

    # Shuffle the train set
    random.shuffle(short_train_set)
    # For each batch in train set
    for j in range(math.ceil(len(short_train_set)/batch_size)):

        # Initialize gradiant vector of weight
        grad_w = [np.zeros((16, 784)), np.zeros((16, 16)), np.zeros((10, 16))]
        # Initialize gradiant vector of bias
        grad_b = [np.zeros((16, 1)), np.zeros((16, 1)), np.zeros((10, 1))]

        # For each image in batch
        for k in range(batch_size):

            # Compute th output for this image
            a, z = feedforward(short_train_set[(j * batch_size) + k][0], w, a, b, z)
            cost[i] += np.sum(np.power(np.subtract(a[2], short_train_set[(j * batch_size) + k][1]), 2))

            # # Calculate gradient vector of weight and bias for last layer
            # for p in range(10):
            #     for q in range(16):
            #         grad_w[2][p][q] += a[1][q] * sigmoid_deriv(z[2][p]) * (2 * a[2][p] - 2 * short_train_set[(j * batch_size) + k][1][p])
            #         grad_b[2][p] += sigmoid_deriv(z[2][p]) * (2 * a[2][p] - 2 * short_train_set[(j * batch_size) + k][1][p])
            # # print(f"[STATUS] Last layer gradient finished for sample {k} in batch {j}")

            # Vectorized
            grad_w[2] += (2 * sigmoid_deriv(z[2]) * (a[2] - short_train_set[(j * batch_size) + k][1])) @ (np.transpose(a[1]))
            grad_b[2] += (2 * sigmoid_deriv(z[2]) * (a[2] - short_train_set[(j * batch_size) + k][1]))

            grad_a1 = np.zeros((16,1))
            # for q in range(16):
            #     for p in range(10):
            #         grad_a1[q][0] += w[2][p][q] * sigmoid_deriv(z[2][p]) * (2 * a[2][p] - 2 * short_train_set[(j * batch_size) + k][1][p])

            # Vectorized
            grad_a1 = np.transpose(w[2]) @ (2 * sigmoid_deriv(z[2]) * (a[2] - short_train_set[(j * batch_size) + k][1]))

            # # Calculate gradient vector of weight and bias for second layer
            # for q in range(16):
            #     for r in range(16):
            #         grad_w[1][q][r] += a[0][r] * sigmoid_deriv(z[1][q]) * grad_a1[q]
            #         grad_b[1][q] += sigmoid_deriv(z[1][q]) * grad_a1[q]
            # # print(f"[STATUS] second layer gradient finished for sample {k} in batch {j}")

            # Vectorized
            grad_w[1] += (sigmoid_deriv(z[1]) * grad_a1) @ (np.transpose(a[0]))
            grad_b[1] += (sigmoid_deriv(z[1]) * grad_a1)

            grad_a0 = np.zeros((16, 1))
            # for q in range(16):
            #     for p in range(16):
            #         grad_a0[q][0] += w[1][p][q] * sigmoid_deriv(z[1][p]) * grad_a1[p]

            # Vectorized
            grad_a0 = np.transpose(w[1]) @ (sigmoid_deriv(z[1]) * grad_a1)

            # # Calculate gradient vector of weight and bias for first layer
            # for p in range(16):
            #     for o in range(784):
            #         grad_w[0][p][o] += short_train_set[(j * batch_size) + k][0][o] * sigmoid_deriv(z[0][p]) * grad_a0[p]
            #         grad_b[0][p] += 1 * sigmoid_deriv(z[0][p]) * grad_a0[p]

            # Vectorized
            grad_w[0] += (sigmoid_deriv(z[0]) * grad_a0) @ (np.transpose(short_train_set[(j * batch_size) + k][0]))
            grad_b[0] += (sigmoid_deriv(z[0]) * grad_a0)

        # Update weights and biases
        w[0] -= learning_rate * (grad_w[0] / batch_size)
        w[1] -= learning_rate * (grad_w[1] / batch_size)
        w[2] -= learning_rate * (grad_w[2] / batch_size)
        b[0] -= learning_rate * (grad_b[0] / batch_size)
        b[1] -= learning_rate * (grad_b[1] / batch_size)
        b[2] -= learning_rate * (grad_b[2] / batch_size)
    print(f"[STATUS] Epoch {i} completed.")

# Plotting cost value over epochs
cost = np.divide(cost, len(short_train_set))
plt.plot(np.arange(number_of_epochs), cost, color ="red")
plt.show()
print("[STATUS] Learning finished!")
stop = time.time()

# Testing the network with train set
hit = 0
for i in range(len(short_train_set)):
    a, z = feedforward(train_set[i][0], w, a, b, z)
    result = np.argmax(a[2])
    label = np.argmax(train_set[i][1])
    # print(result, label)
    if result == label:
        hit += 1

print("Train accuracy = ", hit/len(short_train_set))

# Testing the network with test set
hit = 0
for i in range(len(test_set)):
    a, z = feedforward(test_set[i][0], w, a, b, z)
    result = np.argmax(a[2])
    label = np.argmax(test_set[i][1])
    # print(result, label)
    if result == label:
        hit += 1

print("Test accuracy = ", hit/len(test_set))

print(f"Learn time = {math.floor(stop - start)} seconds")









