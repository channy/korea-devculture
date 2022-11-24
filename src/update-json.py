# load json

import json
import asyncio
import aiohttp
import os.path
import sys

TOKEN = sys.argv[1]

dir_path = os.path.dirname(os.path.realpath(__file__))

async def fetchStat(organization, session):
  url = f'https://api.github.com/orgs/{organization}'
  print(url)

  async with session.get(url) as response:
    data = await response.text()
    info = json.loads(data)

  try:
    return [organization, info['public_repos'], info['followers']]
  except:
    print(info)
    return [organization]

async def main():
  file_path = os.path.join(dir_path, './github.json')

  with open(file_path, 'r') as file:
    companies = json.load(file)

  items = []
  async with aiohttp.ClientSession(headers={
'Authorization': f'Bearer {TOKEN}'
  }) as session:
    for company in companies:
      await asyncio.sleep(0.3)
      stats = await asyncio.gather(*[fetchStat(item[0], session) for item in company['organizations']])
      print(stats)

      for idx, stat in enumerate(stats):
        if len(stat) == 1:
          for org in company['organizations']:
            if org[0] == stat[0]:
              if len(org) != 3:
                stats[idx] = [org[0], 0, 0]
              else:
                stats[idx] = org

      items.append({ 'name': company['name'], 'organizations': stats })

  with open(file_path, 'w') as file:
    json.dump(items, file, ensure_ascii=False, indent=2, sort_keys=True)

    # add newline to eof
    file.write('\n')

asyncio.run(main())
