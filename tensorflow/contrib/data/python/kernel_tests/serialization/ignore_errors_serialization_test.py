# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for the IgnoreErrors input pipeline ops."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from tensorflow.contrib.data.python.kernel_tests.serialization import dataset_serialization_test_base
from tensorflow.contrib.data.python.ops import error_ops
from tensorflow.python.data.ops import dataset_ops
from tensorflow.python.ops import array_ops
from tensorflow.python.platform import test


class IgnoreErrorsSerializationTest(
    dataset_serialization_test_base.DatasetSerializationTestBase):

  def _build_ds(self, components):
    return dataset_ops.Dataset.from_tensor_slices(components).map(
        lambda x: array_ops.check_numerics(x, "message")).apply(
            error_ops.ignore_errors())

  def testIgnoreErrorsCore(self):
    components = np.array([1., 2., 3., np.nan, 5.]).astype(np.float32)
    diff_components = np.array([1., 2., 3., np.nan]).astype(np.float32)
    num_outputs = 4
    self.run_core_tests(lambda: self._build_ds(components),
                        lambda: self._build_ds(diff_components), num_outputs)


if __name__ == "__main__":
  test.main()
