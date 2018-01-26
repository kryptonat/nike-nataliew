#!/usr/bin/env python

import json
import mock

from model.list import list_all


class TestModelListAll(object):

  @mock.patch("model.list.GenericModel", autospec=True)
  def test_list_all(self, MockGenericModelClass):

    mock_sports_values = {"baseball", "softball", "tennis"}
    mock_furniture_values = {"chair"}
    mock_entries = [
      mock.MagicMock(key="sports", values=mock_sports_values),
      mock.MagicMock(key="furniture", values=mock_furniture_values),
    ]

    MockGenericModelClass.scan.return_value = mock_entries

    response = list_all({}, {})

    assert response.get("statusCode") == 200
    body_data = json.loads(response.get("body"))
    expected_key_values = [
      {
        "key": "sports",
        "values": list(mock_sports_values)
      },
      {
        "key": "furniture",
        "values": list(mock_furniture_values)
      }
    ]
    assert body_data == expected_key_values

  @mock.patch("model.list.GenericModel", autospec=True)
  def test_list_all_empty(self, MockGenericModelClass):

    MockGenericModelClass.scan.return_value = []

    response = list_all({}, {})

    assert response.get("statusCode") == 200
