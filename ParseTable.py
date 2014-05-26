def ParseTable(entry):
    print "\n".join(["".join(x) for x in [[a[0].split("-")[-1],':"'," ".join(a[1:]),'",'] for a in [x.split(" ") for x in entry.split("\n")]]])[:-1]
