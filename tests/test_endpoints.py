#!/usr/bin/env python

import json
import requests

from .config import ENDPOINT_TO_TEST


class TestEndpoints(object):
  """
  Very basic endpoint tests.
  """

  def test_add_with_endpoint(self):

    response = requests.post(ENDPOINT_TO_TEST + "/" + "furniture", json={
      "value": "couch"
    })

    assert response.status_code == 200

  def test_add_with_endpoint_with_bad_input(self):

    response = requests.post(ENDPOINT_TO_TEST + "/" + "furniture", data={
      "some-key": "XYZ"
    })

    assert response.status_code == 422

  def test_get_with_endpoint(self):

    requests.post(ENDPOINT_TO_TEST + "/" + "furniture", json={
      "value": "couch"
    })
    response = requests.get(ENDPOINT_TO_TEST  + "/" + "furniture")
    result = json.loads(response.content).get("result", {})
    values = result.get("values")
    assert "couch" in values

  def test_update_with_endpoint(self):

    requests.post(ENDPOINT_TO_TEST + "/" + "sports", json={
      "value": "high jump"
    })
    response = requests.put(ENDPOINT_TO_TEST + "/" + "sports", json={
      "values": ["running", "soccer"]
    })

    assert response.status_code == 200
    result = json.loads(response.content).get("result", {})
    assert result.get("values") == ["running", "soccer"]
    assert result.get("key") == "sports"

  def test_delete_with_endpoint(self):

    response = requests.delete(ENDPOINT_TO_TEST + "/" + "sports", json={
      "value": "soccer"
    })

    assert response.status_code == 200

  def test_delete_with_endpoint_with_bad_payload(self):

    response = requests.delete(ENDPOINT_TO_TEST + "/" + "sports")

    assert response.status_code == 422

  def test_list_with_endpoint(self):

    response = requests.get(ENDPOINT_TO_TEST)

    assert response.status_code == 200
    results = json.loads(response.content)
    assert len(results) > 0
