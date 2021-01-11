#!/usr/bin/env python3

import csv
import sys
import textwrap

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} DATA_TABLE_FILE OUTPUT_FILE")
    sys.exit(-1)

data_table_filename = sys.argv[1]
output_filename = sys.argv[2]

entries = []

with open(data_table_filename, "r") as fh:
    reader = csv.DictReader(fh)

    for row in reader:
        entries.append(row)

with open(output_filename, "w") as fh:
    fh.write(textwrap.dedent("""\
    /* This file is generated by scripts/generate_voice_param_table.py. Do not edit directly. */
    /* clang-format off */

    #include "gem_voice_param_table.h"
    #include "fix16.h"

    const struct GemVoltageAndPeriod gem_voice_voltage_and_period_table[] = {
    """))

    for row in entries:
        fh.write(f"  {{.voltage = F16({row['Input CV']}), .period = {row['period reg']}}},\n")

    fh.write(textwrap.dedent("""\
    };

    struct GemDACCodePair gem_voice_dac_codes_table[] = {
    """))

    for row in entries:
        fh.write(f"  {{.castor = {row['castor calibrated dac code']}, .pollux = {row['pollux calibrated dac code']} }},\n")


    fh.write(textwrap.dedent("""\
    };

    size_t gem_voice_param_table_len = sizeof(gem_voice_voltage_and_period_table) / sizeof(struct GemVoltageAndPeriod);
    
    /* clang-format on */
    """))
