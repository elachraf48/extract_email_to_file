import QtQuick 6.5
import QtQuick.Controls 6.5
import ExtractionAppInter

Rectangle {
    width: 500
    height: 400
    color: "#ef565478"
    property alias buttonFlat: reload_button.flat

    Text {
        width: 28
        height: 19
        text: qsTr("Email")
        anchors.verticalCenterOffset: -106
        anchors.horizontalCenterOffset: -211
        anchors.centerIn: parent
        font.family: Constants.font.family
    }

    Label {
        id: label
        x: 25
        y: 43
        text: qsTr("Provide")
    }

    ComboBox {
        id: email_provider_combo
        x: 86
        y: 34
        width: 288
        height: 44
    }

    ComboBox {
        id: selected_email_combo
        x: 86
        y: 72
        width: 288
        height: 44
    }

    Button {
        id: reload_button
        x: 380
        y: 72
        width: 89
        height: 44
        visible: true
        text: qsTr("Reload")
        highlighted: true
        flat: false
        clip: false
    }

    Button {
        id: extract_button
        x: 86
        y: 111
        width: 288
        height: 48
        text: qsTr("Strat Extraction")
        flat: false
        topPadding: 14
        font.pointSize: 17
        icon.cache: true
        icon.color: "#ddeb0b0b"
        scale: 1
    }

    TextInput {
        id: error_text
        x: 25
        y: 171
        width: 437
        height: 37
        visible: false
        font.pixelSize: 12
        readOnly: true
        clip: false
    }

    Button {
        id: add_button
        x: 34
        y: 340
        width: 192
        height: 52
        text: qsTr("Add New Email")
    }

    Button {
        id: delete_button
        x: 270
        y: 340
        width: 192
        height: 52
        text: qsTr("Delete Email")
    }
}
