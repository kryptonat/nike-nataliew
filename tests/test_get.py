#!/usr/bin/env python

import mock
import pytest

from pynamodb.exceptions import DoesNotExist

from model.get import get


class TestModelGet(object):

  @mock.patch("model.get.GenericModel", autospec=True)
  def test_get_key_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
    }

    mock_values = {"soccer", "basketball"}
    mock_gm = mock.MagicMock(key="sports", values=mock_values)
    MockGenericModelClass.get.return_value = mock_gm

    response = get(mock_event, {})

    assert response.get("statusCode") == 200
    body_data = response.get("result", {})
    assert body_data.get("key") == "sports"
    assert body_data.get("values") == list(mock_values)

  @mock.patch("model.get.GenericModel", autospec=True)
  def test_get_non_existent_key_value(self, MockGenericModelClass):

    mock_event = {
      "path": {
        "key": "sports"
      },
    }

    MockGenericModelClass.get.side_effect = DoesNotExist

    with pytest.raises(Exception):
      get(mock_event, {})

  def test_get_with_bad_input_event(self):

    bad_input_event = {}
    with pytest.raises(Exception):
      get(bad_input_event, {})
