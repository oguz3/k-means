from func import calculateTSS, calculateWCSS, search


def readFile():
    fileObject = open("Final-data.txt", "r")
    data = []
    while(True):
        line = fileObject.readline()
        if not line:
            break

        newLineArr = line.strip().split(",")
        data.append(newLineArr);
    fileObject.close
    return data

def writeFile(data, cluster):
    with open('result.txt', 'w', encoding='utf-8') as f:
        for index, line in enumerate(data):
            result = search(cluster, line);
            f.write("Kayıt " + str(index+1) + ": " + "Küme " + str(result) +  "\n")
        f.write("\n")
        for property in cluster:
            f.write("Küme " + str(property) + ": " + str(len(cluster[property])) + " Kayıt " +  "\n")
        f.write("\n")
        wcss = calculateWCSS(cluster)
        f.write("WCSS: "+ str(wcss) +  "\n")

        tss = calculateTSS(data)
        f.write("TSS: "+ str(tss) +  "\n")

        bcss = tss - wcss
        f.write("BCSS: "+ str(round(bcss, 2)))