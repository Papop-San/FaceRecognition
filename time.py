from datetime import datetime, time

# Get the current time
current_time = datetime.now().time()

# Define the time range
start_time = time(9, 0, 0)
end_time = time(12, 0, 0)

# Check if the current time falls between 09:00:00 and 12:00:00
if start_time <= current_time <= end_time:
    # Set the time to 09:00:00
    current_time = start_time

# Convert the time to string format HH:MM:SS
current_time_str = current_time.strftime('%H:%M:%S')

print("Adjusted time:", current_time_str)
