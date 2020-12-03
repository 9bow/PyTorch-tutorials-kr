# -*- coding: utf-8 -*-
"""
numpy 와 scipy 를 이용한 확장(Extensions) 생성하기
=====================================================
**Author**: `Adam Paszke <https://github.com/apaszke>`_

**Updated by**: `Adam Dziedzic <https://github.com/adam-dziedzic>`_

**번역**: `Ajin Jeong <https://github.com/ajin-jng>`_

이번 튜토리얼에서는 두 가지 작업을 수행할 것입니다:

1. 매개 변수가 없는 신경망 계층 만들기

    - 이는 구현의 일부로서 **numpy** 를 호출합니다.

2. 학습 가능한 가중치가 있는 신경망 계층 생성하기

    - 이는 구현의 일부로서 **Scipy** 를 호출합니다.
"""

import torch
from torch.autograd import Function

###############################################################
# 매개 변수가 없는 예
# ----------------------
#
# 이 레이어는 특별히 유용하거나 수학적으로 올바른 작업을 수행하지 않습니다.
#
# 이름은 BadFFTFunction입니다.
#
# **레이어 구현**

from numpy.fft import rfft2, irfft2


class BadFFTFunction(Function):
    @staticmethod
    def forward(ctx, input):
        numpy_input = input.detach().numpy()
        result = abs(rfft2(numpy_input))
        return input.new(result)

    @staticmethod
    def backward(ctx, grad_output):
        numpy_go = grad_output.numpy()
        result = irfft2(numpy_go)
        return grad_output.new(result)

# 이 계층에는 매개 변수가 없으므로 nn.Module 클래스가 아닌 함수로 간단히 선언 할 수 있습니다.


def incorrect_fft(input):
    return BadFFTFunction.apply(input)

###############################################################
# **생성된 레이어의 사용 예시:**

input = torch.randn(8, 8, requires_grad=True)
result = incorrect_fft(input)
print(result)
result.backward(torch.randn(result.size()))
print(input)

###############################################################
# 매개 변수화 된 예시
# --------------------
#
# 딥러닝 문헌에서 이 레이어는 혼동스럽게도 컨볼루션이라고 칭하지만 실제로는 상호 상관 연산입니다.
# (컨볼루션과 상호 상관의 유일한 차이점은 컨볼루션에서는 필터를 뒤집어서 연산을 한다는 것입니다).
#
# 학습 가능한 가중치를 가진 필터 (커널)을 갖는 교차 상관 연산 계층의 구현
#
# 역방향 패스는 입력에 대한 기울기와 필터에 대한 기울기를 계산합니다.

from numpy import flip
import numpy as np
from scipy.signal import convolve2d, correlate2d
from torch.nn.modules.module import Module
from torch.nn.parameter import Parameter


class ScipyConv2dFunction(Function):
    @staticmethod
    def forward(ctx, input, filter, bias):
        # detach so we can cast to NumPy
        input, filter, bias = input.detach(), filter.detach(), bias.detach()
        result = correlate2d(input.numpy(), filter.numpy(), mode='valid')
        result += bias.numpy()
        ctx.save_for_backward(input, filter, bias)
        return torch.as_tensor(result, dtype=input.dtype)

    @staticmethod
    def backward(ctx, grad_output):
        grad_output = grad_output.detach()
        input, filter, bias = ctx.saved_tensors
        grad_output = grad_output.numpy()
        grad_bias = np.sum(grad_output, keepdims=True)
        grad_input = convolve2d(grad_output, filter.numpy(), mode='full')
        # the previous line can be expressed equivalently as:
        # grad_input = correlate2d(grad_output, flip(flip(filter.numpy(), axis=0), axis=1), mode='full')
        grad_filter = correlate2d(input.numpy(), grad_output, mode='valid')
        return torch.from_numpy(grad_input), torch.from_numpy(grad_filter).to(torch.float), torch.from_numpy(grad_bias).to(torch.float)


class ScipyConv2d(Module):
    def __init__(self, filter_width, filter_height):
        super(ScipyConv2d, self).__init__()
        self.filter = Parameter(torch.randn(filter_width, filter_height))
        self.bias = Parameter(torch.randn(1, 1))

    def forward(self, input):
        return ScipyConv2dFunction.apply(input, self.filter, self.bias)


###############################################################
# **사용 예시:**

module = ScipyConv2d(3, 3)
print("Filter and bias: ", list(module.parameters()))
input = torch.randn(10, 10, requires_grad=True)
output = module(input)
print("Output from the convolution: ", output)
output.backward(torch.randn(8, 8))
print("Gradient for the input map: ", input.grad)

###############################################################
# **기울기 확인:**

from torch.autograd.gradcheck import gradcheck

moduleConv = ScipyConv2d(3, 3)

input = [torch.randn(20, 20, dtype=torch.double, requires_grad=True)]
test = gradcheck(moduleConv, input, eps=1e-6, atol=1e-4)
print("Are the gradients correct: ", test)
