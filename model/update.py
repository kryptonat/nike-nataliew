#!/usr/bin/env python

import logging

from pynamodb.exceptions import DoesNotExist

from model.generic_model import GenericModel


def update(event, context):
  m_key = event.get("path", {}).get("key")
  m_values = event.get("body", {}).get("values")

  if not m_values or not m_key:
    logging.error("Update Error: Must have key and values. Event %s" % event)
    raise Exception("[422] Could not update item")

  try:
    gm = GenericModel.get(hash_key=m_key)
  except DoesNotExist:
    raise Exception("[404] Item does not exist")

  gm.values = set(m_values)
  gm.save()

  return {
    "statusCode": 200,
    "result": {
      "key": gm.key,
      "values": list(gm.values)
    }
  }
