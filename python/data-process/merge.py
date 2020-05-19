import csv
import json
import re

r = {}
movies = {}
ids = []

def qidGenerator():
    n = 101
    while True:
        yield n
        n += 1

qid = qidGenerator()


with open("simplified_tmdb.json", "r") as fin:
    s = json.loads(fin.read())
    for movie in s:
        movies[s[movie]["title"]] = movie

with open('ml-25m/movies.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Header: " + ", ".join(row))
            line_count += 1
        else:
            movie = row[1] if not re.match(r"\(\d{4}\)", row[1][-6:]) else row[1][:-7]
            if line_count < 10:
                print(movie)
            if movie in movies:
                r[row[0]] = {"qid": next(qid), "id": row[0], "tmdb": movies[movie], "title": movie} #, "genre": row[2].split("|")}
                line_count += 1
    print(line_count)

string = ""
string2 = ""
qids_unique = set()
qids_header_set = set()
ratings_set = set()

with open("ml-25m/ratings.csv", "r") as fin:
    a = fin.read().split("\n")[1:-1]
    for row in a:
        row = row.split(",")
        if row[1] in r.keys():
            ra = int(float(row[2])) if int(float(row[2])) < 5 else 4
            q = r[row[1]]["qid"]
            t = r[row[1]]["tmdb"]
            ti = r[row[1]]["title"]
            
            if(q in qids_unique):
                pass # don't add to header if id already present
            else:
                string2 += "# qid:" + str(q) + ": " + str(ti) + "\n"
                qids_header_set.add("# qid:" + str(q) + ": " + str(ti) + "\n")

            qids_unique.add(q)
            string += str(ra) + " qid:" + str(q) + " # " + str(t) + "\t" + str(ti) + "\n"
            #string2 += "# qid:" + str(q) + ": " + str(ti) + "\n"
            ratings_set.add(str(ra) + " qid:" + str(q) + " # " + str(t) + "\t" + str(ti) + "\n")

# Sort the List of QIDs
qids_unique_sorted = sorted(qids_unique)
# Initialize final QID Header
string_header =""
string_rating =""
# Iterate through sorted set & write the headers per sort order
#for qid_entry in qids_unique_sorted:
for qid_entry in range(19000):
    for qidh in qids_header_set:
        if(qidh.startswith("# qid:" + str(qid_entry) + ":")):
            string_header += qidh
            break



    for qidr in ratings_set:
        strTemp = "qid:" + str(qid_entry) + " "
        if(strTemp in qidr):
            string_rating += qidr


with open("judgements_header.txt", "w+") as fout:
    fout.write(string_header[:-1])


with open("judgements.txt", "w+") as fout:
    fout.write(string_rating[:-1])
