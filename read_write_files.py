import asyncio
import aiofiles                # Asynchronous file I/O
from aioconsole import ainput # Asynchronous console input


def callback(future):
	# First check if any exceptions arose, like a file not found
	e = future.exception()
	if e:
		print(e)
	else:
		# Get the result, check which function called it and act accordingly
		result = future.result()
		if result[0] == read:
			print("Read from "+result[1]+":\n\t"+result[2])
		else:
			print("Wrote to "+result[1]+":\n\t"+result[2])
	# Important! Notice how release() isn't a coroutine, so it doesn't have to be awaited
	# This allows us to signal a waiting coroutine from a synchronous callback like this one
	lock.release()

async def read(filename):
	async with aiofiles.open(filename, "r") as file:
		text = await file.read()
	# A pretty bad way to signal to a callback which coroutine called it
	return (read, filename, text)

async def write(filename, text):
	async with aiofiles.open(filename, "w") as file:
		await file.write(text)
	return (write, filename, text)

async def main():
	while True:
		# Only ask for input again when the callback ends,
		# so we don't end up with a mess of output
		await lock.acquire()
		action = await ainput("Would you like to read ('r') or write ('w') to a file? ('s' to stop)\n> ")
		if action in ["read", "r"]:
			# The user wants to read from a file, get the filename
			filename = await ainput("Which file would you like to read from?\n> ")
			# Create the coroutine
			co = read(filename)
			
		elif action in ["write", "w"]:
			# The user wants to write to a file, get the file name and the text
			filename = await ainput("Which file would you like to write to?\n> ")
			text = await ainput("What would you like to write to "+filename+"?\n> ")
			# Create the coroutine
			co = write(filename, text)
		
		elif action in ["s", "stop"]:
			break
		else:
			continue
		
		# If the coroutine was created, get a task for it
		# and add a callback for that task
		task = loop.create_task(co)
		task.add_done_callback(callback)

if __name__ == "__main__":
	# A lock used by the main() coroutine
	lock = asyncio.Lock()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()
