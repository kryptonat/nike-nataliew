#!/usr/bin/env python

import mock
import pytest

from pynamodb.exceptions import DoesNotExist

from model.add import add


class TestModelAdd(object):

  @mock.patch("model.add.GenericModel", autospec=True)
  def test_add_item_with_existing_key(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "value": "baseball"
      }
    }

    mock_gm = mock.MagicMock()
    mock_gm.values = {"softball"}
    MockGenericModelClass.get.return_value = mock_gm

    response = add(mock_event, {})

    MockGenericModelClass.get.assert_called_with("sports")
    assert mock_gm.save.calledOnce
    assert mock_gm.values == {"softball", "baseball"}
    assert response.get("statusCode") == 201

  @mock.patch("model.add.GenericModel", autospec=True)
  def test_add_new_item(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "value": "baseball"
      }
    }

    mock_gm = mock.MagicMock(key="sports", values=set())
    MockGenericModelClass.get.side_effect = DoesNotExist
    MockGenericModelClass.return_value = mock_gm

    response = add(mock_event, {})

    MockGenericModelClass.get.assert_called_with("sports")
    MockGenericModelClass.assert_called_with(key="sports")

    assert mock_gm.save.calledOnce
    assert mock_gm.key == "sports"
    assert mock_gm.values == {"baseball"}
    assert response.get("statusCode") == 201

  def test_add_with_bad_input_event(self):

    bad_input_events = [
      {},
      {"body": {"value": "soccer"}},
      {"path": {"key": "sports"}}
    ]

    for event in bad_input_events:
      with pytest.raises(Exception):
        add(event, {})
