#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for `skeleton` CLI."""

import pytest
import re

from skeleton.cli import run

from click.testing import CliRunner

runner = CliRunner()


def test_usage():
    result = runner.invoke(run, [])
    assert result.exit_code == 0
    assert re.match(r"Usage:.*", result.output)


def test_create():
    result = runner.invoke(
        run,
        [
            "--debug",
            "create",
        ],
    )
    assert "Error: Missing option '--db-file'."
    assert result.exit_code == 2


def test_file_not_found():
    result = runner.invoke(run, ["missing.json"])
    assert result.exit_code == 2
