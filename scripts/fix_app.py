with open("portal/app.js", "r", encoding="utf-8") as f:
    app_js = f.read()

# Fix allChannels shadowing
app_js = app_js.replace(
    "var allChannels = [];",
    "var allChannels = (typeof window.allChannels !== 'undefined' && window.allChannels && window.allChannels.length > 0) ? window.allChannels : [];"
)

with open("portal/app.js", "w", encoding="utf-8") as f:
    f.write(app_js)

print("portal/app.js guncellendi!")
