#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : primitives
# @Time         : 2020/9/5 2:55 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from featuretools.primitives import *
from featuretools.variable_types import *


# import featuretools as ft
# ft.primitives.list_primitives()

class Quarter(TransformPrimitive):
    name = "quarter"
    input_types = [Datetime]
    return_type = Ordinal

    def get_function(self):
        def weekday(vals):
            return vals.dt.quarter

        return weekday


class DivideNumericPlus(DivideNumeric):
    name = "divide_numeric_plus"

    def get_function(self):
        return lambda s1, s2: s1 / (s2 + 1e-8)  # pd.Series

    def generate_name(self, base_feature_names):
        return "%s / %s" % (base_feature_names[0], base_feature_names[1])


class PowerByFeature(TransformPrimitive):
    name = "power_by_feature"
    input_types = [Numeric]
    return_type = Numeric

    def __init__(self, value=2):
        super().__init__()
        self.value = value

    def get_function(self):
        return lambda df: df.pow(self.value)  # pd.Series

    def generate_name(self, base_feature_names):
        return f"{base_feature_names[0]}^{self.value})"
