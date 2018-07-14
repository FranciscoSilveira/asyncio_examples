import asyncio
import aiohttp
import aiofiles
import os

async def download(session, url):
	filename = os.path.basename(url)
	async with session.get(url) as response:
		async with aiofiles.open(filename, "wb") as fd:
			while True:
				data = await response.content.read(1024)
				if not data:
					break
				fd.write(data)
		return await response.release()
		
		
async def main(loop):
	urls = [
		"http://www.irs.gov/pub/irs-pdf/f1040.pdf",
		"http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
		"http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
		"http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
		"http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
	]
	async with aiohttp.ClientSession(loop=loop) as session:
		tasks = [ download(session, url) for url in urls ]
		await asyncio.gather(*tasks)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop))
