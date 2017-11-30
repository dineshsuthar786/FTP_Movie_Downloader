import urllib2,sys,string,time
from bs4 import BeautifulSoup

ignore_links = ['../','/']

class MyDownloader:
	"""This program will download the movies/serials from ftp server. provide the ftp server link for this.
	   This program will also display the download progress bar and download speed.
	"""

	def __init__(self):
		self.user_link = ''
		self.download_links = []
		self.duplicate_movies = []
		self.movie_names = []
	
	def enable_proxy(self,user_proxy):
		proxy = urllib2.ProxyHandler({'http': user_proxy, 'https': user_proxy})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
	
	def find_all_download_links_and_movie_names(self,user_link):
		self.user_link = user_link
		page = urllib2.urlopen(user_link)
		soup = BeautifulSoup(page,'lxml')

		all_links = soup.find_all('a')

		for each_link in all_links:
			if each_link.get('href') not in ignore_links:
				movie = each_link.get('href')
				if '.' not in movie:
					continue
				try:
					movie = urllib2.unquote(movie).decode('utf8')
				except Exception as e:
					print e
					continue
				movie_check = ''
				if '1080p' in movie:
					movie_check = movie.split('1080p')[0].strip()
				elif '720p' in movie:
					movie_check = movie.split('720p')[0].strip()
				elif '480p' in movie:
					movie_check = movie.split('480p')[0].strip()
				elif '576p' in movie:
					movie_check = movie.split('576p')[0].strip()

				if (movie_check == '') or (movie_check not in self.duplicate_movies):
					self.download_links.append(self.user_link + each_link.get('href'))
					self.duplicate_movies.append(movie_check)
					self.movie_names.append(movie)

	def start_downloading(self):
		for i in xrange(len(self.download_links)):
			try:
				print "\r\nDownloading %s" %self.movie_names[i]
				movie = urllib2.urlopen(self.download_links[i])
				with open(self.movie_names[i],'wb') as f:
					movie_size = movie.info().getheader('Content-Length').strip()
					movie_size = int(movie_size)
					print "File Size is = %.2f MB" %float(movie_size/(1024*1024*1.0))
					downloaded_size = 0
					download_start_time = time.clock()
					while 1:
						chunk = movie.read(4096)
						downloaded_size += len(chunk)
						if not chunk:
							break
						downloaded = int(50 * downloaded_size/movie_size)
						f.write(chunk)
						sys.stdout.write("\r[%s%s] %d%% Completed  %7sKbps" %('=' * downloaded, ' ' * (50 - downloaded), downloaded*2, (downloaded_size/1024)//(time.clock() - download_start_time)))
						sys.stdout.flush()
					f.close()
				print "\r\nDownloaded %s" %self.movie_names[i]
			except Exception as e:
				print e
				print('\r\nFailed to download')

if __name__ == '__main__':
	print "\n         Hello User\n\n"
	print """****************************************
*                                      *
*     Welcome to Movie Downloader      *
*                                      *
****************************************\n\n"""

	mydownloader = MyDownloader()
	print "Enter FTP Server Movie Link"
	link = raw_input()

	proxy_flag = raw_input("\nEnable proxy?(yes/no) => ")

	if proxy_flag == "yes":
		proxy = raw_input("\nEnter proxy => ")
		mydownloader.enable_proxy(proxy)

	mydownloader.find_all_download_links_and_movie_names(link)
	mydownloader.start_downloading()