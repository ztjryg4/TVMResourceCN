import tvm
import datetime
from matplotlib import pyplot as plt
from tvm.relay.testing.config import ctx_list
from tvm import relay
from tvm.contrib import graph_runtime
from tvm.contrib.download import download_testdata
from gluoncv import model_zoo, data, utils


######################################################################
# Preliminary and Set parameters
# ------------------------------
# .. note::
#
#   We support compiling SSD on bot CPUs and GPUs now.
#
#   To get best inference performance on CPU, change
#   target argument according to your device and
#   follow the :ref:`tune_relay_x86` to tune x86 CPU and
#   :ref:`tune_relay_arm` for arm CPU.
#
#   To get best performance fo SSD on Intel graphics,
#   change target argument to 'opencl -device=intel_graphics'

supported_model = [
    'ssd_512_resnet50_v1_voc',
    'ssd_512_resnet50_v1_coco',
    'ssd_512_resnet101_v2_voc',
    'ssd_512_mobilenet1.0_voc',
    'ssd_512_mobilenet1.0_coco',
    'ssd_300_vgg16_atrous_voc'
    'ssd_512_vgg16_atrous_coco',
]

model_name = supported_model[3]
dshape = (1, 3, 512, 512)
target_list = ctx_list()
#print(target_list)
#input()

######################################################################
# Convert and compile model for CPU.

block = model_zoo.get_model(model_name, pretrained=True)

def build(target):
    mod, params = relay.frontend.from_mxnet(block, {"data": dshape})
    with relay.build_config(opt_level=3):
        graph, lib, params = relay.build(mod, target, params=params)
    return graph, lib, params

def run(graph, lib, params, ctx):
    # Build TVM runtime
    m = graph_runtime.create(graph, lib, ctx)
    tvm_input = tvm.nd.array(x.asnumpy(), ctx=ctx)
    m.set_input('data', tvm_input)
    m.set_input(**params)
    # execute
    m.run()
    # get outputs
    class_IDs, scores, bounding_boxs = m.get_output(0), m.get_output(1), m.get_output(2)
    return class_IDs, scores, bounding_boxs

start1 = datetime.datetime.now()

for target, ctx in target_list:
    graph, lib, params = build(target)

TEST_NUM = 6

end1 = datetime.datetime.now()

print(end1-start1)

for i in range(0,TEST_NUM):
    start2 = datetime.datetime.now()
    
    im_fname = '/home/ztj/.tvm_test_data/data/mxnet_multi/'+str(i)+'.jpg'
    x, img = data.transforms.presets.ssd.load_test(im_fname, short=512)

    class_IDs, scores, bounding_boxs = run(graph, lib, params, ctx)
    
    end2 = datetime.datetime.now()
    print(end2-start2)
    # ax = utils.viz.plot_bbox(img, bounding_boxs.asnumpy()[0], scores.asnumpy()[0],
                         # class_IDs.asnumpy()[0], class_names=block.classes)
    # plt.show()
