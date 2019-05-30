@ECHO off

kernprof -l countHand_profile.py
python -m line_profiler ../Python/countHand_profile.py > profile_countHand.txt