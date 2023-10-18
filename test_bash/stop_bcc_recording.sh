#! /bin/bash
pkill -f "./start_bcc_recording.sh"
killall ext4slower
# mv ~/logs/buffer.log ~/logs/ext4slower.log