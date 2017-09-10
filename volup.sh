#!/bin/bash
sudo amixer set PCM -- $[$(amixer get PCM|grep -o [0-9]*%|sed 's/%//')+2]%
