import requests
import glob
import json
import csv
from mebsuta_api.models import Cell_Image, Debris, Annotation, Mebsuta_Users, Library
import os

from dotenv import load_dotenv

from os import listdir
from os.path import isfile, join

from elasticsearch import Elasticsearch


load_dotenv()


def loadUsers():
    with open('mebsuta_api/data/users.csv', newline='') as csvfile:
        users = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(users)
        for row in users:
            print(os.getenv("SAS_TOKEN"))
            '''
            Mebsuta_Users.objects.create(
                user_id=row[0],
                name=row[1]
            )
            '''

# from mebsuta_api.scripts.loading import loadCellsFromRemote


def createLibraryJiraDict():
    jiraDict = {}
    with open('mebsuta_api/data/library_jira.csv', newline='') as library_jirafile:
        library_jiras = csv.reader(
            library_jirafile, delimiter=',', quotechar='|')
        for line in library_jiras:
            jiraDict[line[0]] = line[1]
        return jiraDict


# from mebsuta_api.scripts.loading import loadCellsFromRemote


def loadCellsFromRemote():
    URL = "https://singlecellmisc.blob.core.windows.net/results/merged_images.csv"
    # url: `${URL}?${process.env.SAS_TOKEN}`,
    token = os.getenv("SAS_TOKEN")

    with requests.get(f"{URL}?{token}", stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())

        jiraDict = createLibraryJiraDict()
        for line in csv.DictReader(lines, delimiter=','):

            cell_id = createCellID(line["chip_row"], line["chip_column"])
            jiraTicket = ""
            if line["library_id"] in jiraDict:
                jiraTicket = jiraDict[line["library_id"]]
            Cell_Image.objects.create(
                cell_id=cell_id,
                microscope_image_filename=line["microscope_image_filename"],
                microscope_image_url=line["microscope_image_url"],
                library_id=line["library_id"],
                chip_row=line["chip_row"],
                chip_column=line["chip_column"],
                condition=line["condition"],
                pick_met=line["pick_met"],
                cellenone_image_filename=line["cellenone_image_filename"],
                cellenone_image_url=line["cellenone_image_url"],
                cellenone_background_filename=line["cellenone_background_filename"],
                cellenone_background_url=line["cellenone_background_url"],
                X=line["X"],
                Y=line["Y"],
                Diameter=line["Diameter"],
                Elongation=line["Elongation"],
                Circularity=line["Circularity"],
                Intensity=line["Intensity"],
                ejection_zone_boundary=line["ejection_zone_boundary"],
                row=line["chip_row"],
                col=line["chip_column"],
                jira_ticket=jiraTicket,
                sample_id=line["sample_id"],
            )


def createCellID(row, col):
    cellID = "R"
    if len(row) == 1:
        cellID += "0"
    cellID += row + "_C"
    if len(col) == 1:
        cellID += "0"
    cellID += col
    return cellID


def addAnnoTestData():
    library_id = "A108740A"
    annos = ["Dividing", "Dividing", "Dividing"]
    test_users = ["tester_1", "tester_2", 'tester_3']
    cell_ids = ["R03_C08"]
    '''
    for user in test_users:
        Mebsuta_Users.objects.create(
            user_id=user,
            name=user
            )
    '''

    for user in test_users:
        for cell in cell_ids:
            for anno in annos:
                foreign_user = Mebsuta_Users.objects.get(user_id=user)
                foreign_cell_image = Cell_Image.objects.get(
                    library_id=library_id, cell_id=cell)
                rowcol = [int(x[1:]) for x in cell.split("_")]
                Annotation.objects.create(
                    library_id=library_id,
                    cell_id=cell,
                    user_id=user,
                    user=foreign_user,
                    Cell_Image=foreign_cell_image,
                    row=rowcol[0],
                    col=rowcol[1],
                    annotation=anno
                )


def clearAll():
    Debris.objects.all().delete()
    Annotation.objects.all().delete()


def loadAll():
    loadCells()
    loadUsers()
    loadAnnotations()
    loadDebris()


