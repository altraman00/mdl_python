#-*- coding: UTF-8 -*-

import os
import sys
import time

import numpy as np
import tensorflow as tf
from PIL import Image
from captcha.image import ImageCaptcha

import random
from Alexnet import Network

# Author: AlexFang, alex.holla@foxmail.com.
# Author: AlexFang, alex.holla@foxmail.com.
# %load alexnet.py
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Contains a model definition for AlexNet.

This work was first described in:
  ImageNet Classification with Deep Convolutional Neural Networks
  Alex Krizhevsky, Ilya Sutskever and Geoffrey E. Hinton

and later refined in:
  One weird trick for parallelizing convolutional neural networks
  Alex Krizhevsky, 2014

Here we provide the implementation proposed in "One weird trick" and not
"ImageNet Classification", as per the paper, the LRN layers have been removed.

Usage:
  with slim.arg_scope(alexnet.alexnet_v2_arg_scope()):
    outputs, end_points = alexnet.alexnet_v2(inputs)

@@alexnet_v2
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
slim = tf.contrib.slim
trunc_normal = lambda stddev: tf.truncated_normal_initializer(0.0, stddev)


class Network:
    def __init__(self, num_classes, weight_decay, is_training):
        self.num_classes = num_classes
        self.weight_decay = weight_decay
        self.is_training = is_training
        self.alexnet_v2_arg_scope(weight_decay=0.0005)

    def alexnet_v2_arg_scope(self, weight_decay=0.0005):
        with slim.arg_scope([slim.conv2d, slim.fully_connected],
                            activation_fn=tf.nn.relu,
                            biases_initializer=tf.constant_initializer(0.1),
                            weights_regularizer=slim.l2_regularizer(weight_decay)):
            with slim.arg_scope([slim.conv2d], padding='SAME'):
                with slim.arg_scope([slim.max_pool2d], padding='VALID') as arg_sc:
                    return arg_sc

    def construct(self, inputs):
        num_classes = self.num_classes
        is_training = self.is_training
        dropout_keep_prob = 0.5
        spatial_squeeze = True
        scope = 'alexnet_v2'
        global_pool = False
        """AlexNet version 2.

        Described in: http://arxiv.org/pdf/1404.5997v2.pdf
        Parameters from:
        github.com/akrizhevsky/cuda-convnet2/blob/master/layers/
        layers-imagenet-1gpu.cfg

        Note: All the fully_connected layers have been transformed to conv2d layers.
              To use in classification mode, resize input to 224x224 or set
              global_pool=True. To use in fully convolutional mode, set
              spatial_squeeze to false.
              The LRN layers have been removed and change the initializers from
              random_normal_initializer to xavier_initializer.

        Args:
          inputs: a tensor of size [batch_size, height, width, channels].
          num_classes: the number of predicted classes. If 0 or None, the logits layer
          is omitted and the input features to the logits layer are returned instead.
          is_training: whether or not the model is being trained.
          dropout_keep_prob: the probability that activations are kept in the dropout
            layers during training.
          spatial_squeeze: whether or not should squeeze the spatial dimensions of the
            logits. Useful to remove unnecessary dimensions for classification.
          scope: Optional scope for the variables.
          global_pool: Optional boolean flag. If True, the input to the classification
            layer is avgpooled to size 1x1, for any input size. (This is not part
            of the original AlexNet.)

        Returns:
          net: the output of the logits layer (if num_classes is a non-zero integer),
            or the non-dropped-out input to the logits layer (if num_classes is 0
            or None).
          end_points: a dict of tensors with intermediate activations.
        """
        with tf.variable_scope(scope, 'alexnet_v2', [inputs]) as sc:
            end_points_collection = sc.original_name_scope + '_end_points'
            # Collect outputs for conv2d, fully_connected and max_pool2d.
            with slim.arg_scope([slim.conv2d, slim.fully_connected, slim.max_pool2d],
                                outputs_collections=[end_points_collection]):
                net = slim.conv2d(inputs, 64, [11, 11], 4, padding='VALID',
                                  scope='conv1')
                net = slim.max_pool2d(net, [3, 3], 2, scope='pool1')
                net = slim.conv2d(net, 192, [5, 5], scope='conv2')
                net = slim.max_pool2d(net, [3, 3], 2, scope='pool2')
                net = slim.conv2d(net, 384, [3, 3], scope='conv3')
                net = slim.conv2d(net, 384, [3, 3], scope='conv4')
                net = slim.conv2d(net, 256, [3, 3], scope='conv5')
                net = slim.max_pool2d(net, [3, 3], 2, scope='pool5')

            # Use conv2d instead of fully_connected layers.
            with slim.arg_scope([slim.conv2d],
                                weights_initializer=trunc_normal(0.005),
                                biases_initializer=tf.constant_initializer(0.1)):
                net = slim.conv2d(net, 4096, [5, 5], padding='VALID',
                                  scope='fc6')
                net = slim.dropout(net, dropout_keep_prob, is_training=is_training,
                                   scope='dropout6')
                net = slim.conv2d(net, 4096, [1, 1], scope='fc7')
                net = slim.dropout(net, dropout_keep_prob, is_training=is_training,
                                   scope='dropout7')

                net0 = slim.conv2d(net, num_classes, [1, 1],
                                   activation_fn=None,
                                   normalizer_fn=None,
                                   biases_initializer=tf.zeros_initializer(),
                                   scope='fc8_0')
                net1 = slim.conv2d(net, num_classes, [1, 1],
                                   activation_fn=None,
                                   normalizer_fn=None,
                                   biases_initializer=tf.zeros_initializer(),
                                   scope='fc8_1')
                net2 = slim.conv2d(net, num_classes, [1, 1],
                                   activation_fn=None,
                                   normalizer_fn=None,
                                   biases_initializer=tf.zeros_initializer(),
                                   scope='fc8_2')
                net3 = slim.conv2d(net, num_classes, [1, 1],
                                   activation_fn=None,
                                   normalizer_fn=None,
                                   biases_initializer=tf.zeros_initializer(),
                                   scope='fc8_3')

                # Convert end_points_collection into a end_point dict.
                end_points = slim.utils.convert_collection_to_dict(end_points_collection)

                if spatial_squeeze:
                    net0 = tf.squeeze(net0, [1, 2], name='fc8_0/squeezed')
                    end_points[sc.name + '/fc8_0'] = net0

                    net1 = tf.squeeze(net1, [1, 2], name='fc8_1/squeezed')
                    end_points[sc.name + '/fc8_1'] = net1

                    net2 = tf.squeeze(net2, [1, 2], name='fc8_2/squeezed')
                    end_points[sc.name + '/fc8_2'] = net2

                    net3 = tf.squeeze(net3, [1, 2], name='fc8_3/squeezed')
                    end_points[sc.name + '/fc8_3'] = net3

                return net0, net1, net2, net3, end_points

            alexnet_v2.default_image_size = 224


