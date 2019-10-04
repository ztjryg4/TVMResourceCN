from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
import datetime

net = model_zoo.get_model('ssd_512_mobilenet1.0_voc', pretrained=True)

TEST_NUM = 6

for i in range(0,TEST_NUM):
    start1 = datetime.datetime.now()
    im_fname = '/home/ztj/.tvm_test_data/data/mxnet_multi/'+str(i)+'.jpg'
    x, img = data.transforms.presets.ssd.load_test(im_fname, short=512)
    class_IDs, scores, bounding_boxes = net(x)
    end1 = datetime.datetime.now()
    print(end1-start1)
    # ax = utils.viz.plot_bbox(img, bounding_boxes[0], scores[0],
    #                      class_IDs[0], class_names=net.classes)
    # plt.show()
