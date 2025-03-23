url = "https://tailieuhust.com/?s=khoa+hoc+du+lieu"

import os, sys
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from base64 import b64decode

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url, 
            cache_mode=CacheMode.BYPASS, 
            pdf=True,
            screenshot=True
        )

        if result.success:
            if result.screenshot:
                
                with open("tailieuhust.png", "wb") as f:
                    f.write(b64decode(result.screenshot))
            if result.pdf:
                with open("tailieuhust.pdf", "wb") as f:
                    f.write(result.pdf)


if __name__=="__main__":
    asyncio.run(main())