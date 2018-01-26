#!/usr/bin/env python

import mock
import pytest

from pynamodb.exceptions import DoesNotExist

from model.update import update


class TestModelUpdate(object):

  @mock.patch("model.update.GenericModel", autospec=True)
  def test_update_item_with_existing_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "values": ["tennis", "swimming"]
      }
    }

    mock_gm = mock.MagicMock(key="sports", values={"soccer", "baseball"})
    MockGenericModelClass.get.return_value = mock_gm

    response = update(mock_event, {})

    body_data = response.get("result", {})
    assert body_data.get("key") == "sports"
    assert body_data.get("values") == ["tennis", "swimming"]
    assert response.get("statusCode") == 200

  @mock.patch("model.update.GenericModel", autospec=True)
  def test_update_item_with_no_existing_key_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "values": ["baseball"]
      }
    }

    MockGenericModelClass.get.side_effect = DoesNotExist

    with pytest.raises(Exception):
      update(mock_event, {})

  def test_update_with_bad_input_event(self):

    bad_input_events = [
      {},
      {"body": {"value": "soccer"}},
      {"body": {"values": "soccer"}},
      {"body": ""},
      {"path": {"key": "sports"}}
    ]

    for event in bad_input_events:
      with pytest.raises(Exception):
        update(event, {})
