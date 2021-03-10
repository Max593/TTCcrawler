from crawler import *
import time
if __name__ == '__main__':
    # fast changing
    #url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='
    # URL for Perfect Roe
    #url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=6132&ItemNamePattern=Perfect+Roe&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000'
    url = input("Paste the TTC url here: ")
    crawler = Crawler(url)
    #crawler.request_item()
    crawler.add_url('https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=Mother%27s+Sorrow&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=18&ItemTraitID=13&ItemQualityID=&IsChampionPoint=true&IsChampionPoint=false&LevelMin=160&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000')
    crawler.add_url('https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=')
    crawler.open_pages()
    time.sleep(3)
    crawler.refresh_pages()
    crawler.request_items_from_urls()
