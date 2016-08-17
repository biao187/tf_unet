# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jul 28, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from tf_unet import image_gen
from tf_unet import unet
from tf_unet import util


if __name__ == '__main__':
    nx = 572*2
    ny = 572*2
    channels = 1
    n_class = 2
     
    training_iters = 20
    epochs = 10
    dropout = 0.75 # Dropout, probability to keep units
    display_step = 2
    restore = False
 
    generator = image_gen.get_image_gen(nx, ny, cnt=20)
    
    net = unet.Unet(channels=channels, n_class=n_class, layers=4, features_root=64)
    
    trainer = unet.Trainer(net)
    path = trainer.train(generator, "./unet_trained", 
                         training_iters=training_iters, 
                         epochs=epochs, 
                         dropout=dropout, 
                         display_step=display_step, 
                         restore=restore)
     
    x_test, y_test = generator(4)
    prediction = net.predict(path, x_test)
     
    print("Testing error rate: {:.2f}%".format(unet.error_rate(prediction, y_test)))
    img = util.combine_img_prediction(x_test, y_test, prediction)
    util.save_image(img, "prediction.jpg")
