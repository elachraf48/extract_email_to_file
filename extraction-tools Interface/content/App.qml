// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick 6.5
import ExtractionAppInter

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    color: "#c01818"
    title: "ExtractionAppInter"

    Screen01 {
        id: mainScreen
        x: 0
        y: 0
        width: 500
        height: 400
        color: "#304b90"
    }

}

