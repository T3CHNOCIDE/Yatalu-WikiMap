import json, wikiapi, requests
import regex as re

def pull_listed_wikis(site, username, password):
	"""
	Pulls all listed wikis from the interlanguage map page 
	in order to update each international page number
	"""
	
	#:ogs into given wiki
	wikiapi.login(site, username, password)
	
	#Pulls map page from wiki & finds all mapped wikis
	mapped_wikis_page = wikiapi.view("Interlanguage_map")
	mapped_wikis = re.findall(r"\[\[Interlanguage map\/(.*?)\|", mapped_wikis_page, re.DOTALL, overlapped=False)
	
	#Cycles through each wiki
	for wiki in mapped_wikis:
		
		#Finds all languages on current wiki map page
		updateable_wiki_page = wikiapi.view("Interlanguage_map/%s" % wiki)
		
		if not updateable_wiki_page:
			print "\tPage does not exist. Skipping!"
			continue
		
		interlanguage_wikis = re.findall(r"\|([A-z][A-z])\s.*?url.*?\=(.*?)\n\|[A-z][A-z]\s", updateable_wiki_page, re.DOTALL, overlapped=False)
		
		print "Updating %s ..." % wiki
		
		#Cycles through each language and finds article numbers
		for lang_wiki in interlanguage_wikis:
		
			#Pulls site info & saves article number
			try:
				lang_data = wikiapi.site_info(lang_wiki[1].strip())
				lang_articles = lang_data["query"]["statistics"]["articles"]
			except:
				print "\tWiki doesn't exist anymore. Skipping!"
				continue
			
			#Replaces article number on wiki map page
			updateable_wiki_page = re.sub(r"\|%s\s.*?pages.*?\=(.*?)\n" % lang_wiki[0], "|%s pages = %s \n" % (lang_wiki[0], lang_articles), updateable_wiki_page)
			
			print "\t%s -> %s" % (lang_wiki[1], lang_articles)
		
		#Updates map page at end of list.
		wikiapi.edit("Interlanguage_map/%s" % wiki, updateable_wiki_page, summary="Automated article number update.")
		
		print "Complete!"
		
if __name__ == "__main__":
	
	pull_listed_wikis("WIKI", "USERNAME", "PASSWORD")
