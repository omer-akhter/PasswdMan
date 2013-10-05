import QtQuick 1.0

ListView {
    id: passwd_list
    width: 800
    height: 600

    model: passwd_model
    /*model: ListModel {
        ListElement {
            title: "title-01"
            passwd: "passwd-01"
            expiry: "expiry-01"
        }
        ListElement {
            title: "title-02"
            passwd: "passwd-02"
            expiry: "expiry-02"
        }
        ListElement {
            title: "title-03"
            passwd: "passwd-03"
            expiry: "expiry-03"
        }
    }*/

    delegate: Component {
        Rectangle {
            id: rectangle1
            width: passwd_list.width
            height: Math.max(txt_title.implicitHeight,
                             col_btns.implicitHeight) + 6
            color: ((index % 2 == 0) ? "#222" : "#111")
            Text {
                id: txt_title
                elide: Text.ElideRight
                text: model.title
                color: "white"
                font.bold: true
                anchors.leftMargin: 10
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: { model.on_select() }
            }

            Column {
                id: col_btns
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.top: parent.top
                anchors.topMargin: 5
                anchors.bottomMargin: 5
                anchors.rightMargin: 5
                spacing: 5
                width: Math.max(txt_copy.implicitWidth,
                                txt_show.implicitWidth) + 12
                Rectangle {
                    width: Math.max(txt_copy.implicitWidth,
                                    txt_show.implicitWidth) + 12
                    height: txt_copy.implicitHeight + 12
                    radius: 9
                    smooth: true
                    border.width: 2
                    border.color: "#000000"

                    Text {
                        id: txt_copy
                        text: "copy"
                        font.italic: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        anchors.fill: parent
                    }
                }

                Rectangle {
                    width: Math.max(txt_copy.implicitWidth,
                                    txt_show.implicitWidth) + 12
                    height: txt_show.implicitHeight + 12
                    radius: 9
                    smooth: true
                    border.width: 2
                    border.color: "#000000"

                    Text {
                        id: txt_show
                        text: "show"
                        font.italic: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        anchors.fill: parent
                    }
                }
            }
        }
    }
}
