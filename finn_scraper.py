# -*- coding: utf-8 -*-
import scrapy
import datetime
import json


HEADERS = [  # TODO: define as item
    'URL',
    #'solgtURL',
    'Dato',
    'PostNr',
    'PostNrNum',
    'Addresse',
    'Adr stripped',
    'Sentrum',
    'Distanse',
    'Dist num',
    'Standard',
    'Prisantydning',
    'solgtPris',
    'solgtDato',
    'Diff',
    'Fellesgjeld',
    'Fellesformue',
    'Totalpris',
    'Tot.pris/kvm',
    'Ligningsverdi',
    'Felleskost/mnd.',
    'Kommunale avg.',
    'Utgifter',
    'Primærrom',
    'Bruksareal',
    'Bruttoareal',
    'Rom',
    'Soverom',
    'Soverom',
    'Etasje',
    'Boligtype',
    'Eieform',
    'Tomteareal',
    'Byggeår',
    'Renovert år',
    'Energimerking',
]


class FinnScraperSpider(scrapy.Spider):
    name = 'finn_scraper'
    allowed_domains = ['finn.no', 'eiendomspriser.no']
    
    input_urls = [
                 
     ('https://www.finn.no/realestate/homes/ad.html?finnkode=111451319&fks=111451319', datetime.datetime.now().strftime("%Y-%m-%d"), 7),                         
     ('https://www.finn.no/realestate/homes/ad.html?finnkode=102515642&fks=102515642', datetime.datetime.now().strftime("%Y-%m-%d"), 7),                         
     ('https://www.finn.no/realestate/homes/ad.html?finnkode=111934948&fks=111934948', datetime.datetime.now().strftime("%Y-%m-%d"), 7),  
    ]

    #Thing we do before the parsing
    def start_requests(self):
        for url, dato, standard, in self.input_urls:
            yield scrapy.Request(url, meta={'Dato': dato,'Standard': standard})

    def parse(self, response):

        variables = {
            #Dictionay of the "labels" and their values on the page
            
            label.xpath("text()").extract_first(): ''.join(label.xpath("following-sibling::dd[1]//text()").extract()).replace("\n", "").replace("\xa0", "").replace("m²", "").replace(",-", "").replace("(eiet)", '').replace(".", '').strip()
            #dd[1] means the first dd element after sibling 
            #.replace("m²", "").replace("(eiet)", '').replace(".", '')
            for label in response.xpath("//dt[@data-automation-id='key']")
        }
        price = response.xpath("//dt[contains(., 'Prisantydning')]/following-sibling::dd/text()").extract_first().replace(",-", '').replace("\n", '').replace("\xa0", '').strip()
        #price = price.replace(",-", '').replace("\n", '').replace("\xa0", '').strip()
        
        adr = response.xpath('/html/body/div[2]/div/div[5]/div[1]/div/div/div/p[2]/text()').extract_first()
        if not adr:
            adr = response.xpath('/html/body/div[2]/div/div[5]/div[1]/div/div/div/p[1]/text()').extract_first()
        if not adr:
            adr = response.xpath('/html/body/div[3]/div/div[5]/div[1]/div/div/div/p[1]/text()').extract_first()

        variables['Addresse'] = adr
        variables['Sentrum'] = "Bergen"
        variables['Distanse'] = None
        variables['Dist num'] = None
        variables['PostNrNum'] = None
        variables['PostNr'] = None
        variables['Adr stripped'] = None
        variables['Solgt'] = None
        variables['Diff'] = None

        if 'Felleskost/mnd.' in variables and 'Kommunale avg.' in variables:
            variables['Utgifter'] = round(int(variables['Kommunale avg.'])/12 + int(variables['Felleskost/mnd.']))
        elif 'Felleskost/mnd.' in variables:
            variables['Utgifter'] = int(variables['Felleskost/mnd.'])
        elif 'Kommunale avg.' in variables:
            variables['Utgifter'] = round(int(variables['Kommunale avg.'])/12)
        else:
            variables['Utgifter'] = 0
        
        variables['Prisantydning'] = price

        if 'Fellesgjeld' in variables:
            variables['Totalpris'] = int(price) + int(variables['Fellesgjeld'])
        else:
            variables['Totalpris'] = int(price) 

        variables['Tot.pris/kvm'] = int(variables['Totalpris'])/int(variables['Primærrom'])
        
        totpris = variables['Tot.pris/kvm']

        variables['URL'] = response.url

        variables.update(**response.meta)

        result = {
            header: variables.get(header, '')
            for header in HEADERS
        }

        #If this reuquest doesn't "go thorugh" I still must return results.

        return scrapy.Request("https://siste.eiendomspriser.no/service/search?query={adr}&sort=1&fromDate=&toDate=&placeFilter=&municipalities=&_=1508208049229".format(adr=adr),
                              callback=self.parse_eiendomspriser,
                              meta={'result': result},
                              headers={
                                  'Accept': 'application/json, text/javascript, */*; q=0.01',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                                  'X-Requested-With': 'XMLHttpRequest'})

    def parse_eiendomspriser(self, response):
        result = response.meta['result']

        response = json.loads(response.body)

        try:
            first_property = response['Properties'][0]

            if first_property['Title'].lower() == result['Addresse'].lower():
                property_date = first_property['SoldDate']
                property_price = first_property['Price']
                
                solgtaar = property_date[-4::] #4 last digits

                if (int(solgtaar)>2015): #Check that sold after 2016 (cannot access total price here)
                    print("test2")
                    result['solgtDato'] = property_date
                    result['solgtPris'] = property_price


        finally:
            return result

