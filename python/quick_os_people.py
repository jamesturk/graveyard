import csv
import requests


def process_row(row):
    lat = row["lat"]
    lng = row["lon"]

    url = f"https://v3.openstates.org/divisions.geo?lat={lat}&lng={lng}"
    resp = requests.get(url).json()

    ids = sorted(d["id"] for d in resp["divisions"])
    if not ids:
        print(row)
        return row
    sldl, sldu = ids

    row["house_district"] = sldl.split(":")[-1]
    row["senate_district"] = sldu.split(":")[-1]

    return row


def process(infile, outfile, max_n=10000000, skip=0):
    encoding = "Windows-1252"
    with open(infile, encoding=encoding) as inf, open(outfile, "w", encoding="utf8") as outf:
        reader = csv.DictReader(inf)
        writer = csv.DictWriter(
            outf, reader.fieldnames + ["house_district", "senate_district"]
        )
        writer.writeheader()

        n = 0
        for row in reader:
            if skip:
                skip -= 1
                continue
            writer.writerow(process_row(row))
            n += 1
            if n % 1000 == 0:
                print(n)
            if n > max_n:
                break

        print(n, "processed")


process("CPD_PROJECT.CSV", "cpd_processed_pt4.csv", skip=12800)
