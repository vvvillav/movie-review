import csv

def parse_line(line):
    if ': ' in line:
        key, value = line.split(': ', 1)
        return key.strip(), value.strip()
    else:
        return None, None


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['productId', 'userId', 'profileName', 'helpfulness', 'score', 'time', 'summary', 'text'])  # encabezados de columnas

        review = {}
        for line in infile:
            line = line.strip()
            if line:
                key, value = parse_line(line)
                if key is not None:
                    review[key] = value
            else:
                if review:
                    csv_writer.writerow([review.get('product/productId', ''),
                                         review.get('review/userId', ''),
                                         review.get('review/profileName', ''),
                                         review.get('review/helpfulness', ''),
                                         review.get('review/score', ''),
                                         review.get('review/time', ''),
                                         review.get('review/summary', ''),
                                         review.get('review/text', '')])
                    review = {}


# Cambia 'movies.txt' y 'movies.csv' por las rutas y nombres de tus archivos
process_file('movies.txt', 'movies.csv')
