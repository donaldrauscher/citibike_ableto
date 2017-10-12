#!/usr/bin/env bash

gsutil -m cp *.csv gs://np-training/data/citibike/

bq load --schema schema.json --skip_leading_rows=1 ableto.citibike_raw gs://np-training/data/citibike/*.csv



bq query --destination_table=ableto.citibike --use_legacy_sql=False --flagfile=query.sql