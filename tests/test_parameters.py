from solr_manager.parameters import parse_params, unparse_params


def test_parse_params():
    params = dict(
        q="*:*",
        indent=True,
        q__op="OR",
        omit_header=False,
    )

    parsed = parse_params(params)

    assert parsed["q"] == "*:*"
    assert parsed["indent"] == "true"
    assert parsed["q.op"] == "OR"
    assert parsed["omitHeader"] == "false"

    assert unparse_params(parsed) == params
