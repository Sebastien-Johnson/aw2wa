import subprocess
import time

def main():
    start_time = time.time()
    subprocess.run(["scrapy", "runspider", "pdf_spider.py"], cwd="./web_scraper/web_scraper/spiders")
    end_time = time.time()
    print("=============================")
    print(f"Runtime: {end_time-start_time:.5f} sec")
    print("=============================")
if __name__ == "__main__":
    main()