def addPK():
    with open('mebsuta_api/mebsuta_data/cellsDataWithJira.db', encoding='utf-8') as data_file:
        new_file = open('mebsuta_api/mebsuta_data/cellsDataWithJiraPK.db', 'w')
        for cell in data_file:
            curr_cell = json.loads(cell)
            curr_cell["comp_cell_id"] = curr_cell["library_id"] + \
                "_"+curr_cell["cell_id"]
            new_file.write(json.dumps(curr_cell) + "\n")


def lengthCells():
    with open('mebsuta_api/mebsuta_data/shortestcells.db', encoding='utf-8') as data_file:
        for cell in data_file:
            data = json.loads(cell)
            print("cell_id:" + str(len(data["cell_id"])))
            print("microscope_image_filename:" +
                  str(len(data["microscope_image_filename"])))
            print("microscope_image_url:" +
                  str(len(data["microscope_image_url"])))
            print("library_id:" + str(len(data["library_id"])))
            print("chip_row:" + str(len(data["chip_row"])))
            print("chip_column:" + str(len(data["chip_column"])))
            print("condition:" + str(len(data["condition"])))
            print("pick_met:" + str(len(data["pick_met"])))
            print("cellenone_image_filename:" +
                  str(len(data["cellenone_image_filename"])))
            print("cellenone_image_url:" +
                  str(len(data["cellenone_image_url"])))
            print("cellenone_background_filename:" +
                  str(len(data["cellenone_background_filename"])))
            print("cellenone_background_url:" +
                  str(len(data["cellenone_background_url"])))
            print("X:" + str(len(data["X"])))
            print("Y:" + str(len(data["Y"])))
            print("Diameter:" + str(len(data["Diameter"])))
            print("Elongation:" + str(len(data["Elongation"])))
            print("Circularity:" + str(len(data["Circularity"])))
            print("Intensity:" + str(len(data["Intensity"])))
            print("ejection_zone_boundary:" +
                  str(len(data["ejection_zone_boundary"])))
            print("row:" + str(len(data["row"])))
            print("col:" + str(len(data["col"])))
            print("jira_ticket:" + str(len(data["jira_ticket"])))
            print("sample_id:" + str(len(data["sample_id"])))


def loadCells():
    with open('mebsuta_api/mebsuta_data/cellsDataWithJira.db', encoding='utf-8') as data_file:
        for cell in data_file:
            data = json.loads(cell)
            Cell_Image.objects.create(
                cell_id=data["cell_id"],
                microscope_image_filename=data["microscope_image_filename"],
                microscope_image_url=data["microscope_image_url"],
                library_id=data["library_id"],
                chip_row=data["chip_row"],
                chip_column=data["chip_column"],
                condition=data["condition"],
                pick_met=data["pick_met"],
                cellenone_image_filename=data["cellenone_image_filename"],
                cellenone_image_url=data["cellenone_image_url"],
                cellenone_background_filename=data["cellenone_background_filename"],
                cellenone_background_url=data["cellenone_background_url"],
                X=data["X"],
                Y=data["Y"],
                Diameter=data["Diameter"],
                Elongation=data["Elongation"],
                Circularity=data["Circularity"],
                Intensity=data["Intensity"],
                ejection_zone_boundary=data["ejection_zone_boundary"],
                row=data["row"],
                col=data["col"],
                jira_ticket=data["jira_ticket"],
                sample_id=data["sample_id"],
            )

# from mebsuta_api.scripts.loading import updateAnnoDebris


def get_length():
    es = Elasticsearch(port=9211)
    index = "image_cells"
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {
                        "isDebris": "true"
                    }},
                    {"bool": {
                        "must_not": [
                            {"term": {"annotation": "null"}}
                        ]
                    }}

                ]
            }
        }
    }
    res = es.count(index=index, body=query)
    print(res)


def process_hits(hits):
    for cell in hits:
        curr_cell = cell["_source"]
        createDebris(curr_cell)
        createAnno(curr_cell)


