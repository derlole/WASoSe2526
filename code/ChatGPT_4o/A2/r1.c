#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <limits.h>
#include <sys/inotify.h>
#include <sys/stat.h>
#include <dirent.h>

/* -------- CONFIG -------- */
#define EVENT_BUF_LEN (1024 * (sizeof(struct inotify_event) + NAME_MAX + 1))

/* -------- UTIL -------- */
static void timestamp(char *buf, size_t len) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    struct tm tm;
    localtime_r(&ts.tv_sec, &tm);
    snprintf(buf, len,
             "%04d-%02d-%02d %02d:%02d:%02d.%03ld",
             tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday,
             tm.tm_hour, tm.tm_min, tm.tm_sec,
             ts.tv_nsec / 1000000);
}

/* -------- WATCH MANAGEMENT -------- */
typedef struct Watch {
    int wd;
    char path[PATH_MAX];
    struct Watch *next;
} Watch;

static Watch *watch_list = NULL;

static void add_watch_node(int wd, const char *path) {
    Watch *w = malloc(sizeof(Watch));
    w->wd = wd;
    strncpy(w->path, path, PATH_MAX - 1);
    w->path[PATH_MAX - 1] = 0;
    w->next = watch_list;
    watch_list = w;
}

static const char *path_from_wd(int wd) {
    for (Watch *w = watch_list; w; w = w->next)
        if (w->wd == wd)
            return w->path;
    return NULL;
}

/* -------- RECURSIVE DIRECTORY WATCH -------- */
static void add_recursive(int fd, const char *path) {
    int wd = inotify_add_watch(
        fd,
        path,
        IN_CREATE | IN_DELETE | IN_MODIFY |
        IN_MOVED_FROM | IN_MOVED_TO |
        IN_DELETE_SELF | IN_MOVE_SELF
    );

    if (wd < 0) {
        fprintf(stderr, "inotify_add_watch failed on %s: %s\n",
                path, strerror(errno));
        return;
    }

    add_watch_node(wd, path);

    DIR *dir = opendir(path);
    if (!dir) return;

    struct dirent *ent;
    while ((ent = readdir(dir))) {
        if (ent->d_type == DT_DIR &&
            strcmp(ent->d_name, ".") != 0 &&
            strcmp(ent->d_name, "..") != 0) {

            char sub[PATH_MAX];
            snprintf(sub, sizeof(sub), "%s/%s", path, ent->d_name);
            add_recursive(fd, sub);
        }
    }
    closedir(dir);
}

/* -------- MAIN -------- */
int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        return EXIT_FAILURE;
    }

    struct stat st;
    if (stat(argv[1], &st) < 0 || !S_ISDIR(st.st_mode)) {
        fprintf(stderr, "Invalid directory\n");
        return EXIT_FAILURE;
    }

    int fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0) {
        perror("inotify_init1");
        return EXIT_FAILURE;
    }

    add_recursive(fd, argv[1]);

    char buffer[EVENT_BUF_LEN];

    printf("Monitoring %s\n", argv[1]);

    for (;;) {
        ssize_t length = read(fd, buffer, sizeof(buffer));
        if (length < 0) {
            if (errno == EAGAIN) {
                usleep(1000); /* micro-sleep only to avoid busy spin */
                continue;
            }
            perror("read");
            break;
        }

        for (char *ptr = buffer; ptr < buffer + length; ) {
            struct inotify_event *ev = (struct inotify_event *)ptr;

            char ts[64];
            timestamp(ts, sizeof(ts));

            const char *base = path_from_wd(ev->wd);
            char full[PATH_MAX];

            if (ev->len)
                snprintf(full, sizeof(full), "%s/%s", base, ev->name);
            else
                snprintf(full, sizeof(full), "%s", base);

            if (ev->mask & IN_CREATE)
                printf("[%s] CREATE      %s\n", ts, full);

            if (ev->mask & IN_DELETE)
                printf("[%s] DELETE      %s\n", ts, full);

            if (ev->mask & IN_MODIFY)
                printf("[%s] MODIFY      %s\n", ts, full);

            if (ev->mask & IN_MOVED_FROM)
                printf("[%s] MOVED_FROM  %s\n", ts, full);

            if (ev->mask & IN_MOVED_TO)
                printf("[%s] MOVED_TO    %s\n", ts, full);

            /* Automatically watch newly created directories */
            if ((ev->mask & IN_CREATE) && (ev->mask & IN_ISDIR)) {
                add_recursive(fd, full);
            }

            ptr += sizeof(struct inotify_event) + ev->len;
        }
    }

    close(fd);
    return EXIT_SUCCESS;
}
