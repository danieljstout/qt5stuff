import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    title: qsTr("Hello World")
    width: 640
    height: 480
    visible: true

    Text {
        id: element
        x: 183
        y: 11
        width: 274
        height: 84
        text: qsTr("Hellooooo")
        font.pixelSize: 55
    }

    Flickable {
        id: flickable
        x: 170
        y: 126
        width: 300
        height: 300
    }
}