os.environ['CUDA_VISIBLE_DEVICES'] = '1'

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
          'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
          'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

base_data_path = '/content/drive/MyDrive/data'

# 数据集路径
img_code_path = base_data_path + '/valid_code/train'

# tfrecord文件存放路径
tfrecord_path = base_data_path + '/tfrecord'

TRAIN_TFRECORD_FILE = tfrecord_path + '/train.tfrecords'

TEST_TFRECORD_FILE = tfrecord_path + '/test.tfrecords'

CHECKPOINT_DIR = base_data_path + '/ckpt/'


# 1---------------------
def generate_folder():
    if not os.path.exists(img_code_path):
        os.makedirs(img_code_path)
    for i in os.listdir(img_code_path):
        if i == 'tfrecord':
            continue
        os.remove(os.path.join(img_code_path, i))

    if not os.path.exists(tfrecord_path):
        os.makedirs(tfrecord_path)
    for i in os.listdir(tfrecord_path):
        os.remove(os.path.join(tfrecord_path, i))


# def random_captcha_text(char_set=number,captcha_size=4):
def random_captcha_text(char_set=number, captcha_size=4):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


def gen_captcha_text_and_image():
    image = ImageCaptcha()
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)
    image.write(captcha_text, img_code_path + '/' + captcha_text + '.png')  # write it