def updateAnnoDebris():
    '''
    1. hit elastic Search endpoint
        python elastic search
        hit all cells_images that have
        either annotation not null
        or isdebris = True

    2. where do we go for that?

    '''
    es = Elasticsearch(port=9211)
    index = "image_cells"
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {
                        "isDebris": "true"
                    }},
                    {"bool": {
                        "must_not": [
                            {"term": {"annotation": "null"}}
                        ]
                    }}

                ]
            }
        }
    }
    res = es.search(index=index, body=query,
                    size=2500,
                    scroll='15m'
                    )

    sid = res['_scroll_id']
    scroll_size = (len(res["hits"]["hits"]))

    while scroll_size > 0:
        print("scrolling!")

        process_hits(res["hits"]["hits"])
        res = es.scroll(scroll_id=sid, scroll='15m')
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

    print("created all current Annotation and Debris objects")


def createAnno(curr_cell):
    user = curr_cell["user_id"]
    row = curr_cell["row"]
    col = curr_cell["col"]
    library_id = curr_cell["library_id"]
    annotation = curr_cell["annotation"]
    cell_id = curr_cell["cell_id"]

    ref_user = Mebsuta_Users.objects.get(user_id=user)
    ref_cell = Cell_Image.objects.get(
        library_id=library_id, cell_id=cell_id)

    obj, created = Annotation.objects.update_or_create(
        user=ref_user, row=row, col=col, Cell_Image=ref_cell, library_id=library_id, cell_id=cell_id,
        defaults={'annotation': annotation}
    )
    print(obj, created)


def createDebris(curr_cell):
    user = curr_cell["user_id"]
    row = curr_cell["row"]
    col = curr_cell["col"]
    library_id = curr_cell["library_id"]
    isDebris = curr_cell["isDebris"]
    cell_id = curr_cell["cell_id"]

    ref_user = Mebsuta_Users.objects.get(user_id=user)
    try:
        ref_cell = Cell_Image.objects.get(
            library_id=library_id, cell_id=cell_id)
    except:
        print(library_id, cell_id)
    obj, created = Debris.objects.update_or_create(
        user=ref_user, row=row, col=col, Cell_Image=ref_cell, library_id=library_id, cell_id=cell_id,
        defaults={'isDebris': isDebris}
    )
    print(obj, created)


'''


def loadUsers():
    with open('mebsuta_api/mebsuta_data/users.db', encoding='utf-8') as data_file:
        for user in data_file:
            data = json.loads(user)
            Mebsuta_Users.objects.create(
                user_id=data["userID"],
                name=data["name"]
            )
'''


def loadDebris():
    with open('mebsuta_api/mebsuta_data/debris.db', encoding='utf-8') as data_file:
        for cell in data_file:
            data = json.loads(cell)

            foreign_user = Mebsuta_Users.objects.get(user_id=data["user_id"])
            foreign_cell_image = Cell_Image.objects.get(
                library_id=data["library_id"], cell_id=data["cell_id"])

            Debris.objects.create(
                library_id=data["library_id"],
                cell_id=data["cell_id"],
                user_id=data["user_id"],
                user=foreign_user,
                Cell_Image=foreign_cell_image,
                row=data["row"],
                col=data["col"],
                isDebris=data["isDebris"]
            )


def loadAnnotations():
    with open('mebsuta_api/mebsuta_data/annotations.db', encoding='utf-8') as data_file:
        for annotation in data_file:
            data = json.loads(annotation)

            foreign_user = Mebsuta_Users.objects.get(user_id=data["user_id"])
            foreign_cell_image = Cell_Image.objects.get(
                library_id=data["library_id"], cell_id=data["cell_id"])

            Annotation.objects.create(
                library_id=data["library_id"],
                cell_id=data["cell_id"],
                user_id=data["user_id"],
                user=foreign_user,
                Cell_Image=foreign_cell_image,
                row=data["row"],
                col=data["col"],
                annotation=data["annotation"]
            )


def loadLibraries():
    pass
