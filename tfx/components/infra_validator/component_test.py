# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Tests for tfx.components.infra_validator.component."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tfx.components.infra_validator import component
from tfx.proto import infra_validator_pb2
from tfx.types import channel_utils
from tfx.types import standard_artifacts


class ComponentTest(tf.test.TestCase):

  def testConstruct(self):
    model = standard_artifacts.Model()
    serving_spec = infra_validator_pb2.ServingSpec()
    validation_spec = infra_validator_pb2.ValidationSpec()
    infra_validator = component.InfraValidator(
        model=channel_utils.as_channel([model]),
        serving_spec=serving_spec,
        validation_spec=validation_spec)

    # Check channels have been created with proper type.
    self.assertEqual(standard_artifacts.Model,
                     infra_validator.inputs['model'].type)
    self.assertEqual(standard_artifacts.InfraBlessing,
                     infra_validator.outputs['blessing'].type)

    # Check exec_properties have been populated.
    self.assertIn('serving_spec', infra_validator.exec_properties)
    self.assertIn('validation_spec', infra_validator.exec_properties)

  def testEnableCache(self):
    model = standard_artifacts.Model()
    serving_spec = infra_validator_pb2.ServingSpec()
    validation_spec = infra_validator_pb2.ValidationSpec()
    infra_validator_1 = component.InfraValidator(
        model=channel_utils.as_channel([model]),
        serving_spec=serving_spec,
        validation_spec=validation_spec)
    self.assertEqual(None, infra_validator_1.enable_cache)
    infra_validator_2 = component.InfraValidator(
        model=channel_utils.as_channel([model]),
        serving_spec=serving_spec,
        validation_spec=validation_spec,
        enable_cache=True)
    self.assertEqual(True, infra_validator_2.enable_cache)


if __name__ == '__main__':
  tf.test.main()
