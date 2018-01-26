#!/usr/bin/env python

import logging

from pynamodb.exceptions import DoesNotExist

from model.generic_model import GenericModel


def add(event, context):

  m_key = event.get("path", {}).get("key")
  m_value = event.get("body", {}).get("value")

  if not m_value or not m_key:
    logging.error("Add Error: Must have key and value. key: %s, value: %s" % (m_key, m_value))
    raise Exception("[422] Could not add item")

  try:
    gm = GenericModel.get(hash_key=m_key)
  except DoesNotExist:
    # Create item if it does not yet exist.
    gm = GenericModel(key=m_key)

  gm.values.add(m_value)

  print gm.key

  gm.save()

  return {
    "statusCode": 201,
    "message": "Item successfully added"
  }
