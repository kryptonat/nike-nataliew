#!/usr/bin/env python

import mock
import pytest

from pynamodb.exceptions import DoesNotExist

from model.delete import delete


class TestModelDelete(object):

  @mock.patch("model.delete.GenericModel", autospec=True)
  def test_delete_item_with_existing_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "value": "baseball"
      }
    }

    mock_gm = mock.MagicMock(key="sports", values={"soccer", "baseball"})
    MockGenericModelClass.get.return_value = mock_gm

    response = delete(mock_event, {})

    assert mock_gm.save.calledOnce
    assert mock_gm.values == {"soccer"}
    assert response.get("statusCode") == 204

  @mock.patch("model.delete.GenericModel", autospec=True)
  def test_delete_item_with_no_existing_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "value": "baseball"
      }
    }

    mock_gm = mock.MagicMock(key="sports", values={"soccer", "tennis"})
    MockGenericModelClass.get.return_value = mock_gm

    response = delete(mock_event, {})

    assert mock_gm.save.calledOnce
    assert mock_gm.values == {"soccer", "tennis"}
    assert response.get("statusCode") == 204

  @mock.patch("model.delete.GenericModel", autospec=True)
  def test_delete_invalid_key(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
      "body": {
        "value": "baseball"
      }
    }

    MockGenericModelClass.get.side_effect = DoesNotExist

    with pytest.raises(Exception):
      delete(mock_event, {})

  def test_delete_with_bad_input_event(self):

    bad_input_events = [
      {},
      {"body": {"value": "soccer"}},
      {"path": {"key": "sports"}}
    ]

    for event in bad_input_events:
      with pytest.raises(Exception):
        delete(event, {})
