#
# Fetches Arma 3 changelogs.
#
# Dependencies:
#	beautifulsoup4
# 	requests



pathChangelogRaw = r"output\ChangelogRaw.txt"
pathChangelogFormatted = r"output\ChangelogFormatted.txt"

# Format sourceFile
sourceFile = open(pathChangelogRaw,"r", encoding="utf-8")
targetFile = open(pathChangelogFormatted,"w+", encoding="utf-8")

lines = sourceFile.readlines()

ulStartCount = 0
liStartCount = 0
h1StartCount = 0
h2StartCount = 0
strongCount = 0
emCount = 0
boxInNextLine = False

for line in lines:
    print(liStartCount)

    line = line.lstrip()
    lineFormatted = line.lstrip()

    if (liStartCount == 1):
        lineFormatted = "* " + lineFormatted

    if (liStartCount == 2):
        lineFormatted = "** " + lineFormatted

    if (strongCount == 1):
        lineFormatted = f"* '''{line.rstrip()}'''\n"

    # if (emCount == 1):
    #     # lineFormatted = f"* ''{line.rstrip()}''\n"
    #     continue

    if (h1StartCount == 1):
        lineFormatted = f"\n=== {line.rstrip()} ===\n"

    if (h2StartCount == 1):
        lineFormatted = f"\n==== {line.rstrip()} ====\n\n"

    if (boxInNextLine):
        lineFormatted = f"\n==== {line.rstrip()} ====\n\n"
        boxInNextLine = False

    if (line.startswith("FROM:") or
        line.startswith("TO:") or
        line.startswith("UNIT:") or
        line.startswith("ACTIVITY:") or
        line.startswith("SIZE:")):
        lineFormatted = "* " + line

    if (line.startswith(r"<br>") or
        line.startswith(r"</br>") or
        line.startswith(r"<br/>")):
        # lineFormatted = "\n"
        continue

    if (line.startswith(r'<div class="post-content">') or
        line.startswith(r"</p>") or
        line.startswith(r"<p>") or
        line.startswith(r"<div>") or
        line.startswith(r"</div>")):
        continue

    if (line.startswith(r"<li>")):
        liStartCount += 1
        continue

    if (line.startswith(r"</li>")):
        liStartCount -= 1
        continue

    if (line.startswith(r"<ul>")):
        ulStartCount += 1
        continue

    if (line.startswith(r"</ul>")):
        ulStartCount -= 1
        continue

    if (line.startswith(r"<h1>")):
        h1StartCount += 1
        continue

    if (line.startswith(r"</h1>")):
        h1StartCount -= 1
        continue

    if (line.startswith(r"<h2>")):
        h2StartCount += 1
        continue

    if (line.startswith(r"</h2>")):
        h2StartCount -= 1
        continue

    if (line.startswith(r"<strong>")):
        strongCount += 1
        continue

    if (line.startswith(r"</strong>")):
        strongCount -= 1
        continue

    if (line.startswith(r"<em>")):
        # emCount += 1
        continue

    if (line.startswith(r"</em>")):
        # emCount -= 1
        continue

    if (line.startswith(r'<h2 class="box_title">')):
        boxInNextLine = True
        continue

    print(lineFormatted)
    targetFile.write(lineFormatted)

sourceFile.close()
targetFile.close()