"""
Formatuotojas - tai skriptas, kuris nuparsina nurodyto mii.lt puslapi
nurparsinta puslapio HTML suformatuoja norima tvarka ir ji isveda i tekstini faila
"""

import requests
from bs4 import BeautifulSoup

def extract_site(url):
        """
        Funkcija, kuri nuparsina HTML is nurodyto URL

        Gauta url is input atidaro ir nuparsina jo HTML

        Parameters
        ----------
        url
        Norimo puslapio URL

        Returns
        -------
        info
        Grazina nuparsintus norimus HTML tag'us
        """
        
        info=[]
        response=requests.get(url)
        soup=BeautifulSoup(response.content,'html.parser')
        article_body=soup.find('div',itemprop="articleBody")
        left=article_body.find('p',attrs={'style':'padding-left: 30px;'})
        info.append(str(left.getText()))
        span=article_body.find('span',attrs={'style':'font-size: 12pt;'})
        info.append(str(span.getText()))
        text1=soup.find_all('strong')
        info.append(str(text1[2].getText()))
        link_text=soup.find_all('a',attrs={'class':'wf_file'})
        for x in link_text:
        	info.append(str(x.text))
        	info.append(str(x['href']))
        for x in article_body:
        	try:
        		z=x.string
        		info.append(str(z))
        	except Exception as e:
        		zz=0
        return info

def write_to_file(Lines):
        """
        Funkcija, kuri suraso suformatuota HTML i faila

        Suformatuota HTML suraso i faila

        Parameters
        ----------
        Lines
        Suformatuotas HTML
        """
        file_obj=open("kodas.txt",'a+')
        file_obj.writelines(Lines)
        file_obj.close()

def format_file(info,url):
        """
        Funkcija, kuri suformatuoja nuparsina HTML

        Suformatuoja norima tvarka nuparsinta HTML is gauto URL

        Parameters
        ----------
        url
        Norimo puslapio URL
        info
        Nuparsinti reikiami HTML tag'ai      
        """
        
        url_format=url.split('/')
        url_part=url_format[5]
        url_format=url_format[-1]
        url_format=url_format.split('-')
        url_id=url_format[0]
        last_term="-".join(url_format[1:])
        year_term=info[10]
        title_term=info[16].split('(')[0]
        term1=info[0].split(',')[-1]
        prof_term=info[0]
        text_term=info[3]
        text_link=info[4]
        text_term_2=info[5]
        text_link_2=info[6]
        text_theme=info[2]
        text_theme=text_theme[1:-1]
        first_line="{}\n\n".format(url)
        para_1="""<p><a href="index.php?option=com_content&amp;view=article&amp;id={}:{}&amp;catid=27:{}&amp;lang=lt-LT"><strong><em>{} </em>{}</strong></a></p><p>&nbsp;</p>\n\n""".format(url_id,last_term,url_part,year_term,title_term)				
        para_2="""<p><strong>{}</strong> –{} – gynė:&nbsp;<em>{}</em><br />{}<br />disertacija&nbsp;„<strong><a class="wf_file" href="{}" target="_blank" rel="noopener noreferrer"><span class="wf_file_text">{}</span></a></strong>“&nbsp;[anglų k.] (<a class="wf_file" href="{}" target="_blank" rel="noopener noreferrer"><span class="wf_file_text">santrauka</span></a>)</p>\n\n""".format(title_term,term1,year_term,prof_term,text_link,text_theme,text_link_2)
        Lines=[first_line,para_1,para_2]
        write_to_file(Lines)

if __name__ == "__main__":
        print("Įrašykite puslapio adresą:")
        url=input()
        info=extract_site(url)
        format_file(info,url)
        print("Failas kodas.txt sėkmingai sukurtas!")
