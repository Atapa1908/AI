# TRAFFIC
In this project, a neural network is designed and trained to classify 26640 traffic signs.

## EXPERIMENTATION PROCESS

Before building and designing the model, the channel values (which are up to 255) are normalized so that all values are between 0 and 1, which is ideal for a neural network.

### 1
Initially, we implemented a network containing three convolutional layers each with 32 filters and a kernel size of 3x3. This layer detects and features by applying ReLU (Rectified Linear Activation) activation function. Next, a 2x2 pooling layer is applied in order to reduce the dimensions of the initial image to better capture features. After three convolutional-pooling layers the three-dimensional tensors are reduced to a one-dimensional data point. Then, dense layer with 128 units (or neurons) is applied utilizing the ReLU function once again. Finally, the ultimate dense layer contains `NUM_CATEGORIES` units, using the "sofftmax" activation to generate a probability distribution over output categories.

### 2
To increase efficiency and accuracy a hierarchical approach was implemented by reducing the three filters to two and changing the first layer's size to 64. This ensures that features are captures more efficiently and accurately. Also, a dropout layer is applied after the first hidden (dense) layer of rate 0.5 in order to prevent overfitting by dropping out 50% of units during training. Each epoch, an epoch referring to a single iteration during the training process, takes 4 seconds and accuracy is around 97%.

### 3
To further experiment with the network another dense layer is introduced containing 512 units followed by a dropout layer of 0.75 prior to the already existing dense layer with 128 units. Having 26640 images to analyze and playing around with different dropout rates, a rate of 0.5 for 512 units and a rate of 0.5 for 128 units seems to be most appropriate. Each epoch takes around 5 seconds and has an accuracy consistently of above 98%.