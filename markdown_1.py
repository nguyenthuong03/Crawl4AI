import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

url = "https://cellphones.com.vn/sforum/bang-gia-chatgpt"

async def main():
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.8, threshold_type="fixed")
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        markdown_generator=md_generator
    )

    browser_config = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)

        print("Raw markdown length: ", len(result.markdown))
        print("Filtered markdown length: ", len(result.markdown_v2.fit_markdown))
        print(result.markdown_v2.fit_markdown)

        # **Lưu vào file markdown**
        filename = "output.md"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(result.markdown_v2.fit_markdown)
        
        print(f"\nData has been saved to {filename}")

if __name__ == "__main__":
    asyncio.run(main())
