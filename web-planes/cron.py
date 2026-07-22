#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import requests


template_url = (
    "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/"
    "intranet/admin/rest/v1.0/consulta/{resource}"
)

resources = [
    "13063",      # Ind 16 - Intensidad energética en la industria [no IECA]
    "15002",      # Ind 06 - Ocupados del sector TIC [no IECA]
    "15041",      # Ind 05 - Indicador sintético de Economía Digital para microempresas [no IECA]
    "15346",      # Ind 13 - VAB generado por las actividades de alta y media-alta tecnología [no IECA]
    "16604",      # Ind 20 - Proporción de personas entre 25 y 64 años que han realizado estudios o formación en las últimas cuatro semanas [no IECA]
    "16719",      # Ind    - Gastos en investigación y desarrollo en proporción al PIB por sector [no IECA]
    "16721",      # Ind    - Gastos en investigación y desarrollo en proporción al PIB por sector [no IECA]
    "16724",      # Ind    - Gastos en investigación y desarrollo en proporción al PIB por sector [no IECA]
    "16725",      # Ind    - Gastos en investigación y desarrollo en proporción al PIB por sector [no IECA]
    "17996",      # Ind 01 - Gasto en Investigación y Desarrollo [no IECA]
    "18009",      # Ind    - Empresas innovadoras [no IECA]
    "18377",      # Ind    - Número de empresas [no IECA]
    "36361",      # Ind    - Edad media de la población por sexo (Padrón) [no IECA]
    "56735",      # Ind    - Personal en investigación y desarrollo respecto a la población activa por sector [no IECA]
    "16717",      # Ind 01 - Gastos en investigación y desarrollo en proporción al PIB
    "102085",     # Ind 02 - Nivel de innovación de Andalucía
    "112021",     # Ind 03 - Gasto en innovación en proporción al PIB
    "112122",     # Ind 04 - Empresas de más de 10 asalariados incorporadas al mercado digital
    "112152",     # Ind 05 - Indicador sintético de economía digital para microempresas
    "105437",     # Ind 06 - Ocupados del sector TIC
    "112181",     # Ind 07 - Densidad empresarial
    "118995",     # Ind 08 - Número de empresas por tamaño según estrato de asalariados
    "112296",     # Ind 09 - Número de empresas exportadoras regulares
    "112295",     # Ind 10 - Proporción de las exportaciones en relación al PIB
    "112375",     # Ind 11 - Inversión extranjera directa (descontada la ETVE - Empresas de Tenencia de Valores Extranjeros)
    "116129",     # Ind 12 - Proporción del VAB por sectores productivos
    "103085",     # Ind 13 - VAB generado por las actividades de alta y media-alta tecnología
    "",     # Ind 14 - Proporción de personas ocupadas por sector
    "116257",     # Ind 15 - Productividad laboral por sectores productivos
    "112604",     # Ind 16 - Intensidad energética en el sector industrial
    "46948",      # Ind 17 - Emisiones de CO2 por unidad de valor añadido del sector manufacturero
    "112626",     # Ind 18 - Gasto en protección ambiental
    "107433",     # Ind 19a - Tasa de temporalidad del empleo en la industria por sexo
    "107573",     # Ind 19b - Índice de incidencia de accidentes de trabajo con baja en jornada en el sector de la industria
    "107575",     # Ind 19c - Ganancia por hora normal de trabajo en el sector de la industria por sexo
    "16613",      # Ind 20 - Proporción de personas entre 25 y 64 años que han realizado estudios o formación en las últimas cuatro semanas
    "",           # Ind 21
    "46946",      # Ind 22 - Emisiones de CO2 por unidad de PIB
    "60467",      # Ind 23 - Proporción de energías renovables en la producción de energía eléctrica
    "16688",      # Ind 24 - Proporción de energías renovables sobre el consumo de energía final por sector (total)
    "16691",      # Ind 26 - Dependencia de la importación de energía por productos
    "60447",      # Ind 27 - Proporción de personas que reciben suministro de agua con cobertura del Sistema Nacional de Aguas de Consumo
    "16778",      # Ind 28 - Proporción de residuos municipales reciclados en relación al total de residuos municipales generados y tratados
    "87717",      # Ind 29 - Emisiones de partículas en suspensión de tamaño inferior a 2,5 micras (PM2,5) [no IECA]
    "107585",     # Ind 30 - Cobertura de redes fijas a velocidades superiores a 100Mbps
    "107586",     # Ind 31 - Cobertura rural de redes fijas a velocidades superiores a 100Mbps
    "16743",      # Ind 32 - Proporción de transporte fluvial y ferroviario sobre el total de transporte de mercancías
    "107588",     # Ind 33 - Longitud de red ferroviaria según tipo de vía y tipo de red
    "16690",      # Ind 34 - Proporción de energías renovables sobre el consumo de energía final por sector (transporte)
    "",           # Ind 35
    "16160",      # Ind 36 - Tasa de riesgo de pobreza en el trabajo
    "115450",     # Ind 37a - Tasa de desempleo por sexo
    "107149",     # Ind 37b - Tasa de temporalidad del empleo por sexo
    "16320",      # Ind 38 - Abandono temprano de la educación por sexo
    "73268",      # Ind 39 - Proporción de personas en riesgo de pobreza o exclusión social
    "73271",      # Ind 39a - Proporción de personas en situación de carencia material y social severa
    "49869",      # Ind 39b - Proporción de personas incapaz de mantener el hogar adecuadamente caliente por situación de pobreza
    "46844",      # Ind 40 - Tasa de mortalidad atribuida a las enfermedades cardiovasculares
    "46835",      # Ind 41 - Tasa de mortalidad de los niños menores de 5 años
    "108252",     # Ind 42 - Esperanza de vida al nacer por sexo
    "108254",     # Ind 43 - Esperanza de vida a los 65 años por sexo
    "60402",      # Ind 44 - Proporción del gasto de las administraciones públicas autonómicas que se dedica a salud
    "20960",      # Ind 45 - Estructura del personal de los centros de Atención Primaria del Servicio Andaluz de Salud
    "15694",      # Ind 46 - Número de Camas en funcionamiento según dependencia por provincia
    "115520",     # Ind 47 - Proporción de personas que vive en hogares con determinadas deficiencias en la vivienda - ODS
    "108271",     # Ind 48 - Proporción de vivienda rehabilitada protegida
    "",     # Ind 49
    "",     # Ind 50
    "108418",     # Ind 51 - Proporción de personas residentes con tiempo de acceso superior a 15 minutos a centro de atención sanitaria de urgencia
    "108421",     # Ind 52 - Número de centros de salud en Andalucía por grado de urbanización en Andalucía
    "108439",     # Ind 53 - Índice europeo de calidad institucional
    "108479",     # Ind 54 - Uso de la administración electrónica por las personas entre 16 y 74 años en los últimos 12 meses
    "",     # Ind 55
    "16620",      # Ind 56 - Brecha de género en el empleo de las personas entre 20 y 64 años por tipo de empleo
    "16619",      # Ind 57 - Brecha salarial de género no ajustada
    "108393",     # Ind    - Índice de envejecimiento con respecto a la población menor de 16 años por grado de urbanización
    "118996",     # Ind    - Número de establecimientos por tamaño según estrato de asalariados
    "108385",     # Ind    - Índice de envejecimiento con respecto a la población total por grado de urbanización en Andalucía
    "85172",      # Ind    - Nivel medio de PM10 en las ciudades ponderado según la población
]

urls = []
for r in resources:
    urls.append(template_url.format(resource=r))

# print(urls)

def download_file(resource):
    response = requests.get(template_url.format(resource=resource))
    
    filename = "./assets/consultas/consulta-" + resource + ".json"
    with open(filename, mode="wb") as file:
        file.write(response.content)
        print(f"Downloaded file {filename}")


def get_data():
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, resources)

if __name__ == "__main__":
    get_data()
