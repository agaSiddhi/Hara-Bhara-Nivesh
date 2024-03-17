from bs4 import BeautifulSoup
import http.client
import csv

def parse_and_save_to_csv(result, csv_writer):
    soup = BeautifulSoup(result, "html.parser")
    company_rows = soup.find_all(class_="company-row d-flex")
    for row in company_rows:
        company_name = row.find('a').text
        esg_risk_rating = row.find(class_="col-lg-6").text.strip()
        score = row.find(class_="col-2").text
        csv_writer.writerow([company_name, esg_risk_rating, score])

def scrape_sustainalytics_data(filename='sustainalytics_data.csv', total_pages=1384):
    conn = http.client.HTTPSConnection("www.sustainalytics.com")

    headersList = {
        "Accept": "/:",
        "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A"
    }

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Company', 'ESG Risk Rating', 'Score'])  # Write header

        for page_number in range(1, total_pages + 1):
            payload = f"--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"industry\"\r\n\r\n\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"rating\"\r\n\r\n\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"filter\"\r\n\r\n\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n{page_number}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"pageSize\"\r\n\r\n10\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"resourcePackage\"\r\n\r\nSustainalytics\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"

            conn.request("POST", "/sustapi/companyratings/getcompanyratings", payload, headersList)
            response = conn.getresponse()
            result = response.read()
            result = result.decode("utf-8")

            try:
                parse_and_save_to_csv(result, csv_writer)
                print(f"Processed page {page_number}")
            except Exception as e:
                print(f"An error occurred while processing page {page_number}:", e)

    print("All pages processed. Data saved to", filename)