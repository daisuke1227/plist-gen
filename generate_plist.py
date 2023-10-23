import zipfile
import plistlib
import os

def extract_info_from_ipa(ipa_path):
    with zipfile.ZipFile(ipa_path) as ipa_zip:
        info_plist_data = ipa_zip.read('Payload/*.app/Info.plist')
        info_plist = plistlib.loads(info_plist_data)
        bundle_id = info_plist['CFBundleIdentifier']
        version = info_plist['CFBundleShortVersionString']
    return bundle_id, version

ipa_file = os.path.abspath('uploads/' + request.files['ipaFile'].filename)
bundle_id, version = extract_info_from_ipa(ipa_file)

app_label = request.form['appLabel']

# Create the plist content
plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd …">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>https://app.eonhub.co/{ipa_file}</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>display-image</string>
                    <key>url</key>
                    <string>https://app.eonhub.co/img/icon.png</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>full-size-image</string>
                    <key>url</key>
                    <string>https://app.eonhub.co/img/icon.png</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{bundle_id}</string>
                <key>bundle-version</key>
                <string>{version}</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{app_label}</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
"""

# Save the plist content to a file
with open('generated.plist', 'w') as plist_file:
    plist_file.write(plist_content)
