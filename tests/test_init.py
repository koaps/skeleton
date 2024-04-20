#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for `skeleton` package."""

import pytest

import skeleton


def test_version() -> None:
    assert skeleton.__version__.count(".") == 2
