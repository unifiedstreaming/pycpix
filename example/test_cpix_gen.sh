#!/bin/sh

python3 \
    cpix_gen.py \
    --log_level DEBUG \
    --key 0D6B40238DA15E75AF6875C514C59B63:582D6B71611BE04C88E22AAA10441E2C \
    --usage_rule_preset 0D6B40238DA15E75AF6875C514C59B63 audio \
    --key E82F184C3AAA57B4ACE8606B5E3FEBAD:C2FAF66E2852CC4C4A751F0A2A941FDB \
    --usage_rule E82F184C3AAA57B4ACE8606B5E3FEBAD video:max_pixels=442368,bitrate:max_bitrate=500000 \
    --key 087BCFC6F7A55716B8406AA6EBA3369E:8281CE8DB9083697D9770D87DB962835 \
    --usage_rule_preset 087BCFC6F7A55716B8406AA6EBA3369E video_hd \
    --widevine \
    --playready \
    --playready.la_url https://test.playready.microsoft.com/service/rightsmanager.asmx \
    --stdout 
    
    
    
