package main

import (
    "time"
    "log"
    "fmt"
    "os"

    "github.com/fsnotify/fsnotify"
    "github.com/go-vgo/robotgo"
)

func fsWatch(callback func(string)) {
    watcher, err := fsnotify.NewWatcher()
    if err != nil {
        log.Fatal(err)
    }
    defer watcher.Close()

    DIR := "./public"

    err = watcher.Add(DIR)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Watching:", DIR)

    for {
        select {
        case event := <-watcher.Events:
            if event.Op&fsnotify.Create == fsnotify.Create {
                callback(event.Name)
            }

        case err := <-watcher.Errors:
            log.Println("Error:", err)
        }
    }
}

func main() {
    fsWatch(func(filePath string) {
        time.Sleep(200 * time.Millisecond)

        data, err := os.ReadFile(filePath)
        if err != nil {
            log.Println("Couldn't read the file")
            log.Fatal(err)
            return
        }

        text := fmt.Sprintf("%s", data)

        for _, ch := range text {
            robotgo.TypeStr(string(ch))
            time.Sleep(50 * time.Millisecond)
        }

        time.Sleep(200 * time.Millisecond)
        robotgo.KeyTap("enter")
    })
}
