from pytest import raises

from chalicelib.aws import SSMConfigStore


def test_ssm_config_store_raises_if_no_prefix():
    with raises(ValueError):
        SSMConfigStore(None)
    with raises(ValueError):
        SSMConfigStore("")


class StubbedSSMConfigStore(SSMConfigStore):

    def _get_param(self, param_name):
        return f"value-for-{param_name}"


def test_store_uses_prefix():
    store = StubbedSSMConfigStore("foo-bar ")
    assert store.banana == "value-for-FOO_BAR_BANANA"
