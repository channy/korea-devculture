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
    return { 'organization_id': organization, 'public_repos': info['public_repos'], 'followers': info['followers'] }
  except:
    print(info)
    return { 'organization_id': organization }

async def main():
  file_path = os.path.join(dir_path, '../github.json')

  with open(file_path, 'r') as file:
    companies = json.load(file)

  items = []
  async with aiohttp.ClientSession(headers={
    'Authorization': f'Bearer {TOKEN}'
  }) as session:
    for company in companies:
      await asyncio.sleep(0.3)
      stats = await asyncio.gather(*[fetchStat(item['organization_id'], session) for item in company['organizations']])
      print(stats)

      for idx, stat in enumerate(stats):
        if len(list(stat.keys())) == 1 and stat['organization_id'] != "":
          for org in company['organizations']:
            if org['organization_id'] == stat['organization_id']:
              if len(list(org.keys())) != 3:
                stats[idx] = { 'organization_id': org['organization_id'], 'public_repos': 0, 'followers': 0 }
              else:
                stats[idx] = org

      items.append({ 'name': company['name'], 'organizations': stats })

  with open(file_path, 'w') as file:
    json.dump(items, file, ensure_ascii=False, indent=2, sort_keys=True)

    # add newline to eof
    file.write('\n')

asyncio.run(main())
