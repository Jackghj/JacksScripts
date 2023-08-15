import json

# Set the path to the file containing the IP addresses to filter for
ip_file_path = "ips.txt"

# Set the field to filter for
field = input("Enter the field to filter for: ")

# Set the output file path
output_file_path = "output.txt"

# Read the IP addresses from the file
with open(ip_file_path) as f:
    ips = [line.strip() for line in f]

# Create the filter
filter_list = []
for ip in ips:
    filter_list.append({"match_phrase": {field: ip}})

filter = {"query": {"bool": {"should": filter_list, "minimum_should_match": 1}}}

# Write the filter to the output file
with open(output_file_path, "w") as f:
    f.write(json.dumps(filter, indent=2))
    
print(f"Filter has been written to {output_file_path}")