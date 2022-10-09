# Copyright 2022 Oscar Higgott

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from pymatching.matching import Matching


def test_qubit_id_accepted_using_add_edge():
    m = Matching()
    m.add_edge(0, 1, qubit_id=0)
    m.add_edge(1, 2, qubit_id={1, 2})
    es = list(m.edges())
    expected_edges = [
        (0, 1, {'fault_ids': {0}, 'weight': 1.0, 'error_probability': -1.0}),
        (1, 2, {'fault_ids': {1, 2}, 'weight': 1.0, 'error_probability': -1.0})
    ]
    assert es == expected_edges


def test_add_edge_raises_value_error_if_qubit_id_and_fault_ids_both_supplied():
    with pytest.raises(ValueError):
        m = Matching()
        m.add_edge(0, 1, qubit_id=0, fault_ids=0)
        m.add_edge(1, 2, qubit_id=1, fault_ids=1)


def test_add_edge():
    m = Matching()
    m.add_edge(0, 1)
    m.add_edge(1, 2)
    assert m.num_nodes == 3
    assert m.num_edges == 2

    m = Matching()
    m.add_edge(0, 1, weight=0.123, error_probability=0.6)
    m.add_edge(1, 2, weight=0.6, error_probability=0.3, fault_ids=0)
    m.add_edge(2, 3, weight=0.01, error_probability=0.5, fault_ids={1, 2})
    expected = [(0, 1, {'fault_ids': set(), 'weight': 0.123, 'error_probability': 0.6}),
                (1, 2, {'fault_ids': {0}, 'weight': 0.6, 'error_probability': 0.3}),
                (2, 3, {'fault_ids': {1, 2}, 'weight': 0.01, 'error_probability': 0.5})]
    assert m.edges() == expected