# 2------------------
def generate():
    num = 1000
    for i in range(num):
        gen_captcha_text_and_image()
        sys.stdout.write('\r>>creating images %d/%d' % (i + 1, num))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()
    print('All picture has been generated')


# 3--------------------
def save_as_tf():
    _NUM_TEST = 500
    _RANDOM_SEED = 0
    DATASET_DIR = img_code_path + '/'
    TFRECORD_DIR = tfrecord_path + '/'

    def _dataset_exists(dataset_dir):
        for split_name in ['train', 'test']:
            output_filename = os.path.join(dataset_dir, split_name + 'tfrecords')
            if not tf.gfile.Exists(output_filename):
                return False
        return True

    def _get_filenames_and_classes(dataset_dir):
        photo_filenames = []
        for filename in os.listdir(dataset_dir):
            path = os.path.join(dataset_dir, filename)
            photo_filenames.append(path)
        return photo_filenames

    def int64_feature(values):
        if not isinstance(values, (tuple, list)):
            values = [values]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

    def bytes_feature(values):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

    def image_to_tfexample(image_data, label0, label1, label2, label3):
        return tf.train.Example(features=tf.train.Features(feature={
            'image': bytes_feature(image_data),
            'label0': int64_feature(label0),
            'label1': int64_feature(label1),
            'label2': int64_feature(label2),
            'label3': int64_feature(label3),
        }))

    def _convert_dataset(split_name, filenames, dataset_dir):
        assert split_name in ['train', 'test']

        with tf.Session() as sess:
            output_filename = os.path.join(TFRECORD_DIR, split_name + '.tfrecords')
            with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
                for i, filename in enumerate(filenames):
                    try:
                        sys.stdout.write('\r>>changing picture %d / %d' % (i + 1, len(filenames)))
                        sys.stdout.flush()

                        image_data = Image.open(filename)
                        image_data = image_data.resize((224, 224))
                        image_data = np.array(image_data.convert('L'))
                        image_data = image_data.tobytes()

                        labels = filename.split('/')[-1][0:4]
                        num_labels = []
                        for j in range(4):
                            num_labels.append(ord(labels[j]))

                        example = image_to_tfexample(image_data, num_labels[0], num_labels[1], num_labels[2],
                                                     num_labels[3])
                        tfrecord_writer.write(example.SerializeToString())

                    except IOError as e:
                        print('\n sth wrong:', filename)
                        print('Error:', e)
            sys.stdout.write('\n')
            sys.stdout.flush()

    if _dataset_exists(DATASET_DIR):
        print('file already exists')
    else:
        photo_filenames = _get_filenames_and_classes(DATASET_DIR)

        random.seed(_RANDOM_SEED)
        random.shuffle(photo_filenames)
        training_filenames = photo_filenames[_NUM_TEST:]
        testing_filenames = photo_filenames[:_NUM_TEST]

        _convert_dataset('train', training_filenames, DATASET_DIR)
        _convert_dataset('test', testing_filenames, DATASET_DIR)
        print('-------------We have produced all tfrecord file------------------')


