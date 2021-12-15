# py 00_get_data.py clicks.txt > denormalized_data.txt && py 01_count_over_clicks.py denormalized_data.txt > grouped.txt && py 03_count_time_locations.py denormalized_data.txt > pre_location.txt && py 04_beautify_time_locations.py
py 00_get_data.py clicks.txt > denormalized_data.txt \
&& py 01_count_over_clicks.py denormalized_data.txt > grouped.txt \
&& py 03_count_time_locations.py denormalized_data.txt > pre_location.txt \
&& py 04_beautify_time_locations.py