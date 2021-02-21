import scrapy

class EraSpider(scrapy.Spider):
    name = "era"
    start_urls = [
        'https://www.era.pt/imoveis/comprar/apartamentos/porto',
        'https://www.era.pt/imoveis/comprar/moradias/porto',
    ]
    download_delay = 5.0


    def parse(self, response):

        BASE_URL = 'https://www.era.pt'
        houses_url = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_DataList_imoveis"]//*//@href').getall()
        
        for url in houses_url:
            yield scrapy.Request(url = BASE_URL+url, callback=self.parse_house)
        

        next_page = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_pnl_paginacao_setas2"]//*//@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)    


    def parse_house(self, response):

        # Informacao Geral
        titulo_lista = response.xpath('//*[@class="titulos"]/h2//span/text()').getall()
        titulo = ' '.join(titulo_lista)
        subtitulo = response.xpath('//*[@class="openSansR t18 cinza33 line_height150"]/text()').get()

        preco = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_preco1"]/text()').get()
        quartos = response.xpath('//*[@class="icon-imovel-quartos"]/following-sibling::span[@class="num"]/text()').get()
        casas_banho = response.xpath('//*[@class="icon-imovel-wc"]/following-sibling::span[@class="num"]/text()').get()
        estacionamento = response.xpath('//*[@class="icon-imovel-garagens"]/following-sibling::span[@class="num"]/text()').get()
        area_util = response.xpath('//*[@class="icon-imovel-area"]/following-sibling::span[@class="num"]/text()').get()
        area_terreno = response.xpath('//*[@class="icon-imovel-area-terreno"]/following-sibling::span[@class="num"]/text()').get()
        certificado_energetico = response.xpath('//*[@class="icon-imovel-certificado"]/img/@alt').get().replace('Cert.Energ.: ', '')
        
        descricao_lista = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_texto_imovel"]/text()').getall()
        descricao = ' '.join(descricao_lista)
        
        tipo_de_imovel = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_tipo_imovel"]/text()').get()
        estado = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_estado"]/text()').get()
        preco_venda = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_preco_venda"]/text()').get()
        area_bruta = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_area_bruta"]/text()').get()
        distrito = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_distrito"]/text()').get()
        concelho = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_concelho"]/text()').get()
        freguesia = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_freguesia"]/text()').get()
        zona = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_zona"]/text()').get()
        referencia = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lbl_imovel_show_ref"]/text()').get()

        # Divisoes
        divisoes_nomes = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tabshow1"]/div[@class="divisao-item"]/span[@class="lbl_divisoes_divisao"]/text()').getall()
        divisoes_valores = [valor.replace('m', '') for valor in response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tabshow1"]/div[@class="divisao-item"]/span[@class="lbl_divisoes_area"]/text()').getall()]
        divisoes = {nomes:valores for nomes, valores in zip(divisoes_nomes, divisoes_valores)}

        # Caracteristicas
        caracteristicas_lista = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tabshow0"]//div[@class="imovel_show_list_caracteristicas box"]//span[@class="caracteristicas_titulo_nome"]')
        caracteristicas = {caracteristica.xpath('.//text()').get():''.join(caracteristica.xpath('.//following-sibling::span//text()').getall()).replace("; ", "") for caracteristica in caracteristicas_lista}
    
        # Zonas
        zonas_verdes = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_1"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        servicos_saude = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_3"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        acessibilidade = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_5"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        cultura_lazer = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_7"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        escolas = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_2"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        negocios = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_4"]/span[@class="class_rating_on"]/text()').get().replace('/9','')
        comercio = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_rating_6"]/span[@class="class_rating_on"]/text()').get().replace('/9','')

        # Mapa
        coordenadas = response.xpath('//*[@class="mapa-holder"]/img/@onclick').get().replace("window.open('https://www.google.com/maps/search/?api=1&query=","").replace("', '_blank')", "")
         
        
        yield {
            'titulo': titulo,
            'subtitulo': subtitulo,
            'preco': preco,
            'quartos': quartos,
            'casas_banho': casas_banho,
            'estacionamento': estacionamento,
            'area_terreno': area_terreno,
            'area_util': area_util,
            'certificado_energetico': certificado_energetico,
            'descricao': descricao,
            'tipo_de_imovel': tipo_de_imovel, 
            'estado': estado,
            'preco_venda': preco_venda,
            'area_bruta': area_bruta,
            'distrito': distrito,
            'concelho': concelho,
            'freguesia': freguesia,
            'zona': zona,
            'referencia' : referencia,
            'divisoes': divisoes,
            'caracteristicas': caracteristicas,
            'zonas_verdes': zonas_verdes,
            'servicos_saude': servicos_saude,
            'acessibilidade': acessibilidade,
            'cultura_lazer': cultura_lazer,
            'escolas': escolas,
            'negocios': negocios,
            'comercio': comercio,
            'coordenadas': coordenadas,
        }