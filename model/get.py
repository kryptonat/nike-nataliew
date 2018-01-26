#!/usr/bin/env python

from pynamodb.exceptions import DoesNotExist

from model.generic_model import GenericModel


def get(event, context):
  m_key = event.get("path", {}).get("key")

  if not m_key:
    raise Exception("[422] Key must be specified")

  try:
    gm = GenericModel.get(hash_key=m_key)
  except DoesNotExist:
    raise Exception("[404] Item does not exist")

  return {
    "statusCode": 200,
    "result": {
      "key": gm.key,
      "values": list(gm.values),
    }
  }
