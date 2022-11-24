import os.path
import json

def render_table_header():
  return '''| **회사명** | **레포지터리 수** | **팔로워 수** | **Github 주소** |
|:---|---:|---:|:---|
'''

def render_table_row(company):
  print(company)
  markdown = '|'
  markdown += f" {company['name']} |"

  total_public_repos = 0
  total_followers = 0

  stats = company['organizations']
  for stat in stats:
    total_public_repos += stat[1]
    total_followers += stat[2]

  markdown += f" {total_public_repos} |"
  markdown += f" {total_followers} |"

  if len(stats) == 1:
    markdown += f" https://github.com/{stats[0][0]} |"
  else:
    markdown += " "
    for idx, stat in enumerate(stats):
      markdown += f"https://github.com/{stat[0]} ({stat[1]})"
      if idx != len(stats) - 1:
        markdown += '<br />'
    markdown += " |"

  markdown += "\n"
  return markdown

START_TAG = '<!-- MARKDOWN_TABLE(GITHUB): START -->\n'
END_TAG = '\n<!-- MARKDOWN_TABLE(GITHUB): END -->'

def inject_result_to_readme(readme_path, injected_content):
  with open(readme_path) as readme:
    readme_content = readme.read()
    start_index = readme_content.find(START_TAG)
    end_index = readme_content.find(END_TAG)

    updated_content = (readme_content[0:start_index]
      + START_TAG + '\n'
      + injected_content
      + readme_content[end_index:])

  with open(readme_path, 'w') as readme:
      readme.write(updated_content)

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, './github.json')

with open(file_path, 'r') as file:
  companies = json.load(file)

# all companies
readme_path = os.path.join(dir_path, '../github.md')
markdown = render_table_header()

for company in companies:
  markdown += render_table_row(company)

inject_result_to_readme(readme_path, markdown)

# top 10 companies
readme_path = os.path.join(dir_path, '../README.md')
markdown = render_table_header()

top_10_companies = sorted(companies, key = lambda item: sum(org[1] for org in item['organizations']), reverse=True)[:10]
for company in top_10_companies:
  markdown += render_table_row(company)

inject_result_to_readme(readme_path, markdown)
