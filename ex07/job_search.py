import requests
from bs4 import BeautifulSoup

def scrape_jobs(language="python", max_results=7):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    url = "https://www.juniors.ro/jobs"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="job-item")
    if not jobs:
        print("No job elements found. The website structure may have changed.")
        return []
    results = []

    for job in jobs:
        title = job.find("h2")
        company = job.find("div", class_="job-company")
        location = job.find("div", class_="job-location")
        date = job.find("div", class_="job-date")

        if not title:
            continue

        title_text = title.get_text(strip=True)
        if language.lower() not in title_text.lower():
            continue

        tech_tags = [t.get_text(strip=True) for t in job.find_all("span", class_="badge")]

        results.append({
            "title": title,
            "company": company.get_text(strip=True) if company else "N/A",
            "location": location.get_text(strip=True) if location else "N/A",
            "technologies": ", ".join(tech_tags) if tech_tags else "N/A",
            "date": date.get_text(strip=True) if date else "N/A",
        })

        if len(results) >= max_results:
            break

    return results

def display_jobs(jobs):
    if not jobs:
        print("No jobs found")
        return

    print(f"\nTop {len(jobs)} recent jobs: \n" + "-"*60)
    for i, job in enumerate(jobs, start=1):
        print(f"{i}. {job['title']}")
        print(f"    Company: {job['company']}")
        print(f"    Location: {job['location']}")
        print(f"    Technologies: {job['technologies']}")
        print(f"    Posted: {job['date']}")
        print("-"*60)

if __name__ == "__main__":
    language = input("Enter preferred programming language: ").strip()
    jobs = scrape_jobs(language)
    display_jobs(jobs)
