# -*- coding: utf-8 -*-
"""Tries different implementations to query many urls and detects
the optimal implementation and the possible parallelism of the
internet connection and the hardware used
"""
from __future__ import print_function

import datetime
import pickle
import os

import pandas

from query_model.query_url_implementations import (
    run_urllib2_multiprocessing,
    run_curl_multiprocessing,
    run_human_curl_async
)
from query_model.measurement_utils import (
    repeat_measurement_and_describe, get_actor_list,
    conf2strargs)


def measure_all_query_url_implementations(
        url_list,
        repetitions,
        parallelism_test_array
        ):
    print("Comparing query operation of {0} urls with "
        "repetitions={1}, parallelism_test_array={2}".format(
        len(url_list),repetitions,parallelism_test_array
    ))

    points = []

    # excluded because non deterministic behaviour
    #points.append(repeat_measurement_and_describe(
    #    url_list=url_list,
    #    repetitions=repetitions,
    #    parallelism=0,
    #    measurement_fct=run_pycurl_async
    #))

    # excluded because every implementation is faster with p>1
    #points.append(repeat_measurement_and_describe(
    #    url_list=url_list,
    #    repetitions=repetitions,
    #    parallelism=1,
    #    measurement_fct=run_curl_single_process
    #))

    for parallelism in parallelism_test_array:
        for fct in (
                run_human_curl_async,
                run_urllib2_multiprocessing,
                run_curl_multiprocessing
                ):
            points.append(repeat_measurement_and_describe(
                url_list=url_list,
                repetitions=repetitions,
                parallelism=parallelism,
                measurement_fct=fct
            ))
    return points


def find_best_query_urls_implementation(
        actor_count,
        repetitions,
        parallelism_test_array_minimum,
        parallelism_test_array_maximum,
        parallelism_test_array_step_size,
        actor_source,
        quiet=False
        ):

    parallelism_test_array = range(
        parallelism_test_array_minimum,
        parallelism_test_array_maximum+1,
        parallelism_test_array_step_size
    )

    file_name = u'{0}__{1}__{2}.pickle'.format(
        find_best_query_urls_implementation.__name__,
        u'__'.join(conf2strargs(dict(
            actor_count=actor_count,
            repetitions=repetitions,
            test_array="{0}_up_to_{1}".format(
                min(parallelism_test_array),
                max(parallelism_test_array)
            )
        ), sep="_")),
        datetime.datetime.strftime(datetime.datetime.now(),
            '%Y%m%d-%H%M%S')
    )
    assert not os.path.exists(file_name)

    res = measure_all_query_url_implementations(
        url_list=get_actor_list(actor_source=actor_source, limit=actor_count),
        repetitions=repetitions,
        parallelism_test_array=parallelism_test_array
    )
    df = pandas.DataFrame(res)

    with open(file_name, 'wb') as fp:
        pickle.dump(df, fp)

    if not quiet:
        print("Saved the result as '{0}'.".format(file_name))

    #df.set_index(['parallelism','identifier']).sort(['median','sd'])
    if not quiet:
        res = df.set_index(['parallelism','identifier'])\
            .sort(['max','median','sd'])
        print(res)

    optimal_row = df[df['max'] == min(df['max'])]
    if not quiet:
        print('\n',optimal_row,'\n')

    best_algorithm = optimal_row['identifier'].item()
    optimal_parallelism = int(optimal_row['parallelism'])

    if not quiet:
        print("Best algorithm: '{0}'. Optimal parallelism value: {1}".format(
            best_algorithm, optimal_parallelism
        ))
    return best_algorithm, optimal_parallelism


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Measure different implementations to query many urls and detect "
        "optimal implementation and parallelism of connection"
    )
    parser.add_argument("-n", "--actor-count",
        default=20, type=int,
        help="Urls to crawl during a test. Default: 20"
    )
    parser.add_argument("--parallelism-test-array-step-size",
        default=2, type=int,
        help=("Stepsize for test array. Default: 2")
    )
    parser.add_argument("--parallelism-test-array-minimum",
        default=2, type=int,
        help=("Script will test starting from <p> "
            "parallel workers. Default: 2")
    )
    parser.add_argument("-p", "--parallelism-test-array-maximum",
        default=12, type=int,
        help=("Script will test up to <p> parallel workers. Default: 12")
    )
    parser.add_argument(
        "-r", "--repetitions", default=10, type=int,
        help="Repeat the test of each <p> <r> times. Default: 10"
    )
    parser.add_argument(
        "-s", "--actor-source", default='http://141.52.218.200', type=str,
        help=("Source that responds with a JSON list "
              "of actor URIs. Default: 'http://141.52.218.200'")
    )
    find_best_query_urls_implementation(
        quiet=False,
        **parser.parse_args().__dict__
    )
