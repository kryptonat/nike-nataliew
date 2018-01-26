#!/usr/bin/env python

import os

from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute
from pynamodb.models import Model


class GenericModel(Model):
  """
  A generic model that stores values for a given key.
  """
  class Meta:
    table_name = os.environ.get("DYNAMODB_TABLE")
    if "ENV" in os.environ:
      host = "http://localhost:8000"
    else:
      region = "us-west-1"
      host = "https://dynamodb.us-west-1.amazonaws.com"

  key = UnicodeAttribute(hash_key=True)
  values = UnicodeSetAttribute(null=True, default=set())
