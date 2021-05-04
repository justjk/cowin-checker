#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Enter district id"
    exit 1
fi

scrapy crawl cowin -a district_ids=$1 -a age=$2