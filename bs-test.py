from bs4 import BeautifulSoup

soup = BeautifulSoup('<h1><span id="favOptions"><input type="checkbox" id="fav-2147483663-1991" name="2147483663-1991"/></span>Eric Fahsl</h1>')

# for child in soup.h1.children :
# 	print child

print soup.h1.contents[1]