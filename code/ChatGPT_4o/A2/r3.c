#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <limits.h>
#include <errno.h>
#include <string.h>
#include <time.h>

#define EVENT_BUF_LEN (1024 * (sizeof(struct inotify_event) + NAME_MAX + 1))

static void log_timestamp(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);

    struct tm tm;
    localtime_r(&ts.tv_sec, &tm);

    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm);

    printf("[%s.%03ld] ",
           buf,
           ts.tv_nsec / 1000000);
}

static void handle_event(struct inotify_event *event) {
    log_timestamp();

    if (event->mask & IN_CREATE)
        printf("CREATED ");
    else if (event->mask & IN_DELETE)
        printf("DELETED ");
    else if (event->mask & IN_MODIFY)
        printf("MODIFIED ");
    else
        printf("OTHER ");

    if (event->len)
        printf("file: %s\n", event->name);
    else
        printf("(unknown)\n");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *path = argv[1];

    int fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0) {
        perror("inotify_init1");
        exit(EXIT_FAILURE);
    }

    int wd = inotify_add_watch(
        fd,
        path,
        IN_CREATE | IN_DELETE | IN_MODIFY
    );

    if (wd < 0) {
        perror("inotify_add_watch");
        close(fd);
        exit(EXIT_FAILURE);
    }

    printf("Monitoring directory: %s\n", path);

    char buffer[EVENT_BUF_LEN];

    while (1) {
        ssize_t length = read(fd, buffer, sizeof(buffer));

        if (length < 0) {
            if (errno == EAGAIN) {
                usleep(10000);  // yield CPU, not polling for FS changes
                continue;
            } else {
                perror("read");
                break;
            }
        }

        ssize_t i = 0;
        while (i < length) {
            struct inotify_event *event =
                (struct inotify_event *)&buffer[i];

            handle_event(event);

            i += sizeof(struct inotify_event) + event->len;
        }
    }

    inotify_rm_watch(fd, wd);
    close(fd);
    return 0;
}
