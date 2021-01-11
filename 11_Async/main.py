import asyncio
import aiohttp
import argparse
import time
import pathlib
import os


def save_binary(binary, path):
    with open(path, 'wb') as f:
        f.write(binary)


async def fetch(url, session, output_path):
    async with session.get(url, allow_redirects=True) as resp:
        data = await resp.read()
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, save_binary, data,
                                   f'{output_path}{os.sep if output_path else ""}{time.time()}.txt')


async def main(conn_n, urls, output_path):
    while urls:
        coroutines = []
        async with aiohttp.ClientSession() as session:
            for _ in range(conn_n if (urls_n := len(urls)) >= conn_n else urls_n):
                coroutines.append(fetch(urls.pop(0), session, output_path))
            await asyncio.gather(*coroutines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='TextFile', help='Text file with urls to download')
    parser.add_argument('-c', '--concurrent', type=int, default=0, help='How many urls will be processed concurrently')
    parser.add_argument('-o', '--output', help='Folder, where the files will be saved', type=str, default='')
    parser.add_argument('-v', '--verbose', help='Some performance and info stats', action="store_true")
    args = parser.parse_args()
    if save_folder := args.output:
        try: pathlib.Path(save_folder).mkdir(parents=True, exist_ok=False)
        except FileExistsError: pass
    with open(args.file, 'r') as file:
        urls = file.readlines()
    concurrent_n = args.concurrent if args.concurrent else len(urls)
    if args.verbose:
        print(f'Saving {len(urls)} urls to {save_folder if save_folder else "root folder"}'
              f' using {concurrent_n} connections simultaneously')
        t1 = time.perf_counter()
    asyncio.run(main(concurrent_n, urls, save_folder))
    if args.verbose:
        print(f'Successfully finished in {"%.2f" % (time.perf_counter()-t1)}s')