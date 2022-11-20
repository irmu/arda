# -*- coding: utf-8 -*-
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info), PlatformCode y Core del Grupo Balandro (https://linktr.ee/balandro)

import os, sys, urllib, re, shutil, zipfile, base64
#import xbmc, xbmcgui, xbmcaddon, xbmcplugin, requests
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import locale, time, random, plugintools
import resolvers

if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.error as urllib2

from core import httptools
from core.item import Item
from platformcode.config import WebErrorException
from platformcode import platformtools


usaHorus = True
setting = xbmcaddon.Addon().getSetting
if setting('lanzarCon') == "0":  ##0 = Solo Acestream  1 = Horus+Acestream
    usaHorus = False


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

version="(v0.2.1) Fix 016"
comparaVersion="0.2.1 Fix 016"


addonPath           = xbmcaddon.Addon().getAddonInfo("path")
mi_data = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.FutbolTream/'))
mi_addon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.FutbolTream'))

fondo = xbmc.translatePath(os.path.join(mi_addon,'fanart.jpg'))
logoprin = xbmc.translatePath(os.path.join(mi_addon,'icon.png'))

mislogos = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.FutbolTream/jpg/'))
logo_transparente = xbmc.translatePath(os.path.join(mislogos , 'transparente.png'))
logoLiga = "https://i.imgur.com/JCnA8k6.png"
logoGuia = "https://i.imgur.com/AYGUJyq.png"

audios = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.FutbolTream/audios/'))
lasliao = xbmc.translatePath(os.path.join(audios, 'error.mp3'))

horusTorrent = "eydhY3Rpb24nOiAncGxheScsICdmYW5hcnQnOiAnJywgJ2ljb24nOiAnTUktSUNPTk8nLCAndXJsJzogJ01JLVRPUlJFTlQnLCAnbGFiZWwnOiAnTUktVElUVUxPJ30="  ## Para Torrents
horusAce = "eydhY3Rpb24nOiAncGxheScsICdmYW5hcnQnOiAnTUktRkFOQVJUJywgJ2ljb24nOiAnTUktSUNPTk8nLCAnaWQnOiAnTUktSUQtQUNFJywgJ2xhYmVsJzogJ01JLVRJVFVMTyd9"  ##Para id-Aces

datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0FjZVRvcnIvZnV0dHJlYW0vbWFpbi9EYXRvc0NvbmY=".encode('utf-8')).decode('utf-8')).data

if not "<FutbolTream2>" in datosConf:
    datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yZW50cnkuY28veHM2YmYvcmF3".encode('utf-8')).decode('utf-8')).data

lista2M = plugintools.find_single_match(datosConf,'dobleM>(.*?)<Fin')
m2Internacional = plugintools.find_single_match(datosConf,'mmInternacional>(.*?)<Fin')

ListaCentralAcotaInicio = plugintools.find_single_match(datosConf,'ListaCentralAcotaInicio>(.*?)<Fin')
ListaCentralAcotaFin = plugintools.find_single_match(datosConf,'ListaCentralAcotaFin>(.*?)<Fin')

pongo_Agenda = plugintools.find_single_match(datosConf,'laAgenda>(.*?)<Fin')

Lista1_Titulo = plugintools.find_single_match(datosConf,'Lista1_Titulo>(.*?)<Fin')
Lista1_AcotaInicio = plugintools.find_single_match(datosConf,'Lista1_AcotaInicio>(.*?)<Fin')
Lista1_AcotaFin = plugintools.find_single_match(datosConf,'Lista1_AcotaFin>(.*?)<Fin')

Lista2_Titulo = plugintools.find_single_match(datosConf,'Lista2_Titulo>(.*?)<Fin')
Lista2_AcotaInicio = plugintools.find_single_match(datosConf,'Lista2_AcotaInicio>(.*?)<Fin')
Lista2_AcotaFin = plugintools.find_single_match(datosConf,'Lista2_AcotaFin>(.*?)<Fin')

Lista3_Titulo = plugintools.find_single_match(datosConf,'Lista3_Titulo>(.*?)<Fin')
Lista3_AcotaInicio = plugintools.find_single_match(datosConf,'Lista3_AcotaInicio>(.*?)<Fin')
Lista3_AcotaFin = plugintools.find_single_match(datosConf,'Lista3_AcotaFin>(.*?)<Fin')

Lista4_Titulo = plugintools.find_single_match(datosConf,'Lista4_Titulo>(.*?)<Fin')
Lista4_AcotaInicio = plugintools.find_single_match(datosConf,'Lista4_AcotaInicio>(.*?)<Fin')
Lista4_AcotaFin = plugintools.find_single_match(datosConf,'Lista4_AcotaFin>(.*?)<Fin')

web = plugintools.find_single_match(datosConf,'FutbolTream2>(.*?)<Fin')
headers = {'Referer': web}

##Para evitar error en ejecución cuando el ISP ha bloqueado la web usamos el Try-Except
try:
    dataWeb = httptools.downloadpage(web).data + "<END>"
    
    quita = '<font class="wsw-13">'
    dataWeb = dataWeb.replace(quita , "").replace("&nbsp;" , " ")

    ##Vamos a quitar los que tienen "Comentados" en la web
    acotaIni = "<!--"
    acotaFinal = "-->"
    aQuitar = plugintools.find_multiple_matches(dataWeb,acotaIni+'(.*?)'+acotaFinal)
    for quitalo in aQuitar:
        borra = acotaIni + quitalo + acotaFinal
        dataWeb = dataWeb.replace(borra , "")

    guia_eventos = plugintools.find_multiple_matches(dataWeb,'<tr>(.*?)</tr>')

except:
    dataWeb = ""
    guia_eventos = ""


lCanales = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yZW50cnkuY28vM3k0MmQvcmF3".encode('utf-8')).decode('utf-8')).data
lCanales = lCanales.replace("[" , "&").replace("]" , "&")
acotaIni = '&Linea&'
acotaFinal = '&/L'
lCanales = lCanales.replace("&DE&" ,"[DE]").replace("&PL&" ,"[PL]")
listaCanales = plugintools.find_multiple_matches(lCanales,acotaIni+'(.*?)'+acotaFinal)

if not os.path.exists(mi_data):
	os.makedirs(mi_data)  # Si no existe el directorio, lo creo


cabecera = "[COLOR mediumslateblue][B]      FutbolTream  "+version+" [COLOR red]        ····[COLOR yellowgreen]by AceTorr[COLOR red]····[/B][/COLOR]"
	

# Punto de Entrada
def run():
	plugintools.log('[%s %s] Running %s... ' % (addonName, addonVersion, addonName))

	# Obteniendo parámetros...
	params = plugintools.get_params()
    
	
	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		exec(action+"(params)")
        

	plugintools.close_item_list()            



# Principal
def miDefault(params):
    
    plugintools.add_item(action="",url="",title=cabecera,thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)

    '''
    if len(guia_eventos) > 0 and pongo_Agenda == "SI":
        plugintools.add_item(action="guiaEventos",url=web,title='[COLOR lime]>>>  Guía de Eventos  (entrar)  <<<[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    else:
        plugintools.add_item(action="",url="",title="[COLOR red]····Guia de Eventos temporalmente Inactiva en la Web····[/COLOR]",thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)
    '''
    if pongo_Agenda == "SI":
        plugintools.add_item(action="guiaMarca",url=web,title='[COLOR lime]>>>  Guía de Eventos [COLOR red][B]Marca[/B]  [COLOR lime](entrar)  <<<[/COLOR]', thumbnail=logoGuia, fanart=fondo, folder=True, isPlayable=False)
        #plugintools.add_item(action="",url="",title="[COLOR red]····Guia de Eventos temporalmente Inactiva en la Web····[/COLOR]",thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)
    
    
    plugintools.add_item(action="dobleM",url=web,title='[COLOR white]Recopilación Canales Acestream de [COLOR orangered][B]"dobleM"[/B][/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="mmInternacional",url=web,title='[COLOR white]Recopilación Canales [COLOR blue]Internacionales [COLOR white]Acestream de [COLOR orangered][B]"dobleM"[/B][/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    
    if ("Lucas_m_" in dataWeb):
        plugintools.add_item(action="bylucas",url=web,title='[COLOR white]'+Lista1_Titulo+'[/COLOR]', extra="", thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    else:
        plugintools.add_item(action="errorLectura",url=web,title='[COLOR slategray]**'+Lista1_Titulo+'**[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    if ("@MANUK0S" in dataWeb):
        plugintools.add_item(action="manukos",url=web,title='[COLOR white]'+Lista2_Titulo+'[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    if ("Canales HD" in dataWeb):
        plugintools.add_item(action="canalesHD",url=web,title='[COLOR white]'+Lista3_Titulo+'[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    if (Lista4_AcotaInicio in dataWeb):
        plugintools.add_item(action="menuVarios",url=web,title='[COLOR white]'+Lista4_Titulo+'[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    '''
    if not ("Lucas_m_" in dataWeb) and not ("@MANUK0S" in dataWeb):  ##Intentamos coger todos los links en una única lista
        plugintools.add_item(action="listaCentral",url=web,title='[COLOR white]Recopilación Temporal de Listas [COLOR lime]>>entrar<< [COLOR coral](Faltan datos de creadores en la Web)[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    else:
        if "Canales 365" in dataWeb:
            plugintools.add_item(action="canales365",url="",title='[COLOR white]Canales 365[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)

        #if ("NBA Tv" in dataWeb) or ("@ManuK0S" in dataWeb) or ("@MANUK0S" in dataWeb):
        if (Lista4_AcotaInicio in dataWeb):
            plugintools.add_item(action="menuVarios",url=web,title='[COLOR white]'+Lista4_Titulo+'[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    '''
    if "<Varios>" in datosConf:
        plugintools.add_item(action="variosTemp",url=web,title='[COLOR white]Canales Temporales[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    
    plugintools.add_item(action="laLiga",url="",title='[COLOR white]Resúmenes partidos de Liga[/COLOR]', thumbnail=logoLiga, fanart=fondo, folder=True, isPlayable=False)
    
    if "<MotoGP>" in datosConf:
        plugintools.add_item(action="Motor",url="<MotoGP",title='[COLOR white]Carreras MotoGP (Diferidos -[COLOR red]Acestream[COLOR white] o [COLOR blue]mp4[COLOR white]-)[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    
    if "<Formula1>" in datosConf:
        plugintools.add_item(action="Motor",url="<Formula1",title='[COLOR white]Carreras Formula-1 (Diferidos -[COLOR red]Acestream[COLOR white] o [COLOR blue]mp4[COLOR white]-)[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    
    plugintools.add_item(action="FutballEver",url=web,title='[COLOR white]Football Ever [COLOR blue][B](Parser Web)[/B][/COLOR]', thumbnail="https://www.giltedgesoccer.com/wp-content/uploads/2021/08/gesm-most-attended-soccer-games-usa.jpg", fanart=fondo, folder=True, isPlayable=False)
    
    
    acotacion = "a visionar<"
    zapp = plugintools.find_single_match(dataWeb,acotacion+'(.*?)</strong')
    if len(zapp) > 0:
        plugintools.add_item(action="zapping",url="",title='[COLOR white]Zapping Arena[/COLOR]', thumbnail=logoprin, fanart=fondo, folder=True, isPlayable=False)
    
    plugintools.add_item(action="", url="", title="", genre="", thumbnail=logo_transparente, fanart=fondo, folder=False, isPlayable=False)
    ### ¡¡¡SEÑORES DE LUAR!!!:
    ### Está muy FEO el distribuir un Addon SIN permiso del creador
    ### Y rompe con todos los códigos ÉTICOS el modificar dicho Addon para que no aparezca algo que NO os interesa.
    ### Dejad de usar MI Addon.
    mensaje = "[COLOR firebrick]*Este addon se suministra gratuitamente desde [COLOR yellow][B]Kelebek[/B][COLOR firebrick]. Si está en algún otro paquete, es sin la AUTORIZACIÓN de sus creadores.[/COLOR]"
    plugintools.add_item(action="", url="", title=mensaje, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    
    if not usaHorus:
        mensaje = "[COLOR aqua]**Recuerde abrir previamente [COLOR red]Acestream [COLOR aqua]si no tiene activado [COLOR yellow]Horus [COLOR aqua]en los Ajustes del Addon.[/COLOR]"
        plugintools.add_item(action="", url="", title=mensaje, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)





def guiaMarca(params):

    laGuia = httptools.downloadpage("https://www.marca.com/programacion-tv.html").data
    ##Cojo los 7 días de la Agenda
    acotacion = 'class="title-section-widget'
    #Hoy = plugintools.find_single_match(laGuia,acotacion+'(.*?)</ol')
    dias7 = plugintools.find_multiple_matches(laGuia,acotacion+'(.*?)</ol')
    ##Capturo la fecha x ej: <strong>Martes</strong>6 de Septiembre de 2022</span>
    
    #plugintools.add_item(action="", url="", title="[COLOR greenyellow]***Apartado Informativo, aquí solo se ve donde están disponibles los Eventos.***[/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    #plugintools.add_item(action="", url="", title="[COLOR greenyellow]***Apunte el/los canales del evento y vuelva al Menú Ppal para buscarlos y reproducirlos.***[/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)

    for Hoy in dias7:
        fecha1 = plugintools.find_single_match(Hoy,'strong>(.*?)</span').replace("</strong>" , "  ")
        plugintools.add_item(action="", url="", title="[COLOR red][B]····"+fecha1+"····[/B][/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)

        ##Separo los eventos
        acotacion = 'li class="dailyevent'
        eventos = plugintools.find_multiple_matches(Hoy,acotacion+'(.*?)</li')
        for item in eventos:
            deporte = plugintools.find_single_match(item,'dailyday">(.*?)<')
            if "tbol" in deporte: deporte = "Fútbol"
            if "rmula 1" in deporte: deporte = "Fórmula 1"
            #plugintools.log("*****************Deporte: "+deporte+"********************")
            hora = plugintools.find_single_match(item,'dailyhour">(.*?)<')
            competicion = plugintools.find_single_match(item,'dailycompetition">(.*?)<')
            partido = plugintools.find_single_match(item,'title="(.*?)"')
            acotacion = 'icon-pantalla"></i>'
            canales = plugintools.find_single_match(item,acotacion+'(.*?)<')

            titu = ""
            #titu = " [COLOR lime](" + hora + ") [COLOR orange] " + deporte.title()
            #titu = titu + ": " + competicion.title() + "-> [COLOR blue] " + partido + ":  [COLOR red]" + canales + "[/COLOR]"
            titu = " [COLOR lime](" + hora + ") [COLOR orange] " + deporte
            titu = titu + ": " + competicion + "-> [COLOR blue] " + partido + ":  [COLOR red]" + canales + "[/COLOR]"
            
            #plugintools.add_item(action="laLiaste", url="", title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
            plugintools.add_item(action="adivinaCanal", url="", title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    






def guiaEventos(params):

    acotacion = 'class="title">'
    elTitulo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)</h1')
    plugintools.add_item(action="", url="", title="[COLOR red][B]····"+elTitulo+"····[/B][/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    plugintools.add_item(action="", url="", title="[COLOR greenyellow]***Apartado Informativo, aquí solo se ve donde están disponibles los Eventos.***[/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    plugintools.add_item(action="", url="", title="[COLOR greenyellow]***Apunte el/los canales del evento y vuelva al Menú Ppal para buscarlos y reproducirlos.***[/COLOR]", genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)

    primeraLin = True
    for item in guia_eventos:
        if primeraLin:  ##Si es la 1ª línea la salto pues es la cabecera en la web
            primeraLin = False
        else:
            evento = plugintools.find_multiple_matches(item,'<td(.*?)/td>')
            
            dia = plugintools.find_single_match(evento[0],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            hora = plugintools.find_single_match(evento[1],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            deporte = plugintools.find_single_match(evento[2],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            competicion = plugintools.find_single_match(evento[3],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            partido = plugintools.find_single_match(evento[4],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            evento[5] = evento[5].replace("<br>" , " y ").replace("<BR>" , " y ").replace("</br>" , " y ")
            evento[5] = evento[5].replace("<br/>" , " y ").replace("<BR/>" , " y ").replace("</BR>" , " y ")
            canales = plugintools.find_single_match(evento[5],'>(.*?)<').replace("td&gt;" , "").replace("\n" , "")
            
            titu = ""
            titu = "[COLOR white]-" + dia + " [COLOR lime](" + hora + ") [COLOR orange] " + deporte.title()
            titu = titu + ": " + competicion.title() + "-> [COLOR blue] " + partido + ":  [COLOR red]" + canales + "[/COLOR]"
            
            plugintools.add_item(action="laLiaste", url="", title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
            


def dobleM(params):
    lBusca = params.get("extra")
    aEncontrar = params.get("info_labels")
    
    hayBusca = False
    if lBusca == "BUSCAR":
        hayBusca = True
        encontrados = []

    listaDoble = httptools.downloadpage(lista2M).data
    
    ##Obtengo datos de cuando se ha actualizado
    acotacion = "EXTM3U Acestream Deportes"
    acotaFin = "#"
    fecActu = plugintools.find_single_match(listaDoble,acotacion+'(.*?)'+acotaFin).replace("\r\n" , "").replace("\n" , "")
    
    plugintools.add_item(action="",url="",title="[COLOR orangered]***Actualizado: [B]"+fecActu+"[/B]***[/COLOR]",thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)
    
    acotacion = "EXTINF:-1"
    acotaFin = ".mp4"
    canales = plugintools.find_multiple_matches(listaDoble,acotacion+'(.*?)'+acotaFin)  
    for item in canales:
        titulo = plugintools.find_single_match(item,'tvg-id="(.*?)"')
        acotacion = "/pid/"
        acotaFin = "/stream"
        link = "acestream://" + plugintools.find_single_match(item,acotacion+'(.*?)'+acotaFin)
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        NoM3U = True
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus and NoM3U:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if NoM3U:
                    if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                        mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                    else:  ## Es un ID clásico de Acestream
                        mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link

            if hayBusca:
                for item2 in aEncontrar:
                    if item2.upper() == titulo.upper():
                        lLinea = "&Titu&" + titulo + "&Link&" + mivideo + "&Fin"
                        encontrados.append(lLinea)
            
            else:
                plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    
    if hayBusca:
        return encontrados
            
            




def mmInternacional(params):
    lBusca = params.get("extra")
    aEncontrar = params.get("info_labels")
    
    hayBusca = False
    if lBusca == "BUSCAR":
        hayBusca = True
        encontrados = []


    listaDoble = httptools.downloadpage(m2Internacional).data
    listaDoble = listaDoble + "#"
    
    ##Obtengo datos de cuando se ha actualizado
    acotacion = "EXTM3U Acestream Search"
    acotaFin = "#"
    fecActu = plugintools.find_single_match(listaDoble,acotacion+'(.*?)'+acotaFin).replace("\r\n" , "").replace("\n" , "")
    
    plugintools.add_item(action="",url="",title="[COLOR orangered]***Actualizado: [B]"+fecActu+"[/B]***[/COLOR]",thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)
    
    acotacion = "EXTINF:-1"
    acotaFin = "#"
    canales = plugintools.find_multiple_matches(listaDoble,acotacion+'(.*?)'+acotaFin)
    for item in canales:
        item = item + "#"
        plugintools.log("*****************Item: "+item+"********************")
        titulo = plugintools.find_single_match(item,'tvg-id="(.*?)"')
        item = item.replace("tvg-id" , "elTitulo")
        acotacion = "id="
        acotaFin = "#"
        link = "acestream://" + plugintools.find_single_match(item,acotacion+'(.*?)'+acotaFin).replace("\r\n" , "").replace("\n" , "") 
        plugintools.log("*****************Link: "+link+"********************")
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        NoM3U = True
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus and NoM3U:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if NoM3U:
                    if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                        mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                    else:  ## Es un ID clásico de Acestream
                        mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            if hayBusca:
                for item2 in aEncontrar:
                    if item2.upper() == titulo.upper():
                        lLinea = "&Titu&" + titulo + "&Link&" + mivideo + "&Fin"
                        encontrados.append(lLinea)
            
            else:
                plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    
    if hayBusca:
        return encontrados




def Motor(params):
    acotacion = params.get("url")

    #plugintools.add_item(action="",url="",title="[COLOR greenyellow]***Enlaces de [B]Deportes_AcestreamVideosMotor[/B]***[/COLOR]",thumbnail=logoprin,fanart=fondo,folder=False,isPlayable=False)
    
    acotaFin = "Fin>"
    canales = plugintools.find_multiple_matches(datosConf,acotacion+'(.*?)'+acotaFin)  
    for item in canales:
        titulo = plugintools.find_single_match(item,'>(.*?)<')
        link = plugintools.find_single_match(item,'link>(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        NoM3U = True
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus and NoM3U:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if NoM3U:
                    if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                        mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                    else:  ## Es un ID clásico de Acestream
                        mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)


def variosTemp(params):

    acotacion = "<Varios"
    acotaFin = "Fin>"
    canales = plugintools.find_multiple_matches(datosConf,acotacion+'(.*?)'+acotaFin)  
    for item in canales:
        titulo = plugintools.find_single_match(item,'>(.*?)<')
        link = plugintools.find_single_match(item,'link>(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        NoM3U = True
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus and NoM3U:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if NoM3U:
                    if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                        mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                    else:  ## Es un ID clásico de Acestream
                        mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)



def listaCentral(params):
    
    acotacion = ListaCentralAcotaInicio
    acotaFin = ListaCentralAcotaFin
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)'+acotaFin)  
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        #plugintools.log("*****************Titu: "+titulo+"********************")
        #plugintools.log("*****************Link: "+link+"********************")
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                horus = horusTorrent
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-TORRENT" , link)
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)


def bylucas(params):  ##Lista 1
    lBusca = params.get("extra")
    aEncontrar = params.get("info_labels")
    
    hayBusca = False
    if lBusca == "BUSCAR":
        hayBusca = True
        encontrados = []
        
    acotacion = Lista1_AcotaInicio
    acotaFin = Lista1_AcotaFin
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)'+acotaFin)  
    plugintools.log("*****************Grupo: "+grupo+"********************")
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    #plugintools.log("*****************WEB: "+dataWeb+"********************")
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                horus = horusTorrent
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-TORRENT" , link)
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            if hayBusca:
                for item2 in aEncontrar:
                    if item2.upper() == titulo.upper():
                        lLinea = "&Titu&" + titulo + "&Link&" + mivideo + "&Fin"
                        encontrados.append(lLinea)
            
            else:
                plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    
    if hayBusca:
        return encontrados



def canalesHD(params):  ##Lista 3
    
    acotacion = Lista3_AcotaInicio
    acotaFin = Lista3_AcotaFin
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)'+acotaFin)  
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        #plugintools.log("*****************Titu:2 "+titulo+"********************")
        #plugintools.log("*****************Link: "+link+"********************")
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link  and NoM3U:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)



def manukos(params):  ##Lista 2
    
    acotacion = Lista2_AcotaInicio
    acotaFin = Lista2_AcotaFin
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)'+acotaFin)  
    #plugintools.log("*****************Grupo "+grupo+"********************")
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                horus = horusTorrent
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-TORRENT" , link)
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)



def menuVarios(params):  ##Lista 4... Varios
    lBusca = params.get("extra")
    aEncontrar = params.get("info_labels")
    
    hayBusca = False
    if lBusca == "BUSCAR":
        hayBusca = True
        encontrados = []
    
    acotacion = Lista4_AcotaInicio
    acotaFin = Lista4_AcotaFin
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)'+acotaFin)  
    #plugintools.log("*****************Acota1 "+acotacion+"********************")
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        
        ##Ahora están metiendo algunos canales m3u8 en emisión directa de su propia web... Los identifico e intento sacar el link real
        if "futbolgratis.workers.dev" in link:
            web2 = httptools.downloadpage(link).data
            acotacion = 'source src="'
            link = plugintools.find_single_match(web2,acotacion+'(.*?)"')  
        
        NoM3U = True
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                mivideo = link
                NoM3U = False
                
            if usaHorus and NoM3U:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if NoM3U:
                    if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                        mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                    else:  ## Es un ID clásico de Acestream
                        mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
        
            if hayBusca:
                for item2 in aEncontrar:
                    if item2.upper() == titulo.upper():
                        lLinea = "&Titu&" + titulo + "&Link&" + mivideo + "&Fin"
                        encontrados.append(lLinea)
            
            else:
                plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)
    
    if hayBusca:
        return encontrados



def canales365(params):
    
    acotacion = "Canales 365"
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)<hr')
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        titu = "[COLOR white]" + titulo + "[/COLOR]"
        if len(titulo) > 0:
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                horus = horusTorrent
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-TORRENT" , link)
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)



def zapping(params):
    
    acotacion = "a visionar<"
    grupo = plugintools.find_single_match(dataWeb,acotacion+'(.*?)</strong')
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        link = plugintools.find_single_match(item,'href="(.*?)"')
        titulo = plugintools.find_single_match(item,'follow">(.*?)<')
        if len(titulo) > 0:
            titu = "[COLOR white]Canal " + titulo + "[/COLOR]"
            #plugintools.log("*****************Titu: "+titu+"********************")
            if "acestream" in link:
                link = link.replace("acestream://" , "")
                horus = horusAce
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-ID-ACE" , link)
            else:
                horus = horusTorrent
                reemplaza = base64.b64decode(horus.encode('utf-8')).decode('utf-8').replace("MI-TORRENT" , link)
                
            if usaHorus:
                reemplaza = reemplaza.replace("MI-FANART" , "")
                reemplaza = reemplaza.replace("MI-ICONO" , logoprin)
                reemplaza = reemplaza.replace("MI-TITULO" , titulo)
                
                mivideo = "plugin://script.module.horus/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
            else:
                if "://" in link:  ##Es una url o de un link acortado o de una url torrent
                    mivideo = "http://127.0.0.1:6878/ace/getstream?url=" + link
                else:  ## Es un ID clásico de Acestream
                    mivideo = "http://127.0.0.1:6878/ace/getstream?id=" + link
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)




def FutballEver(params):
    logo1 = params.get("thumbnail")
    
    futData = httptools.downloadpage("http://www.footballever.net/", headers={'Referer': "http://www.footballever.net/"}).data
    
    ##Cabecera
    plugintools.add_item(action="",url="",title="     [COLOR blue]····FootBall Ever. Parser de la web footballever.net····[/COLOR]",thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)
    
    #Los canales permanentes 24h
    acotacion = "class='homepage"
    grupo = plugintools.find_single_match(futData,acotacion+'(.*?)</ul')
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        if (not "Home" in item) and (not "Multi Streams" in item):
            futData2 = ""
            urlweb = "http://www.footballever.net" + plugintools.find_single_match(item,"href='(.*?)'")
            titulo = plugintools.find_single_match(item,"menuitem'>(.*?)<") + "[COLOR lime]    -Emisión 24h-[/COLOR]"
            titu = "[COLOR white]" + titulo + "[/COLOR]"
            
            ##Capturo el link de la emisión
            futData2 = httptools.downloadpage(urlweb, headers={'Referer': "http://www.footballever.net/"}).data
            acota2 = 'source: "'
            mivideo = plugintools.find_single_match(futData2, acota2 + '(.*?)"')
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)

    #Los canales de Eventos
    acotacion = "ul id='navbar-link-list"
    grupo = plugintools.find_single_match(futData,acotacion+'(.*?)</ul')
    canales = plugintools.find_multiple_matches(grupo,'<a(.*?)/a>')
    for item in canales:
        futData2 = ""
        urlweb = "http://www.footballever.net" + plugintools.find_single_match(item,"href='(.*?)'")
        titulo = plugintools.find_single_match(item,"html'>(.*?)<")
        
        if len(titulo) > 0:
            titu = "[COLOR white]" + titulo + "[COLOR orange]    -Activo solo en Eventos-" + "[/COLOR]"
            
            ##Capturo el link de la emisión
            futData2 = httptools.downloadpage(urlweb, headers={'Referer': "http://www.footballever.net/"}).data
            acota2 = 'source: "'
            mivideo = plugintools.find_single_match(futData2, acota2 + '(.*?)"')
            
            plugintools.add_item(action="lanza", url=mivideo, title=titu, genre="", thumbnail=logoprin, fanart=fondo, folder=False, isPlayable=False)

    ##Pie
    plugintools.add_item(action="",url="",title="[COLOR lime]**Si no aparece ningún canal, será necesario usar [COLOR blue]VPN [COLOR lime](depende del proveedor de Internet)[/COLOR]",thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="[COLOR salmon]***Canales en formato [COLOR blue]m3u8,[COLOR salmon] no precisan [COLOR red]Acestream[/COLOR]",thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)




def laLiga(params):
    logo = logoLiga
    youtube = "plugin://plugin.video.youtube/channel/UCTv-XvfzLX3i4IGWAm4sbmA/playlists/"
    duff = "eydhY3Rpb24nOiAnaW9pSWlpMUlJJywgJ2ZhbmFydCc6ICcnLCAnaWNvbic6ICcnLCAnaWQnOiAnTUktSUQtQ0FOQUwnLCAnbGFiZWwnOiAnJywgJ3BhZ2UnOiAxLCAncGxvdCc6ICIiLCAncXVlcnknOiAiIiwgJ3RpcG8nOiAnY2hhbm5lbCd9"
    reemplaza = base64.b64decode(duff.encode('utf-8')).decode('utf-8').replace("MI-ID-CANAL" , "UCTv-XvfzLX3i4IGWAm4sbmA")
    duffyou = "plugin://plugin.video.duffyou/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')

    titu = "[COLOR white]Ver usando addon [COLOR red][B]YouTube[/B][/COLOR]"
    plugintools.add_item(action="lanza", url=youtube, title=titu, genre="", thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)
    titu = "[COLOR white]Ver usando addon [COLOR orange][B]DuffYou[/B][/COLOR]"
    plugintools.add_item(action="lanza", url=duffyou, title=titu, genre="", thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)

    plugintools.add_item(action="",url="",title="",thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="[COLOR lime]**Los Resúmenes de los partidos de cada jornada y mucho mas...[/COLOR]",thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)





def lanza(params):
    mivideo = params.get("url")
    logo = params.get("thumbnail")
    titu = params.get("title")
    titulo = params.get("extra")
    #mivideo = "https://streamtape.com/v/9BLGV8YadVUawjb/F.1.GP.Jpn.09.10.2022.mp4"
    #mivideo = "plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url=http://270777632905317581.nicesbot.xyz:80/5CD6UASN8T/4533181220/317581"
    #mivideo = "plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;url=http://s846397078.mialojamiento.es/w2jy/toro.php/mono.m3u8"
    
    if "tokyvideo.com" in mivideo:
        mivideo2 = httptools.downloadpage(mivideo).data
        acotacion = 'source src="'
        mivideo = plugintools.find_single_match(mivideo2,acotacion+'(.*?)"')
    
    if "streamtape" in mivideo:
        mivideo = StreaTape(mivideo)
        
        
    #xbmc.Player().play(mivideo)
    li = xbmcgui.ListItem(titu)
    li.setInfo(type='Video', infoLabels="")
    li.setArt({ 'thumb': logo})
    xbmc.Player().play(mivideo, li)



def StreaTape(mi_url):

    import time
    mivideo2 = httptools.downloadpage(mi_url).data
    mivideo2 = mivideo2.replace("getElementById('ideoooolink" , "DESDE_AQUI")
    #acotacion = "getElementById('ideoooolink"
    acotacion = "DESDE_AQUI"
    provisional = plugintools.find_single_match(mivideo2,acotacion+"(.*?)substring")
    provisional = provisional.replace("ideo?id=" , "ID_VIDEO")
    #plugintools.log("*****************Provi: "+provisional+"********************")
    #acotacion = "ideo?id="  ##Casi todas las veces lo genera de esta forma
    acotacion = "ID_VIDEO"  ##Casi todas las veces lo genera de esta forma: ideo?id=
    el_ID = ""
    el_ID = plugintools.find_single_match(provisional,acotacion+"(.*?)'")

    if not "&token" in el_ID:  ##No nos sirve, hay q volver a llamarlo
        el_ID = ""
    contador = 0
    while len(el_ID) == 0 and contador < 5:  ## Lo intento hasta 5 veces pues de cada 5, 3 vienen con la estructura correcta
        time.sleep(1)
        mivideo2 = httptools.downloadpage(mi_url).data
        mivideo2 = mivideo2.replace("getElementById('ideoooolink" , "DESDE_AQUI")
        acotacion = "DESDE_AQUI"
        provisional = plugintools.find_single_match(mivideo2,acotacion+"(.*?)substring")
        provisional = provisional.replace("ideo?id=" , "ID_VIDEO")
        acotacion = "ID_VIDEO"  ##Casi todas las veces lo genera de esta forma: ideo?id=
        el_ID = ""
        el_ID = plugintools.find_single_match(provisional,acotacion+"(.*?)'")

        if not "&token" in el_ID:  ##No nos sirve, hay q volver a llamarlo
            el_ID = ""
        
        contador = contador + 1
        
    plantilla = "https://streamtape.com/get_video?id=MI-ID-VIDEO|User-Agent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F68.0.3440.106+Safari%2F537.36+OPR%2F55.0.2994.37"    
    
    mi_url = plantilla.replace("MI-ID-VIDEO" , el_ID)
    
    return mi_url
    



def laLiaste(params):
	
    xbmc.Player().play(lasliao)
    l1 = "         [COLOR red]La AGENDA es sólo informativa, NO reproduce enlaces.[/COLOR]"+"\n"+"\n"
    l2 = "Localice el evento, tome nota del canal en que se va a ver..."+"\n"
    l3 = "vuelva al Menú Principal y busque el canal en sus Carpetas."
    mensaje = l1+l2+l3
    xbmcgui.Dialog().ok( "[COLOR lime]¡¡¡INCORRECTO!!![/COLOR]" , mensaje )




def errorLectura(params):
	
    xbmc.Player().play(lasliao)
    l1 = "La página a la se intenta acceder no está disponible."+"\n"
    l2 = "El motivo puede ser por un mantenimiento de dicha web o por estar"+"\n"
    l3 = "bloqueada desde tu Proveedor de Internet... [COLOR red]Prueba otras opciones del Menú.[/COLOR]"
    mensaje = l1+l2+l3
    xbmcgui.Dialog().ok( "[COLOR lime]¡¡¡ERROR de Lectura de Página Web!!![/COLOR]" , mensaje )



def adivinaCanal(params):
    titu = params.get("title")

    titu = titu.replace("[" , "&").replace("]" , "&")
    acota1 = "COLOR red&"
    acota2 = "&/COLOR"
    busca = plugintools.find_single_match(titu,acota1+"(.*?)"+acota2).upper()

    listaTitu = []
    for item in listaCanales:
        acota1 = "canal&"
        acota2 = "&/canal"
        compara = plugintools.find_single_match(item,acota1+"(.*?)"+acota2).upper()
        if busca == compara: 
            #Cojo todos los equivalentes de las listas
            aEncontrar = plugintools.find_multiple_matches(item,"<(.*?)>")
            
            #Ahora toca buscarlos en las Listas q usamos
            params["info_labels"] = aEncontrar
            params["extra"]="BUSCAR"
            listaTitu = []
            listaLink = []
            #Primero busco en LucasMoon
            vuelta = bylucas(params)
            vuelta2 = menuVarios(params)
            vuelta = vuelta + vuelta2
            vuelta3 = dobleM(params)
            vuelta = vuelta + vuelta3
            vuelta4 = mmInternacional(params)
            vuelta = vuelta + vuelta4
            
            for item2 in vuelta:
                aco1 = "Titu&"
                aco2 = "&Link"
                titu2 = plugintools.find_single_match(item2,aco1+"(.*?)"+aco2)
                titu2 = titu2.replace("[DE]" , "[Alemán]").replace("[PL]" , "[Polaco]")
                aco1 = "Link&"
                aco2 = "&Fin"
                mivideo = plugintools.find_single_match(item2,aco1+"(.*?)"+aco2)
                plugintools.log("*****************item2: "+item2+"********************")
                
                #Compruebo que ese Link no lo tenga ya en uno anterior, así no repito elementos (aunq tengan diferente titulo)
                noEsta = True
                if len(listaLink) > 0:
                    for item3 in listaLink:
                        if item3 == mivideo:
                            noEsta = False
                
                if noEsta:  ##Lo añado
                    listaTitu.append(titu2)
                    listaLink.append(mivideo)
                

            if len(listaTitu) > 0:
                #Los de LaLiga, cambio el orden para q no salgan los primeros los de LaLiga TV Bar
                try:
                    i0 = listaTitu.index("Popito")
                    i1 = listaTitu.index("M. LaLiga 1080 MultiAudio")
                    i2 = listaTitu.index("LaLiga Tv Bar 1080")
                    i3 = listaTitu.index("M. LaLiga 720")
                    i4 = listaTitu.index("LaLiga Tv Bar 720")
                    
                    listaTitu[i1], listaTitu[i2], listaTitu[i3], listaTitu[i4] = listaTitu[i2], listaTitu[i1], listaTitu[i4], listaTitu[i3]
                    listaLink[i1], listaLink[i2], listaLink[i3], listaLink[i4] = listaLink[i2], listaLink[i1], listaLink[i4], listaLink[i3]
                except:
                    NoHagoNada = "Nada"
                    
                seleccion = platformtools.dialog_select('Buscado en las Listas... Puedes Buscar en las opciones del Menú Ppal.', listaTitu, autoclose=0, preselect=-1, useDetails=False)
                '''
                if seleccion == 0:
                    mivideo = mivideo_mp4
                '''
                if seleccion > -1: ##Ha seleccionado alguna
                    params["url"]=listaLink[seleccion]
                    params["title"]=listaTitu[seleccion]
                    
                    lanza(params)

    if len(listaTitu) == 0:
        xbmc.Player().play(lasliao)
        l1 = "Se ha intentado buscar en todas las listas disponibles."+"\n"
        l2 = "No ha habido resultados. Esto es una búsqueda aproximada."+"\n"
        l3 = "Pruebe a buscar Manualmente en las opciones del Menú Principal."
        mensaje = l1+l2+l3
        xbmcgui.Dialog().ok( "[COLOR lime]¡¡¡Busqueda Inteligente [COLOR red]No Tan Inteligente!!![/COLOR]" , mensaje )
            
            
            
            


                
    



def salida(params):

	xbmc.executebuiltin('ActivateWindow(10000,return)')
