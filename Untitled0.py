{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled0.ipynb",
      "provenance": [],
      "toc_visible": true,
      "authorship_tag": "ABX9TyOb/pgi1aHRXxkBB7T73DsQ",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/ZuyangWan/ZuyangWan.github.io/blob/master/Untitled0.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "MJRWwuIwAMBT",
        "colab_type": "code",
        "outputId": "7ca38403-ec70-4ede-aac2-a9d144792e11",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 53
        }
      },
      "source": [
        "%tensorflow_version 1.x\n",
        "import tensorflow as tf\n",
        "tf.__version__"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "TensorFlow 1.x selected.\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'1.15.2'"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 1
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "1cSfqFZ6Al9v",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import tensorflow as tf\n",
        "import os\n",
        "from tensorflow.examples.tutorials.mnist import input_data\n",
        "\n",
        "\n",
        "def create_weights(shape):\n",
        "    return tf.Variable(initial_value=tf.random_normal(shape=shape, stddev=0.1))\n",
        "\n",
        "\n",
        "def create_model(x):\n",
        "\n",
        "    # 1) 第一个卷积大层\n",
        "    input_x = tf.reshape(x, shape=[-1, 28, 28, 1])\n",
        "    # 卷积层\n",
        "    conv1_weights = create_weights(shape=[5, 5, 1, 32])\n",
        "    conv1_bias = create_weights(shape=[32])\n",
        "    conv1_x = tf.nn.conv2d(input=input_x, filter=conv1_weights, strides=[1, 1, 1, 1], padding=\"SAME\") + conv1_bias\n",
        "    # 激活层\n",
        "    relu1_x = tf.nn.relu(conv1_x)\n",
        "    # 池化层\n",
        "    pool1_x = tf.nn.max_pool(relu1_x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding=\"SAME\")\n",
        "    # 2) 第二个卷起大层\n",
        "    # 卷积层\n",
        "    conv2_weights = create_weights(shape=[5, 5, 32, 64])\n",
        "    conv2_bias = create_weights(shape=[64])\n",
        "    conv2_x = tf.nn.conv2d(input=pool1_x, filter=conv2_weights, strides=[1, 1, 1, 1], padding=\"SAME\") + conv2_bias\n",
        "    # 激活层\n",
        "    relu2_x = tf.nn.relu(conv2_x)\n",
        "    # 池化层\n",
        "    pool2_x = tf.nn.max_pool(relu2_x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding=\"SAME\")\n",
        "    # 3) 全连接层\n",
        "    full_x_1 = tf.reshape(pool2_x, shape=[-1, 7 * 7 * 64])\n",
        "    full_weights = create_weights(shape=[7 * 7 * 64, 10])\n",
        "    full_bias = create_weights(shape=[10])\n",
        "    y_predict = tf.matmul(full_x_1, full_weights) + full_bias\n",
        "\n",
        "    return y_predict\n",
        "\n",
        "\n",
        "def cnn_mnist():\n",
        "\n",
        "    mnist = input_data.read_data_sets(\"./mnist_data\", one_hot=True)\n",
        "    x = tf.placeholder(tf.float32, shape=[None, 784])\n",
        "    y = tf.placeholder(tf.float32, shape=[None, 10])\n",
        "\n",
        "    # weights = tf.Variable(initial_value=tf.random_normal(shape=[784, 10]))\n",
        "    # bias = tf.Variable(initial_value=tf.random_normal(shape=[10]))\n",
        "    # y_predict = tf.matmul(x, weights) + bias\n",
        "\n",
        "    y_predict = create_model(x)\n",
        "\n",
        "    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_predict))\n",
        "\n",
        "    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)\n",
        "\n",
        "    equal_list = tf.equal(tf.argmax(y, 1), tf.argmax(y_predict, 1))\n",
        "    accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))\n",
        "\n",
        "    tf.summary.scalar(\"loss\", loss)\n",
        "    tf.summary.scalar(\"accuracy\", accuracy)\n",
        "\n",
        "    merged = tf.summary.merge_all()\n",
        "\n",
        "    init = tf.global_variables_initializer()\n",
        "\n",
        "    with tf.Session() as sess:\n",
        "        sess.run(init)\n",
        "        file_writer = tf.summary.FileWriter(\"./tmp/summary/cnn_mnist\", graph=sess.graph)\n",
        "\n",
        "        for i in range(3000):\n",
        "            image, label = mnist.train.next_batch(50)\n",
        "            _, summary = sess.run([optimizer, merged], feed_dict={x:image, y:label})\n",
        "            file_writer.add_summary(summary, i)\n",
        "\n",
        "            acc = sess.run(accuracy, feed_dict={x:image, y:label})\n",
        "            print(\"Iter %d, Testing Accuracy=%f\" % (i, acc))\n",
        "\n",
        "    return None\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    cnn_mnist()\n"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "-3o-9Dn-BePC",
        "colab_type": "text"
      },
      "source": [
        "# 新段落"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "oETfDZvaBe0j",
        "colab_type": "text"
      },
      "source": [
        "# 新段落"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "s9gxMRKkBnrR",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "from google.colab import files\n",
        "\n",
        "with open('example.txt', 'w') as f:\n",
        "  f.write('some content')\n",
        "\n",
        "files.download('example.txt')"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "BG6uNiJkB6Br",
        "colab_type": "code",
        "outputId": "9427856c-1600-42a7-f3bb-04888447173d",
        "colab": {
          "resources": {
            "http://localhost:8080/nbextensions/google.colab/files.js": {
              "data": "Ly8gQ29weXJpZ2h0IDIwMTcgR29vZ2xlIExMQwovLwovLyBMaWNlbnNlZCB1bmRlciB0aGUgQXBhY2hlIExpY2Vuc2UsIFZlcnNpb24gMi4wICh0aGUgIkxpY2Vuc2UiKTsKLy8geW91IG1heSBub3QgdXNlIHRoaXMgZmlsZSBleGNlcHQgaW4gY29tcGxpYW5jZSB3aXRoIHRoZSBMaWNlbnNlLgovLyBZb3UgbWF5IG9idGFpbiBhIGNvcHkgb2YgdGhlIExpY2Vuc2UgYXQKLy8KLy8gICAgICBodHRwOi8vd3d3LmFwYWNoZS5vcmcvbGljZW5zZXMvTElDRU5TRS0yLjAKLy8KLy8gVW5sZXNzIHJlcXVpcmVkIGJ5IGFwcGxpY2FibGUgbGF3IG9yIGFncmVlZCB0byBpbiB3cml0aW5nLCBzb2Z0d2FyZQovLyBkaXN0cmlidXRlZCB1bmRlciB0aGUgTGljZW5zZSBpcyBkaXN0cmlidXRlZCBvbiBhbiAiQVMgSVMiIEJBU0lTLAovLyBXSVRIT1VUIFdBUlJBTlRJRVMgT1IgQ09ORElUSU9OUyBPRiBBTlkgS0lORCwgZWl0aGVyIGV4cHJlc3Mgb3IgaW1wbGllZC4KLy8gU2VlIHRoZSBMaWNlbnNlIGZvciB0aGUgc3BlY2lmaWMgbGFuZ3VhZ2UgZ292ZXJuaW5nIHBlcm1pc3Npb25zIGFuZAovLyBsaW1pdGF0aW9ucyB1bmRlciB0aGUgTGljZW5zZS4KCi8qKgogKiBAZmlsZW92ZXJ2aWV3IEhlbHBlcnMgZm9yIGdvb2dsZS5jb2xhYiBQeXRob24gbW9kdWxlLgogKi8KKGZ1bmN0aW9uKHNjb3BlKSB7CmZ1bmN0aW9uIHNwYW4odGV4dCwgc3R5bGVBdHRyaWJ1dGVzID0ge30pIHsKICBjb25zdCBlbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3BhbicpOwogIGVsZW1lbnQudGV4dENvbnRlbnQgPSB0ZXh0OwogIGZvciAoY29uc3Qga2V5IG9mIE9iamVjdC5rZXlzKHN0eWxlQXR0cmlidXRlcykpIHsKICAgIGVsZW1lbnQuc3R5bGVba2V5XSA9IHN0eWxlQXR0cmlidXRlc1trZXldOwogIH0KICByZXR1cm4gZWxlbWVudDsKfQoKLy8gTWF4IG51bWJlciBvZiBieXRlcyB3aGljaCB3aWxsIGJlIHVwbG9hZGVkIGF0IGEgdGltZS4KY29uc3QgTUFYX1BBWUxPQURfU0laRSA9IDEwMCAqIDEwMjQ7Ci8vIE1heCBhbW91bnQgb2YgdGltZSB0byBibG9jayB3YWl0aW5nIGZvciB0aGUgdXNlci4KY29uc3QgRklMRV9DSEFOR0VfVElNRU9VVF9NUyA9IDMwICogMTAwMDsKCmZ1bmN0aW9uIF91cGxvYWRGaWxlcyhpbnB1dElkLCBvdXRwdXRJZCkgewogIGNvbnN0IHN0ZXBzID0gdXBsb2FkRmlsZXNTdGVwKGlucHV0SWQsIG91dHB1dElkKTsKICBjb25zdCBvdXRwdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQob3V0cHV0SWQpOwogIC8vIENhY2hlIHN0ZXBzIG9uIHRoZSBvdXRwdXRFbGVtZW50IHRvIG1ha2UgaXQgYXZhaWxhYmxlIGZvciB0aGUgbmV4dCBjYWxsCiAgLy8gdG8gdXBsb2FkRmlsZXNDb250aW51ZSBmcm9tIFB5dGhvbi4KICBvdXRwdXRFbGVtZW50LnN0ZXBzID0gc3RlcHM7CgogIHJldHVybiBfdXBsb2FkRmlsZXNDb250aW51ZShvdXRwdXRJZCk7Cn0KCi8vIFRoaXMgaXMgcm91Z2hseSBhbiBhc3luYyBnZW5lcmF0b3IgKG5vdCBzdXBwb3J0ZWQgaW4gdGhlIGJyb3dzZXIgeWV0KSwKLy8gd2hlcmUgdGhlcmUgYXJlIG11bHRpcGxlIGFzeW5jaHJvbm91cyBzdGVwcyBhbmQgdGhlIFB5dGhvbiBzaWRlIGlzIGdvaW5nCi8vIHRvIHBvbGwgZm9yIGNvbXBsZXRpb24gb2YgZWFjaCBzdGVwLgovLyBUaGlzIHVzZXMgYSBQcm9taXNlIHRvIGJsb2NrIHRoZSBweXRob24gc2lkZSBvbiBjb21wbGV0aW9uIG9mIGVhY2ggc3RlcCwKLy8gdGhlbiBwYXNzZXMgdGhlIHJlc3VsdCBvZiB0aGUgcHJldmlvdXMgc3RlcCBhcyB0aGUgaW5wdXQgdG8gdGhlIG5leHQgc3RlcC4KZnVuY3Rpb24gX3VwbG9hZEZpbGVzQ29udGludWUob3V0cHV0SWQpIHsKICBjb25zdCBvdXRwdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQob3V0cHV0SWQpOwogIGNvbnN0IHN0ZXBzID0gb3V0cHV0RWxlbWVudC5zdGVwczsKCiAgY29uc3QgbmV4dCA9IHN0ZXBzLm5leHQob3V0cHV0RWxlbWVudC5sYXN0UHJvbWlzZVZhbHVlKTsKICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKG5leHQudmFsdWUucHJvbWlzZSkudGhlbigodmFsdWUpID0+IHsKICAgIC8vIENhY2hlIHRoZSBsYXN0IHByb21pc2UgdmFsdWUgdG8gbWFrZSBpdCBhdmFpbGFibGUgdG8gdGhlIG5leHQKICAgIC8vIHN0ZXAgb2YgdGhlIGdlbmVyYXRvci4KICAgIG91dHB1dEVsZW1lbnQubGFzdFByb21pc2VWYWx1ZSA9IHZhbHVlOwogICAgcmV0dXJuIG5leHQudmFsdWUucmVzcG9uc2U7CiAgfSk7Cn0KCi8qKgogKiBHZW5lcmF0b3IgZnVuY3Rpb24gd2hpY2ggaXMgY2FsbGVkIGJldHdlZW4gZWFjaCBhc3luYyBzdGVwIG9mIHRoZSB1cGxvYWQKICogcHJvY2Vzcy4KICogQHBhcmFtIHtzdHJpbmd9IGlucHV0SWQgRWxlbWVudCBJRCBvZiB0aGUgaW5wdXQgZmlsZSBwaWNrZXIgZWxlbWVudC4KICogQHBhcmFtIHtzdHJpbmd9IG91dHB1dElkIEVsZW1lbnQgSUQgb2YgdGhlIG91dHB1dCBkaXNwbGF5LgogKiBAcmV0dXJuIHshSXRlcmFibGU8IU9iamVjdD59IEl0ZXJhYmxlIG9mIG5leHQgc3RlcHMuCiAqLwpmdW5jdGlvbiogdXBsb2FkRmlsZXNTdGVwKGlucHV0SWQsIG91dHB1dElkKSB7CiAgY29uc3QgaW5wdXRFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoaW5wdXRJZCk7CiAgaW5wdXRFbGVtZW50LmRpc2FibGVkID0gZmFsc2U7CgogIGNvbnN0IG91dHB1dEVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChvdXRwdXRJZCk7CiAgb3V0cHV0RWxlbWVudC5pbm5lckhUTUwgPSAnJzsKCiAgY29uc3QgcGlja2VkUHJvbWlzZSA9IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7CiAgICBpbnB1dEVsZW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignY2hhbmdlJywgKGUpID0+IHsKICAgICAgcmVzb2x2ZShlLnRhcmdldC5maWxlcyk7CiAgICB9KTsKICB9KTsKCiAgY29uc3QgY2FuY2VsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYnV0dG9uJyk7CiAgaW5wdXRFbGVtZW50LnBhcmVudEVsZW1lbnQuYXBwZW5kQ2hpbGQoY2FuY2VsKTsKICBjYW5jZWwudGV4dENvbnRlbnQgPSAnQ2FuY2VsIHVwbG9hZCc7CiAgY29uc3QgY2FuY2VsUHJvbWlzZSA9IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7CiAgICBjYW5jZWwub25jbGljayA9ICgpID0+IHsKICAgICAgcmVzb2x2ZShudWxsKTsKICAgIH07CiAgfSk7CgogIC8vIENhbmNlbCB1cGxvYWQgaWYgdXNlciBoYXNuJ3QgcGlja2VkIGFueXRoaW5nIGluIHRpbWVvdXQuCiAgY29uc3QgdGltZW91dFByb21pc2UgPSBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gewogICAgc2V0VGltZW91dCgoKSA9PiB7CiAgICAgIHJlc29sdmUobnVsbCk7CiAgICB9LCBGSUxFX0NIQU5HRV9USU1FT1VUX01TKTsKICB9KTsKCiAgLy8gV2FpdCBmb3IgdGhlIHVzZXIgdG8gcGljayB0aGUgZmlsZXMuCiAgY29uc3QgZmlsZXMgPSB5aWVsZCB7CiAgICBwcm9taXNlOiBQcm9taXNlLnJhY2UoW3BpY2tlZFByb21pc2UsIHRpbWVvdXRQcm9taXNlLCBjYW5jZWxQcm9taXNlXSksCiAgICByZXNwb25zZTogewogICAgICBhY3Rpb246ICdzdGFydGluZycsCiAgICB9CiAgfTsKCiAgaWYgKCFmaWxlcykgewogICAgcmV0dXJuIHsKICAgICAgcmVzcG9uc2U6IHsKICAgICAgICBhY3Rpb246ICdjb21wbGV0ZScsCiAgICAgIH0KICAgIH07CiAgfQoKICBjYW5jZWwucmVtb3ZlKCk7CgogIC8vIERpc2FibGUgdGhlIGlucHV0IGVsZW1lbnQgc2luY2UgZnVydGhlciBwaWNrcyBhcmUgbm90IGFsbG93ZWQuCiAgaW5wdXRFbGVtZW50LmRpc2FibGVkID0gdHJ1ZTsKCiAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7CiAgICBjb25zdCBsaSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2xpJyk7CiAgICBsaS5hcHBlbmQoc3BhbihmaWxlLm5hbWUsIHtmb250V2VpZ2h0OiAnYm9sZCd9KSk7CiAgICBsaS5hcHBlbmQoc3BhbigKICAgICAgICBgKCR7ZmlsZS50eXBlIHx8ICduL2EnfSkgLSAke2ZpbGUuc2l6ZX0gYnl0ZXMsIGAgKwogICAgICAgIGBsYXN0IG1vZGlmaWVkOiAkewogICAgICAgICAgICBmaWxlLmxhc3RNb2RpZmllZERhdGUgPyBmaWxlLmxhc3RNb2RpZmllZERhdGUudG9Mb2NhbGVEYXRlU3RyaW5nKCkgOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnbi9hJ30gLSBgKSk7CiAgICBjb25zdCBwZXJjZW50ID0gc3BhbignMCUgZG9uZScpOwogICAgbGkuYXBwZW5kQ2hpbGQocGVyY2VudCk7CgogICAgb3V0cHV0RWxlbWVudC5hcHBlbmRDaGlsZChsaSk7CgogICAgY29uc3QgZmlsZURhdGFQcm9taXNlID0gbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHsKICAgICAgY29uc3QgcmVhZGVyID0gbmV3IEZpbGVSZWFkZXIoKTsKICAgICAgcmVhZGVyLm9ubG9hZCA9IChlKSA9PiB7CiAgICAgICAgcmVzb2x2ZShlLnRhcmdldC5yZXN1bHQpOwogICAgICB9OwogICAgICByZWFkZXIucmVhZEFzQXJyYXlCdWZmZXIoZmlsZSk7CiAgICB9KTsKICAgIC8vIFdhaXQgZm9yIHRoZSBkYXRhIHRvIGJlIHJlYWR5LgogICAgbGV0IGZpbGVEYXRhID0geWllbGQgewogICAgICBwcm9taXNlOiBmaWxlRGF0YVByb21pc2UsCiAgICAgIHJlc3BvbnNlOiB7CiAgICAgICAgYWN0aW9uOiAnY29udGludWUnLAogICAgICB9CiAgICB9OwoKICAgIC8vIFVzZSBhIGNodW5rZWQgc2VuZGluZyB0byBhdm9pZCBtZXNzYWdlIHNpemUgbGltaXRzLiBTZWUgYi82MjExNTY2MC4KICAgIGxldCBwb3NpdGlvbiA9IDA7CiAgICB3aGlsZSAocG9zaXRpb24gPCBmaWxlRGF0YS5ieXRlTGVuZ3RoKSB7CiAgICAgIGNvbnN0IGxlbmd0aCA9IE1hdGgubWluKGZpbGVEYXRhLmJ5dGVMZW5ndGggLSBwb3NpdGlvbiwgTUFYX1BBWUxPQURfU0laRSk7CiAgICAgIGNvbnN0IGNodW5rID0gbmV3IFVpbnQ4QXJyYXkoZmlsZURhdGEsIHBvc2l0aW9uLCBsZW5ndGgpOwogICAgICBwb3NpdGlvbiArPSBsZW5ndGg7CgogICAgICBjb25zdCBiYXNlNjQgPSBidG9hKFN0cmluZy5mcm9tQ2hhckNvZGUuYXBwbHkobnVsbCwgY2h1bmspKTsKICAgICAgeWllbGQgewogICAgICAgIHJlc3BvbnNlOiB7CiAgICAgICAgICBhY3Rpb246ICdhcHBlbmQnLAogICAgICAgICAgZmlsZTogZmlsZS5uYW1lLAogICAgICAgICAgZGF0YTogYmFzZTY0LAogICAgICAgIH0sCiAgICAgIH07CiAgICAgIHBlcmNlbnQudGV4dENvbnRlbnQgPQogICAgICAgICAgYCR7TWF0aC5yb3VuZCgocG9zaXRpb24gLyBmaWxlRGF0YS5ieXRlTGVuZ3RoKSAqIDEwMCl9JSBkb25lYDsKICAgIH0KICB9CgogIC8vIEFsbCBkb25lLgogIHlpZWxkIHsKICAgIHJlc3BvbnNlOiB7CiAgICAgIGFjdGlvbjogJ2NvbXBsZXRlJywKICAgIH0KICB9Owp9CgpzY29wZS5nb29nbGUgPSBzY29wZS5nb29nbGUgfHwge307CnNjb3BlLmdvb2dsZS5jb2xhYiA9IHNjb3BlLmdvb2dsZS5jb2xhYiB8fCB7fTsKc2NvcGUuZ29vZ2xlLmNvbGFiLl9maWxlcyA9IHsKICBfdXBsb2FkRmlsZXMsCiAgX3VwbG9hZEZpbGVzQ29udGludWUsCn07Cn0pKHNlbGYpOwo=",
              "ok": true,
              "headers": [
                [
                  "content-type",
                  "application/javascript"
                ]
              ],
              "status": 200,
              "status_text": ""
            }
          },
          "base_uri": "https://localhost:8080/",
          "height": 254
        }
      },
      "source": [
        "from google.colab import files\n",
        "\n",
        "uploaded = files.upload()\n",
        "\n",
        "for fn in uploaded.keys():\n",
        "  print('User uploaded file \"{name}\" with length {length} bytes'.format(\n",
        "      name=fn, length=len(uploaded[fn])))"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "\n",
              "     <input type=\"file\" id=\"files-ea7bd36d-b7c4-4797-8241-6407b67b1e80\" name=\"files[]\" multiple disabled />\n",
              "     <output id=\"result-ea7bd36d-b7c4-4797-8241-6407b67b1e80\">\n",
              "      Upload widget is only available when the cell has been executed in the\n",
              "      current browser session. Please rerun this cell to enable.\n",
              "      </output>\n",
              "      <script src=\"/nbextensions/google.colab/files.js\"></script> "
            ],
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "Saving t10k-images-idx3-ubyte.gz to t10k-images-idx3-ubyte.gz\n",
            "Saving t10k-labels-idx1-ubyte.gz to t10k-labels-idx1-ubyte.gz\n",
            "Saving train-images-idx3-ubyte.gz to train-images-idx3-ubyte.gz\n",
            "Saving train-labels-idx1-ubyte.gz to train-labels-idx1-ubyte.gz\n",
            "User uploaded file \"t10k-images-idx3-ubyte.gz\" with length 1648877 bytes\n",
            "User uploaded file \"t10k-labels-idx1-ubyte.gz\" with length 4542 bytes\n",
            "User uploaded file \"train-images-idx3-ubyte.gz\" with length 9912422 bytes\n",
            "User uploaded file \"train-labels-idx1-ubyte.gz\" with length 28881 bytes\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}