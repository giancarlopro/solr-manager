from solr_manager.parameters import unparse_params
from solr_manager.response import SolrResponse

SAMPLE = {
    "responseHeader": {
        "zkConnected": True,
        "status": 0,
        "QTime": 159,
        "params": {
            "q": "*:*",
            "indent": "true",
            "q.op": "OR",
            "useParams": "",
            "_": "1693348907428",
        },
    },
    "response": {
        "numFound": 99777993,
        "start": 0,
        "maxScore": 1.0,
        "numFoundExact": True,
        "docs": [
            {
                "id": "d9adac9321c111df350b7efde4eb50e43dc3f894069c8dc6806df7b016c254c0",  # noqa: E501
                "chat_id": "919032925925-1572134337@g.us",
                "sender_id": (
                    "3a3d660772af614a7f48474faed3e06047af0f7dfef138ad0c9ba49fc317e6ed"
                ),
                "forwarding_score": 0,
                "type_label": "unknown",
                "datetime": "2022-01-12T18:57:29Z",
                "shard_key": "2021-01-01T00:00:00Z",
                "_version_": 1774622286761951232,
            }
        ],
    },
}


def test_response():
    response = SolrResponse(SAMPLE)

    assert response.docs == SAMPLE["response"]["docs"]
    assert response.raw == SAMPLE
    assert response.header.q_time == SAMPLE["responseHeader"]["QTime"]
    assert response.header.status == SAMPLE["responseHeader"]["status"]
    assert response.header.params == unparse_params(SAMPLE["responseHeader"]["params"])
    assert response.header.zk_connected == SAMPLE["responseHeader"]["zkConnected"]
    assert response.num_found == SAMPLE["response"]["numFound"]
    assert response.start == SAMPLE["response"]["start"]
    assert response.max_score == SAMPLE["response"]["maxScore"]
