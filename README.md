# Image Manipulator

A short program to hide messages within images.

The message is first turned into binary by the `dec_to_bin()` function and each digit replaces the ending digit of one of the color values in a pixel in the image. These pixels are spread out throughout the image with the size of the stride depending on the length of the message.

The `manipulate_image()` function takes in the image and the binary message and hides the message in the image.

The `decrypt()` function takes in the image and message length and tries to find a message in the image and returns the result. Message length is required to determine the stride of the pixels