# 4-------------
def train():
    tf.reset_default_graph()
    CHAR_NUM = 10
    IMAGE_HEIGHT = 60
    IMAGE_WIDTH = 160
    BATCH_SIZE = 10

    # placeholder
    x = tf.placeholder(tf.float32, [None, 224, 224])
    y0 = tf.placeholder(tf.float32, [None])
    y1 = tf.placeholder(tf.float32, [None])
    y2 = tf.placeholder(tf.float32, [None])
    y3 = tf.placeholder(tf.float32, [None])

    lr = tf.Variable(0.0003, dtype=tf.float32)

    def read_and_decode(filename):
        filename_queue = tf.train.string_input_producer([filename])
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(serialized_example, features={'image': tf.FixedLenFeature([], tf.string),
                                                                         'label0': tf.FixedLenFeature([], tf.int64),
                                                                         'label1': tf.FixedLenFeature([], tf.int64),
                                                                         'label2': tf.FixedLenFeature([], tf.int64),
                                                                         'label3': tf.FixedLenFeature([], tf.int64)
                                                                         })
        image = tf.decode_raw(features['image'], tf.uint8)
        image = tf.reshape(image, [224, 224])
        image = tf.cast(image, tf.float32) / 255.0
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)
        label0 = tf.cast(features['label0'], tf.int32)
        label1 = tf.cast(features['label1'], tf.int32)
        label2 = tf.cast(features['label2'], tf.int32)
        label3 = tf.cast(features['label3'], tf.int32)
        return image, label0, label1, label2, label3

    image, label0, label1, label2, label3 = read_and_decode(TRAIN_TFRECORD_FILE)

    image_batch, label_batch0, label_batch1, label_batch2, label_batch3 = tf.train.shuffle_batch(
        [image, label0, label1, label2, label3]
        , batch_size=BATCH_SIZE
        , capacity=1075
        , min_after_dequeue=1000
        , num_threads=128
    )

    network = Network(num_classes=CHAR_NUM, weight_decay=0.0005, is_training=True)

    # gpu_options = tf.GPUOptions(allow_growth=True)

    # with tf.Session(config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True,gpu_options=gpu_options)) as sess:
    #     gpu_options = tf.GPUOptions(allow_growth=True)
    #     tf.Session(config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True,gpu_options=gpu_options))

    with tf.Session() as sess:

        X = tf.reshape(x, [BATCH_SIZE, 224, 224, 1])

        logits0, logits1, logits2, logits3, end_pintos = network.construct(X)

        one_hot_labels0 = tf.one_hot(indices=tf.cast(y0, tf.int32), depth=CHAR_NUM)
        one_hot_labels1 = tf.one_hot(indices=tf.cast(y1, tf.int32), depth=CHAR_NUM)
        one_hot_labels2 = tf.one_hot(indices=tf.cast(y2, tf.int32), depth=CHAR_NUM)
        one_hot_labels3 = tf.one_hot(indices=tf.cast(y3, tf.int32), depth=CHAR_NUM)

        loss0 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits0, labels=one_hot_labels0))
        loss1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits1, labels=one_hot_labels1))
        loss2 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits2, labels=one_hot_labels2))
        loss3 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits3, labels=one_hot_labels3))
        total_loss = (loss0 + loss1 + loss2 + loss3) / 4.0
        optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(total_loss)

        correct_prediction0 = tf.equal(tf.argmax(one_hot_labels0, 1), tf.argmax(logits0, 1))
        accuracy0 = tf.reduce_mean(tf.cast(correct_prediction0, tf.float32))

        correct_prediction1 = tf.equal(tf.argmax(one_hot_labels1, 1), tf.argmax(logits1, 1))
        accuracy1 = tf.reduce_mean(tf.cast(correct_prediction1, tf.float32))

        correct_prediction2 = tf.equal(tf.argmax(one_hot_labels2, 1), tf.argmax(logits2, 1))
        accuracy2 = tf.reduce_mean(tf.cast(correct_prediction2, tf.float32))

        correct_prediction3 = tf.equal(tf.argmax(one_hot_labels3, 1), tf.argmax(logits3, 1))
        accuracy3 = tf.reduce_mean(tf.cast(correct_prediction3, tf.float32))

        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        # saver.restore(sess, './ckpt/crack_captcha-10000.ckpt')
        # sess.run(tf.local_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        for i in range(10001):
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            b_image, b_label0, b_label1, b_label2, b_label3 = sess.run(
                [image_batch, label_batch0, label_batch1, label_batch2, label_batch3])
            sess.run(optimizer, feed_dict={x: b_image, y0: b_label0, y1: b_label1, y2: b_label2, y3: b_label3})

            if i % 100 == 0:
                if i % 5000 == 0:
                    sess.run(tf.assign(lr, lr / 3))
                acc0, acc1, acc2, acc3, loss_ = sess.run([accuracy0, accuracy1, accuracy2, accuracy3, total_loss],
                                                         feed_dict={x: b_image, y0: b_label0,
                                                                    y1: b_label1,
                                                                    y2: b_label2,
                                                                    y3: b_label3})
                learning_rate = sess.run(lr)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                print("Iter: %d , Loss:%.3f , Accuracy:%.3f, %.3f, %.3f, %.3f  Learning_rate:%.7f" % (
                    i, loss_, acc0, acc1, acc2, acc3, learning_rate))

                # if acc0 > 0.9 and acc1 > 0.9 and acc2 > 0.9 and acc3 > 0.9 :

                if i % 5000 == 0:
                    # saver.save(sess,'./ckpt/crack_captcha.ckpt', global_step=1)
                    saver.save(sess, CHECKPOINT_DIR + 'crack_captcha-' + str(i) + '.ckpt')
                    print("Save model %s------" % str(i))
                    continue
        coord.request_stop()
        coord.join(threads)


