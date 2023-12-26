from create_excel import create_excel
from user_prompt import user_prompt
import asyncio
from scraping_process import match_page


async def main():
    columns_title = ['Date', 'H/A/Neutral', 'Teams', "TN Rank", 'Spread', 'Total', 'ATS W', 'ATS L', 'ATS%', 'O', 'U',
                     'OU%', '2p%O', '2p%D', '3p%O', '3p%D', 'FT%O',
                     'FT%D', 'ATSStrk', 'OUStrk', 'ATS L6 W', 'ATS L6 L', "O L6", 'U L6']
    final_data = [columns_title]
    failed_links=[]

    # User prompt
    user = await user_prompt()
    links = user['links']
    for link in links:
        result = await match_page(link)
        if list(result.keys())[0] == 'failed_links':
            failed_links.append(link)
        else:
            final_data.append(result['team1'])
            final_data.append(result['team2'])
            # # create excel
            await create_excel(csv_file_path=f"{user['date']}.csv", final_data=final_data)
    print("Retry for failed links.")
    if len(failed_links) != 0:
        for link in failed_links:
            try:
                result = await match_page(link)
                final_data.append(result['team1'])
                final_data.append(result['team2'])
                # # create excel
                await create_excel(csv_file_path=f"{user['date']}.csv", final_data=final_data)
            except:
                print(f"{link.split('/')[-1]} Failed again:(")

if __name__ == "__main__":
    asyncio.run(main())
