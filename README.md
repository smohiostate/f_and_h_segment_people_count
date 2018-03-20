# F&H segment based people count

R-CNN based people-detection algorithm works as follows:
1. Region-proposals are generated based on F&H segments and selective-search based hierarchical proposal generation
2. A pre-trained CNN based people-classifier is deployed on each proposed region
3. A non-maximal suppression layer acts on the results of the previous layer, and removes proposals that are deemed "too close" to each other

See https://docs.microsoft.com/en-us/cognitive-toolkit/object-detection-using-fast-r-cnn for a nice illustration of above. See
https://www.cs.cornell.edu/~dph/papers/seg-ijcv.pdf for original paper on segmentation by Felzenszwalb & Huttenlocher (F&H).

An issue with the above approach is that, when two persons are close together in an image, the bounding boxes around them are merged. For people-counting applications, this leads to incorrect results (lower number of counts).
We address this by introducing a new distance measure between bounding boxes based on F&H segments, and feeding this measure to the NMS layer. The hypothesis here is that, even if two persons are close together, the core segments constituting each person would be different and hence the bounding boxes around these people are better separable in the segment-space.
An illustration is below. Below, on the left is the people-detections performed by classic R-CNN using NMS as post-processing layer. In the middle is the core F&H segments constituting the persons, and on the right is the result of using F&H segment based distance measure in NMS layer. 

![Optional Text](../commit_branch/illustration/illus_1.png)

![Optional Text](../commit_branch/illustration/illus_2.png)

![Optional Text](../commit_branch/illustration/illus_3.png)

![Optional Text](../commit_branch/illustration/illus_4.png)


It can be readily noted that, on the left, persons are grouped together due to closeness at pixel level. While on the right, using the unique segments separating the persons, we are able to better separate the persons and get a more accurate count of persons.

The code is within notebooks folder - 07-Segment-Based-Counting-Validation.ipynb. The various parameters used were:
1. Percentage threshold to determine if an F&H segment constitutes a bounding box
2. Percentage threshold to determine if a bounding box is considered a super-set of another
3. Percentage threshold on segment overlap to determine if two bounding boxes need to be merged.

These parameters were tuned recursively and set at specific values within the code. A new set of images from a specific domain may need re-tuning of the parameters. 

Also, the R-CNN model file 'VGGnet_fast_rcnn_iter_150000.ckpt' is widely available in open source, and need to be loaded into /models/human folder.

Open source repositories used to build this: 

[Fast-RCNN] https://github.com/rbgirshick/fast-rcnn

[Selective Search] https://github.com/AlpacaDB/selectivesearch