# 5-------------
def test():
    CHAR_NUM = 10  # category
    IMAGE_HEIGHT = 60
    IMAGE_WIDTH = 160
    BATCH_SIZE = 1

    x = tf.placeholder(tf.float32, [None, 224, 224])

    def read_and_decode(filename):
        filename_queue = tf.train.string_input_producer([filename])
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(serialized_example, features={'image': tf.FixedLenFeature([], tf.string),
                                                                         'label0': tf.FixedLenFeature([], tf.int64),
                                                                         'label1': tf.FixedLenFeature([], tf.int64),
                                                                         'label2': tf.FixedLenFeature([], tf.int64),
                                                                         'label3': tf.FixedLenFeature([], tf.int64)
                                                                         })
        image = tf.decode_raw(features['image'], tf.uint8)
        image_raw = tf.reshape(image, [224, 224])  # raw data

        image = tf.reshape(image, [224, 224])
        image = tf.cast(image, tf.float32) / 255.0  # standardlize
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)

        label0 = tf.cast(features['label0'], tf.int32)
        label1 = tf.cast(features['label1'], tf.int32)
        label2 = tf.cast(features['label2'], tf.int32)
        label3 = tf.cast(features['label3'], tf.int32)
        return image, image_raw, label0, label1, label2, label3

    # get label
    image, image_raw, label0, label1, label2, label3 = read_and_decode(TEST_TFRECORD_FILE)
    # print(len(sess.run(image)))
    image_batch, image_raw_batch, label_batch0, label_batch1, label_batch2, label_batch3 = tf.train.shuffle_batch(
        [image, image_raw, label0, label1, label2, label3], \
        batch_size=BATCH_SIZE, \
        capacity=53, min_after_dequeue=50, \
        num_threads=1)

    network = Network(num_classes=CHAR_NUM, weight_decay=0.0005, is_training=True)
    gpu_options = tf.GPUOptions(allow_growth=True)
    # with tf.Session(config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True,gpu_options=gpu_options)) as sess:
    with tf.Session() as sess:
        X = tf.reshape(x, [BATCH_SIZE, 224, 224, 1])

        logits0, logits1, logits2, logits3, end_pintos = network.construct(X)

        prediction0 = tf.reshape(logits0, [-1, CHAR_NUM])
        prediction0 = tf.argmax(prediction0, 1)

        prediction1 = tf.reshape(logits1, [-1, CHAR_NUM])
        prediction1 = tf.argmax(prediction1, 1)

        prediction2 = tf.reshape(logits2, [-1, CHAR_NUM])
        prediction2 = tf.argmax(prediction2, 1)

        prediction3 = tf.reshape(logits3, [-1, CHAR_NUM])
        prediction3 = tf.argmax(prediction3, 1)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess, './ckpt/crack_captcha-10000.ckpt')

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        for i in range(5):
            b_image, b_image_raw, b_label0, b_label1, b_label2, b_label3 = sess.run([image_batch,
                                                                                     image_raw_batch,
                                                                                     label_batch0,
                                                                                     label_batch1,
                                                                                     label_batch2,
                                                                                     label_batch3])

            # img = np.array(b_image_raw[0],dtype=np.uint8)

            # [1,224,224]
            img = Image.fromarray(b_image_raw[0], 'L')
            '''
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            '''
            print('label:', b_label0, b_label1, b_label2, b_label3)

            label0, label1, label2, label3 = sess.run([prediction0, prediction1, prediction2, prediction3],
                                                      feed_dict={x: b_image})
            print('predict:', label0, label1, label2, label3)

        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    generate_folder()
    # generate()
    save_as_tf()
    train()
    # test()
