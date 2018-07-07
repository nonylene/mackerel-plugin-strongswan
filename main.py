import vici
import os
import json
import time
from typing import Any, Tuple, Iterable, Dict
from collections import Counter
from itertools import chain

SAS_GRAPH_KEY = 'strongswan.sas'
POOLS_GRAPH_KEY = 'strongswan.pools'

SAS_ACTIVE_KEY = 'active'
POOLS_ONLINE_KEY = 'online'
POOLS_SIZE_KEY = 'size'

Metric = Tuple[str, Any]


def meta():
    sas_graph_name = '{0}.#'.format(SAS_GRAPH_KEY)
    pools_graph_name = '{0}.#'.format(POOLS_GRAPH_KEY)
    meta = {
        "graphs": {
            sas_graph_name: {
                "label": "StrongSwan IKE_SAs",
                "unit": "integer",
                "metrics": [{
                    "name": SAS_ACTIVE_KEY,
                    "label": SAS_ACTIVE_KEY
                }]
            },
            pools_graph_name: {
                "label": "StrongSwan Address pool",
                "unit": "integer",
                "metrics": [
                    {
                        "name": POOLS_SIZE_KEY,
                        "label": POOLS_SIZE_KEY
                    },
                    {
                        "name": POOLS_ONLINE_KEY,
                        "label": POOLS_ONLINE_KEY
                    }
                ]
            },
        },
    }
    print("# mackerel-agent-plugin")
    print(json.dumps(meta))


def _print_metric(metric: Metric):
    epoch = int(time.time())
    print('{0}\t{1}\t{2}'.format(metric[0], metric[1], epoch))


def _sas(sess: vici.Session) -> Iterable[Metric]:
    conns = (_conn.decode('UTF-8') for _conn in sess.get_conns()['conns'])
    sas = sess.list_sas()
    sa_names = chain.from_iterable(sa.keys() for sa in sas)
    counter = Counter(sa_names)

    def _create_metric(counter: Counter, conn: str) -> Metric:
        metric_name = '{0}.{1}.{2}'.format(SAS_GRAPH_KEY, conn, SAS_ACTIVE_KEY)
        count = counter[conn]
        return metric_name, count

    return (_create_metric(counter, conn) for conn in conns)


def _pools(sess: vici.Session) -> Iterable[Metric]:
    pools = sess.get_pools(options=None)

    def _create_metrics(pool_name: str, pool: Dict) -> Iterable[Metric]:
        metric_base_name = '{0}.{1}'.format(POOLS_GRAPH_KEY, pool_name)
        return [
            ('{0}.{1}'.format(metric_base_name, 'size'), int(pool['size'])),
            ('{0}.{1}'.format(metric_base_name, 'online'), int(pool['online'])),
        ]

    metricses = (_create_metrics(name, pool) for name, pool in pools.items())
    return chain.from_iterable(metricses)


def main():
    sess = vici.Session()
    for metric in _sas(sess):
        _print_metric(metric)
    for metric in _pools(sess):
        _print_metric(metric)


if __name__ == '__main__':
    if os.environ.get('MACKEREL_AGENT_PLUGIN_META') == '1':
        meta()
    else:
        main()
