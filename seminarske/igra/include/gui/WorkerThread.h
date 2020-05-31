//
// Created by urosjarc on 31. 05. 20.
//

#ifndef IGRA_WORKERTHREAD_H
#define IGRA_WORKERTHREAD_H

#include <QThread>
#include "MainWindow.h"

#include <QThread>

class WorkerThread: public QThread
{
Q_OBJECT
public:
    void run();

    // if Stop = true, the thread will break
    // out of the loop, and will be disposed
    bool Stop;

signals:
    // To communicate with Gui Thread
    // we need to emit a signal
    void valueChanged(int);

public slots:

};

#endif //IGRA_WORKERTHREAD_H
