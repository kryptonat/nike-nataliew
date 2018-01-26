#!/usr/bin/env python

import json

from model.generic_model import GenericModel


def list_all(event, context):
  all_gm = GenericModel.scan()
  gm_params = [{"key": gm.key, "values": list(gm.values)} for gm in all_gm]

  return {
    "statusCode": 200,
    "body": json.dumps(gm_params)
  }
