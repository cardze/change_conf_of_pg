#! /bin/bash
rm -f ~/logs/ext4slower.log
ext4slower -j > ~/logs/ext4slower.log 2>&1 &