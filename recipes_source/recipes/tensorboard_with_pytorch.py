"""
PyTorch�� TensorBoard ����ϱ�
===================================
TensorBoard�� �ӽŷ��� ������ ���� �ð�ȭ ��Ŷ(toolkit)�Դϴ�.
TensorBoard�� ����ϸ� �ս� �� ��Ȯ���� ���� ���� �׸��� ���� �� �ð�ȭ�ϴ� ��,
�� �׷����� �ð�ȭ�ϴ� ��, ������׷��� ���� ��, �̹����� ����ϴ� �� ���� �� �� �ֽ��ϴ�.
�� Ʃ�丮�󿡼��� TensorBoard ��ġ, PyTorch�� �⺻ ����,
TensorBoard UI�� ����� �����͸� �ð�ȭ �ϴ� ����� �ٷ� ���Դϴ�.

��ġ
----------------------
�𵨰� ���� �׸��� TensorBoard �α� ���͸��� ����Ϸ��� PyTorch�� ��ġ�ؾ� �մϴ�.
Anaconda�� ���� PyTorch 1.4+�� ��ġ�ϴ� ����� ������ �����ϴ�.(����):
::

   $ conda install pytorch torchvision -c pytorch 
   

�Ǵ� pip�� �̿��� ���� �ֽ��ϴ�.

::

   $ pip install torch torchvision

"""

######################################################################
# PyTorch�� TensorBoard ����ϱ�
# -----
# 
# ���� PyTorch�� TensorBoard�� ����غ��ô�! � ���� ����ϱ� ����, 
# ``SummaryWriter`` �ν��Ͻ��� �����ؾ� �մϴ�.
#   

import torch
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

######################################################################
# Writer�� �⺻������ ``./runs/`` ���͸��� ����մϴ�.
# 


######################################################################
# Scalar ����ϱ�
# -----
# 
# �ӽŷ��׿����� �ս� ���� �ֿ� ���� �׸�� �װ��� �н� �� ��� ���ϴ��� �����ϴ� ����
# �߿��մϴ�. Scalar�� �� �н� �ܰ�(step)������ �ս� ���̳� �� ���� ������ ��Ȯ���� �����ϴ� ��
# ������ �ݴϴ�.
#
# Scalar ���� ����Ϸ��� ``add_scalar(tag, scalar_value, global_step=None, walltime=None)``
# �� ����ؾ� �մϴ�. ����, ������ ���� ȸ�� �н��� ����� ``add_scalar``�� �����
# �ս� ���� ����� ���ô�.

x = torch.arange(-5, 5, 0.1).view(-1, 1)
y = -5 * x + 0.1 * torch.randn(x.size())

model = torch.nn.Linear(1, 1)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)

def train_model(iter):
    for epoch in range(iter):
        y1 = model(x)
        loss = criterion(y1, y)
        writer.add_scalar("Loss/train", loss, epoch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
train_model(10)
writer.flush()


###################################################################### 
# ��� ��������(pending) �̺�Ʈ�� ��ũ�� ��ϵǾ����� Ȯ���Ϸ��� ``flush()``
# �޼ҵ带 ȣ���մϴ�.
# 
# ����� �� �ִ� �� ���� TensorBoard �ð�ȭ ����� ã������ 
# `torch.utils.tensorboard tutorials <https://pytorch.org/docs/stable/tensorboard.html>`_ ��
# �����ϼ���.
#
# Summary writer�� �� �̻� �ʿ����� ������ ``close()`` �޼ҵ带 ȣ���մϴ�.
#

writer.close()

######################################################################
# TensorBoard �����ϱ�
# -----
# 
# ����� �����͸� �ð�ȭ�ϱ� ���ؼ� ������ ���� TensorBoard�� ��ġ�մϴ�.
#
# ::
# 
#    $ pip install tensorboard
# 
#
# ����, ������ ����� ��Ʈ �α� ���͸��� �����Ͽ� TensorBoard�� �����մϴ�.
# the directory structure rooted at logdir, looking for .*tfevents.* files.
# ``logdir`` ���ڴ� TensorBoard�� ����� �� �ִ� �̺�Ʈ ���ϵ��� ã�� ���͸��� ����ŵ�ϴ�. 
# TensorBoard�� .*tfevents.* ������ ã�� ���� lodgir�� ���͸� ������ ��������� Ž���մϴ�.
#
# ::
# 
#    $ tensorboard --logdir=runs
# 
# �����ϴ� URL�� �̵��ϰų� `http://localhost:6006/ <http://localhost:6006/>`_ �� �̵��մϴ�.
# 
# .. image:: ../../_static/img/thumbnails/tensorboard_scalars.png
#    :scale: 40 %
# 
# �� ��ú���� �� �������� �սǰ� ��Ȯ���� ��� ���ϴ��� �����ݴϴ�.
# �̸� ����Ͽ� �н� �ӵ�, �н��� �� ��Ÿ ��Į�� ������ ������ ���� �ֽ��ϴ�.
# ���� ����Ű���� ���� �ٸ� �н��� �����鼭 �̷��� ���� ���ص��� ���ϴ� ���� �����ϴ�.


######################################################################
# TensorBoard ��ú��� �����ϱ�
# -----
# 
# `TensorBoard.dev <https://tensorboard.dev/>`_�� ����ϸ� ML ���� ����� 
# �����ϰ� ���ε��ϰ� ������ �� �ֽ��ϴ�. TensorBoard.dev�� ����Ͽ� 
# TensorBoard ��ú��带 ȣ����, ���� �� �����ϼ���.
# 
# ���δ�(uploader)�� ����Ϸ��� TensorBoard �ֽ� ������ ��ġ�ϼ���.
#
# :: 
# 
#    $ pip install tensorboard --upgrade
#
# ������ ���� ����� ����Ͽ� TensorBoard�� ���ε��ϰ� �����ϼ���.
#
# :: 
# 
#   $ tensorboard dev upload --logdir runs \
#   --name "My latest experiment" \ # optional
#   --description "Simple comparison of several hyperparameters" # optional
# 
# ������ �ʿ��ϸ� ``$ tensorboard dev --help``�� �����ϼ���.
#
# **����:** ���ε� �� TensorBoard�� �������̸� ��� ����� �� �� �ֽ��ϴ�. 
# �ΰ��� �����͸� ���ε����� ������.
#
# �͹̳ο��� ������ URL�� TensorBoard�� �ǽð����� Ȯ���Ͻʽÿ�.
# ��: `https://tensorboard.dev/experiment/AdYd1TgeTlaLWXx6I8JUbA <https://tensorboard.dev/experiment/AdYd1TgeTlaLWXx6I8JUbA>`_
#
#
# .. image:: ../../_static/img/thumbnails/tensorboard_dev.png
#    :scale: 40 %
# 
# 
# .. ����::
#   TensorBoard.dev�� ���� ��Į�� ��ú��常 �����մϴ�.

########################################################################
# �� �˾ƺ���
# ----------------------------
# 
# -  `torch.utils.tensorboard <https://pytorch.org/docs/stable/tensorboard.html>`_ docs
# -  `Visualizing models, data, and training with TensorBoard <https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html>`_ tutorial
#
