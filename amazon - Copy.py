import json
import csv
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

url = "https://www.amazon.com/s?k=macbook+air+m4&crid=2XZR11J5Z7UL0&sprefix=macbook%2Caps%2C428&ref=nb_sb_ss_ts-doa-p_6_7"

async def extract_amazon_products():
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True
    )

    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Amazon product search result",
                "baseSelector": "[data-component-type='s-search-result']",
                "fields": [
                    {"name": "title", "selector": "h2 span", "type": "text"},
                    {"name": "image", "selector": ".s-image", "type": "attribute", "attribute": "src"},
                    {"name": "rating", "selector": ".a-icon-star-small .a-icon-alt", "type": "text"},
                    {"name": "reviews_count", "selector": "[data-csa-c-func-deps=aui-da-a-popover]", "type": "text"},
                    {"name": "price", "selector": ".a-price .a-offscreen", "type": "text"}
                ]
            }
        )
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawler_config, cache_mode=CacheMode.BYPASS)

        if result and result.extracted_content:
            products = json.loads(result.extracted_content)
            print(f"Total products found: {len(products)}")
            
            # Hiển thị dữ liệu ra console
            for product in products:
                print("\n Product Details:")
                print(f"Title:  {product.get('title')}")
                print(f"Price: {product.get('price')}")
                print(f"Rating: {product.get('rating')}")
                print(f"Image: {product.get('image')}")
                print(f"Review Count: {product.get('reviews_count')}")
                print("-" * 80)
            
            # Ghi vào file CSV
            csv_filename = "amazon_products.csv"
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["title", "price", "rating", "image", "reviews_count"])
                writer.writeheader()
                writer.writerows(products)
            
            print(f"\nData saved to {csv_filename}")

if __name__ == "__main__":
    asyncio.run(extract_amazon_products())
