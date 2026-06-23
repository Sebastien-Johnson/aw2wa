import subprocess

def main():
    subprocess.run(["scrapy", "runspider", "pdf_spider.py"], cwd="./web_scraper/web_scraper/spiders")

if __name__ == "__main__":
    main()