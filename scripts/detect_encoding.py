import chardet

# Path to your CSV file
csv_file = "CSV-files/data.csv"

# Read the first 10,000 bytes to detect encoding
with open(csv_file, 'rb') as f:
    rawdata = f.read(10000)

result = chardet.detect(rawdata)
print("Detected encoding:", result)