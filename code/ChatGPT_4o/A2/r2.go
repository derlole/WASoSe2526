package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/fsnotify/fsnotify"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("Usage: %s <directory_to_watch>", os.Args[0])
	}

	root := os.Args[1]

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	// Recursively watch all directories
	err = filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			err = watcher.Add(path)
			if err != nil {
				log.Printf("Failed to watch %s: %v\n", path, err)
			}
		}
		return nil
	})

	if err != nil {
		log.Fatal(err)
	}

	log.Printf("Watching directory: %s\n", root)

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			handleEvent(event, watcher)

		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			log.Println("Watcher error:", err)
		}
	}
}

func handleEvent(event fsnotify.Event, watcher *fsnotify.Watcher) {
	timestamp := time.Now().Format(time.RFC3339Nano)

	switch {
	case event.Op&fsnotify.Create == fsnotify.Create:
		fmt.Printf("[%s] CREATED: %s\n", timestamp, event.Name)

		// If a new directory is created, start watching it
		info, err := os.Stat(event.Name)
		if err == nil && info.IsDir() {
			err = watcher.Add(event.Name)
			if err != nil {
				log.Printf("Failed to watch new directory %s: %v\n", event.Name, err)
			}
		}

	case event.Op&fsnotify.Write == fsnotify.Write:
		fmt.Printf("[%s] MODIFIED: %s\n", timestamp, event.Name)

	case event.Op&fsnotify.Remove == fsnotify.Remove:
		fmt.Printf("[%s] DELETED: %s\n", timestamp, event.Name)

	case event.Op&fsnotify.Rename == fsnotify.Rename:
		fmt.Printf("[%s] RENAMED: %s\n", timestamp, event.Name)

	case event.Op&fsnotify.Chmod == fsnotify.Chmod:
		fmt.Printf("[%s] PERMISSIONS CHANGED: %s\n", timestamp, event.Name)
	}
}
