#!/usr/bin/env python

import logging

from pynamodb.exceptions import DoesNotExist

from model.generic_model import GenericModel


def delete(event, context):
  m_key = event.get("path", {}).get("key")
  m_value = event.get("body", {}).get("value")

  if not m_value or not m_key:
    logging.error("Delete Error: Must specify key and value")
    raise Exception("[422] Could not delete item")

  try:
    gm = GenericModel.get(hash_key=m_key)
  except DoesNotExist:
    raise Exception("[404] Item does not exist")

  try:
    gm.values.remove(m_value)
  except KeyError:
    # Assumed that it's ok if value was not in the set.
    pass
  gm.save()

  return {
    "statusCode": 204
  }
