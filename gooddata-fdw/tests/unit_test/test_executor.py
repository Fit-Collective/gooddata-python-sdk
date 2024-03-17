# (C) 2022 GoodData Corporation

import unittest.mock as mock

import gooddata_fdw.executor as executor
import gooddata_fdw.options as options
import pytest


@pytest.mark.parametrize(
    "table_options, expected_executor",
    [
        (dict(workspace="123"), executor.CustomExecutor),
        (dict(workspace="123", insight="abcd"), executor.InsightExecutor),
        (dict(workspace="123", insight="abcd", compute="c"), executor.InsightExecutor),
        (dict(workspace="123", compute="c"), executor.ComputeExecutor),
    ],
    ids=["custom", "insight", "insight-priority", "compute"],
)
def test_executor_factory(test_config, table_options, expected_executor):
    inputs = executor.InitData(
        mock.Mock(name="sdk"),
        options.ServerOptions(dict(host=test_config["host"], token=test_config["token"])),
        options.TableOptions(table_options),
        mock.Mock(name="table_columns"),
    )

    assert isinstance(executor.ExecutorFactory.create(inputs), expected_executor)
